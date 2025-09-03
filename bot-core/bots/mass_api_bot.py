#!/usr/bin/env python3
"""
MASS API BOT - Brute Force API Testing
Test semua kemungkinan API endpoint untuk join
"""

import time
import random
import json
import os
import requests
import csv
from datetime import datetime
import threading
from concurrent.futures import ThreadPoolExecutor

class MassAPIBot:
    def __init__(self):
        self.verified_cookies = []
        self.successful_joins = []
        
        # Setup logging
        log_dir = os.path.join('bot-core', 'logs')
        os.makedirs(log_dir, exist_ok=True)
        self.log_file = os.path.join(log_dir, f'mass_api_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')
        
        # Load verified cookies
        self.load_verified_cookies()
    
    def load_verified_cookies(self):
        """Load verified cookies from CSV file"""
        csv_path = os.path.join('bot-core', 'accounts', 'verified_cookies.csv')
        if not os.path.exists(csv_path):
            self.log("❌ verified_cookies.csv tidak ditemukan!")
            return
            
        try:
            with open(csv_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['status'] == 'active':
                        self.verified_cookies.append({
                            'account_id': row['account_id'],
                            'spc_f': row['spc_f'],
                            'spc_u': row['spc_u'], 
                            'spc_st': row['spc_st'],
                            'spc_ec': row['spc_ec'],
                            'device_id': row['device_id'],
                            'user_agent': row['user_agent']
                        })
            
            self.log(f"✅ Loaded {len(self.verified_cookies)} API cookies")
        except Exception as e:
            self.log(f"❌ Error loading cookies: {e}")
    
    def log(self, message):
        """Log message to console and file"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_msg = f"[{timestamp}] {message}"
        print(log_msg)
        
        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(log_msg + "\n")
        except:
            pass
    
    def test_api_endpoint(self, endpoint, method, session_id, cookie_data):
        """Test single API endpoint"""
        try:
            # Setup cookies
            cookies = {
                'SPC_F': cookie_data['spc_f'],
                'SPC_U': cookie_data['spc_u'],
                'SPC_ST': cookie_data['spc_st'],
                'SPC_EC': cookie_data['spc_ec']
            }
            
            # Setup headers
            headers = {
                'User-Agent': cookie_data['user_agent'],
                'Accept': 'application/json, text/plain, */*',
                'Accept-Language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
                'Content-Type': 'application/json',
                'Origin': 'https://live.shopee.co.id',
                'Referer': f'https://live.shopee.co.id/share?from=live&session={session_id}',
                'X-Requested-With': 'XMLHttpRequest'
            }
            
            # Payload for POST requests
            payload = {
                'session_id': session_id,
                'device_id': cookie_data['device_id']
            }
            
            # Make request
            if method == 'POST':
                response = requests.post(endpoint, headers=headers, cookies=cookies, json=payload, timeout=10)
            else:
                response = requests.get(endpoint, headers=headers, cookies=cookies, timeout=10)
            
            return {
                'endpoint': endpoint,
                'method': method,
                'status': response.status_code,
                'response': response.text[:200],
                'account': cookie_data['account_id'],
                'success': response.status_code == 200
            }
            
        except Exception as e:
            return {
                'endpoint': endpoint,
                'method': method,
                'status': 'ERROR',
                'response': str(e)[:100],
                'account': cookie_data['account_id'],
                'success': False
            }
    
    def mass_api_test(self, session_id):
        """Test multiple API endpoints secara mass"""
        self.log("🚀 === MASS API BRUTE FORCE TEST ===")
        
        # API endpoints to test
        endpoints = [
            # Live API endpoints
            f"https://live.shopee.co.id/api/v1/session/{session_id}/join",
            f"https://live.shopee.co.id/api/v1/session/{session_id}/joinv2", 
            f"https://live.shopee.co.id/api/v1/session/{session_id}/viewer/join",
            f"https://live.shopee.co.id/api/v2/session/{session_id}/join",
            f"https://live.shopee.co.id/api/v2/session/{session_id}/joinv2",
            
            # Shopee main API endpoints
            f"https://shopee.co.id/api/v1/live/session/{session_id}/join",
            f"https://shopee.co.id/api/v2/live/session/{session_id}/join",
            f"https://shopee.co.id/api/v3/live/session/{session_id}/join",
            f"https://shopee.co.id/api/v4/live/session/{session_id}/join",
            
            # Alternative endpoints
            f"https://live.shopee.co.id/session/{session_id}/join",
            f"https://live.shopee.co.id/viewer/session/{session_id}/join",
            f"https://live.shopee.co.id/live/session/{session_id}/join",
            
            # Mobile endpoints  
            f"https://mall.shopee.co.id/api/v1/live/session/{session_id}/join",
            f"https://m.shopee.co.id/api/v1/live/session/{session_id}/join",
            
            # GraphQL style
            f"https://shopee.co.id/api/graphql/live/join",
            
            # Alternative domains
            f"https://cf.shopee.co.id/api/v1/live/session/{session_id}/join",
            f"https://api.shopee.co.id/v1/live/session/{session_id}/join"
        ]
        
        methods = ['POST', 'GET']
        
        # Track results
        all_results = []
        successful_results = []
        
        total_tests = len(endpoints) * len(methods) * len(self.verified_cookies)
        self.log(f"🎯 Total tests to run: {total_tests}")
        
        # Test each combination
        test_count = 0
        for endpoint in endpoints:
            for method in methods:
                for cookie_data in self.verified_cookies:
                    test_count += 1
                    
                    self.log(f"[{test_count}/{total_tests}] Testing {method} {endpoint.split('/')[-1]} - {cookie_data['account_id']}")
                    
                    result = self.test_api_endpoint(endpoint, method, session_id, cookie_data)
                    all_results.append(result)
                    
                    if result['success']:
                        self.log(f"  ✅ SUCCESS: {result['status']} - {result['response'][:50]}...")
                        successful_results.append(result)
                    elif result['status'] in [301, 302]:
                        self.log(f"  🔄 REDIRECT: {result['status']}")
                    elif result['status'] == 'ERROR':
                        self.log(f"  💥 ERROR: {result['response']}")
                    else:
                        self.log(f"  ❌ FAILED: {result['status']}")
                    
                    # Small delay
                    time.sleep(random.uniform(0.5, 1.5))
        
        # Summary results
        self.log(f"\n" + "=" * 60)
        self.log("🚀 MASS API TEST RESULTS")
        self.log(f"Total tests: {len(all_results)}")
        self.log(f"Successful: {len(successful_results)}")
        self.log(f"Success rate: {len(successful_results)/len(all_results)*100:.1f}%")
        self.log("=" * 60)
        
        # Show successful endpoints
        if successful_results:
            self.log("\n✅ SUCCESSFUL ENDPOINTS:")
            for result in successful_results:
                self.log(f"  🎯 {result['method']} {result['endpoint']} - {result['account']}")
                self.log(f"     Response: {result['response'][:100]}...")
        
        # Group by status code
        status_counts = {}
        for result in all_results:
            status = result['status']
            if status in status_counts:
                status_counts[status] += 1
            else:
                status_counts[status] = 1
        
        self.log(f"\n📊 STATUS CODE DISTRIBUTION:")
        for status, count in sorted(status_counts.items()):
            self.log(f"  {status}: {count} times ({count/len(all_results)*100:.1f}%)")
        
        return successful_results
    
    def mass_parallel_test(self, session_id):
        """Mass test dengan parallel processing"""
        self.log("⚡ === MASS PARALLEL API TEST ===")
        
        endpoints = [
            f"https://live.shopee.co.id/api/v1/session/{session_id}/joinv2",
            f"https://live.shopee.co.id/api/v1/session/{session_id}/join", 
            f"https://shopee.co.id/api/v4/live/session/{session_id}/join",
            f"https://live.shopee.co.id/api/v2/session/{session_id}/joinv2"
        ]
        
        # Create test tasks
        tasks = []
        for endpoint in endpoints:
            for method in ['POST', 'GET']:
                for cookie_data in self.verified_cookies:
                    tasks.append((endpoint, method, session_id, cookie_data))
        
        self.log(f"⚡ Running {len(tasks)} parallel tests...")
        
        # Execute in parallel
        successful_results = []
        
        with ThreadPoolExecutor(max_workers=5) as executor:
            # Submit all tasks
            future_to_task = {
                executor.submit(self.test_api_endpoint, *task): task 
                for task in tasks
            }
            
            # Process results
            completed = 0
            for future in future_to_task:
                completed += 1
                try:
                    result = future.result(timeout=15)
                    endpoint, method = future_to_task[future][:2]
                    
                    if result['success']:
                        self.log(f"[{completed}/{len(tasks)}] ✅ {method} {endpoint.split('/')[-1]} - SUCCESS")
                        successful_results.append(result)
                    else:
                        self.log(f"[{completed}/{len(tasks)}] ❌ {method} {endpoint.split('/')[-1]} - {result['status']}")
                        
                except Exception as e:
                    self.log(f"[{completed}/{len(tasks)}] 💥 ERROR: {str(e)[:50]}...")
        
        self.log(f"\n⚡ PARALLEL TEST COMPLETE:")
        self.log(f"✅ Successful: {len(successful_results)}/{len(tasks)}")
        
        return successful_results
    
    def start_mass_api_bot(self, session_id):
        """Start mass API testing"""
        self.log("=" * 60)
        self.log("🚀 MASS API SHOPEE BOT")
        self.log("Brute Force API Testing")
        self.log("=" * 60)
        self.log(f"🎯 Session: {session_id}")
        self.log(f"🚀 Available cookies: {len(self.verified_cookies)}")
        self.log("=" * 60)
        
        if not self.verified_cookies:
            self.log("❌ No cookies available!")
            return
        
        # Test 1: Sequential mass test
        self.log("\n🚀 PHASE 1: SEQUENTIAL MASS TEST")
        sequential_results = self.mass_api_test(session_id)
        
        # Test 2: Parallel mass test
        self.log("\n⚡ PHASE 2: PARALLEL MASS TEST") 
        parallel_results = self.mass_parallel_test(session_id)
        
        # Combined results
        all_successful = sequential_results + parallel_results
        unique_successful = list({(r['endpoint'], r['method'], r['account']): r for r in all_successful}.values())
        
        # Final summary
        self.log(f"\n" + "=" * 60)
        self.log("🚀 MASS API FINAL RESULTS")
        self.log(f"Sequential successful: {len(sequential_results)}")
        self.log(f"Parallel successful: {len(parallel_results)}")
        self.log(f"Unique successful: {len(unique_successful)}")
        self.log("=" * 60)
        
        if unique_successful:
            self.log(f"\n🎯 WORKING API ENDPOINTS:")
            for result in unique_successful:
                endpoint_name = result['endpoint'].split('/')[-1] 
                self.log(f"  ✅ {result['method']} {endpoint_name} - {result['account']}")
            
            self.log(f"\n💚 Found {len(unique_successful)} working API combinations!")
        else:
            self.log(f"\n❌ No working API endpoints found. Anti-bot system blocking all requests.")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) >= 2:
        session_id = sys.argv[1]
        
        print("🚀" + "=" * 60)
        print("           MASS API BOT - Brute Force Mode")
        print("🚀" + "=" * 60)
        
        bot = MassAPIBot()
        bot.start_mass_api_bot(session_id)
    else:
        session_id = input("Session ID: ").strip()
        
        bot = MassAPIBot()
        bot.start_mass_api_bot(session_id)
