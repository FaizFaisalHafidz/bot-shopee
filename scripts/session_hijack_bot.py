#!/usr/bin/env python3
"""
STRATEGI 1: Browser Session Hijacking
- Connect ke Chrome yang sudah berjalan dengan --remote-debugging-port
- Hijack session yang sudah login
- Manipulasi device_id langsung di browser
"""

import sys
import os
import time
import json
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

def find_existing_chrome_sessions():
    """Cari Chrome yang sudah berjalan dengan debugging port"""
    sessions = []
    
    # Cek port debugging yang umum digunakan
    for port in range(9222, 9232):
        try:
            response = requests.get(f"http://localhost:{port}/json", timeout=2)
            if response.status_code == 200:
                tabs = response.json()
                sessions.append({
                    'port': port,
                    'tabs': tabs,
                    'count': len(tabs)
                })
        except:
            continue
    
    return sessions

def connect_to_existing_chrome(port):
    """Connect ke Chrome yang sudah berjalan"""
    try:
        options = Options()
        options.add_experimental_option("debuggerAddress", f"localhost:{port}")
        
        driver = webdriver.Chrome(options=options)
        
        # Manipulasi device_id langsung
        device_id = generate_device_id()
        driver.execute_script(f"""
            // Manipulasi device fingerprint
            Object.defineProperty(navigator, 'deviceMemory', {{get: () => 8}});
            Object.defineProperty(navigator, 'hardwareConcurrency', {{get: () => 8}});
            
            // Override WebGL fingerprint  
            const canvas = document.createElement('canvas');
            const gl = canvas.getContext('webgl');
            const debugInfo = gl.getExtension('WEBGL_debug_renderer_info');
            
            Object.defineProperty(debugInfo, 'UNMASKED_VENDOR_WEBGL', {{
                get: () => 'Custom Vendor {device_id[:8]}'
            }});
            
            Object.defineProperty(debugInfo, 'UNMASKED_RENDERER_WEBGL', {{
                get: () => 'Custom Renderer {device_id[8:16]}'
            }});
            
            // Set device ID di localStorage dan sessionStorage
            localStorage.setItem('device_id', '{device_id}');
            localStorage.setItem('browser_id', '{device_id[:16]}');
            sessionStorage.setItem('session_device_id', '{device_id}');
            
            // Inject ke window object
            window.deviceId = '{device_id}';
            window.browserId = '{device_id[:16]}';
            
            console.log('[HIJACK] Device fingerprint injected:', '{device_id[:8]}...{device_id[-4:]}');
        """)
        
        return driver
        
    except Exception as e:
        print(f"[ERROR] Failed to connect to Chrome port {port}: {e}")
        return None

def generate_device_id():
    """Generate device ID"""
    import random
    import string
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choice(chars) for _ in range(32))

def main():
    print("=" * 50)
    print("    SHOPEE BOT - SESSION HIJACKING")  
    print("=" * 50)
    
    # Step 1: Cari existing Chrome sessions
    print("[STEP 1] Mencari Chrome sessions yang sudah login...")
    sessions = find_existing_chrome_sessions()
    
    if not sessions:
        print("[ERROR] Tidak ada Chrome session aktif!")
        print("[INFO] Cara menggunakan:")
        print("1. Buka Chrome dengan: chrome.exe --remote-debugging-port=9222")
        print("2. Login ke akun Google di Chrome tersebut")
        print("3. Jalankan bot ini lagi")
        return
    
    print(f"[SUCCESS] Ditemukan {len(sessions)} Chrome sessions:")
    for i, session in enumerate(sessions):
        print(f"  {i+1}. Port {session['port']} - {session['count']} tabs")
    
    # Step 2: Connect ke session pertama
    target_port = sessions[0]['port']
    print(f"[STEP 2] Connecting ke Chrome port {target_port}...")
    
    driver = connect_to_existing_chrome(target_port)
    if not driver:
        print("[ERROR] Gagal connect ke Chrome session")
        return
    
    # Step 3: Navigate ke Shopee Live
    session_id = input("Masukkan Session ID Shopee: ").strip()
    shopee_url = f"https://live.shopee.co.id/share?from=live&session={session_id}&in=1"
    
    print(f"[STEP 3] Navigating ke Shopee Live...")
    driver.get(shopee_url)
    
    # Step 4: Inject viewer manipulation
    print(f"[STEP 4] Injecting viewer manipulation...")
    
    manipulation_script = """
    // Viewer count manipulation
    setInterval(() => {
        // Cari elemen viewer count
        const viewerElements = document.querySelectorAll('[class*="viewer"], [class*="count"], [data-testid*="viewer"]');
        
        viewerElements.forEach(el => {
            const text = el.textContent || el.innerText;
            if (text && text.match(/\\d+/)) {
                const currentCount = parseInt(text.match(/\\d+/)[0]);
                const newCount = currentCount + Math.floor(Math.random() * 5) + 1;
                
                el.textContent = text.replace(/\\d+/, newCount);
                el.innerText = text.replace(/\\d+/, newCount);
            }
        });
        
        // Network request manipulation untuk viewer count
        const originalFetch = window.fetch;
        window.fetch = function(...args) {
            return originalFetch.apply(this, args).then(response => {
                if (args[0] && args[0].includes('viewer') || args[0].includes('count')) {
                    console.log('[MANIPULATED] Viewer API call intercepted');
                }
                return response;
            });
        };
        
    }, 5000);
    
    console.log('[SUCCESS] Viewer manipulation active');
    """
    
    driver.execute_script(manipulation_script)
    
    print(f"[SUCCESS] Bot active! Viewer manipulation running...")
    print(f"[INFO] Chrome akan tetap terbuka dengan session yang di-hijack")
    print(f"[INFO] Tekan Ctrl+C untuk stop")
    
    try:
        while True:
            time.sleep(10)
            # Keep alive dan re-inject jika perlu
            driver.execute_script("console.log('[ALIVE] Bot still running...');")
    except KeyboardInterrupt:
        print(f"[STOP] Bot dihentikan")
        driver.quit()

if __name__ == "__main__":
    main()
