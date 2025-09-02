#!/usr/bin/env python3
"""
QUICK TEST LAUNCHER - RDP Bot
Launcher sederhana untuk test bot di RDP
"""

import sys
import os

def main():
    print("="*60)
    print("      SHOPEE RDP BOT - QUICK TEST LAUNCHER")
    print("="*60)
    
    # Get session ID
    if len(sys.argv) < 2:
        session_id = input("Enter Session ID: ").strip()
    else:
        session_id = sys.argv[1]
    
    # Get viewer count
    if len(sys.argv) < 3:
        viewer_count_input = input("Enter Viewer Count (default 1): ").strip()
        viewer_count = int(viewer_count_input) if viewer_count_input else 1
    else:
        viewer_count = int(sys.argv[2])
    
    print(f"\n[CONFIG] Session ID: {session_id}")
    print(f"[CONFIG] Viewers: {viewer_count}")
    print(f"[CONFIG] Mode: RDP Ultra-Optimized")
    print("-"*60)
    
    # Import and run bot
    try:
        sys.path.append('bot-core/bots')
        from real_url_bot_rdp import ShopeeRealURLBotRDP
        
        print("[INIT] Starting RDP bot...")
        bot = ShopeeRealURLBotRDP()
        bot.start_rdp_bot(session_id, viewer_count)
        
    except KeyboardInterrupt:
        print("\n[STOP] Bot stopped by user")
    except ImportError as e:
        print(f"[ERROR] Import error: {e}")
        print("[FIX] Make sure you're in the correct directory")
    except Exception as e:
        print(f"[ERROR] Bot error: {e}")

if __name__ == "__main__":
    main()
