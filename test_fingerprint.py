#!/usr/bin/env python3
"""
Quick Device Fingerprint Test
Tests if device fingerprint manipulation is working correctly
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import json
import random
import string
from datetime import datetime

def generate_device_id():
    """Generate unique device ID"""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=32))

def create_chrome_options(user_data_dir=None, profile_name="Default"):
    """Create Chrome options with fingerprint protection"""
    options = Options()
    
    if user_data_dir:
        options.add_argument(f"--user-data-dir={user_data_dir}")
        options.add_argument(f"--profile-directory={profile_name}")
    
    # Basic options
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    # Random user agent
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    ]
    options.add_argument(f"--user-agent={random.choice(user_agents)}")
    
    return options

def inject_fingerprint_script(driver, device_id):
    """Inject device fingerprint manipulation script"""
    
    script = f"""
    // Override localStorage to return our custom device_id
    const originalSetItem = localStorage.setItem;
    const originalGetItem = localStorage.getItem;
    
    localStorage.setItem = function(key, value) {{
        if (key === 'device_id' || key.includes('device')) {{
            console.log('Intercepted localStorage.setItem for device_id:', value);
            return originalSetItem.call(this, key, '{device_id}');
        }}
        return originalSetItem.call(this, key, value);
    }};
    
    localStorage.getItem = function(key) {{
        if (key === 'device_id' || key.includes('device')) {{
            console.log('Intercepted localStorage.getItem for device_id, returning:', '{device_id}');
            return '{device_id}';
        }}
        return originalGetItem.call(this, key);
    }};
    
    // Set device_id in localStorage immediately
    localStorage.setItem('device_id', '{device_id}');
    
    // Override navigator properties
    Object.defineProperty(navigator, 'deviceMemory', {{
        writable: false,
        value: {random.choice([2, 4, 8, 16])}
    }});
    
    Object.defineProperty(navigator, 'hardwareConcurrency', {{
        writable: false, 
        value: {random.choice([2, 4, 6, 8, 12, 16])}
    }});
    
    // Override screen properties
    Object.defineProperty(screen, 'width', {{
        writable: false,
        value: {random.choice([1920, 1366, 1440, 1536])}
    }});
    
    Object.defineProperty(screen, 'height', {{
        writable: false,
        value: {random.choice([1080, 768, 900, 864])}
    }});
    
    console.log('Device fingerprint injected:');
    console.log('- Device ID:', '{device_id}');
    console.log('- Device Memory:', navigator.deviceMemory);
    console.log('- CPU Cores:', navigator.hardwareConcurrency);
    console.log('- Screen:', screen.width + 'x' + screen.height);
    """
    
    driver.execute_cdp_cmd('Runtime.evaluate', {
        'expression': script
    })

def test_device_fingerprint():
    """Test device fingerprint on Shopee"""
    print("🧪 Testing Device Fingerprint Manipulation")
    print("=" * 50)
    
    device_id = generate_device_id()
    print(f"Generated Device ID: {device_id}")
    
    # Create Chrome driver
    options = create_chrome_options()
    service = Service(ChromeDriverManager().install())
    
    try:
        driver = webdriver.Chrome(service=service, options=options)
        
        # Navigate to Shopee first
        print("\n📱 Opening Shopee...")
        driver.get("https://shopee.co.id")
        
        # Inject fingerprint script
        print("🔧 Injecting device fingerprint...")
        inject_fingerprint_script(driver, device_id)
        
        # Wait a bit for script to take effect
        time.sleep(2)
        
        # Test script to check device_id
        test_script = """
        return {
            device_id_localStorage: localStorage.getItem('device_id'),
            device_memory: navigator.deviceMemory,
            cpu_cores: navigator.hardwareConcurrency,
            screen_width: screen.width,
            screen_height: screen.height,
            user_agent: navigator.userAgent
        };
        """
        
        result = driver.execute_script(test_script)
        
        print("\n📋 Device Fingerprint Test Results:")
        print("-" * 30)
        print(f"Device ID (localStorage): {result.get('device_id_localStorage', 'NOT SET')}")
        print(f"Device Memory: {result.get('device_memory', 'DEFAULT')} GB")
        print(f"CPU Cores: {result.get('cpu_cores', 'DEFAULT')}")
        print(f"Screen Resolution: {result.get('screen_width')}x{result.get('screen_height')}")
        print(f"User Agent: {result.get('user_agent', 'DEFAULT')[:80]}...")
        
        # Check if our device_id was set
        if result.get('device_id_localStorage') == device_id:
            print("\n✅ SUCCESS: Device ID manipulation working!")
        else:
            print("\n❌ FAILED: Device ID not set correctly")
        
        # Test on a sample Shopee live URL
        test_url = "https://live.shopee.co.id/share?from=live&session=157658364&in=1"
        print(f"\n🎥 Testing on Shopee Live: {test_url}")
        
        driver.get(test_url)
        time.sleep(5)
        
        # Check device_id again on live page
        live_result = driver.execute_script(test_script)
        print(f"\nDevice ID on Live Page: {live_result.get('device_id_localStorage', 'NOT SET')}")
        
        if live_result.get('device_id_localStorage') == device_id:
            print("✅ Device ID persisted on live page!")
        else:
            print("❌ Device ID lost on live page")
        
        print(f"\n⏱️ Keeping browser open for 10 seconds...")
        time.sleep(10)
        
    except Exception as e:
        print(f"\n❌ Error during test: {e}")
        
    finally:
        try:
            driver.quit()
        except:
            pass
        
        print("\n🏁 Test completed!")

def test_multiple_instances():
    """Test multiple browser instances with different device IDs"""
    print("\n🔄 Testing Multiple Browser Instances")
    print("=" * 50)
    
    drivers = []
    device_ids = []
    
    try:
        # Create 3 browser instances
        for i in range(3):
            device_id = generate_device_id()
            device_ids.append(device_id)
            
            print(f"\n🌐 Creating browser instance {i+1}...")
            print(f"   Device ID: {device_id}")
            
            options = create_chrome_options()
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=options)
            drivers.append(driver)
            
            # Navigate and inject fingerprint
            driver.get("https://shopee.co.id")
            inject_fingerprint_script(driver, device_id)
            time.sleep(1)
            
            # Verify device_id
            result = driver.execute_script("return localStorage.getItem('device_id');")
            if result == device_id:
                print(f"   ✅ Device ID set correctly")
            else:
                print(f"   ❌ Device ID failed: {result}")
        
        print(f"\n📊 Summary of {len(drivers)} instances:")
        for i, device_id in enumerate(device_ids):
            print(f"   Instance {i+1}: {device_id}")
        
        # Check for unique device IDs
        if len(set(device_ids)) == len(device_ids):
            print("\n✅ All device IDs are unique!")
        else:
            print("\n❌ Some device IDs are duplicated!")
        
        print(f"\n⏱️ Keeping all browsers open for 5 seconds...")
        time.sleep(5)
        
    except Exception as e:
        print(f"\n❌ Error during multi-instance test: {e}")
        
    finally:
        # Clean up all drivers
        for i, driver in enumerate(drivers):
            try:
                print(f"   Closing instance {i+1}...")
                driver.quit()
            except:
                pass
        
        print("\n🏁 Multi-instance test completed!")

def main():
    """Main test function"""
    print("🧪 DEVICE FINGERPRINT TEST SUITE")
    print("=" * 60)
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    try:
        # Test 1: Single instance
        test_device_fingerprint()
        
        # Test 2: Multiple instances
        test_multiple_instances()
        
        print("\n" + "=" * 60)
        print("✅ ALL TESTS COMPLETED")
        print("=" * 60)
        
    except KeyboardInterrupt:
        print("\n⚠️ Tests interrupted by user")
    except Exception as e:
        print(f"\n❌ Test suite failed: {e}")

if __name__ == "__main__":
    main()
