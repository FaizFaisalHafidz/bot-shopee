#!/usr/bin/env python3
"""
Test cookie parsing dan API login
"""

import requests
import json
import time

# Baca cookie pertama dari input.csv
with open('input.csv', 'r') as f:
    cookie_line = f.readline().strip()

print(f"Raw cookie string:")
print(f"{cookie_line[:100]}...")

# Parse cookies seperti di main.py (dengan semicolon)
cookies = {}
for cookie in cookie_line.split(';'):
    if '=' in cookie:
        key, value = cookie.strip().split('=', 1)
        cookies[key.strip()] = value.strip()

print(f"\nParsed cookies:")
important_keys = ['SPC_U', 'SPC_T_ID', 'SPC_ST', 'SPC_EC', 'csrftoken']
for key in important_keys:
    if key in cookies:
        print(f"✅ {key}: {cookies[key][:20]}...")
    else:
        print(f"❌ {key}: MISSING")

# Test dengan session ID yang valid
session_id = "146205526"

# Test API dengan cookies yang sudah diparsing
url = f"https://live.shopee.co.id/api/v1/session/{session_id}/like"

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'id,en-US;q=0.9,en;q=0.8',
    'Content-Type': 'application/json;charset=UTF-8',
    'Cookie': '; '.join([f"{k}={v}" for k, v in cookies.items()]),
    'Origin': 'https://live.shopee.co.id',
    'Referer': f'https://live.shopee.co.id/share?session={session_id}',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
    'X-Livestreaming-Source': 'shopee',
}

payload = {"timestamp": int(time.time() * 1000)}

print(f"\n🔥 Testing like API...")
print(f"URL: {url}")
print(f"Payload: {payload}")

try:
    response = requests.post(url, headers=headers, json=payload, timeout=10)
    
    print(f"\nResponse Status: {response.status_code}")
    print(f"Response Headers: {dict(response.headers)}")
    
    try:
        data = response.json()
        print(f"Response JSON: {json.dumps(data, indent=2)}")
    except:
        print(f"Response Text: {response.text}")
        
except Exception as e:
    print(f"❌ Request failed: {e}")

# Test session info API juga
print(f"\n📊 Testing session info API...")
info_url = f"https://live.shopee.co.id/api/v1/session/{session_id}"
try:
    info_response = requests.get(info_url, headers=headers, timeout=10)
    print(f"Session Info Status: {info_response.status_code}")
    
    if info_response.status_code == 200:
        try:
            info_data = info_response.json()
            print(f"Session Info: {json.dumps(info_data, indent=2)[:500]}...")
        except:
            print(f"Session Info Text: {info_response.text[:200]}...")
except Exception as e:
    print(f"❌ Session info failed: {e}")
