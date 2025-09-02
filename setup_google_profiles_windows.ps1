# Google Profile Setup - Windows PowerShell
# Setup 100 Google profiles untuk RDP Windows

Write-Host "========================================" -ForegroundColor Cyan
Write-Host " Google Profile Setup - Windows PS1" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check Python installation
try {
    $pythonVersion = python --version
    Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ ERROR: Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python first: https://www.python.org/downloads/" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Check Chrome installation
$chromePaths = @(
    "${env:ProgramFiles}\Google\Chrome\Application\chrome.exe",
    "${env:ProgramFiles(x86)}\Google\Chrome\Application\chrome.exe",
    "${env:LOCALAPPDATA}\Google\Chrome\Application\chrome.exe"
)

$chromeFound = $false
foreach ($path in $chromePaths) {
    if (Test-Path $path) {
        Write-Host "✅ Chrome found: $path" -ForegroundColor Green
        $chromeFound = $true
        break
    }
}

if (-not $chromeFound) {
    Write-Host "❌ ERROR: Google Chrome not found!" -ForegroundColor Red
    Write-Host "Please install Chrome first: https://www.google.com/chrome/" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Create virtual environment if not exists
if (-not (Test-Path "venv")) {
    Write-Host "🔧 Creating Python virtual environment..." -ForegroundColor Yellow
    python -m venv venv
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ ERROR: Failed to create virtual environment" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
}

# Activate virtual environment
Write-Host "🔄 Activating virtual environment..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1

# Install/upgrade packages
Write-Host "📦 Installing required packages..." -ForegroundColor Yellow
pip install --upgrade pip
pip install selenium webdriver-manager requests

# Check CSV file
if (-not (Test-Path "accounts\google_accounts_100.csv")) {
    Write-Host "❌ ERROR: accounts\google_accounts_100.csv not found!" -ForegroundColor Red
    Write-Host "Please create the CSV file with your Google accounts first." -ForegroundColor Yellow
    
    # Create sample CSV
    $sampleCSV = @"
email,password,profile_name,status,setup_date
your_email1@gmail.com,your_password1,profile1,active,
your_email2@gmail.com,your_password2,profile2,active,
your_email3@gmail.com,your_password3,profile3,active,
"@
    
    New-Item -ItemType Directory -Path "accounts" -Force | Out-Null
    $sampleCSV | Out-File -FilePath "accounts\google_accounts_100.csv" -Encoding UTF8
    
    Write-Host "📝 Sample CSV created: accounts\google_accounts_100.csv" -ForegroundColor Green
    Write-Host "Please edit this file with your actual Google accounts." -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Count accounts
$accountCount = (Import-Csv "accounts\google_accounts_100.csv").Count
Write-Host "📊 Found $accountCount Google accounts in CSV" -ForegroundColor Green

# Confirm setup
Write-Host ""
Write-Host "🎯 READY TO SETUP GOOGLE PROFILES" -ForegroundColor Cyan
Write-Host "   Accounts: $accountCount" -ForegroundColor White
Write-Host "   Chrome: Real Chrome (not Chromium)" -ForegroundColor White
Write-Host "   Profiles: Individual per account" -ForegroundColor White
Write-Host "   Location: sessions/google_profiles/" -ForegroundColor White
Write-Host ""

$confirm = Read-Host "Continue with Google profile setup? (y/N)"
if ($confirm -ne 'y' -and $confirm -ne 'Y') {
    Write-Host "❌ Setup cancelled" -ForegroundColor Red
    exit 0
}

Write-Host ""
Write-Host "🚀 Starting Google Profile Setup..." -ForegroundColor Cyan
Write-Host "   Please complete any 2FA/Captcha manually when prompted" -ForegroundColor Yellow
Write-Host "   Keep this PowerShell window open during setup" -ForegroundColor Yellow
Write-Host ""

# Run setup
python google_profile_setup_windows.py

Write-Host ""
Write-Host "✅ Google Profile Setup Complete!" -ForegroundColor Green
Read-Host "Press Enter to exit"
