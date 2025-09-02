# Shopee Bot - Windows RDP Python Fixer
# PowerShell version with advanced Python detection and installation

$ErrorActionPreference = "SilentlyContinue"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host " SHOPEE BOT - WINDOWS RDP PYTHON FIX" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

function Test-PythonCommand {
    param([string]$Command)
    
    try {
        $output = & $Command --version 2>$null
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ Python found via '$Command': $output" -ForegroundColor Green
            return $Command
        }
    } catch {}
    
    Write-Host "❌ '$Command' command not found" -ForegroundColor Red
    return $null
}

function Find-PythonInstallation {
    Write-Host "[SCAN] Searching for Python installations..." -ForegroundColor Yellow
    
    $searchPaths = @(
        "C:\Python*\python.exe",
        "${env:LOCALAPPDATA}\Programs\Python\Python*\python.exe",
        "${env:PROGRAMFILES}\Python*\python.exe",
        "${env:PROGRAMFILES(X86)}\Python*\python.exe",
        "${env:USERPROFILE}\AppData\Local\Microsoft\WindowsApps\python.exe"
    )
    
    foreach ($pattern in $searchPaths) {
        $pythons = Get-ChildItem -Path $pattern -ErrorAction SilentlyContinue
        foreach ($python in $pythons) {
            if ($python.Exists) {
                try {
                    $version = & $python.FullName --version 2>$null
                    if ($LASTEXITCODE -eq 0) {
                        Write-Host "✅ Found Python: $($python.FullName)" -ForegroundColor Green
                        Write-Host "   Version: $version" -ForegroundColor Gray
                        return $python.FullName
                    }
                } catch {}
            }
        }
    }
    
    return $null
}

function Install-PythonViaWinget {
    try {
        $wingetVersion = winget --version 2>$null
        if ($LASTEXITCODE -eq 0) {
            Write-Host "📦 Installing Python via Windows Package Manager..." -ForegroundColor Yellow
            winget install Python.Python.3.11 --silent --accept-package-agreements --accept-source-agreements --scope machine
            Start-Sleep -Seconds 15
            
            # Refresh environment variables
            $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
            
            return Test-PythonCommand "python"
        }
    } catch {}
    return $null
}

function Install-PythonViaChocolatey {
    try {
        $chocoVersion = choco --version 2>$null
        if ($LASTEXITCODE -eq 0) {
            Write-Host "🍫 Installing Python via Chocolatey..." -ForegroundColor Yellow
            choco install python -y
            Start-Sleep -Seconds 15
            
            # Refresh environment variables
            $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
            
            return Test-PythonCommand "python"
        }
    } catch {}
    return $null
}

function Install-PythonDirect {
    Write-Host "📥 Downloading Python directly from python.org..." -ForegroundColor Yellow
    
    $pythonUrl = "https://www.python.org/ftp/python/3.11.5/python-3.11.5-amd64.exe"
    $tempDir = New-Item -ItemType Directory -Path "python_temp" -Force
    $installerPath = Join-Path $tempDir.FullName "python-3.11.5.exe"
    
    try {
        Write-Host "   Downloading from: $pythonUrl" -ForegroundColor Gray
        Invoke-WebRequest -Uri $pythonUrl -OutFile $installerPath -UseBasicParsing
        
        if (Test-Path $installerPath) {
            Write-Host "✅ Download complete" -ForegroundColor Green
            Write-Host "🔧 Installing Python..." -ForegroundColor Yellow
            
            # Install Python silently
            $process = Start-Process -FilePath $installerPath -ArgumentList "/quiet", "InstallAllUsers=1", "PrependPath=1", "Include_test=0", "Include_doc=0" -Wait -PassThru
            
            if ($process.ExitCode -eq 0) {
                Write-Host "✅ Python installation completed" -ForegroundColor Green
                
                # Refresh environment variables
                $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
                
                Start-Sleep -Seconds 5
                return Test-PythonCommand "python"
            } else {
                Write-Host "❌ Installation failed (Exit code: $($process.ExitCode))" -ForegroundColor Red
            }
        }
    } catch {
        Write-Host "❌ Download/installation failed: $($_.Exception.Message)" -ForegroundColor Red
    } finally {
        Remove-Item -Path $tempDir -Recurse -Force -ErrorAction SilentlyContinue
    }
    
    return $null
}

function Test-ChromeInstallation {
    Write-Host "[2/4] Checking Chrome installation..." -ForegroundColor Yellow
    
    $chromePaths = @(
        "${env:PROGRAMFILES}\Google\Chrome\Application\chrome.exe",
        "${env:PROGRAMFILES(X86)}\Google\Chrome\Application\chrome.exe", 
        "${env:LOCALAPPDATA}\Google\Chrome\Application\chrome.exe"
    )
    
    foreach ($path in $chromePaths) {
        if (Test-Path $path) {
            Write-Host "✅ Chrome found: $path" -ForegroundColor Green
            return $true
        }
    }
    
    Write-Host "⚠️ Chrome not found!" -ForegroundColor Yellow
    Write-Host "   Please install Chrome from: https://www.google.com/chrome/" -ForegroundColor White
    return $false
}

