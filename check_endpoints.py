#!/usr/bin/env python3
import requests
import json

# Session ID yang valid dari user
session_id = "146205526"

# Ambil cookie dari input.csv untuk testing
with open('input.csv', 'r') as f:
    cookie_line = f.readline().strip()

# Parse cookies
cookies = {}
for item in cookie_line.split(';'):
    if '=' in item:
        key, value = item.strip().split('=', 1)
        cookies[key] = value

print(f"🔍 Testing endpoints untuk session: {session_id}")
print(f"🍪 Using cookies from first account")

# Headers standar
headers = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'id-ID,id;q=0.9,en;q=0.8',
    'Referer': f'https://live.shopee.co.id/{session_id}',
    'X-Requested-With': 'XMLHttpRequest',
}

# Test berbagai endpoint
endpoints = [
    f"https://live.shopee.co.id/api/v1/session/{session_id}",
    f"https://live.shopee.co.id/api/v1/sessions/{session_id}",
    f"https://live.shopee.co.id/api/v2/session/{session_id}",
    f"https://live.shopee.co.id/api/v1/live/{session_id}",
    f"https://live.shopee.co.id/api/v1/stream/{session_id}",
    f"https://shopee.co.id/api/v4/live/session/{session_id}",
    f"https://shopee.co.id/api/v1/live/session/{session_id}",
    f"https://live.shopee.co.id/{session_id}/info",
    f"https://live.shopee.co.id/{session_id}/data",
]

for endpoint in endpoints:
    try:
        print(f"\n📡 Testing: {endpoint}")
        response = requests.get(endpoint, headers=headers, cookies=cookies, timeout=10)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"   ✅ JSON Response: {json.dumps(data, indent=2)[:200]}...")
            except:
                print(f"   📄 HTML Response: {response.text[:100]}...")
        elif response.status_code == 404:
            print(f"   ❌ Not Found")
        elif response.status_code == 403:
            print(f"   🚫 Forbidden")
        else:
            print(f"   ⚠️ Other error: {response.text[:50]}")
            
    except Exception as e:
        print(f"   💥 Error: {str(e)}")

# Test action endpoints
print(f"\n🎯 Testing action endpoints:")

action_endpoints = [
    f"https://live.shopee.co.id/api/v1/session/{session_id}/like",
    f"https://live.shopee.co.id/api/v1/session/{session_id}/heart", 
    f"https://live.shopee.co.id/api/v1/like",
    f"https://shopee.co.id/api/v4/live/like",
    f"https://shopee.co.id/api/v1/live/like",
]

for endpoint in action_endpoints:
    try:
        print(f"\n🔥 Testing POST: {endpoint}")
        
        # Test dengan payload minimal
        payload = {
            'session_id': session_id,
            'type': 'like'
        }
        
        response = requests.post(endpoint, 
                               headers=headers, 
                               cookies=cookies, 
                               json=payload,
                               timeout=10)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"   ✅ Success: {data}")
            except:
                print(f"   ✅ Success: {response.text[:50]}")
        else:
            print(f"   Response: {response.text[:100]}")
            
    except Exception as e:
        print(f"   💥 Error: {str(e)}")
