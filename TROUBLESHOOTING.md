# TROUBLESHOOTING GUIDE - Window Closing Issues

## Problem
Command Prompt window closes unexpectedly after user input during bot execution.

## Root Causes Analysis
The window closing issue can occur due to:
1. Python script errors causing sys.exit() calls
2. Command Prompt encoding issues  
3. Missing dependencies causing import errors
4. Invalid parameters causing script crashes
5. File path issues on Windows systems

## Debugging Tools Created

### 1. test_cmd_stability.bat
**Purpose**: Test Windows Command Prompt stability
**Usage**: 
```
test_cmd_stability.bat
```
**What it tests**:
- Basic input handling
- Python calls
- Parameter parsing
- File existence
- Multiple inputs simulation
- Error handling

### 2. debug_comprehensive.bat  
**Purpose**: Complete system diagnosis
**Usage**:
```
debug_comprehensive.bat
```
**What it checks**:
- System information
- Python installation
- Dependencies (selenium, webdriver-manager)
- File structure
- Chrome profiles detection  
- Bot syntax validation
- Parameter testing
- Chrome instance creation

### 3. run_safe_mode.bat
**Purpose**: Safe execution with comprehensive error handling
**Usage**:
```
run_safe_mode.bat
```
**Features**:
- Step-by-step validation
- Safe user input handling
- Detailed logging
- Error trapping
- Graceful exit handling

### 4. test_encoding.bat + test_encoding.py
**Purpose**: Test Unicode/encoding compatibility
**Usage**:
```
test_encoding.bat
```

## Fixes Applied

### Python Scripts (detect_profiles.py, shopee_bot.py)
1. **Encoding fixes**:
   - Replaced emoji characters with ASCII text
   - Added UTF-8 encoding handlers
   - Fixed Windows codepage compatibility

2. **Error handling**:
   - Added comprehensive try-catch blocks
   - Better parameter validation  
   - Graceful exit instead of sys.exit()

3. **Logging enhancements**:
   - Detailed debug output
   - Error code reporting
   - Step-by-step execution logs

### BAT Files (run.bat, etc.)
1. **Error trapping**:
   - Capture exit codes before testing
   - Use pause >nul instead of pause  
   - Better error messaging

2. **Input validation**:
   - Check for empty inputs
   - Validate numeric inputs
   - Confirmation prompts

## Troubleshooting Steps

### Step 1: Run Stability Test
```
test_cmd_stability.bat
```
This will identify exactly where the window closing occurs.

### Step 2: Run Comprehensive Debug
```  
debug_comprehensive.bat
```
This checks all system components and creates debug_comprehensive.log.

### Step 3: Use Safe Mode
```
run_safe_mode.bat
```
This provides the safest execution environment with full error handling.

### Step 4: Check Log Files
If issues persist, check these log files:
- `bot_safe_mode.log` - Safe mode execution log
- `debug_comprehensive.log` - System diagnostic log  
- `%TEMP%\shopee_bot\*.txt` - Detailed execution logs

## Common Solutions

### Issue: Python not found
**Solution**: Install Python and add to PATH

### Issue: Missing dependencies  
**Solution**: Run `pip install selenium webdriver-manager`

### Issue: Chrome profiles not detected
**Solution**: 
1. Run Chrome at least once to create profiles
2. Check Windows profile paths in debug log
3. Manually create profiles if needed

### Issue: Encoding errors
**Solution**: Use run_safe_mode.bat which handles encoding automatically

### Issue: Parameter parsing errors
**Solution**: Use safe mode which validates all inputs

## Windows RDP Specific Issues

### Issue: Window closing in RDP environment
**Solutions**:
1. Use run_safe_mode.bat instead of run.bat
2. Check RDP session stability
3. Increase RDP timeout settings
4. Use alternative terminal (PowerShell)

### Issue: Chrome driver issues in RDP  
**Solutions**:
1. Install Chrome in RDP session
2. Use --no-sandbox Chrome option
3. Check display settings

## Next Steps

1. Run `test_cmd_stability.bat` first to identify specific failure point
2. If that passes, run `debug_comprehensive.bat` for full system check  
3. Use `run_safe_mode.bat` for actual bot execution
4. Share log files if issues persist

## Contact Information
If issues continue after following this guide, provide:
1. Contents of debug_comprehensive.log
2. Contents of bot_safe_mode.log  
3. Output from test_cmd_stability.bat
4. Windows version and RDP details
