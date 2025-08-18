#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Live Stream Validator
Debug tool untuk mengecek API endpoint Shopee Live
"""

import requests
import json

def test_live_api(session_id):
    """Test berbagai endpoint API Shopee Live"""
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'id-ID,id;q=0.9,en;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Origin': 'https://live.shopee.co.id',
        'Referer': 'https://live.shopee.co.id/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site'
    }
    
    # Test berbagai endpoint
    endpoints = [
        f"https://live.shopee.co.id/api/v1/session/{session_id}",
        f"https://live.shopee.co.id/api/v2/session/{session_id}",
        f"https://shopee.co.id/api/live/v1/session/{session_id}",
        f"https://live.shopee.co.id/api/v1/live/{session_id}",
        f"https://live.shopee.co.id/api/session/{session_id}"
    ]
    
    print(f"🔍 Testing API endpoints for session: {session_id}")
    print("=" * 70)
    
    for i, url in enumerate(endpoints, 1):
        print(f"\n🌐 Test {i}: {url}")
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    print(f"   ✅ JSON Response received")
                    
                    # Check structure
                    if 'error' in data:
                        print(f"   Error field: {data['error']}")
                    if 'data' in data:
                        print(f"   ✅ Data field exists")
                        if isinstance(data['data'], dict):
                            keys = list(data['data'].keys())[:5]  # First 5 keys
                            print(f"   Data keys: {keys}")
                    
                    # Print small sample
                    sample = str(data)[:200] + "..." if len(str(data)) > 200 else str(data)
                    print(f"   Sample: {sample}")
                    
                except json.JSONDecodeError:
                    print(f"   ❌ Not valid JSON")
                    print(f"   Text: {response.text[:200]}...")
            else:
                print(f"   ❌ Error: {response.status_code}")
                print(f"   Response: {response.text[:200]}...")
                
        except requests.exceptions.Timeout:
            print(f"   ⏰ Timeout")
        except requests.exceptions.ConnectionError:
            print(f"   🔌 Connection Error")
        except Exception as e:
            print(f"   ❌ Exception: {e}")

def test_live_page(session_id):
    """Test akses ke halaman live stream"""
    print(f"\n🌐 Testing live page access...")
    
    urls = [
        f"https://live.shopee.co.id/{session_id}",
        f"https://live.shopee.co.id/share?session={session_id}"
    ]
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    for url in urls:
        print(f"\n📄 Testing: {url}")
        try:
            response = requests.get(url, headers=headers, timeout=10)
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                content = response.text
                if 'live' in content.lower() and 'shopee' in content.lower():
                    print(f"   ✅ Live page accessible")
                else:
                    print(f"   ⚠️ Unexpected content")
            else:
                print(f"   ❌ Page not accessible")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")

if __name__ == "__main__":
    session_id = "146205526"
    
    print("🧪 Shopee Live API Debugger")
    print("=" * 70)
    
    test_live_api(session_id)
    test_live_page(session_id)
    
    print(f"\n💡 Recommendations:")
    print(f"   - Cek apakah live stream dengan ID {session_id} masih aktif")
    print(f"   - Coba session ID dari live stream yang sedang berlangsung")
    print(f"   - API endpoint mungkin berubah atau memerlukan authentication")
