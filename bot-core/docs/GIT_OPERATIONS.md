# GIT OPERATIONS GUIDE - SHOPEE BOT

## 📦 Repository Size Management

**Current Status:**
- Total size: 1.0GB
- Large files: sessions/ (909MB) + venv/ (64MB) + node_modules/ (31MB) = 1004MB
- Core code: ~50MB (safe for git)

## 🧹 Before Git Operations (REQUIRED)

**Run cleanup to remove large files:**
```bash
./cleanup.sh
```

**This will remove:**
- `sessions/` (909MB) - Chrome profiles and user data
- `venv/` (64MB) - Python virtual environment  
- `node_modules/` (31MB) - Node.js dependencies
- Log files and temporary data

**Result: 1.0GB → ~50MB (95% size reduction)**

## 📤 Git Operations

**After cleanup, repository is ready for git:**
```bash
git add .
git commit -m "Add Shopee ultimate real URL bot with authentication bypass"
git push
```

## 📥 After Git Clone

**Recreate environment on target machine:**
```bash
# Linux/Mac
./setup.sh

# Windows
setup.bat
```

**This will:**
- Create virtual environment
- Install Python dependencies (selenium, webdriver-manager, requests)
- Install Node.js dependencies (if npm available)
- Create necessary directories
- Verify installation

## 🔒 .gitignore Coverage

**Automatically excluded:**
- ✅ `sessions/` - Chrome browser data (very large)
- ✅ `venv/` - Virtual environment
- ✅ `node_modules/` - Node dependencies
- ✅ `logs/` - Log files
- ✅ `accounts/` - Sensitive account data
- ✅ `*.log` - All log files
- ✅ `__pycache__/` - Python cache
- ✅ `input.csv` - Sensitive data
- ✅ OS files (.DS_Store, Thumbs.db)
- ✅ IDE files (.vscode/, .idea/)

**Included in git:**
- ✅ Core bot scripts (*.py)
- ✅ Launcher scripts (*.sh, *.bat)
- ✅ Chrome extension source
- ✅ Configuration templates
- ✅ Documentation (README.md, DEPLOYMENT_GUIDE.md)
- ✅ Dependencies list (requirements.txt, package.json)

## 🚀 Deployment Workflow

**Developer side:**
1. `./cleanup.sh` - Remove large files
2. `git add .` - Stage changes
3. `git commit -m "message"` - Commit
4. `git push` - Push to repository

**Target machine side:**
1. `git clone <repository>` - Clone repository
2. `./setup.sh` or `setup.bat` - Setup environment
3. `./ultimate_launcher.sh` - Run bot

## ⚡ Quick Commands

**Development:**
```bash
./cleanup.sh && git add . && git commit -m "Update bot" && git push
```

**Deployment:**
```bash
git clone <repo> && cd bot-live-shopee && ./setup.sh && ./ultimate_launcher.sh
```

---

**Repository optimized for git operations with 95% size reduction while preserving all functionality.**