function Test-ChromeProfiles {
    Write-Host "[3/4] Checking Chrome profiles..." -ForegroundColor Yellow
    
    $userDataPath = "${env:LOCALAPPDATA}\Google\Chrome\User Data"
    $profileCount = 0
    
    if (Test-Path $userDataPath) {
        # Check Default profile
        if (Test-Path "$userDataPath\Default\Preferences") {
            Write-Host "✅ Default profile found" -ForegroundColor Green
            $profileCount++
        }
        
        # Check numbered profiles
        $profiles = Get-ChildItem -Path $userDataPath -Directory | Where-Object { $_.Name -match "^Profile \d+$" }
        foreach ($profile in $profiles) {
            if (Test-Path "$($profile.FullName)\Preferences") {
                Write-Host "✅ Profile found: $($profile.Name)" -ForegroundColor Green
                $profileCount++
            }
        }
    }
    
    Write-Host "Total Chrome profiles: $profileCount" -ForegroundColor Cyan
    
    if ($profileCount -eq 0) {
        Write-Host ""
        Write-Host "⚠️ WARNING: No Chrome profiles found!" -ForegroundColor Yellow
        Write-Host "Please create Chrome profiles first:" -ForegroundColor White
        Write-Host "1. Open Google Chrome" -ForegroundColor White
        Write-Host "2. Click profile icon (top right)" -ForegroundColor White
        Write-Host "3. Click 'Add profile'" -ForegroundColor White
        Write-Host "4. Login with different Google accounts" -ForegroundColor White
        Write-Host "5. Repeat for multiple profiles" -ForegroundColor White
        Write-Host ""
        
        $continue = Read-Host "Continue anyway? (y/N)"
        if ($continue -ne 'y' -and $continue -ne 'Y') {
            return $false
        }
    }
    
    return $true
}

# Main execution
Write-Host "Diagnostic: Checking Python installation methods..." -ForegroundColor Yellow
Write-Host ""

# Test standard Python commands
$pythonCmd = Test-PythonCommand "python"
if (-not $pythonCmd) { $pythonCmd = Test-PythonCommand "python3" }
if (-not $pythonCmd) { $pythonCmd = Test-PythonCommand "py" }

# If no standard commands work, search for installations
if (-not $pythonCmd) {
    Write-Host ""
    $pythonCmd = Find-PythonInstallation
}

# If still not found, try installing
if (-not $pythonCmd) {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Red
    Write-Host " PYTHON NOT FOUND - INSTALLING..." -ForegroundColor Red
    Write-Host "========================================" -ForegroundColor Red
    Write-Host ""
    
    # Try different installation methods
    $pythonCmd = Install-PythonViaWinget
    if (-not $pythonCmd) { $pythonCmd = Install-PythonViaChocolatey }
    if (-not $pythonCmd) { $pythonCmd = Install-PythonDirect }
    
    if (-not $pythonCmd) {
        Write-Host ""
        Write-Host "========================================" -ForegroundColor Red
        Write-Host " MANUAL INSTALLATION REQUIRED" -ForegroundColor Red
        Write-Host "========================================" -ForegroundColor Red
        Write-Host ""
        Write-Host "All automatic installation methods failed." -ForegroundColor Red
        Write-Host "Please install Python manually:" -ForegroundColor White
        Write-Host ""
        Write-Host "Option 1 - Microsoft Store (Recommended):" -ForegroundColor Yellow
        Write-Host "1. Open Microsoft Store" -ForegroundColor White
        Write-Host "2. Search for 'Python 3.11'" -ForegroundColor White
        Write-Host "3. Install the official Python package" -ForegroundColor White
        Write-Host ""
        Write-Host "Option 2 - Direct Download:" -ForegroundColor Yellow
        Write-Host "1. Go to: https://www.python.org/downloads/" -ForegroundColor White
        Write-Host "2. Download Python 3.11 or newer" -ForegroundColor White
        Write-Host "3. During installation check 'Add Python to PATH'" -ForegroundColor White
        Write-Host "4. Restart this script after installation" -ForegroundColor White
        
        Read-Host "Press Enter to exit"
        exit 1
    }
}

# Setup bot environment
Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host " SETTING UP SHOPEE BOT" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

Write-Host "✅ Using Python: $pythonCmd" -ForegroundColor Green
& $pythonCmd --version

Write-Host ""
Write-Host "[1/4] Installing required packages..." -ForegroundColor Yellow
& $pythonCmd -m pip install --upgrade pip --quiet
& $pythonCmd -m pip install selenium webdriver-manager requests colorama --quiet

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to install packages!" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "✅ Packages installed successfully!" -ForegroundColor Green

# Check Chrome and profiles
Test-ChromeInstallation
if (-not (Test-ChromeProfiles)) {
    exit 1
}

# Run the bot
Write-Host ""
Write-Host "[4/4] Starting Shopee Bot..." -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

if (Test-Path "final_shopee_bot.py") {
    Write-Host "🚀 Starting final_shopee_bot.py..." -ForegroundColor Green
    & $pythonCmd final_shopee_bot.py
} else {
    Write-Host "❌ final_shopee_bot.py not found!" -ForegroundColor Red
    Write-Host "Available Python files:" -ForegroundColor Yellow
    Get-ChildItem -Name "*.py"
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host " BOT EXECUTION COMPLETE" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Read-Host "Press Enter to exit"
