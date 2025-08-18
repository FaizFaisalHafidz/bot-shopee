#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session ID Extractor Test
Test untuk memastikan ekstraksi session ID dari berbagai format URL
"""

import re

def extract_session_id(input_text):
    """Extract session ID dari berbagai format URL Shopee"""
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

def test_extraction():
    """Test berbagai format URL"""
    test_cases = [
        # Format yang Anda berikan
        "https://live.shopee.co.id/share?from=live&session=146205526&share_user_id=266236471&stm_medium=referral&stm_source=rw&uls_trackid=536b2vtg003c&viewer=0&in=1#copy_link",
        
        # Format lainnya
        "https://live.shopee.co.id/71875688",
        "146205526",
        "session=146205526",
        "https://live.shopee.co.id/share?session=123456789&other=params",
        
        # Format yang salah
        "https://live.shopee.co.id/",
        "invalid_url",
        ""
    ]
    
    print("🧪 Testing Session ID Extraction")
    print("=" * 80)
    
    for i, test_url in enumerate(test_cases, 1):
        session_id = extract_session_id(test_url)
        
        if session_id:
            print(f"✅ Test {i}: {session_id}")
            print(f"   Input: {test_url[:60]}{'...' if len(test_url) > 60 else ''}")
        else:
            print(f"❌ Test {i}: FAILED")
            print(f"   Input: {test_url[:60]}{'...' if len(test_url) > 60 else ''}")
        print()

if __name__ == "__main__":
    test_extraction()
    
    print("\n🎯 Test URL Anda:")
    your_url = "https://live.shopee.co.id/share?from=live&session=146205526&share_user_id=266236471&stm_medium=referral&stm_source=rw&uls_trackid=536b2vtg003c&viewer=0&in=1#copy_link"
    
    session_id = extract_session_id(your_url)
    if session_id:
        print(f"✅ Session ID berhasil diekstrak: {session_id}")
        print("🚀 Sekarang Anda bisa menggunakan bot dengan session ID ini!")
    else:
        print("❌ Gagal mengekstrak session ID")
