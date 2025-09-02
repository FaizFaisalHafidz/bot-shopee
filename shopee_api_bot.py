#!/usr/bin/env python3
"""
Shopee Live API Bot - Direct API Approach
Ultra-reliable viewer boost using Shopee Live API endpoints
"""

import requests
import time
import random
import json
import threading
from datetime import datetime
import concurrent.futures

class ShopeeAPIBot:
    def __init__(self):
        self.active_sessions = []
        self.headers_templates = [
            {
                'User-Agent': 'Mozilla/5.0 (Linux; Android 12; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36',
                'Accept': 'application/json, text/plain, */*',
                'Accept-Language': 'id-ID,id;q=0.9,en;q=0.8',
                'Accept-Encoding': 'gzip, deflate, br',
                'Origin': 'https://live.shopee.co.id',
                'Referer': 'https://live.shopee.co.id/',
                'Connection': 'keep-alive',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-origin',
                'X-Requested-With': 'XMLHttpRequest'
            },
            {
                'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1',
                'Accept': 'application/json',
                'Accept-Language': 'id-ID,id;q=0.9',
                'Origin': 'https://live.shopee.co.id',
                'Referer': 'https://live.shopee.co.id/',
                'Connection': 'keep-alive'
            },
            {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
                'Accept': 'application/json, text/plain, */*',
                'Accept-Language': 'id-ID,id;q=0.9,en;q=0.8',
                'Origin': 'https://live.shopee.co.id',
                'Referer': 'https://live.shopee.co.id/',
                'Connection': 'keep-alive'
            }
        ]
        
        self.device_profiles = [
            {'platform': 'Android', 'model': 'SM-G998B', 'version': '12'},
            {'platform': 'iPhone', 'model': 'iPhone14,2', 'version': '16.6'},
            {'platform': 'Windows', 'model': 'PC', 'version': '10'},
            {'platform': 'Android', 'model': 'Pixel-7', 'version': '13'},
            {'platform': 'iPhone', 'model': 'iPhone15,3', 'version': '17.0'},
        ]

    def generate_device_id(self):
        """Generate random device ID"""
        return ''.join(random.choices('0123456789ABCDEF', k=32))

    def generate_user_id(self):
        """Generate random user ID"""
        return random.randint(10000000, 99999999)

    def get_session_info(self, session_id):
        """Get session information from API"""
        try:
            url = f"https://live.shopee.co.id/api/v1/session/{session_id}/info"
            headers = random.choice(self.headers_templates).copy()
            
            response = requests.get(url, headers=headers, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('err_code') == 0:
                    return data['data']
            
            return None
        except Exception as e:
            print(f"[ERROR] Failed to get session info: {e}")
            return None

    def join_session_api(self, session_id, viewer_index):
        """Join session using API endpoint"""
        max_attempts = 5
        
        for attempt in range(max_attempts):
            try:
                # Generate unique viewer profile
                device_profile = random.choice(self.device_profiles)
                device_id = self.generate_device_id()
                user_id = self.generate_user_id()
                
                # API endpoint
                url = f"https://live.shopee.co.id/api/v1/session/{session_id}/joinv2"
                
                # Headers
                headers = random.choice(self.headers_templates).copy()
                
                # Add session-specific headers
                headers.update({
                    'X-Device-ID': device_id,
                    'X-User-ID': str(user_id),
                    'X-Platform': device_profile['platform'],
                    'X-App-Version': '4.0.0',
                    'Content-Type': 'application/json'
                })
                
                # Payload
                payload = {
                    'device_id': device_id,
                    'user_id': user_id,
                    'platform': device_profile['platform'],
                    'version': device_profile['version'],
                    'timestamp': int(time.time() * 1000),
                    'viewer_type': 'guest',
                    'source': 'share_link'
                }
                
                print(f"[VIEWER {viewer_index}] Joining session via API (attempt {attempt + 1}/{max_attempts})...")
                print(f"[DEVICE] {device_profile['platform']} - Device ID: {device_id[:16]}...")
                print(f"[USER] User ID: {user_id}")
                
                # Make API request
                response = requests.post(url, headers=headers, json=payload, timeout=30)
                
                print(f"[API] Response Status: {response.status_code}")
                
                if response.status_code == 200:
                    data = response.json()
                    print(f"[API] Response: {json.dumps(data, indent=2)[:200]}...")
                    
                    if data.get('err_code') == 0:
                        session_data = data.get('data', {})
                        session_info = session_data.get('session', {})
                        current_viewers = session_info.get('viewer_count', 0)
                        
                        print(f"[SUCCESS] Viewer {viewer_index} joined successfully!")
                        print(f"[VIEWERS] Current viewer count: {current_viewers}")
                        
                        # Store session info
                        viewer_session = {
                            'viewer_id': viewer_index,
                            'session_id': session_id,
                            'device_id': device_id,
                            'user_id': user_id,
                            'device_profile': device_profile,
                            'joined_at': datetime.now(),
                            'viewer_count': current_viewers,
                            'response_data': data
                        }
                        
                        self.active_sessions.append(viewer_session)
                        
                        # Start keep-alive for this session
                        threading.Thread(target=self.keep_alive_session, 
                                       args=(viewer_session,), daemon=True).start()
                        
                        return viewer_session
                    else:
                        error_msg = data.get('err_msg', 'Unknown error')
                        print(f"[WARNING] API returned error: {error_msg}")
                        if 'rate limit' in error_msg.lower() or 'too many' in error_msg.lower():
                            wait_time = (attempt + 1) * 5
                            print(f"[RATE LIMIT] Waiting {wait_time} seconds...")
                            time.sleep(wait_time)
                        
                else:
                    print(f"[WARNING] HTTP {response.status_code}: {response.text[:100]}")
                
            except Exception as e:
                print(f"[ERROR] Attempt {attempt + 1} failed: {e}")
                
                if attempt < max_attempts - 1:
                    wait_time = (attempt + 1) * 3
                    print(f"[RETRY] Waiting {wait_time} seconds before retry...")
                    time.sleep(wait_time)
        
        print(f"[FAILED] Could not join session with viewer {viewer_index} after {max_attempts} attempts")
        return None

    def keep_alive_session(self, viewer_session):
        """Keep session alive with periodic heartbeat"""
        session_id = viewer_session['session_id']
        device_id = viewer_session['device_id']
        user_id = viewer_session['user_id']
        
        print(f"[KEEPALIVE] Starting heartbeat for viewer {viewer_session['viewer_id']}")
        
        while True:
            try:
                # Heartbeat API call
                url = f"https://live.shopee.co.id/api/v1/session/{session_id}/heartbeat"
                
                headers = random.choice(self.headers_templates).copy()
                headers.update({
                    'X-Device-ID': device_id,
                    'X-User-ID': str(user_id),
                    'Content-Type': 'application/json'
                })
                
                payload = {
                    'device_id': device_id,
                    'user_id': user_id,
                    'timestamp': int(time.time() * 1000)
                }
                
                response = requests.post(url, headers=headers, json=payload, timeout=15)
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get('err_code') == 0:
                        session_info = data.get('data', {}).get('session', {})
                        current_viewers = session_info.get('viewer_count', 0)
                        print(f"[HEARTBEAT] Viewer {viewer_session['viewer_id']} alive - Current viewers: {current_viewers}")
                        viewer_session['viewer_count'] = current_viewers
                    else:
                        print(f"[HEARTBEAT] Error for viewer {viewer_session['viewer_id']}: {data.get('err_msg')}")
                
                # Wait 30 seconds between heartbeats
                time.sleep(30)
                
            except Exception as e:
                print(f"[HEARTBEAT ERROR] Viewer {viewer_session['viewer_id']}: {e}")
                time.sleep(60)  # Longer wait on error

    def start_api_bot(self, session_id, viewer_count):
        """Start API bot with multiple viewers"""
        print(f"\n{'='*80}")
        print(f"   SHOPEE LIVE API BOT - DIRECT API APPROACH")
        print(f"   Ultra-reliable viewer boost using API endpoints")
        print(f"{'='*80}")
        print(f"Target Session: {session_id}")
        print(f"Viewer Count: {viewer_count}")
        print(f"Mode: Direct API Calls")
        print(f"Expected Real Boost: {viewer_count} genuine API viewers")
        print(f"{'='*80}\n")
        
        # Get initial session info
        print("[INFO] Getting session information...")
        session_info = self.get_session_info(session_id)
        
        if session_info:
            session_data = session_info.get('session', {})
            initial_viewers = session_data.get('viewer_count', 0)
            title = session_data.get('title', 'Unknown')
            streamer = session_data.get('nickname', 'Unknown')
            
            print(f"[SESSION] Title: {title}")
            print(f"[SESSION] Streamer: {streamer}")
            print(f"[SESSION] Current viewers: {initial_viewers}")
            print(f"[SESSION] Status: {'Live' if session_data.get('status') == 1 else 'Offline'}")
            print()
        else:
            print("[WARNING] Could not get session info, proceeding anyway...")
            initial_viewers = 0
        
        # Join sessions in parallel for faster execution
        print(f"[LAUNCH] Starting {viewer_count} API viewers...")
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=min(viewer_count, 10)) as executor:
            futures = []
            for i in range(viewer_count):
                future = executor.submit(self.join_session_api, session_id, i + 1)
                futures.append(future)
                time.sleep(2)  # Small delay between launches
            
            # Wait for all viewers to join
            successful_joins = 0
            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                if result:
                    successful_joins += 1
        
        print(f"\n[SUMMARY] Successfully joined {successful_joins}/{viewer_count} viewers")
        
        if successful_joins > 0:
            print(f"[SUCCESS] {successful_joins} API viewers are now active!")
            print(f"[BOOST] Expected viewer increase: +{successful_joins}")
            
            # Show current status
            latest_session = max(self.active_sessions, key=lambda x: x['joined_at']) if self.active_sessions else None
            if latest_session:
                current_count = latest_session.get('viewer_count', initial_viewers)
                boost = current_count - initial_viewers
                print(f"[REAL-TIME] Current viewers: {current_count} (+{boost} from initial {initial_viewers})")
            
            print("\n[MONITORING] Bot will keep sessions alive with heartbeat...")
            print("Press Ctrl+C to stop monitoring")
            
            try:
                while True:
                    time.sleep(30)
                    if self.active_sessions:
                        active_count = len(self.active_sessions)
                        latest_viewers = max(s.get('viewer_count', 0) for s in self.active_sessions)
                        print(f"[STATUS] {active_count} viewers active - Latest count: {latest_viewers}")
            except KeyboardInterrupt:
                print("\n[SHUTDOWN] Stopping bot...")
        else:
            print("[FAILED] No viewers could join successfully")

def main():
    if len(sys.argv) >= 3:
        session_id = sys.argv[1]
        viewer_count = int(sys.argv[2])
    else:
        session_id = input("Enter Shopee Live Session ID (e.g., 157658364): ").strip()
        viewer_count_input = input("Enter viewer count (default 5): ").strip()
        viewer_count = int(viewer_count_input) if viewer_count_input else 5
    
    bot = ShopeeAPIBot()
    bot.start_api_bot(session_id, viewer_count)

if __name__ == "__main__":
    import sys
    main()
