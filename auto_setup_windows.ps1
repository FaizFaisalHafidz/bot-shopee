# Auto Setup and Run Shopee Bot - PowerShell Version
# Automatically installs Python if not found

Write-Host "========================================" -ForegroundColor Cyan
Write-Host " AUTO SETUP SHOPEE BOT - POWERSHELL" -ForegroundColor Cyan  
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Function to check if Python is installed
function Test-PythonInstalled {
    try {
        $version = python --version 2>$null
        if ($version) {
            Write-Host "✅ Python found: $version" -ForegroundColor Green
            return $true
        }
    } catch {}
    return $false
}

# Function to install Python
function Install-Python {
    Write-Host "🔧 Python not found. Installing automatically..." -ForegroundColor Yellow
    
    # Method 1: Try winget (Windows Package Manager)
    try {
        $wingetVersion = winget --version 2>$null
        if ($wingetVersion) {
            Write-Host "📦 Using Windows Package Manager..." -ForegroundColor Yellow
            winget install Python.Python.3.11 --silent --accept-package-agreements --accept-source-agreements
            Start-Sleep -Seconds 10
            
            # Refresh environment
            $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
            
            if (Test-PythonInstalled) {
                return $true
            }
        }
    } catch {
        Write-Host "⚠️ winget not available" -ForegroundColor Yellow
    }
    
    # Method 2: Try Chocolatey
    try {
        $chocoVersion = choco --version 2>$null
        if ($chocoVersion) {
            Write-Host "🍫 Using Chocolatey..." -ForegroundColor Yellow
            choco install python -y
            Start-Sleep -Seconds 10
            
            # Refresh environment
            $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
            
            if (Test-PythonInstalled) {
                return $true
            }
        }
    } catch {
        Write-Host "⚠️ Chocolatey not available" -ForegroundColor Yellow
    }
    
    # Method 3: Direct download
    Write-Host "📥 Downloading Python directly..." -ForegroundColor Yellow
    
    $pythonUrl = "https://www.python.org/ftp/python/3.11.5/python-3.11.5-amd64.exe"
    $installerPath = "$env:TEMP\python-installer.exe"
    
    try {
        Write-Host "   Downloading from: $pythonUrl" -ForegroundColor Gray
        Invoke-WebRequest -Uri $pythonUrl -OutFile $installerPath -UseBasicParsing
        
        if (Test-Path $installerPath) {
            Write-Host "✅ Download complete" -ForegroundColor Green
            Write-Host "🔧 Installing Python (silent mode)..." -ForegroundColor Yellow
            
            # Install Python silently with PATH addition
            $process = Start-Process -FilePath $installerPath -ArgumentList "/quiet", "InstallAllUsers=1", "PrependPath=1", "Include_test=0" -Wait -PassThru
            
            if ($process.ExitCode -eq 0) {
                Write-Host "✅ Python installation completed" -ForegroundColor Green
                
                # Refresh environment variables
                $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
                
                # Wait a bit for PATH to update
                Start-Sleep -Seconds 5
                
                if (Test-PythonInstalled) {
                    Remove-Item -Path $installerPath -Force -ErrorAction SilentlyContinue
                    return $true
                }
            } else {
                Write-Host "❌ Python installation failed (Exit code: $($process.ExitCode))" -ForegroundColor Red
            }
        }
    } catch {
        Write-Host "❌ Failed to download Python: $($_.Exception.Message)" -ForegroundColor Red
    }
    
    return $false
}

# Main script
Write-Host "🔍 Checking Python installation..." -ForegroundColor Yellow

if (-not (Test-PythonInstalled)) {
    if (-not (Install-Python)) {
        Write-Host "❌ Failed to install Python automatically" -ForegroundColor Red
        Write-Host ""
        Write-Host "📋 Manual installation required:" -ForegroundColor Yellow
        Write-Host "   1. Go to: https://www.python.org/downloads/" -ForegroundColor White
        Write-Host "   2. Download Python 3.11 or newer" -ForegroundColor White
        Write-Host "   3. During installation, check 'Add Python to PATH'" -ForegroundColor White
        Write-Host "   4. Restart this script after installation" -ForegroundColor White
        Read-Host "Press Enter to exit"
        exit 1
    }
}

# Setup virtual environment
Write-Host ""
Write-Host "🔧 Setting up virtual environment..." -ForegroundColor Yellow

if (-not (Test-Path "venv")) {
    Write-Host "   Creating virtual environment..." -ForegroundColor Gray
    python -m venv venv
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Failed to create virtual environment" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
}

# Activate virtual environment
Write-Host "   Activating virtual environment..." -ForegroundColor Gray
& .\venv\Scripts\Activate.ps1

# Install required packages
Write-Host "📦 Installing required packages..." -ForegroundColor Yellow
pip install --upgrade pip --quiet
pip install selenium webdriver-manager requests --quiet

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to install required packages" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Check Chrome profiles
Write-Host ""
Write-Host "🔍 Checking for Chrome profiles..." -ForegroundColor Yellow

$chromePaths = @(
    "${env:LOCALAPPDATA}\Google\Chrome\User Data",
    "sessions\google_profiles"
)

$profilesFound = $false
$totalProfiles = 0

foreach ($path in $chromePaths) {
    if (Test-Path $path) {
        $profiles = Get-ChildItem -Path $path -Directory | Where-Object { 
            $_.Name -eq "Default" -or 
            $_.Name -like "Profile *" -or 
            $_.Name -like "*profile*"
        }
        
        if ($profiles.Count -gt 0) {
            Write-Host "   ✅ Found $($profiles.Count) profiles in: $path" -ForegroundColor Green
            $totalProfiles += $profiles.Count
            $profilesFound = $true
        }
    }
}

if (-not $profilesFound) {
    Write-Host "   ⚠️ No Chrome profiles found!" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "📋 To create Chrome profiles:" -ForegroundColor Yellow
    Write-Host "   1. Open Google Chrome" -ForegroundColor White
    Write-Host "   2. Click profile icon (top right)" -ForegroundColor White  
    Write-Host "   3. Add new profile for each Google account" -ForegroundColor White
    Write-Host "   4. Login to different Google accounts in each profile" -ForegroundColor White
    Write-Host "   5. Close Chrome and restart this script" -ForegroundColor White
    Write-Host ""
    $continue = Read-Host "Continue anyway? (y/N)"
    if ($continue -ne 'y' -and $continue -ne 'Y') {
        exit 0
    }
} else {
    Write-Host "   ✅ Total profiles available: $totalProfiles" -ForegroundColor Green
}

# Show setup summary
Write-Host ""
Write-Host "╔══════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║                    SETUP COMPLETE                          ║" -ForegroundColor Cyan
Write-Host "╚══════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""
Write-Host "✅ Python: $(python --version)" -ForegroundColor Green
Write-Host "✅ Virtual Environment: Active" -ForegroundColor Green
Write-Host "✅ Required Packages: Installed" -ForegroundColor Green
Write-Host "✅ Chrome Profiles: $totalProfiles found" -ForegroundColor Green
Write-Host ""
Write-Host "🚀 Starting Shopee Live Viewer Bot..." -ForegroundColor Cyan
Write-Host ""

# Run the bot
try {
    python final_shopee_bot.py
} catch {
    Write-Host "❌ Error running bot: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""
Write-Host "✅ Bot finished!" -ForegroundColor Green
Read-Host "Press Enter to exit"
