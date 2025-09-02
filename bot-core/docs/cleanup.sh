#!/bin/bash
# CLEANUP SCRIPT - Remove large files before git operations
# Total size reduction: ~1GB+ (sessions: 909MB + venv: 64MB + node_modules: 31MB)

echo "=============================================================================="
echo "   SHOPEE BOT - CLEANUP LARGE FILES"
echo "   Removing large directories and temporary files before git operations"
echo "=============================================================================="
echo

# Calculate current size
echo "[BEFORE] Calculating current directory size..."
BEFORE_SIZE=$(du -sh . 2>/dev/null | cut -f1)
echo "Current size: $BEFORE_SIZE"
echo

# Remove Chrome sessions (909MB)
if [ -d "sessions" ]; then
    echo "[CLEANUP] Removing Chrome sessions directory (909MB)..."
    rm -rf sessions/
    echo "✅ Sessions removed"
else
    echo "⚠️ Sessions directory not found"
fi

# Remove virtual environment (64MB) 
if [ -d "venv" ]; then
    echo "[CLEANUP] Removing virtual environment (64MB)..."
    rm -rf venv/
    echo "✅ Virtual environment removed"
else
    echo "⚠️ Virtual environment not found"
fi

# Remove node_modules (31MB)
if [ -d "node_modules" ]; then
    echo "[CLEANUP] Removing node_modules (31MB)..."
    rm -rf node_modules/
    echo "✅ Node modules removed"
else
    echo "⚠️ Node modules not found"
fi

# Remove logs directory
if [ -d "logs" ]; then
    echo "[CLEANUP] Removing logs directory..."
    rm -rf logs/
    echo "✅ Logs removed"
else
    echo "⚠️ Logs directory not found"
fi

# Remove large sensitive files
if [ -f "input.csv" ]; then
    echo "[CLEANUP] Removing sensitive input.csv..."
    rm -f input.csv
    echo "✅ input.csv removed"
fi

# Remove temporary files
echo "[CLEANUP] Removing temporary files..."
find . -name "*.tmp" -delete 2>/dev/null
find . -name "*.temp" -delete 2>/dev/null
find . -name "*.log" -delete 2>/dev/null
find . -name "*.cache" -delete 2>/dev/null
find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null
find . -name "*.pyc" -delete 2>/dev/null
rm -f temp_profiles.json 2>/dev/null
echo "✅ Temporary files cleaned"

# Remove OS files
echo "[CLEANUP] Removing OS files..."
find . -name ".DS_Store" -delete 2>/dev/null
find . -name "Thumbs.db" -delete 2>/dev/null
find . -name "desktop.ini" -delete 2>/dev/null
echo "✅ OS files cleaned"

# Calculate final size
echo
echo "[AFTER] Calculating final directory size..."
AFTER_SIZE=$(du -sh . 2>/dev/null | cut -f1)
echo "Final size: $AFTER_SIZE"
echo

echo "=============================================================================="
echo "   CLEANUP COMPLETED"
echo "=============================================================================="
echo "Size reduction: $BEFORE_SIZE → $AFTER_SIZE"
echo
echo "Removed directories:"
echo "  ✅ sessions/ (909MB) - Chrome profiles and user data"
echo "  ✅ venv/ (64MB) - Python virtual environment"  
echo "  ✅ node_modules/ (31MB) - Node.js dependencies"
echo "  ✅ logs/ - Log files"
echo "  ✅ Temporary and cache files"
echo
echo "Repository is now ready for git operations!"
echo "=============================================================================="
echo
echo "Next steps:"
echo "1. git add ."
echo "2. git commit -m 'Add Shopee bot with ultimate real URL structure'"
echo "3. git push"
echo
echo "Note: Run './setup.sh' on target machine to recreate virtual environment"
