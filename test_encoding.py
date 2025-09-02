import os
import sys

# Fix Windows encoding
if os.name == 'nt':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.detach())

print("[TEST] Windows encoding fix applied")
print("INFO: Test dengan karakter biasa")
print("SUCCESS: Profile detection test")
print("ERROR: Test error message")  
print("WARNING: Test warning message")
print(f"PROFILE_COUNT=3")

# Test JSON creation
import json
test_data = {
    "test": "success",
    "profiles": [
        {"name": "Test Profile", "email": "test@example.com"}
    ]
}

with open('test_encoding.json', 'w', encoding='utf-8') as f:
    json.dump(test_data, f, ensure_ascii=False, indent=2)

print("[DEBUG] Test encoding file created successfully")
