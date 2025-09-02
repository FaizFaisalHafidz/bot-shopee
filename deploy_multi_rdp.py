#!/usr/bin/env python3
"""
Multi-RDP Deployment Script
Deploys Shopee bot to multiple Windows RDP instances
"""

import json
import time
from pathlib import Path
from datetime import datetime

class RDPDeployment:
    def __init__(self):
        self.rdp_configs = []
        self.deployment_status = {}
        
    def load_rdp_config(self):
        """Load RDP configuration from file or create template"""
        config_file = Path("config/rdp_deployment.json")
        
        if config_file.exists():
            with open(config_file, 'r') as f:
                self.rdp_configs = json.load(f)
        else:
            # Create template configuration
            template_config = [
                {
                    "rdp_id": "RDP-1", 
                    "host": "192.168.1.100",
                    "username": "Administrator",
                    "password": "your_password",
                    "viewers_per_rdp": 16,
                    "chrome_profiles": ["Profile 1", "Profile 2", "Profile 3", "Profile 4"]
                },
                {
                    "rdp_id": "RDP-2",
                    "host": "192.168.1.101", 
                    "username": "Administrator",
                    "password": "your_password",
                    "viewers_per_rdp": 17,
                    "chrome_profiles": ["Profile 5", "Profile 6", "Profile 7", "Profile 8"]
                },
                {
                    "rdp_id": "RDP-3",
                    "host": "192.168.1.102",
                    "username": "Administrator", 
                    "password": "your_password",
                    "viewers_per_rdp": 17,
                    "chrome_profiles": ["Profile 9", "Profile 10", "Profile 11", "Profile 12"]
                },
                {
                    "rdp_id": "RDP-4",
                    "host": "192.168.1.103",
                    "username": "Administrator",
                    "password": "your_password", 
                    "viewers_per_rdp": 17,
                    "chrome_profiles": ["Profile 13", "Profile 14", "Profile 15", "Profile 16"]
                },
                {
                    "rdp_id": "RDP-5",
                    "host": "192.168.1.104",
                    "username": "Administrator",
                    "password": "your_password",
                    "viewers_per_rdp": 17,
                    "chrome_profiles": ["Profile 17", "Profile 18", "Profile 19", "Profile 20"]
                },
                {
                    "rdp_id": "RDP-6",
                    "host": "192.168.1.105",
                    "username": "Administrator",
                    "password": "your_password", 
                    "viewers_per_rdp": 16,
                    "chrome_profiles": ["Profile 21", "Profile 22", "Profile 23", "Profile 24"]
                }
            ]
            
            # Save template
            config_file.parent.mkdir(exist_ok=True)
            with open(config_file, 'w') as f:
                json.dump(template_config, f, indent=2)
            
            print(f"📝 Template configuration created: {config_file}")
            print("Please edit the configuration file with your RDP details")
            return False
            
        return True
    
    def create_deployment_package(self):
        """Create deployment package with all necessary files"""
        print("📦 Creating deployment package...")
        
        # Files to include in deployment
        core_files = [
            "final_shopee_bot.py",
            "auto_setup_windows.bat", 
            "auto_setup_windows.ps1",
            "setup_and_run.py",
            "requirements.txt"
        ]
        
        # Create package directory
        package_dir = Path("deployment_package")
        package_dir.mkdir(exist_ok=True)
        
        # Copy core files
        for file_name in core_files:
            source_file = Path(file_name)
            if source_file.exists():
                dest_file = package_dir / file_name
                with open(source_file, 'r', encoding='utf-8') as src:
                    content = src.read()
                with open(dest_file, 'w', encoding='utf-8') as dst:
                    dst.write(content)
                print(f"   ✅ Copied: {file_name}")
            else:
                print(f"   ⚠️ Missing: {file_name}")
        
        # Create RDP-specific config
        rdp_config = {
            "session_url": "https://live.shopee.co.id/share?from=live&session=157658364&in=1",
            "max_viewers": 100,
            "viewers_per_rdp": 16,
            "delay_between_viewers": 2,
            "auto_restart": True,
            "monitoring": {
                "enabled": True,
                "interval": 30,
                "log_level": "INFO"
            }
        }
        
        with open(package_dir / "rdp_config.json", 'w') as f:
            json.dump(rdp_config, f, indent=2)
        
        # Create deployment instructions
        instructions = """
SHOPEE BOT DEPLOYMENT INSTRUCTIONS
=================================

1. AUTOMATIC SETUP (Recommended):
   - Run: auto_setup_windows.bat
   - This will install Python and all dependencies automatically
   
2. MANUAL SETUP (If automatic fails):
   - Install Python 3.8+ from python.org
   - Run: pip install -r requirements.txt
   - Run: python setup_and_run.py

3. RUNNING THE BOT:
   - Method A: Double-click auto_setup_windows.bat
   - Method B: python final_shopee_bot.py
   - Method C: python setup_and_run.py

4. MONITORING:
   - Bot will open Chrome windows automatically
   - Check logs/ folder for detailed logs
   - Each RDP should run 16-17 viewers

5. TROUBLESHOOTING:
   - If Chrome not found: Install Google Chrome
   - If profiles not found: Create Chrome profiles manually
   - If Python errors: Run auto_setup_windows.bat again

6. STOPPING THE BOT:
   - Close all Chrome windows
   - Or press Ctrl+C in command prompt

Configuration:
- Target: 100 total viewers across 6 RDP instances
- Each RDP: 16-17 viewers
- Session URL will be updated in rdp_config.json
        """
        
        with open(package_dir / "DEPLOYMENT_INSTRUCTIONS.txt", 'w') as f:
            f.write(instructions)
        
        print(f"✅ Deployment package created in: {package_dir}")
        return package_dir
    
    def generate_deployment_commands(self):
        """Generate Windows commands for each RDP"""
        print("\n🖥️ Generating deployment commands for each RDP...")
        
        commands = {}
        
        for rdp in self.rdp_configs:
            rdp_id = rdp['rdp_id']
            viewers = rdp['viewers_per_rdp']
            profiles = rdp['chrome_profiles']
            
            # Create RDP-specific batch file content
            batch_content = f"""@echo off
echo ========================================
echo SHOPEE BOT - {rdp_id}
echo Target Viewers: {viewers}
echo Chrome Profiles: {len(profiles)}
echo ========================================

REM Set RDP-specific configuration
set RDP_ID={rdp_id}
set MAX_VIEWERS={viewers}
set CHROME_PROFILES={','.join(profiles)}

REM Run the auto setup
call auto_setup_windows.bat

echo.
echo {rdp_id} deployment complete!
pause
"""
            
            commands[rdp_id] = {
                'batch_file': f"deploy_{rdp_id.lower()}.bat",
                'batch_content': batch_content,
                'powershell_command': f'powershell.exe -ExecutionPolicy Bypass -File auto_setup_windows.ps1',
                'python_command': f'python setup_and_run.py'
            }
            
            print(f"   ✅ {rdp_id}: {viewers} viewers, {len(profiles)} profiles")
        
        return commands
    
    def save_deployment_files(self, commands):
        """Save deployment files for each RDP"""
        deployment_dir = Path("deployment_package/rdp_specific")
        deployment_dir.mkdir(exist_ok=True)
        
        for rdp_id, cmd_info in commands.items():
            # Save batch file
            batch_file = deployment_dir / cmd_info['batch_file']
            with open(batch_file, 'w') as f:
                f.write(cmd_info['batch_content'])
            
            print(f"   📝 Created: {batch_file}")
        
        # Create master deployment script
        master_script = """@echo off
echo ========================================
echo SHOPEE BOT - MASTER DEPLOYMENT
echo ========================================

echo This will deploy the bot to all RDP instances
echo Make sure all RDP connections are ready
echo.

pause

REM Copy files to each RDP (manual step)
echo.
echo DEPLOYMENT STEPS:
echo 1. Copy deployment_package folder to each RDP
echo 2. Run the specific batch file on each RDP:
echo.
"""
        
        for rdp in self.rdp_configs:
            master_script += f'echo    {rdp["rdp_id"]}: run deploy_{rdp["rdp_id"].lower()}.bat\n'
        
        master_script += """
echo.
echo 3. Monitor each RDP for successful bot startup
echo.
pause
"""
        
        with open(deployment_dir.parent / "deploy_all.bat", 'w') as f:
            f.write(master_script)
        
        print(f"   📝 Created master deployment script: deploy_all.bat")
    
    def create_monitoring_dashboard(self):
        """Create monitoring dashboard for all RDPs"""
        dashboard_script = """#!/usr/bin/env python3
# Multi-RDP Monitoring Dashboard

import json
import time
from datetime import datetime

def load_rdp_config():
    try:
        with open('config/rdp_deployment.json', 'r') as f:
            return json.load(f)
    except:
        return []

def display_dashboard():
    rdp_configs = load_rdp_config()
    
    print("\\033[2J\\033[H")  # Clear screen
    print("🖥️  SHOPEE BOT - MULTI-RDP DASHBOARD")
    print("=" * 80)
    print(f"⏰ Last Update: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    total_viewers = 0
    active_rdps = 0
    
    print("RDP STATUS:")
    print("-" * 80)
    print(f"{'RDP ID':<10} {'Host':<15} {'Viewers':<10} {'Status':<10} {'Profiles':<20}")
    print("-" * 80)
    
    for rdp in rdp_configs:
        rdp_id = rdp['rdp_id']
        host = rdp['host']
        viewers = rdp['viewers_per_rdp']
        profiles = len(rdp.get('chrome_profiles', []))
        
        # In real implementation, you'd check actual RDP status
        status = "READY"  # Placeholder
        
        print(f"{rdp_id:<10} {host:<15} {viewers:<10} {status:<10} {profiles:<20}")
        
        total_viewers += viewers
        if status == "ACTIVE":
            active_rdps += 1
    
    print("-" * 80)
    print(f"SUMMARY: {active_rdps}/{len(rdp_configs)} RDPs Active | {total_viewers} Total Viewers")
    print()
    
    print("DEPLOYMENT COMMANDS:")
    print("- deploy_all.bat: Deploy to all RDPs")
    print("- monitor_viewers.py: Monitor active viewers")
    print("- test_fingerprint.py: Test device fingerprints")
    print()
    
    print("Press Ctrl+C to exit")

def main():
    try:
        while True:
            display_dashboard()
            time.sleep(30)  # Update every 30 seconds
    except KeyboardInterrupt:
        print("\\n👋 Dashboard stopped")

if __name__ == "__main__":
    main()
"""
        
        with open("deployment_package/dashboard.py", 'w') as f:
            f.write(dashboard_script)
        
        print("   📊 Created monitoring dashboard: dashboard.py")
    
    def generate_deployment_summary(self):
        """Generate deployment summary"""
        total_viewers = sum(rdp['viewers_per_rdp'] for rdp in self.rdp_configs)
        total_profiles = sum(len(rdp.get('chrome_profiles', [])) for rdp in self.rdp_configs)
        
        summary = f"""
SHOPEE BOT DEPLOYMENT SUMMARY
=============================
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

📊 OVERVIEW:
- Total RDP Instances: {len(self.rdp_configs)}
- Total Target Viewers: {total_viewers}
- Total Chrome Profiles: {total_profiles}
- Average Viewers per RDP: {total_viewers/len(self.rdp_configs):.1f}

🖥️ RDP BREAKDOWN:
"""
        
        for rdp in self.rdp_configs:
            summary += f"""
{rdp['rdp_id']}:
  - Host: {rdp['host']}
  - Target Viewers: {rdp['viewers_per_rdp']}
  - Chrome Profiles: {len(rdp.get('chrome_profiles', []))}
  - Profiles: {', '.join(rdp.get('chrome_profiles', []))}
"""
        
        summary += """
📁 DEPLOYMENT FILES:
- deployment_package/: Main deployment folder
- auto_setup_windows.bat: Automatic setup script
- final_shopee_bot.py: Main bot script
- deploy_all.bat: Master deployment script
- rdp_specific/: Individual RDP scripts
- dashboard.py: Monitoring dashboard

🚀 DEPLOYMENT STEPS:
1. Copy deployment_package to each RDP
2. Run deploy_[rdp-id].bat on each RDP
3. Verify bot startup on each instance
4. Monitor using dashboard.py

⚠️ REQUIREMENTS:
- Windows RDP with internet access
- Google Chrome installed
- Chrome profiles with logged-in Google accounts
- Target Shopee live session URL

🎯 TARGET: 100 viewers across 6 RDP instances
"""
        
        with open("deployment_package/DEPLOYMENT_SUMMARY.txt", 'w') as f:
            f.write(summary)
        
        print(f"📋 Deployment summary saved")
        return summary

