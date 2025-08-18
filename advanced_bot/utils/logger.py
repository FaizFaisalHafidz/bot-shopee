#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bot Logger Utility
Simple logging for bot operations
"""

import os
import time
from datetime import datetime

class BotLogger:
    def __init__(self, log_file="bot_advanced.log"):
        self.log_file = log_file
        self.ensure_log_directory()
    
    def ensure_log_directory(self):
        """Ensure log directory exists"""
        log_dir = os.path.dirname(self.log_file) if os.path.dirname(self.log_file) else "."
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
    
    def _write_log(self, level, message):
        """Write log entry to file"""
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_entry = f"[{timestamp}] {level}: {message}\n"
            
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(log_entry)
        except Exception as e:
            print(f"⚠️  Logging error: {e}")
    
    def info(self, message):
        """Log info message"""
        self._write_log("INFO", message)
    
    def error(self, message):
        """Log error message"""
        self._write_log("ERROR", message)
    
    def success(self, message):
        """Log success message"""
        self._write_log("SUCCESS", message)
    
    def warning(self, message):
        """Log warning message"""
        self._write_log("WARNING", message)
