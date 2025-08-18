#!/bin/bash

# Test RDP Connection dari Mac
# Usage: ./test_rdp_connection.sh

echo "🔍 Testing RDP Connection..."

# Variabel RDP (ganti dengan info dari seller)
RDP_IP="MASUKKAN_IP_DISINI"
RDP_USER="Administrator"
RDP_PASS="MASUKKAN_PASSWORD_DISINI"

echo "📋 RDP Information:"
echo "IP: $RDP_IP"
echo "User: $RDP_USER"
echo "Password: [HIDDEN]"
echo ""

# Test ping ke RDP server
echo "🏓 Testing ping to RDP server..."
if ping -c 3 $RDP_IP > /dev/null 2>&1; then
    echo "✅ Ping successful - Server is reachable"
else
    echo "❌ Ping failed - Check IP address or network"
    exit 1
fi

# Test RDP port (3389)
echo "🔌 Testing RDP port 3389..."
if nc -z -v -w5 $RDP_IP 3389 > /dev/null 2>&1; then
    echo "✅ Port 3389 is open - RDP service running"
else
    echo "❌ Port 3389 is closed or blocked"
    exit 1
fi

echo ""
echo "🎉 RDP server is ready for connection!"
echo "📱 Open Microsoft Remote Desktop and connect"
echo ""
echo "🚀 Next steps:"
echo "1. Connect via Microsoft Remote Desktop"
echo "2. Install Python 3.11 in Windows"
echo "3. Setup bot files"
echo "4. Test bot functionality"
