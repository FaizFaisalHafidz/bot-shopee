#!/usr/bin/env python3
"""
Cookie Refresher - Update fresh cookies dari response
"""

import requests
import time
import json

class CookieRefresher:
    def __init__(self):
        self.session = requests.Session()
        
    def refresh_session(self, session_id="146205526"):
        """Refresh cookies dengan mengakses live page dulu"""
        
        # Step 1: Access live page untuk mendapatkan fresh cookies
        live_url = f"https://live.shopee.co.id/share?session={session_id}"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'id,en-US;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        
        print(f"🔄 Step 1: Accessing live page...")
        response = self.session.get(live_url, headers=headers, timeout=10)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            print(f"   ✅ Got fresh cookies from live page")
            
            # Print cookies yang didapat
            for cookie in self.session.cookies:
                print(f"   🍪 {cookie.name}: {cookie.value[:20]}...")
        
        # Step 2: Test API dengan fresh cookies
        return self.test_api(session_id)
    
    def test_api(self, session_id):
        """Test API dengan fresh cookies"""
        
        api_url = f"https://live.shopee.co.id/api/v1/session/{session_id}/like"
        
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Accept-Language': 'id,en-US;q=0.9,en;q=0.8',
            'Content-Type': 'application/json;charset=UTF-8',
            'Origin': 'https://live.shopee.co.id',
            'Referer': f'https://live.shopee.co.id/share?session={session_id}',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
            'X-Livestreaming-Source': 'shopee',
        }
        
        payload = {"timestamp": int(time.time() * 1000)}
        
        print(f"\n🔥 Step 2: Testing API dengan fresh cookies...")
        
        try:
            response = self.session.post(api_url, headers=headers, json=payload, timeout=10)
            
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    print(f"   Response: {json.dumps(data, indent=2)}")
                    
                    if data.get('err_code') == 0:
                        print(f"   ✅ API SUCCESS! Like sent successfully")
                        return True
                    else:
                        print(f"   ❌ API Error: {data.get('err_msg')}")
                        return False
                except:
                    print(f"   ✅ Non-JSON response (possibly success)")
                    return True
            else:
                print(f"   ❌ HTTP Error: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"   ❌ Exception: {e}")
            return False

if __name__ == "__main__":
    refresher = CookieRefresher()
    success = refresher.refresh_session()
    
    if success:
        print(f"\n🎉 Cookie refresh dan API test BERHASIL!")
    else:
        print(f"\n❌ Cookie refresh GAGAL - perlu investigasi lebih lanjut")
