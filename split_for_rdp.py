#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script untuk membagi input.csv menjadi 3 file untuk Multi-RDP Strategy
RDP1: 9 accounts, RDP2: 9 accounts, RDP3: 9 accounts
"""

def split_input_csv():
    """Split input.csv menjadi 3 file untuk 3 RDP servers"""
    try:
        print("🔄 Reading input.csv...")
        
        # Read input.csv
        with open('input.csv', 'r', encoding='utf-8') as f:
            content = f.read().strip()
            lines = [line.strip() for line in content.split('\n') if line.strip() and not line.startswith('#')]
        
        if len(lines) < 27:
            print(f"⚠️ Warning: Only {len(lines)} accounts found, need 27 for optimal multi-RDP")
            print("📋 Will distribute available accounts across 3 RDPs")
        
        # Calculate distribution
        total_accounts = len(lines)
        accounts_per_rdp = total_accounts // 3
        remainder = total_accounts % 3
        
        print(f"📊 Distribution plan:")
        print(f"   Total accounts: {total_accounts}")
        print(f"   Accounts per RDP: {accounts_per_rdp}")
        print(f"   Extra accounts: {remainder}")
        
        # Split accounts
        rdp_splits = []
        start_idx = 0
        
        for rdp_num in range(3):
            # Add extra account to first RDPs if there's remainder
            current_count = accounts_per_rdp + (1 if rdp_num < remainder else 0)
            end_idx = start_idx + current_count
            
            rdp_accounts = lines[start_idx:end_idx]
            rdp_splits.append(rdp_accounts)
            
            print(f"   RDP {rdp_num + 1}: {len(rdp_accounts)} accounts (accounts {start_idx + 1}-{end_idx})")
            
            start_idx = end_idx
        
        # Create individual files
        for rdp_num, accounts in enumerate(rdp_splits, 1):
            filename = f"input_rdp{rdp_num}.csv"
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("# Shopee Bot Input File - RDP " + str(rdp_num) + "\n")
                f.write("# Format: Cookie string dengan SPC_U, csrftoken, SPC_T_ID, dll\n")
                f.write("# Total accounts: " + str(len(accounts)) + "\n")
                f.write("\n")
                
                for account in accounts:
                    f.write(account + "\n")
            
            print(f"✅ Created {filename} with {len(accounts)} accounts")
        
        # Create master distribution info
        with open('rdp_distribution.txt', 'w', encoding='utf-8') as f:
            f.write("SHOPEE BOT - MULTI-RDP DISTRIBUTION\n")
            f.write("=" * 40 + "\n\n")
            f.write(f"Total Accounts: {total_accounts}\n")
            f.write(f"Generated: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            for rdp_num, accounts in enumerate(rdp_splits, 1):
                f.write(f"RDP {rdp_num}:\n")
                f.write(f"  File: input_rdp{rdp_num}.csv\n")
                f.write(f"  Accounts: {len(accounts)}\n")
                f.write(f"  Command: python rdp_optimized_bot.py\n")
                f.write(f"  Expected Viewers: +{int(len(accounts) * 0.85)}\n\n")
            
            f.write("DEPLOYMENT COMMANDS:\n")
            f.write("-" * 20 + "\n")
            for rdp_num in range(1, 4):
                f.write(f"RDP {rdp_num}:\n")
                f.write(f"  1. Copy input_rdp{rdp_num}.csv to RDP {rdp_num}\n")
                f.write(f"  2. Rename to input.csv on RDP {rdp_num}\n") 
                f.write(f"  3. Run: python rdp_optimized_bot.py\n\n")
        
        print(f"\n✅ Successfully created distribution files:")
        print(f"   📄 input_rdp1.csv ({len(rdp_splits[0])} accounts)")
        print(f"   📄 input_rdp2.csv ({len(rdp_splits[1])} accounts)")  
        print(f"   📄 input_rdp3.csv ({len(rdp_splits[2])} accounts)")
        print(f"   📋 rdp_distribution.txt (deployment guide)")
        
        print(f"\n🚀 DEPLOYMENT READY!")
        print(f"📈 Expected total viewers: +{int(total_accounts * 0.85)} (85% success rate)")
        
        return True
        
    except FileNotFoundError:
        print("❌ input.csv not found!")
        print("💡 Make sure input.csv exists with your account cookies")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    print("""
    ╔═══════════════════════════════════════════════╗
    ║        MULTI-RDP INPUT SPLITTER               ║
    ║           SHOPEE BOT DISTRIBUTION             ║
    ╚═══════════════════════════════════════════════╝
    """)
    
    print("🎯 This tool splits your input.csv into 3 files for Multi-RDP strategy")
    print("📋 Each RDP will get equal distribution of accounts")
    print()
    
    # Check if input.csv exists
    try:
        with open('input.csv', 'r') as f:
            lines = len([line for line in f if line.strip() and not line.startswith('#')])
            print(f"📊 Found {lines} accounts in input.csv")
    except FileNotFoundError:
        print("❌ input.csv not found!")
        return
    
    # Confirm action
    confirm = input("\n🔄 Split input.csv for Multi-RDP deployment? (y/n): ").lower()
    if confirm != 'y':
        print("👋 Operation cancelled!")
        return
    
    # Split the file
    if split_input_csv():
        print("\n" + "="*50)
        print("🎉 MULTI-RDP DISTRIBUTION COMPLETE!")
        print("\n📋 NEXT STEPS:")
        print("1. Copy input_rdp1.csv to RDP Server 1")
        print("2. Copy input_rdp2.csv to RDP Server 2") 
        print("3. Copy input_rdp3.csv to RDP Server 3")
        print("4. Rename each file to input.csv on respective RDP")
        print("5. Run python rdp_optimized_bot.py on each RDP")
        print("\n✨ All 3 RDP will run simultaneously for maximum viewers!")

if __name__ == "__main__":
    main()
