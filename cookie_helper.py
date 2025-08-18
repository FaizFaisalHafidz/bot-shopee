#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cookie Helper untuk Shopee Live Bot
Script bantuan untuk validasi dan parsing cookie
"""

import json
import re

def parse_browser_cookies(cookie_string):
    """Parse cookie dari format browser ke format bot"""
    print("🔍 Parsing cookies...")
    
    # Remove newlines and extra spaces
    cookie_string = ' '.join(cookie_string.split())
    
    # Split by semicolon
    cookies = {}
    for cookie in cookie_string.split(';'):
        if '=' in cookie:
            key, value = cookie.split('=', 1)
            cookies[key.strip()] = value.strip()
    
    return cookies

def validate_cookies(cookies):
    """Validasi cookie yang diperlukan"""
    required_cookies = ['SPC_U', 'csrftoken']
    optional_cookies = ['SPC_T_ID', 'SPC_ST', 'SPC_EC']
    
    print("✅ Cookie validation:")
    valid = True
    
    for cookie in required_cookies:
        if cookie in cookies:
            print(f"   ✅ {cookie}: {cookies[cookie][:20]}...")
        else:
            print(f"   ❌ {cookie}: MISSING (REQUIRED)")
            valid = False
    
    for cookie in optional_cookies:
        if cookie in cookies:
            print(f"   ⚪ {cookie}: {cookies[cookie][:20]}...")
        else:
            print(f"   ⚪ {cookie}: Not found (optional)")
    
    return valid

def format_for_csv(cookies):
    """Format cookie untuk input.csv"""
    return '; '.join([f"{k}={v}" for k, v in cookies.items()])

def main():
    print("🍪 Shopee Cookie Helper")
    print("=" * 50)
    print()
    print("Petunjuk:")
    print("1. Buka shopee.co.id di browser")
    print("2. Login ke akun Shopee")
    print("3. Tekan F12 > Application/Storage > Cookies > shopee.co.id")
    print("4. Copy ALL cookies dan paste di sini")
    print()
    
    while True:
        print("Paste cookies di bawah ini (atau ketik 'quit' untuk keluar):")
        print("=" * 50)
        
        # Read multiple lines until empty line
        lines = []
        while True:
            try:
                line = input()
                if not line.strip():
                    break
                lines.append(line)
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                return
        
        if not lines:
            continue
            
        cookie_string = ' '.join(lines)
        
        if cookie_string.lower().strip() == 'quit':
            print("👋 Goodbye!")
            break
        
        # Parse cookies
        cookies = parse_browser_cookies(cookie_string)
        
        if not cookies:
            print("❌ Tidak ada cookie yang valid ditemukan!")
            continue
        
        print(f"\n📊 Found {len(cookies)} cookies")
        
        # Validate
        if validate_cookies(cookies):
            print("\n✅ Cookie valid! Ready untuk bot")
            
            # Format untuk CSV
            csv_format = format_for_csv(cookies)
            print("\n📋 Format untuk input.csv:")
            print("-" * 50)
            print(csv_format)
            print("-" * 50)
            
            # Save to file option
            save = input("\nSimpan ke input.csv? (y/N): ").strip().lower()
            if save == 'y':
                try:
                    with open('input.csv', 'a', encoding='utf-8') as f:
                        f.write(csv_format + '\n')
                    print("✅ Cookie berhasil ditambahkan ke input.csv")
                except Exception as e:
                    print(f"❌ Error menyimpan: {e}")
        else:
            print("\n❌ Cookie tidak valid! Cookie yang diperlukan tidak lengkap")
        
        print("\n" + "="*50 + "\n")

if __name__ == "__main__":
    main()
