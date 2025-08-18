#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Shopee Live Streaming Bot
Bot untuk menambahkan likes, viewers, dan ATC pada live streaming Shopee
"""

import requests
import time
import random
import json
import csv
import threading
from urllib.parse import urlencode
import sys
import os
from datetime import datetime

class ShopeeBot:
    def __init__(self):
        self.accounts = []
        self.session_id = None
        self.running = False
        self.threads = []
        
        # Headers dasar untuk request
        self.base_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'id-ID,id;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Origin': 'https://live.shopee.co.id',
            'Referer': 'https://live.shopee.co.id/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"'
        }
        
    def load_accounts(self):
        """Memuat akun dari file input.csv"""
        try:
            with open('input.csv', 'r', encoding='utf-8') as file:
                content = file.read().strip()
                lines = [line.strip() for line in content.split('\n') if line.strip()]
                
                for line_num, line in enumerate(lines, 1):
                    # Skip comment lines or empty lines
                    if line.startswith('#') or not line:
                        continue
                        
                    account = self.parse_cookies(line)
                    if account:
                        self.accounts.append(account)
                        print(f"✅ Akun {line_num}: User ID {account['user_id'][:8]}... loaded")
                    else:
                        print(f"⚠️ Akun {line_num}: Cookie tidak valid, dilewati")
            
            print(f"\n✅ Berhasil memuat {len(self.accounts)} akun valid dari input.csv")
            return len(self.accounts) > 0
        except FileNotFoundError:
            print("❌ File input.csv tidak ditemukan!")
            return False
        except Exception as e:
            print(f"❌ Error membaca file: {e}")
            return False
    
    def parse_cookies(self, cookie_string):
        """Parse cookie string menjadi dict"""
        try:
            cookies = {}
            # Membersihkan string cookie dari karakter yang tidak perlu
            cookie_string = cookie_string.strip()
            
            # Split berdasarkan ";" untuk memisahkan setiap cookie (dari input.csv format)
            for cookie in cookie_string.split(';'):
                if '=' in cookie:
                    key, value = cookie.strip().split('=', 1)
                    cookies[key.strip()] = value.strip()
            
            # Validasi cookie yang diperlukan untuk Shopee
            required_cookies = ['SPC_U']
            important_cookies = ['SPC_T_ID', 'SPC_ST', 'SPC_EC']
            
            # Check apakah cookie yang diperlukan ada
            missing_required = [cookie for cookie in required_cookies if cookie not in cookies]
            if missing_required:
                print(f"❌ Cookie tidak lengkap! Missing: {', '.join(missing_required)}")
                return None
            
            # Validasi format SPC_U (harus berupa angka)
            if not cookies['SPC_U'].isdigit():
                print(f"❌ SPC_U tidak valid: {cookies['SPC_U']}")
                return None
            
            return {
                'cookies': cookies,
                'user_id': cookies.get('SPC_U', ''),
                'token': cookies.get('SPC_T_ID', ''),
                'csrf': cookies.get('csrftoken', ''),
                'session_token': cookies.get('SPC_ST', ''),
                'ec_token': cookies.get('SPC_EC', ''),
                'has_important_cookies': all(cookie in cookies for cookie in important_cookies)
            }
            
        except Exception as e:
            print(f"❌ Error parsing cookies: {e}")
            return None
    
    def extract_session_id(self, input_text):
        """Extract session ID dari berbagai format URL Shopee"""
        import re
        
        # Remove whitespace
        input_text = input_text.strip()
        
        # Jika sudah berupa angka saja
        if input_text.isdigit():
            return input_text
        
        # Format 1: https://live.shopee.co.id/share?from=live&session=12345678
        pattern1 = r'[?&]session=(\d+)'
        match1 = re.search(pattern1, input_text)
        if match1:
            return match1.group(1)
        
        # Format 2: https://live.shopee.co.id/12345678 (legacy format)
        pattern2 = r'https://live\.shopee\.co\.id/(\d+)'
        match2 = re.search(pattern2, input_text)
        if match2:
            return match2.group(1)
        
        # Format 3: session=12345678 (jika hanya copy parameter)
        pattern3 = r'session=(\d+)'
        match3 = re.search(pattern3, input_text)
        if match3:
            return match3.group(1)
        
        return None
        
    def get_live_info(self, session_id):
        """Mendapatkan informasi live streaming dengan API yang benar"""
        url = f"https://live.shopee.co.id/api/v1/session/{session_id}"
        
        headers = self.base_headers.copy()
        headers.update({
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'id,en-US;q=0.9,en;q=0.8',
            'Client-Info': 'os=2;platform=9;scene_id=17;language=id;device_id=9c968575-05a6-4a5b-85df-d7ea4bbc31bf',
            'Referer': f'https://live.shopee.co.id/share?from=live&session={session_id}',
        })
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get('err_code') == 0 and 'data' in data:
                    session_data = data['data'].get('session', {})
                    return {
                        'session_id': session_id,
                        'title': session_data.get('title', 'Live Stream'),
                        'username': session_data.get('nickname', 'Streamer'),
                        'like_count': session_data.get('like_cnt', 0),
                        'viewer_count': session_data.get('viewer_count', 0),
                        'status': session_data.get('status', 0),
                        'products': data['data'].get('items', [])
                    }
            return None
        except Exception as e:
            print(f"Error getting live info: {e}")
            return None
    
    def send_like(self, account, session_id):
        """Mengirim like ke live streaming dengan guest session"""
        
        # Buat session fresh untuk setiap request
        session = requests.Session()
        
        # Access live page dulu untuk mendapatkan fresh cookies
        live_url = f"https://live.shopee.co.id/share?session={session_id}"
        
        page_headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'id,en-US;q=0.9,en;q=0.8',
        }
        
        try:
            # Step 1: Access live page to get fresh session
            page_response = session.get(live_url, headers=page_headers, timeout=10)
            
            if page_response.status_code != 200:
                return False
            
            # Step 2: Use fresh session untuk like API
            api_url = f"https://live.shopee.co.id/api/v1/session/{session_id}/like"
            
            api_headers = {
                'Accept': 'application/json, text/plain, */*',
                'Accept-Language': 'id,en-US;q=0.9,en;q=0.8',
                'Content-Type': 'application/json;charset=UTF-8',
                'Origin': 'https://live.shopee.co.id',
                'Referer': live_url,
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
                'X-Livestreaming-Source': 'shopee',
            }
            
            payload = {"timestamp": int(time.time() * 1000)}
            
            response = session.post(api_url, headers=api_headers, json=payload, timeout=10)
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    if data.get('err_code') == 0:
                        return True
                    else:
                        # Don't print error for guest session attempts
                        return False
                except:
                    # Non-JSON response might be success
                    return True
            return False
            
        except Exception as e:
            return False
    
    def join_live(self, account, session_id):
        """Join live streaming sebagai viewer dengan guest session"""
        
        # Gunakan fresh session untuk setiap viewer
        session = requests.Session()
        
        # Access live page multiple times untuk simulate viewer
        live_url = f"https://live.shopee.co.id/share?from=live&session={session_id}"
        
        headers = {
            'User-Agent': f'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{random.randint(100, 120)}.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'id,en-US;q=0.9,en;q=0.8',
            'Referer': 'https://shopee.co.id/',
        }
        
        try:
            response = session.get(live_url, headers=headers, timeout=10)
            return response.status_code == 200
        except Exception:
            return False
    
    def add_to_cart(self, account, session_id):
        """Menambahkan produk ke keranjang (ATC) dengan method yang benar"""
        # Pertama, dapatkan informasi produk dari live
        live_info = self.get_live_info(session_id)
        if not live_info or not live_info.get('products'):
            return False
        
        # Pilih produk random dari yang tersedia
        products = live_info.get('products', [])
        if not products:
            return False
        
        product = random.choice(products)
        product_id = product.get('itemid')
        shop_id = product.get('shopid')
        
        if not product_id or not shop_id:
            return False
        
        url = "https://shopee.co.id/api/v4/cart/add_to_cart"
        
        headers = self.base_headers.copy()
        headers.update({
            'Cookie': '; '.join([f"{k}={v}" for k, v in account['cookies'].items()]),
            'Content-Type': 'application/json;charset=UTF-8',
            'Referer': f"https://shopee.co.id/product/{shop_id}/{product_id}",
            'X-CSRFToken': account.get('csrf', ''),
            'Client-Info': 'os=2;platform=9;scene_id=17;language=id;device_id=9c968575-05a6-4a5b-85df-d7ea4bbc31bf',
        })
        
        data = {
            'quantity': 1,
            'itemid': product_id,
            'shopid': shop_id,
            'add_on_deal_id': None,
            'donot_add_quantity': False
        }
        
        try:
            response = requests.post(url, headers=headers, json=data, timeout=10)
            if response.status_code == 200:
                try:
                    result = response.json()
                    return result.get('error') == 0
                except:
                    return True
            return False
        except Exception:
            return False
    
    def bot_like_worker(self, account_batch, session_id):
        """Worker untuk bot like"""
        for account in account_batch:
            if not self.running:
                break
            
            try:
                if self.send_like(account, session_id):
                    current_time = datetime.now().strftime("%H:%M:%S")
                    print(f"[{current_time}] LIKE = ✅ Berhasil! User: {account['user_id'][:8]}...")
                else:
                    current_time = datetime.now().strftime("%H:%M:%S")
                    print(f"[{current_time}] LIKE = ❌ Gagal! User: {account['user_id'][:8]}...")
                
                # Interval random antara request
                time.sleep(random.uniform(2, 8))
                
            except Exception as e:
                print(f"Error in like worker: {e}")
    
    def bot_viewer_worker(self, account_batch, session_id):
        """Worker untuk bot viewer"""
        for account in account_batch:
            if not self.running:
                break
            
            try:
                if self.join_live(account, session_id):
                    current_time = datetime.now().strftime("%H:%M:%S")
                    print(f"[{current_time}] VIEWER = ✅ Join Berhasil! User: {account['user_id'][:8]}...")
                else:
                    current_time = datetime.now().strftime("%H:%M:%S")
                    print(f"[{current_time}] VIEWER = ❌ Join Gagal! User: {account['user_id'][:8]}...")
                
                # Keep alive untuk viewer
                time.sleep(random.uniform(5, 15))
                
            except Exception as e:
                print(f"Error in viewer worker: {e}")
    
    def bot_atc_worker(self, account_batch, session_id):
        """Worker untuk bot ATC"""
        for account in account_batch:
            if not self.running:
                break
            
            try:
                if self.add_to_cart(account, session_id):
                    current_time = datetime.now().strftime("%H:%M:%S")
                    print(f"[{current_time}] ATC = ✅ Berhasil! User: {account['user_id'][:8]}...")
                else:
                    current_time = datetime.now().strftime("%H:%M:%S")
                    print(f"[{current_time}] ATC = ❌ Gagal! User: {account['user_id'][:8]}...")
                
                # Interval untuk ATC
                time.sleep(random.uniform(3, 10))
                
            except Exception as e:
                print(f"Error in ATC worker: {e}")
    
    def start_bot_like(self, session_id):
        """Memulai bot like"""
        print(f"\n🚀 Memulai Bot Like untuk session: {session_id}")
        print("=" * 50)
        
        self.running = True
        self.session_id = session_id
        
        # Bagi akun ke beberapa thread
        batch_size = max(1, len(self.accounts) // 5)  # 5 thread
        account_batches = [self.accounts[i:i + batch_size] for i in range(0, len(self.accounts), batch_size)]
        
        for batch in account_batches:
            thread = threading.Thread(target=self.bot_like_worker, args=(batch, session_id))
            thread.daemon = True
            thread.start()
            self.threads.append(thread)
            time.sleep(0.5)  # Delay antar thread
        
        try:
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Bot Like dihentikan oleh user")
            self.running = False
    
    def start_bot_viewer(self, session_id):
        """Memulai bot viewer"""
        print(f"\n🚀 Memulai Bot Viewer untuk session: {session_id}")
        print("=" * 50)
        
        self.running = True
        self.session_id = session_id
        
        # Bagi akun ke beberapa thread
        batch_size = max(1, len(self.accounts) // 3)  # 3 thread
        account_batches = [self.accounts[i:i + batch_size] for i in range(0, len(self.accounts), batch_size)]
        
        for batch in account_batches:
            thread = threading.Thread(target=self.bot_viewer_worker, args=(batch, session_id))
            thread.daemon = True
            thread.start()
            self.threads.append(thread)
            time.sleep(1)  # Delay antar thread
        
        try:
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Bot Viewer dihentikan oleh user")
            self.running = False
    
    def start_bot_atc(self, session_id):
        """Memulai bot ATC"""
        print(f"\n🚀 Memulai Bot ATC untuk session: {session_id}")
        print("=" * 50)
        
        self.running = True
        self.session_id = session_id
        
        # Bagi akun ke beberapa thread
        batch_size = max(1, len(self.accounts) // 4)  # 4 thread
        account_batches = [self.accounts[i:i + batch_size] for i in range(0, len(self.accounts), batch_size)]
        
        for batch in account_batches:
            thread = threading.Thread(target=self.bot_atc_worker, args=(batch, session_id))
            thread.daemon = True
            thread.start()
            self.threads.append(thread)
            time.sleep(1)  # Delay antar thread
        
        try:
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Bot ATC dihentikan oleh user")
            self.running = False
    
    def stop_bot(self):
        """Menghentikan bot"""
        self.running = False
        for thread in self.threads:
            thread.join(timeout=2)
        self.threads.clear()

    def refresh_account_session(self, account, session_id):
        """Refresh session cookies untuk account"""
        try:
            # Access live page dulu untuk refresh session
            live_url = f"https://live.shopee.co.id/share?from=live&session={session_id}"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'id,en-US;q=0.9,en;q=0.8',
                'Cookie': '; '.join([f"{k}={v}" for k, v in account['cookies'].items()]),
            }
            
            session = requests.Session()
            
            # Set existing cookies
            for name, value in account['cookies'].items():
                session.cookies.set(name, value, domain='.shopee.co.id')
            
            # Access live page
            response = session.get(live_url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                # Update account cookies dengan yang fresh
                fresh_cookies = {}
                for cookie in session.cookies:
                    fresh_cookies[cookie.name] = cookie.value
                
                # Merge dengan cookies lama, prioritaskan yang fresh
                account['cookies'].update(fresh_cookies)
                
                return True
            return False
            
        except Exception as e:
            print(f"Refresh session error: {e}")
            return False
    
def show_banner():
    """Menampilkan banner bot"""
    banner = """
    ╔═══════════════════════════════════════════════╗
    ║          SHOPEE LIVE STREAMING BOT            ║
    ║               BY FLASHCODE                    ║
    ╚═══════════════════════════════════════════════╝
    
    🎯 Bot Otomatis untuk Live Streaming Shopee
    ⚡ Fitur: Like, Viewer, Add to Cart (ATC)
    🔥 Multi-threading untuk performa maksimal
    """
    print(banner)

def show_menu():
    """Menampilkan menu utama"""
    menu = """
    ╔═══════════════════════════════════════════════╗
    ║                  MENU UTAMA                   ║
    ╠═══════════════════════════════════════════════╣
    ║  1. Bot Like (Ketik: 1)                       ║
    ║  2. Bot Viewer (Ketik: 2)                     ║
    ║  3. Bot ATC - Add to Cart (Ketik: 3)          ║
    ║  4. Keluar (Ketik: 4)                         ║
    ╚═══════════════════════════════════════════════╝
    """
    print(menu)

def main():
    """Fungsi utama"""
    show_banner()
    
    # Inisialisasi bot
    bot = ShopeeBot()
    
    # Load akun dari CSV
    if not bot.load_accounts():
        print("❌ Gagal memuat akun. Pastikan file input.csv tersedia dan berisi data yang valid.")
        return
    
    if len(bot.accounts) == 0:
        print("❌ Tidak ada akun valid yang ditemukan di input.csv")
        return
    
    try:
        while True:
            show_menu()
            choice = input("Pilih menu (1-4): ").strip()
            
            if choice == '4':
                print("👋 Terima kasih telah menggunakan Shopee Live Bot!")
                break
            
            if choice not in ['1', '2', '3']:
                print("❌ Pilihan tidak valid! Silakan pilih 1, 2, 3, atau 4.")
                continue
            
            # Input session ID
            user_input = input("\nMasukkan Session Live ID atau URL lengkap: ").strip()
            if not user_input:
                print("❌ Input tidak boleh kosong!")
                continue
            
            # Extract session ID dari input
            session_id = bot.extract_session_id(user_input)
            if not session_id:
                print("❌ Format tidak valid! Contoh yang benar:")
                print("   - Session ID: 146205526")
                print("   - URL pendek: https://live.shopee.co.id/146205526")
                print("   - URL share: https://live.shopee.co.id/share?session=146205526...")
                continue
            
            print(f"✅ Session ID diekstrak: {session_id}")
            
            # Validasi session ID
            print(f"🔍 Memvalidasi session ID: {session_id}")
            
            # Try accessing live page first (simple validation)
            try:
                page_url = f"https://live.shopee.co.id/share?from=live&session={session_id}"
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
                }
                page_response = requests.get(page_url, headers=headers, timeout=10)
                
                if page_response.status_code == 200:
                    # Try to get actual live info using the proper API
                    live_info = bot.get_live_info(session_id)
                    if live_info:
                        print(f"✅ Live stream ditemukan!")
                        print(f"   📺 Title: {live_info.get('title', 'Live Stream')}")
                        print(f"   👤 Streamer: {live_info.get('username', 'Streamer')}")
                        print(f"   💖 Likes: {live_info.get('like_count', 0)}")
                        print(f"   👀 Viewers: {live_info.get('viewer_count', 0)}")
                        print(f"   🛍️  Products: {len(live_info.get('products', []))}")
                    else:
                        live_info = {
                            'session_id': session_id,
                            'title': 'Live Stream',
                            'username': 'Streamer',
                            'status': 'accessible'
                        }
                else:
                    live_info = None
            except Exception as e:
                print(f"Validation error: {e}")
                live_info = None
            
            if not live_info:
                print("❌ Session ID tidak valid atau live stream tidak ditemukan!")
                print("💡 Tips:")
                print("   - Pastikan live stream masih aktif")
                print("   - Coba session ID dari live stream yang sedang berlangsung")
                print("   - Format URL: https://live.shopee.co.id/share?session=XXXXXX")
                continue
            
            # Konfirmasi untuk menjalankan bot
            confirm = input(f"\nMulai bot dengan {len(bot.accounts)} akun? (y/N): ").strip().lower()
            if confirm != 'y':
                print("❌ Bot dibatalkan oleh user")
                continue
            
            # Jalankan bot sesuai pilihan
            try:
                if choice == '1':
                    bot.start_bot_like(session_id)
                elif choice == '2':
                    bot.start_bot_viewer(session_id)
                elif choice == '3':
                    bot.start_bot_atc(session_id)
            except KeyboardInterrupt:
                print("\n🛑 Bot dihentikan oleh user")
            finally:
                bot.stop_bot()
                print("🔄 Kembali ke menu utama...\n")
    
    except KeyboardInterrupt:
        print("\n👋 Program dihentikan oleh user. Sampai jumpa!")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
