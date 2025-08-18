#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Shopee Live Streaming Bot - Advanced Version
Bot untuk menambahkan likes, viewers, dan ATC pada live streaming Shopee
Dengan dukungan konfigurasi dan logging yang lebih baik
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
import logging

class ShopeeAdvancedBot:
    def __init__(self, config_file='config.json'):
        self.accounts = []
        self.session_id = None
        self.running = False
        self.threads = []
        self.config = self.load_config(config_file)
        self.setup_logging()
        
        # Stats tracking
        self.stats = {
            'likes_sent': 0,
            'viewers_added': 0,
            'atc_success': 0,
            'errors': 0
        }
        
    def load_config(self, config_file):
        """Memuat konfigurasi dari file JSON"""
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"⚠️ Config file {config_file} tidak ditemukan, menggunakan default config")
            return self.get_default_config()
        except Exception as e:
            print(f"❌ Error loading config: {e}")
            return self.get_default_config()
    
    def get_default_config(self):
        """Konfigurasi default jika file config tidak ada"""
        return {
            "bot_settings": {
                "like_interval": {"min": 2, "max": 8},
                "viewer_interval": {"min": 5, "max": 15},
                "atc_interval": {"min": 3, "max": 10},
                "thread_delay": 0.5,
                "request_timeout": 10
            },
            "thread_config": {
                "like_threads": 5,
                "viewer_threads": 3,
                "atc_threads": 4
            },
            "headers": {
                "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            }
        }
    
    def setup_logging(self):
        """Setup logging system"""
        log_format = '%(asctime)s - %(levelname)s - %(message)s'
        logging.basicConfig(
            level=logging.INFO,
            format=log_format,
            handlers=[
                logging.FileHandler('shopee_bot.log', encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def get_base_headers(self):
        """Mendapatkan headers dasar untuk request"""
        return {
            'User-Agent': self.config['headers']['user_agent'],
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
                        status = "🔥" if account['has_important_cookies'] else "⚡"
                        self.logger.info(f"{status} Akun {line_num}: User ID {account['user_id'][:8]}... loaded")
                    else:
                        self.logger.warning(f"⚠️ Akun {line_num}: Cookie tidak valid, dilewati")
            
            self.logger.info(f"Berhasil memuat {len(self.accounts)} akun valid dari input.csv")
            return len(self.accounts) > 0
        except FileNotFoundError:
            self.logger.error("File input.csv tidak ditemukan!")
            return False
        except Exception as e:
            self.logger.error(f"Error membaca file: {e}")
            return False
    
    def parse_cookies(self, cookie_string):
        """Parse cookie string menjadi dict"""
        try:
            cookies = {}
            # Membersihkan string cookie dari karakter yang tidak perlu
            cookie_string = cookie_string.strip()
            
            # Split berdasarkan "; " untuk memisahkan setiap cookie
            for cookie in cookie_string.split('; '):
                if '=' in cookie:
                    key, value = cookie.split('=', 1)
                    cookies[key.strip()] = value.strip()
            
            # Validasi cookie yang diperlukan untuk Shopee
            required_cookies = ['SPC_U', 'csrftoken']
            important_cookies = ['SPC_T_ID', 'SPC_ST', 'SPC_EC']
            
            # Check apakah cookie yang diperlukan ada
            missing_required = [cookie for cookie in required_cookies if cookie not in cookies]
            if missing_required:
                self.logger.warning(f"Cookie tidak lengkap! Missing: {', '.join(missing_required)}")
                return None
            
            # Validasi format SPC_U (harus berupa angka)
            if not cookies['SPC_U'].isdigit():
                self.logger.warning(f"SPC_U tidak valid: {cookies['SPC_U']}")
                return None
            
            return {
                'cookies': cookies,
                'user_id': cookies.get('SPC_U', ''),
                'csrf': cookies.get('csrftoken', ''),
                'session_cookies': '; '.join([f"{k}={v}" for k, v in cookies.items()]),
                'token': cookies.get('SPC_T_ID', ''),
                'session_token': cookies.get('SPC_ST', ''),
                'ec_token': cookies.get('SPC_EC', ''),
                'has_important_cookies': all(cookie in cookies for cookie in important_cookies)
            }
            
        except Exception as e:
            self.logger.error(f"Error parsing cookies: {e}")
            return None
    
    def make_request(self, method, url, account=None, data=None, **kwargs):
        """Wrapper untuk membuat HTTP request dengan error handling"""
        headers = self.get_base_headers()
        
        if account:
            headers['Cookie'] = account['session_cookies']
            headers['X-CSRFToken'] = account['csrf']
        
        try:
            timeout = self.config['bot_settings']['request_timeout']
            if method.upper() == 'GET':
                response = requests.get(url, headers=headers, timeout=timeout, **kwargs)
            elif method.upper() == 'POST':
                response = requests.post(url, headers=headers, json=data, timeout=timeout, **kwargs)
            
            return response
        except requests.exceptions.Timeout:
            self.logger.warning("Request timeout")
            return None
        except requests.exceptions.ConnectionError:
            self.logger.warning("Connection error")
            return None
        except Exception as e:
            self.logger.error(f"Request error: {e}")
            return None
    
    def extract_session_id(self, input_text):
        """Extract session ID dari berbagai format URL Shopee"""
        import re
        
        # Remove whitespace
        input_text = input_text.strip()
        
        # Jika sudah berupa angka saja
        if input_text.isdigit():
            return input_text
        
        # Format 1: https://live.shopee.co.id/12345678
        pattern1 = r'https://live\.shopee\.co\.id/(\d+)'
        match1 = re.search(pattern1, input_text)
        if match1:
            return match1.group(1)
        
        # Format 2: https://live.shopee.co.id/share?...&session=12345678&...
        pattern2 = r'[?&]session=(\d+)'
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
        """Mendapatkan informasi live streaming dengan authentication"""
        # Try multiple endpoints
        endpoints = [
            f"https://live.shopee.co.id/api/v1/session/{session_id}",
            f"https://shopee.co.id/api/v4/live/session/{session_id}",
            f"https://live.shopee.co.id/api/session/{session_id}/info"
        ]
        
        for endpoint in endpoints:
            response = self.make_request('GET', endpoint)
            if response and response.status_code == 200:
                try:
                    data = response.json()
                    if data.get('error') == 0 or 'data' in data:
                        return data.get('data', data)
                except json.JSONDecodeError:
                    continue
                    
        # Fallback: check if live page is accessible
        page_url = f"https://live.shopee.co.id/{session_id}"
        page_response = self.make_request('GET', page_url)
        if page_response and page_response.status_code == 200:
            # Live page accessible, return minimal info
            return {
                'session_id': session_id,
                'status': 'accessible',
                'title': 'Live Stream',
                'username': 'Unknown Streamer',
                'products': []  # Will be populated when needed
            }
        
        return None
    
    def send_like(self, account, session_id):
        """Mengirim like ke live streaming"""
        url = "https://live.shopee.co.id/api/v1/like"
        data = {
            'session_id': session_id,
            'count': 1
        }
        
        response = self.make_request('POST', url, account, data)
        if response and response.status_code == 200:
            try:
                result = response.json()
                return result.get('error', 1) == 0
            except json.JSONDecodeError:
                pass
        return False
    
    def join_live(self, account, session_id):
        """Join live streaming sebagai viewer"""
        url = "https://live.shopee.co.id/api/v1/join"
        data = {
            'session_id': session_id,
            'source': 'live_page'
        }
        
        response = self.make_request('POST', url, account, data)
        if response and response.status_code == 200:
            try:
                result = response.json()
                return result.get('error', 1) == 0
            except json.JSONDecodeError:
                pass
        return False
    
    def add_to_cart(self, account, session_id):
        """Menambahkan produk ke keranjang (ATC)"""
        # Pertama, dapatkan informasi produk dari live
        live_info = self.get_live_info(session_id)
        if not live_info or not live_info.get('products'):
            return False
        
        products = live_info.get('products', [])
        if not products:
            return False
        
        product = random.choice(products)
        product_id = product.get('itemid')
        shop_id = product.get('shopid')
        
        if not product_id or not shop_id:
            return False
        
        url = "https://shopee.co.id/api/v4/cart/add_to_cart"
        data = {
            'quantity': 1,
            'itemid': product_id,
            'shopid': shop_id,
            'add_on_deal_id': None,
            'donot_add_quantity': False
        }
        
        response = self.make_request('POST', url, account, data)
        if response and response.status_code == 200:
            try:
                result = response.json()
                return result.get('error', 1) == 0
            except json.JSONDecodeError:
                pass
        return False
    
    def bot_worker(self, bot_type, account_batch, session_id):
        """Worker umum untuk semua jenis bot"""
        interval_config = self.config['bot_settings'][f'{bot_type}_interval']
        
        for account in account_batch:
            if not self.running:
                break
            
            try:
                success = False
                current_time = datetime.now().strftime("%H:%M:%S")
                user_display = account['user_id'][:8] + "..."
                
                if bot_type == 'like':
                    success = self.send_like(account, session_id)
                    if success:
                        self.stats['likes_sent'] += 1
                elif bot_type == 'viewer':
                    success = self.join_live(account, session_id)
                    if success:
                        self.stats['viewers_added'] += 1
                elif bot_type == 'atc':
                    success = self.add_to_cart(account, session_id)
                    if success:
                        self.stats['atc_success'] += 1
                
                status = "✅ Berhasil" if success else "❌ Gagal"
                if not success:
                    self.stats['errors'] += 1
                
                print(f"[{current_time}] {bot_type.upper()} = {status}! User: {user_display}")
                
                # Interval random
                interval = random.uniform(interval_config['min'], interval_config['max'])
                time.sleep(interval)
                
            except Exception as e:
                self.logger.error(f"Error in {bot_type} worker: {e}")
                self.stats['errors'] += 1
    
    def start_bot(self, bot_type, session_id):
        """Memulai bot dengan tipe tertentu"""
        print(f"\n🚀 Memulai Bot {bot_type.upper()} untuk session: {session_id}")
        print("=" * 60)
        
        self.running = True
        self.session_id = session_id
        
        # Reset stats
        self.stats = {key: 0 for key in self.stats}
        
        # Konfigurasi thread
        thread_count = self.config['thread_config'][f'{bot_type}_threads']
        batch_size = max(1, len(self.accounts) // thread_count)
        account_batches = [self.accounts[i:i + batch_size] for i in range(0, len(self.accounts), batch_size)]
        
        # Start monitoring thread
        monitor_thread = threading.Thread(target=self.monitor_stats)
        monitor_thread.daemon = True
        monitor_thread.start()
        
        # Start worker threads
        for batch in account_batches:
            thread = threading.Thread(target=self.bot_worker, args=(bot_type, batch, session_id))
            thread.daemon = True
            thread.start()
            self.threads.append(thread)
            time.sleep(self.config['bot_settings']['thread_delay'])
        
        try:
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            print(f"\n🛑 Bot {bot_type.upper()} dihentikan oleh user")
        finally:
            self.stop_bot()
    
    def monitor_stats(self):
        """Monitor dan tampilkan statistik secara real-time"""
        start_time = time.time()
        
        while self.running:
            time.sleep(30)  # Update setiap 30 detik
            if not self.running:
                break
            
            runtime = int(time.time() - start_time)
            hours = runtime // 3600
            minutes = (runtime % 3600) // 60
            seconds = runtime % 60
            
            print(f"\n📊 STATISTIK BOT (Runtime: {hours:02d}:{minutes:02d}:{seconds:02d})")
            print(f"   Likes: {self.stats['likes_sent']} | Viewers: {self.stats['viewers_added']} | ATC: {self.stats['atc_success']} | Errors: {self.stats['errors']}")
            print("-" * 60)
    
    def stop_bot(self):
        """Menghentikan bot"""
        self.running = False
        for thread in self.threads:
            thread.join(timeout=2)
        self.threads.clear()
        
        # Tampilkan statistik final
        print(f"\n📊 STATISTIK FINAL:")
        print(f"   ✅ Likes berhasil: {self.stats['likes_sent']}")
        print(f"   👥 Viewers ditambah: {self.stats['viewers_added']}")
        print(f"   🛒 ATC berhasil: {self.stats['atc_success']}")
        print(f"   ❌ Error: {self.stats['errors']}")

def show_advanced_banner():
    """Menampilkan banner bot advanced"""
    banner = """
    ╔═════════════════════════════════════════════════════════╗
    ║              SHOPEE LIVE STREAMING BOT                  ║
    ║                   ADVANCED VERSION                      ║
    ║                   BY FLASHCODE                          ║
    ╠═════════════════════════════════════════════════════════╣
    ║  🎯 Multi-threaded Performance                          ║
    ║  📊 Real-time Statistics                                ║
    ║  ⚙️  Configurable Settings                               ║
    ║  📝 Advanced Logging                                    ║
    ║  🔥 Production Ready                                    ║
    ╚═════════════════════════════════════════════════════════╝
    """
    print(banner)

def show_advanced_menu():
    """Menampilkan menu advanced"""
    menu = """
    ╔═════════════════════════════════════════════════════════╗
    ║                     MENU UTAMA                          ║
    ╠═════════════════════════════════════════════════════════╣
    ║  1. 👍 Bot Like (Auto Like + Real-time Stats)           ║
    ║  2. 👥 Bot Viewer (Auto Join + Keep Alive)              ║
    ║  3. 🛒 Bot ATC - Add to Cart (Smart Product Selection)  ║
    ║  4. 📊 Lihat Statistik                                  ║
    ║  5. ⚙️  Konfigurasi Bot                                  ║
    ║  6. 🚪 Keluar                                           ║
    ╚═════════════════════════════════════════════════════════╝
    """
    print(menu)

def main():
    """Fungsi utama untuk bot advanced"""
    show_advanced_banner()
    
    # Inisialisasi bot
    bot = ShopeeAdvancedBot()
    
    # Load akun dari CSV
    if not bot.load_accounts():
        print("❌ Gagal memuat akun. Pastikan file input.csv tersedia dan berisi data yang valid.")
        return
    
    if len(bot.accounts) == 0:
        print("❌ Tidak ada akun valid yang ditemukan di input.csv")
        return
    
    print(f"✅ Loaded {len(bot.accounts)} valid accounts")
    
    try:
        while True:
            show_advanced_menu()
            choice = input("Pilih menu (1-6): ").strip()
            
            if choice == '6':
                print("👋 Terima kasih telah menggunakan Shopee Live Bot Advanced!")
                break
            
            if choice == '4':
                print(f"\n📊 STATISTIK SESI TERAKHIR:")
                print(f"   ✅ Likes berhasil: {bot.stats['likes_sent']}")
                print(f"   👥 Viewers ditambah: {bot.stats['viewers_added']}")
                print(f"   🛒 ATC berhasil: {bot.stats['atc_success']}")
                print(f"   ❌ Error: {bot.stats['errors']}")
                print(f"   📱 Total akun: {len(bot.accounts)}")
                input("\nTekan Enter untuk kembali ke menu...")
                continue
            
            if choice == '5':
                print(f"\n⚙️ KONFIGURASI SAAT INI:")
                config = bot.config['bot_settings']
                print(f"   Like interval: {config['like_interval']['min']}-{config['like_interval']['max']} detik")
                print(f"   Viewer interval: {config['viewer_interval']['min']}-{config['viewer_interval']['max']} detik")
                print(f"   ATC interval: {config['atc_interval']['min']}-{config['atc_interval']['max']} detik")
                thread_config = bot.config['thread_config']
                print(f"   Like threads: {thread_config['like_threads']}")
                print(f"   Viewer threads: {thread_config['viewer_threads']}")
                print(f"   ATC threads: {thread_config['atc_threads']}")
                print(f"\n💡 Edit file config.json untuk mengubah pengaturan")
                input("\nTekan Enter untuk kembali ke menu...")
                continue
            
            if choice not in ['1', '2', '3']:
                print("❌ Pilihan tidak valid! Silakan pilih 1-6.")
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
            
            # Try with authentication first
            live_info = None
            if bot.accounts:
                account = bot.accounts[0]
                url = f"https://live.shopee.co.id/api/v1/session/{session_id}"
                response = bot.make_request('GET', url, account)
                
                if response and response.status_code == 200:
                    try:
                        data = response.json()
                        if data.get('error') == 0:
                            live_info = data.get('data', {})
                        elif data.get('error') == 90309999:
                            # Permission error but session exists
                            live_info = {
                                'session_id': session_id,
                                'title': 'Live Stream (Auth Required)',
                                'username': 'Streamer',
                                'status': 'accessible'
                            }
                    except json.JSONDecodeError:
                        pass
            
            # Fallback to page check
            if not live_info:
                page_url = f"https://live.shopee.co.id/{session_id}"
                page_response = bot.make_request('GET', page_url)
                if page_response and page_response.status_code == 200:
                    live_info = {
                        'session_id': session_id,
                        'title': 'Live Stream',
                        'username': 'Streamer',
                        'status': 'page_accessible'
                    }
            
            if not live_info:
                print("❌ Session ID tidak valid atau live stream tidak ditemukan!")
                print("💡 Tips:")
                print("   - Pastikan live stream masih aktif")
                print("   - Coba session ID dari live stream yang sedang berlangsung")
                print("   - Format URL: https://live.shopee.co.id/share?session=XXXXXX")
                continue
            
            print(f"✅ Live stream ditemukan!")
            print(f"   📺 Title: {live_info.get('title', 'No Title')}")
            print(f"   👤 Streamer: {live_info.get('username', 'Unknown')}")
            print(f"   🛍️  Products: {len(live_info.get('products', []))}")
            
            # Konfirmasi sebelum mulai
            confirm = input(f"\nMulai bot dengan {len(bot.accounts)} akun? (y/N): ").strip().lower()
            if confirm != 'y':
                print("❌ Bot dibatalkan")
                continue
            
            # Jalankan bot sesuai pilihan
            try:
                if choice == '1':
                    bot.start_bot('like', session_id)
                elif choice == '2':
                    bot.start_bot('viewer', session_id)
                elif choice == '3':
                    bot.start_bot('atc', session_id)
            except KeyboardInterrupt:
                print("\n🛑 Bot dihentikan oleh user")
            finally:
                print("🔄 Kembali ke menu utama...\n")
    
    except KeyboardInterrupt:
        print("\n👋 Program dihentikan oleh user. Sampai jumpa!")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
