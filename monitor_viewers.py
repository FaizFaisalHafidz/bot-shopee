#!/usr/bin/env python3
"""
Shopee Live Monitor
Monitors active viewers and bot performance
"""

import time
import json
import requests
from datetime import datetime, timedelta
from pathlib import Path
import threading
from collections import defaultdict

class ShopeeMonitor:
    def __init__(self):
        self.stats = {
            'total_viewers': 0,
            'active_bots': 0,
            'start_time': datetime.now(),
            'session_url': '',
            'errors': [],
            'device_ids': [],
            'viewer_history': []
        }
        self.running = False
        
    def log_stats(self, message):
        """Log monitoring message with timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {message}")
        
        # Also save to log file
        log_file = Path("logs/monitor.log")
        log_file.parent.mkdir(exist_ok=True)
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(f"[{timestamp}] {message}\n")
    
    def check_live_status(self, session_id):
        """Check if live session is still active"""
        try:
            # This would be actual API call to check session status
            # For now, we'll simulate it
            url = f"https://live.shopee.co.id/share?from=live&session={session_id}&in=1"
            self.stats['session_url'] = url
            return True
        except Exception as e:
            self.log_stats(f"❌ Error checking live status: {e}")
            return False
    
    def count_active_processes(self):
        """Count active Chrome processes (bot instances)"""
        try:
            import psutil
            chrome_processes = []
            
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    if proc.info['name'] and 'chrome' in proc.info['name'].lower():
                        cmdline = ' '.join(proc.info['cmdline'] or [])
                        if 'shopee' in cmdline.lower() or 'live.shopee' in cmdline.lower():
                            chrome_processes.append(proc.info['pid'])
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            return len(chrome_processes)
        except ImportError:
            # psutil not installed, try alternative method
            return self.count_chrome_windows()
        except Exception as e:
            self.log_stats(f"⚠️ Error counting processes: {e}")
            return 0
    
    def count_chrome_windows(self):
        """Alternative method to count Chrome windows"""
        import subprocess
        import platform
        
        try:
            if platform.system() == "Windows":
                # Windows tasklist command
                result = subprocess.run([
                    'tasklist', '/FI', 'IMAGENAME eq chrome.exe'
                ], capture_output=True, text=True)
                lines = result.stdout.split('\n')
                chrome_count = len([line for line in lines if 'chrome.exe' in line])
                return max(0, chrome_count - 1)  # Subtract main Chrome process
                
            elif platform.system() == "Darwin":  # macOS
                result = subprocess.run([
                    'ps', 'aux'
                ], capture_output=True, text=True)
                lines = result.stdout.split('\n')
                chrome_count = len([line for line in lines if 'Chrome' in line and 'shopee' in line.lower()])
                return chrome_count
                
            else:  # Linux
                result = subprocess.run([
                    'ps', 'aux'
                ], capture_output=True, text=True)
                lines = result.stdout.split('\n')
                chrome_count = len([line for line in lines if 'chrome' in line and 'shopee' in line.lower()])
                return chrome_count
                
        except Exception as e:
            self.log_stats(f"⚠️ Error counting Chrome windows: {e}")
            return 0
    
    def read_bot_logs(self):
        """Read bot logs to get device IDs and errors"""
        log_files = [
            "logs/bot.log",
            "logs/hybrid_bot.log", 
            "logs/multi_account_bot.log"
        ]
        
        device_ids = set()
        recent_errors = []
        
        for log_file in log_files:
            log_path = Path(log_file)
            if log_path.exists():
                try:
                    with open(log_path, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                        
                    # Get last 50 lines
                    recent_lines = lines[-50:] if len(lines) > 50 else lines
                    
                    for line in recent_lines:
                        # Extract device IDs
                        if 'device_id' in line.lower() or 'Device ID:' in line:
                            parts = line.split()
                            for part in parts:
                                if len(part) == 32 and part.isupper():
                                    device_ids.add(part)
                        
                        # Extract errors
                        if any(keyword in line.lower() for keyword in ['error', 'failed', 'exception']):
                            recent_errors.append(line.strip())
                            
                except Exception as e:
                    self.log_stats(f"⚠️ Error reading log {log_file}: {e}")
        
        self.stats['device_ids'] = list(device_ids)
        self.stats['errors'] = recent_errors[-5:]  # Keep last 5 errors
        return len(device_ids)
    
    def display_status(self):
        """Display current monitoring status"""
        # Clear screen (works on most terminals)
        import os
        os.system('cls' if os.name == 'nt' else 'clear')
        
        # Header
        print("🤖 SHOPEE LIVE VIEWER BOT MONITOR")
        print("=" * 60)
        print(f"⏰ Running since: {self.stats['start_time'].strftime('%H:%M:%S')}")
        print(f"⏱️ Duration: {datetime.now() - self.stats['start_time']}")
        print(f"🔗 Session URL: {self.stats['session_url']}")
        print()
        
        # Bot Status
        print("🤖 BOT STATUS:")
        print(f"   Active Chrome Processes: {self.stats['active_bots']}")
        print(f"   Unique Device IDs: {len(self.stats['device_ids'])}")
        print(f"   Estimated Viewers: {max(self.stats['active_bots'], len(self.stats['device_ids']))}")
        print()
        
        # Device IDs (show first few)
        if self.stats['device_ids']:
            print("🆔 DEVICE IDs (First 5):")
            for i, device_id in enumerate(self.stats['device_ids'][:5]):
                print(f"   {i+1}. {device_id}")
            if len(self.stats['device_ids']) > 5:
                print(f"   ... and {len(self.stats['device_ids']) - 5} more")
        else:
            print("🆔 DEVICE IDs: None detected")
        print()
        
        # Viewer History (last 10 readings)
        if self.stats['viewer_history']:
            print("📊 VIEWER HISTORY (Last 10):")
            for timestamp, count in self.stats['viewer_history'][-10:]:
                print(f"   {timestamp}: {count} viewers")
        print()
        
        # Recent Errors
        if self.stats['errors']:
            print("❌ RECENT ERRORS:")
            for error in self.stats['errors'][-3:]:
                print(f"   {error}")
        else:
            print("✅ No recent errors")
        print()
        
        # Performance Stats
        uptime = datetime.now() - self.stats['start_time']
        uptime_hours = uptime.total_seconds() / 3600
        avg_viewers = sum(count for _, count in self.stats['viewer_history']) / max(len(self.stats['viewer_history']), 1)
        
        print("📈 PERFORMANCE:")
        print(f"   Uptime: {uptime}")
        print(f"   Average Viewers: {avg_viewers:.1f}")
        print(f"   Viewer Updates: {len(self.stats['viewer_history'])}")
        print()
        
        print("Press Ctrl+C to stop monitoring")
        print("=" * 60)
    
    def monitor_loop(self, session_id=None, update_interval=10):
        """Main monitoring loop"""
        self.log_stats("🚀 Starting Shopee Live Monitor...")
        self.running = True
        
        try:
            while self.running:
                # Count active processes
                self.stats['active_bots'] = self.count_active_processes()
                
                # Read device IDs from logs
                device_count = self.read_bot_logs()
                
                # Record viewer history
                current_time = datetime.now().strftime("%H:%M:%S")
                viewer_count = max(self.stats['active_bots'], device_count)
                self.stats['viewer_history'].append((current_time, viewer_count))
                
                # Keep only last 50 history entries
                if len(self.stats['viewer_history']) > 50:
                    self.stats['viewer_history'] = self.stats['viewer_history'][-50:]
                
                # Check live status if session_id provided
                if session_id:
                    self.check_live_status(session_id)
                
                # Display status
                self.display_status()
                
                # Log summary
                self.log_stats(f"Active: {self.stats['active_bots']} bots, {device_count} unique device IDs")
                
                # Wait for next update
                time.sleep(update_interval)
                
        except KeyboardInterrupt:
            self.log_stats("⚠️ Monitor stopped by user")
        except Exception as e:
            self.log_stats(f"❌ Monitor error: {e}")
        finally:
            self.running = False
            self.log_stats("🏁 Monitor stopped")

def main():
    """Main monitor function"""
    print("🤖 Shopee Live Monitor")
    print("=" * 30)
    
    # Ask for session ID (optional)
    session_id = input("Enter Shopee Live session ID (optional): ").strip()
    if not session_id:
        session_id = None
    
    # Ask for update interval
    try:
        interval = int(input("Update interval in seconds (default 10): ").strip() or "10")
    except ValueError:
        interval = 10
    
    print(f"\n🚀 Starting monitor (update every {interval}s)...")
    print("Press Ctrl+C to stop\n")
    
    # Start monitoring
    monitor = ShopeeMonitor()
    monitor.monitor_loop(session_id, interval)

if __name__ == "__main__":
    main()