def main():
    """Main deployment function"""
    print("🚀 Multi-RDP Shopee Bot Deployment")
    print("=" * 50)
    
    deploy = RDPDeployment()
    
    # Load RDP configuration
    if not deploy.load_rdp_config():
        print("\n❌ Please configure your RDP settings first!")
        return
    
    print(f"✅ Loaded {len(deploy.rdp_configs)} RDP configurations")
    
    # Create deployment package
    package_dir = deploy.create_deployment_package()
    
    # Generate deployment commands
    commands = deploy.generate_deployment_commands()
    
    # Save deployment files
    deploy.save_deployment_files(commands)
    
    # Create monitoring dashboard
    deploy.create_monitoring_dashboard()
    
    # Generate summary
    summary = deploy.generate_deployment_summary()
    
    print("\n" + "=" * 50)
    print("✅ DEPLOYMENT PACKAGE READY!")
    print("=" * 50)
    print(f"📁 Package Location: {package_dir}")
    print(f"🎯 Target: {sum(rdp['viewers_per_rdp'] for rdp in deploy.rdp_configs)} viewers")
    print(f"🖥️ RDP Instances: {len(deploy.rdp_configs)}")
    print()
    print("Next Steps:")
    print("1. Edit config/rdp_deployment.json with your RDP details")
    print("2. Copy deployment_package to each RDP")
    print("3. Run deploy_all.bat to start deployment")
    print("4. Monitor with dashboard.py")
    print("=" * 50)

if __name__ == "__main__":
    main()
