#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Shopee Live Bot - Guest Mode
Bot sederhana untuk like dan view tanpa login
"""

import requests
import time
import random
import threading
from datetime import datetime

class ShopeeLiveBotGuest:
    def __init__(self):
        self.running = False
        self.threads = []
        self.stats = {
            'like_attempts': 0,
            'like_success': 0,
            'viewer_attempts': 0,
            'viewer_success': 0
        }
        
    def create_guest_session(self):
        """Buat session guest baru"""
        session = requests.Session()
        
        # Random User Agent untuk setiap session
        user_agents = [
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36'
        ]
        
        session.headers.update({
            'User-Agent': random.choice(user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'id,en-US;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
        
        return session
    
    def send_guest_like(self, session_id, worker_id):
        """Kirim like sebagai guest"""
        try:
            session = self.create_guest_session()
            
            # Step 1: Access live page untuk get fresh cookies
            live_url = f"https://live.shopee.co.id/share?session={session_id}"
            
            response = session.get(live_url, timeout=10)
            
            if response.status_code != 200:
                return False
            
            # Wait a bit to simulate real user
            time.sleep(random.uniform(1, 3))
            
            # Step 2: Try like API
            like_url = f"https://live.shopee.co.id/api/v1/session/{session_id}/like"
            
            like_headers = {
                'Accept': 'application/json, text/plain, */*',
                'Content-Type': 'application/json;charset=UTF-8',
                'Origin': 'https://live.shopee.co.id',
                'Referer': live_url,
                'X-Livestreaming-Source': 'shopee',
            }
            
            session.headers.update(like_headers)
            
            payload = {"timestamp": int(time.time() * 1000)}
            
            like_response = session.post(like_url, json=payload, timeout=10)
            
            current_time = datetime.now().strftime("%H:%M:%S")
            
            if like_response.status_code == 200:
                try:
                    data = like_response.json()
                    if data.get('err_code') == 0:
                        self.stats['like_success'] += 1
                        print(f"[{current_time}] 👍 LIKE #{worker_id} = ✅ BERHASIL!")
                        return True
                    else:
                        print(f"[{current_time}] 👍 LIKE #{worker_id} = ⚠️ API Error: {data.get('err_msg', 'Unknown')}")
                        return False
                except:
                    # Non-JSON bisa jadi success
                    self.stats['like_success'] += 1
                    print(f"[{current_time}] 👍 LIKE #{worker_id} = ✅ BERHASIL (Non-JSON)!")
                    return True
            else:
                print(f"[{current_time}] 👍 LIKE #{worker_id} = ❌ HTTP {like_response.status_code}")
                return False
                
        except Exception as e:
            current_time = datetime.now().strftime("%H:%M:%S")
            print(f"[{current_time}] 👍 LIKE #{worker_id} = ❌ Exception: {str(e)[:30]}...")
            return False
    
    def simulate_viewer(self, session_id, worker_id):
        """Simulate viewer activity"""
        try:
            session = self.create_guest_session()
            
            live_url = f"https://live.shopee.co.id/share?session={session_id}"
            
            # Simulate viewing activity
            for view_count in range(random.randint(3, 8)):
                if not self.running:
                    break
                
                response = session.get(live_url, timeout=10)
                
                current_time = datetime.now().strftime("%H:%M:%S")
                
                if response.status_code == 200:
                    self.stats['viewer_success'] += 1
                    print(f"[{current_time}] 👀 VIEWER #{worker_id} = ✅ Active (View {view_count + 1})")
                else:
                    print(f"[{current_time}] 👀 VIEWER #{worker_id} = ❌ HTTP {response.status_code}")
                
                # Random wait time between views
                time.sleep(random.uniform(10, 30))
                
        except Exception as e:
            current_time = datetime.now().strftime("%H:%M:%S")
            print(f"[{current_time}] 👀 VIEWER #{worker_id} = ❌ Exception: {str(e)[:30]}...")
    
    def like_worker(self, session_id, target_likes, worker_id):
        """Worker untuk kirim like"""
        likes_sent = 0
        
        while self.running and likes_sent < target_likes:
            self.stats['like_attempts'] += 1
            
            success = self.send_guest_like(session_id, worker_id)
            
            if success:
                likes_sent += 1
            
            # Random delay between likes
            time.sleep(random.uniform(3, 8))
        
        current_time = datetime.now().strftime("%H:%M:%S")
        print(f"[{current_time}] 🏁 Like Worker #{worker_id} finished! Sent: {likes_sent}/{target_likes}")
    
    def viewer_worker(self, session_id, worker_id):
        """Worker untuk simulate viewer"""
        while self.running:
            self.stats['viewer_attempts'] += 1
            self.simulate_viewer(session_id, worker_id)
            
            if not self.running:
                break
            
            # Wait before next viewing session
            time.sleep(random.uniform(5, 15))
        
        current_time = datetime.now().strftime("%H:%M:%S")
        print(f"[{current_time}] 🏁 Viewer Worker #{worker_id} finished!")
    
    def start_like_bot(self, session_id, target_likes=50, workers=5):
        """Start like bot dengan multiple workers"""
        print(f"\n🚀 STARTING GUEST LIKE BOT")
        print(f"{'='*50}")
        print(f"📱 Session ID: {session_id}")
        print(f"🎯 Target Likes: {target_likes}")
        print(f"👥 Workers: {workers}")
        print(f"{'='*50}")
        
        self.running = True
        likes_per_worker = target_likes // workers
        
        # Start like workers
        for i in range(workers):
            thread = threading.Thread(
                target=self.like_worker, 
                args=(session_id, likes_per_worker, i+1),
                daemon=True
            )
            thread.start()
            self.threads.append(thread)
            print(f"👍 Started Like Worker #{i+1} (Target: {likes_per_worker})")
            time.sleep(1)
        
        try:
            # Monitor progress
            while self.running:
                time.sleep(10)
                print(f"\n📊 PROGRESS: Attempts: {self.stats['like_attempts']} | Success: {self.stats['like_success']} | Rate: {(self.stats['like_success']/max(self.stats['like_attempts'],1)*100):.1f}%")
                
                # Check if all workers are done
                if all(not t.is_alive() for t in self.threads):
                    break
                    
        except KeyboardInterrupt:
            print(f"\n🛑 Like Bot dihentikan oleh user!")
            self.running = False
        
        # Final stats
        print(f"\n🎉 LIKE BOT COMPLETED!")
        print(f"📊 Final Stats:")
        print(f"   Attempts: {self.stats['like_attempts']}")
        print(f"   Success: {self.stats['like_success']}")
        print(f"   Success Rate: {(self.stats['like_success']/max(self.stats['like_attempts'],1)*100):.1f}%")
    
    def start_viewer_bot(self, session_id, viewers=10):
        """Start viewer bot"""
        print(f"\n🚀 STARTING GUEST VIEWER BOT")
        print(f"{'='*50}")
        print(f"📱 Session ID: {session_id}")
        print(f"👀 Viewers: {viewers}")
        print(f"{'='*50}")
        
        self.running = True
        
        # Start viewer workers
        for i in range(viewers):
            thread = threading.Thread(
                target=self.viewer_worker,
                args=(session_id, i+1),
                daemon=True
            )
            thread.start()
            self.threads.append(thread)
            print(f"👀 Started Viewer Worker #{i+1}")
            time.sleep(2)
        
        try:
            while self.running:
                time.sleep(15)
                print(f"\n📊 VIEWER STATS: Attempts: {self.stats['viewer_attempts']} | Active: {self.stats['viewer_success']}")
                
        except KeyboardInterrupt:
            print(f"\n🛑 Viewer Bot dihentikan oleh user!")
            self.running = False
        
        print(f"\n🎉 VIEWER BOT COMPLETED!")
        print(f"📊 Final Stats:")
        print(f"   Total Views: {self.stats['viewer_success']}")
    
    def stop_bot(self):
        """Stop bot"""
        self.running = False
        for thread in self.threads:
            thread.join(timeout=2)
        self.threads.clear()

def main():
    print("🚀 SHOPEE LIVE BOT - GUEST MODE")
    print("Simple bot tanpa login untuk like & viewer")
    print("="*60)
    
    session_id = input("📱 Masukkan Session ID: ").strip()
    if not session_id or not session_id.isdigit():
        print("❌ Session ID harus berupa angka!")
        return
    
    print(f"\n📋 PILIH MODE:")
    print(f"1. Like Bot")
    print(f"2. Viewer Bot")
    print(f"3. Both (Like + Viewer)")
    
    mode = input("Pilih mode (1-3): ").strip()
    
    bot = ShopeeLiveBotGuest()
    
    try:
        if mode == '1':
            target_likes = int(input("🎯 Target likes (default: 50): ") or "50")
            workers = int(input("👥 Workers (default: 5): ") or "5")
            bot.start_like_bot(session_id, target_likes, workers)
            
        elif mode == '2':
            viewers = int(input("👀 Jumlah viewers (default: 10): ") or "10")
            bot.start_viewer_bot(session_id, viewers)
            
        elif mode == '3':
            target_likes = int(input("🎯 Target likes (default: 30): ") or "30")
            like_workers = int(input("👥 Like workers (default: 3): ") or "3")
            viewers = int(input("👀 Viewers (default: 7): ") or "7")
            
            # Start both in parallel
            like_thread = threading.Thread(
                target=bot.start_like_bot,
                args=(session_id, target_likes, like_workers),
                daemon=True
            )
            
            viewer_thread = threading.Thread(
                target=bot.start_viewer_bot,
                args=(session_id, viewers),
                daemon=True
            )
            
            like_thread.start()
            time.sleep(2)
            viewer_thread.start()
            
            like_thread.join()
            viewer_thread.join()
        else:
            print("❌ Mode tidak valid!")
            
    except KeyboardInterrupt:
        print(f"\n👋 Bot dihentikan oleh user!")
        bot.stop_bot()
    except Exception as e:
        print(f"❌ Error: {e}")
        bot.stop_bot()

if __name__ == "__main__":
    main()
