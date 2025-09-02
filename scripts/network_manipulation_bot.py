#!/usr/bin/env python3
"""
STRATEGI 2: Network Request Manipulation
- Intercept HTTP requests ke Shopee API
- Manipulasi response viewer count
- Bypass device_id checking via headers
"""

import asyncio
import json
import aiohttp
from aiohttp import web
import ssl

class ShopeeProxyServer:
    def __init__(self):
        self.target_host = "live.shopee.co.id"
        self.viewer_count_boost = 50
        self.device_id = self.generate_device_id()
    
    def generate_device_id(self):
        import random, string
        return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(32))
    
    async def proxy_handler(self, request):
        """Handle semua request dan manipulasi response"""
        
        # Headers untuk bypass detection
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'X-Device-ID': self.device_id,
            'X-Browser-ID': self.device_id[:16],
            'X-Session-ID': self.device_id[16:],
            'Origin': f'https://{self.target_host}',
            'Referer': f'https://{self.target_host}/',
        }
        
        # Forward request ke server asli
        target_url = f"https://{self.target_host}{request.path_qs}"
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.request(
                    method=request.method,
                    url=target_url,
                    headers=headers,
                    data=await request.read() if request.body_exists else None
                ) as response:
                    
                    content = await response.read()
                    
                    # Manipulasi response jika ada data viewer count
                    if response.content_type == 'application/json':
                        try:
                            data = json.loads(content)
                            
                            # Manipulasi viewer count
                            if self.manipulate_viewer_data(data):
                                content = json.dumps(data).encode()
                                print(f"[MANIPULATED] Viewer count boosted by {self.viewer_count_boost}")
                        except:
                            pass
                    
                    # Return response
                    return web.Response(
                        body=content,
                        status=response.status,
                        headers=dict(response.headers)
                    )
                    
        except Exception as e:
            return web.Response(text=f"Proxy error: {e}", status=502)
    
    def manipulate_viewer_data(self, data):
        """Manipulasi data viewer count dalam JSON response"""
        modified = False
        
        def recursive_manipulate(obj):
            nonlocal modified
            
            if isinstance(obj, dict):
                for key, value in obj.items():
                    if 'viewer' in key.lower() or 'count' in key.lower():
                        if isinstance(value, int) and value > 0:
                            obj[key] = value + self.viewer_count_boost
                            modified = True
                    elif isinstance(value, (dict, list)):
                        recursive_manipulate(value)
                        
            elif isinstance(obj, list):
                for item in obj:
                    recursive_manipulate(item)
        
        recursive_manipulate(data)
        return modified
    
    async def start_server(self, host='127.0.0.1', port=8888):
        """Start proxy server"""
        app = web.Application()
        app.router.add_route('*', '/{path:.*}', self.proxy_handler)
        
        runner = web.AppRunner(app)
        await runner.setup()
        
        site = web.TCPSite(runner, host, port)
        await site.start()
        
        print(f"[PROXY] Server running on http://{host}:{port}")
        print(f"[PROXY] Device ID: {self.device_id[:8]}...{self.device_id[-4:]}")
        print(f"[PROXY] Redirect Shopee traffic to: {host}:{port}")

async def main():
    print("=" * 50)
    print("   SHOPEE BOT - NETWORK MANIPULATION")
    print("=" * 50)
    
    proxy = ShopeeProxyServer()
    
    print("[INFO] Starting proxy server...")
    await proxy.start_server()
    
    print("\n[SETUP INSTRUCTIONS]")
    print("1. Set Windows hosts file:")
    print(f"   127.0.0.1 live.shopee.co.id")
    print("2. Or use browser proxy: 127.0.0.1:8888")
    print("3. Navigate to Shopee Live normally")
    print("4. Viewer count akan otomatis ter-boost!")
    
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        print("\n[STOP] Proxy server stopped")

if __name__ == "__main__":
    asyncio.run(main())
