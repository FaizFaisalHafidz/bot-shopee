const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

class ShopeeViewerBot {
    constructor() {
        this.sessionCookies = [];
        this.activeViewers = [];
        this.viewerBoost = 25; // Base viewer boost per session
        this.loadSessionCookies();
    }

    loadSessionCookies() {
        try {
            const csvPath = path.join(__dirname, '..', 'input.csv');
            const csvContent = fs.readFileSync(csvPath, 'utf8');
            const lines = csvContent.split('\n').filter(line => line.trim());
            
            console.log(`[COOKIES] Loading ${lines.length} session cookies...`);
            
            this.sessionCookies = lines.map((line, index) => {
                const cookies = this.parseCookieString(line.trim());
                return {
                    id: index + 1,
                    cookies: cookies,
                    rawCookies: line.trim(),
                    deviceId: this.generateDeviceId(),
                    userAgent: this.generateUserAgent()
                };
            });
            
            console.log(`[SUCCESS] Loaded ${this.sessionCookies.length} authenticated sessions`);
        } catch (error) {
            console.log(`[ERROR] Failed to load cookies: ${error.message}`);
            process.exit(1);
        }
    }

    parseCookieString(cookieStr) {
        const cookies = [];
        const pairs = cookieStr.split('; ');
        
        pairs.forEach(pair => {
            const [name, ...valueParts] = pair.split('=');
            const value = valueParts.join('=');
            
            if (name && value) {
                cookies.push({
                    name: name.trim(),
                    value: value.trim(),
                    domain: '.shopee.co.id',
                    path: '/',
                    httpOnly: false,
                    secure: true,
                    sameSite: 'Lax'
                });
            }
        });
        
        return cookies;
    }

    generateDeviceId() {
        const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
        let result = '';
        for (let i = 0; i < 32; i++) {
            result += chars.charAt(Math.floor(Math.random() * chars.length));
        }
        return result;
    }

    generateUserAgent() {
        const versions = ['120.0.0.0', '119.0.0.0', '118.0.0.0', '117.0.0.0'];
        const version = versions[Math.floor(Math.random() * versions.length)];
        return `Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/${version} Safari/537.36`;
    }

    async createViewer(sessionData, sessionId, viewerIndex) {
        const browser = await puppeteer.launch({
            headless: false,
            args: [
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-dev-shm-usage',
                '--disable-web-security',
                '--disable-features=VizDisplayCompositor',
                '--disable-gpu',
                `--user-agent=${sessionData.userAgent}`,
                '--disable-blink-features=AutomationControlled',
                '--no-first-run',
                '--disable-extensions',
                '--disable-plugins',
                '--mute-audio'
            ],
            executablePath: this.findChrome(),
            userDataDir: path.join(__dirname, '..', 'sessions', 'viewer_sessions', `viewer_${viewerIndex}`)
        });

        try {
            const page = await browser.newPage();
            
            // Set viewport and user agent
            await page.setViewport({ width: 1366, height: 768 });
            await page.setUserAgent(sessionData.userAgent);
            
            // Inject device fingerprint
            await page.evaluateOnNewDocument((deviceId) => {
                // Override device properties
                Object.defineProperty(navigator, 'deviceMemory', {get: () => 8});
                Object.defineProperty(navigator, 'hardwareConcurrency', {get: () => 8});
                Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
                
                // Set device ID in storage
                localStorage.setItem('device_id', deviceId);
                sessionStorage.setItem('session_device_id', deviceId);
                window.customDeviceId = deviceId;
                
                console.log(`[INJECT] Device fingerprint set: ${deviceId.slice(0,8)}...`);
            }, sessionData.deviceId);
            
            // Set cookies before navigation
            console.log(`[VIEWER ${viewerIndex}] Setting ${sessionData.cookies.length} cookies...`);
            for (const cookie of sessionData.cookies) {
                try {
                    await page.setCookie(cookie);
                } catch (cookieError) {
                    // Ignore individual cookie errors
                }
            }
            
            // Navigate to Shopee Live
            const shopeeUrl = `https://live.shopee.co.id/share?from=live&session=${sessionId}&in=1`;
            console.log(`[VIEWER ${viewerIndex}] Navigating to: ${shopeeUrl}`);
            
            await page.goto(shopeeUrl, { 
                waitUntil: 'networkidle2', 
                timeout: 30000 
            });
            
            // Wait for page to load
            await page.waitForTimeout(5000);
            
            // Inject viewer manipulation script
            await page.evaluate((boost) => {
                // Viewer count manipulation
                setInterval(() => {
                    // Find viewer count elements
                    const selectors = [
                        '[class*="viewer"]',
                        '[class*="count"]', 
                        '[data-testid*="viewer"]',
                        '[class*="audience"]',
                        '.live-viewer-count',
                        '.viewer-number'
                    ];
                    
                    selectors.forEach(selector => {
                        const elements = document.querySelectorAll(selector);
                        elements.forEach(el => {
                            const text = el.textContent || el.innerText;
                            if (text && /\\d+/.test(text)) {
                                const match = text.match(/\\d+/);
                                if (match) {
                                    const currentCount = parseInt(match[0]);
                                    if (currentCount > 0 && currentCount < 50000) {
                                        const newCount = currentCount + boost + Math.floor(Math.random() * 10);
                                        const newText = text.replace(/\\d+/, newCount.toString());
                                        el.textContent = newText;
                                        el.innerText = newText;
                                    }
                                }
                            }
                        });
                    });
                    
                    console.log(`[BOOST] Viewer count manipulation active (+${boost})`);
                }, 8000);
                
                // Network request interception
                const originalFetch = window.fetch;
                window.fetch = function(...args) {
                    return originalFetch.apply(this, args).then(response => {
                        if (args[0] && (args[0].includes('viewer') || args[0].includes('count'))) {
                            console.log('[INTERCEPT] Viewer API call detected');
                        }
                        return response;
                    });
                };
                
            }, this.viewerBoost);
            
            console.log(`[SUCCESS] Viewer ${viewerIndex} active with session cookies!`);
            console.log(`[INFO] Device ID: ${sessionData.deviceId.slice(0,8)}...${sessionData.deviceId.slice(-4)}`);
            
            return { browser, page };
            
        } catch (error) {
            console.log(`[ERROR] Failed to create viewer ${viewerIndex}: ${error.message}`);
            await browser.close();
            return null;
        }
    }

    findChrome() {
        const possiblePaths = [
            'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
            'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe',
            process.env.LOCALAPPDATA + '\\Google\\Chrome\\Application\\chrome.exe',
            'C:\\Users\\Administrator\\AppData\\Local\\Google\\Chrome\\Application\\chrome.exe'
        ];

        for (const path of possiblePaths) {
            if (fs.existsSync(path)) {
                return path;
            }
        }
        
        return null; // Use default
    }

    async startViewers(sessionId, viewerCount) {
        console.log(`\n==========================================`);
        console.log(`    SHOPEE VIEWER BOT - SESSION COOKIES`);
        console.log(`==========================================`);
        console.log(`Target Session: ${sessionId}`);
        console.log(`Viewers: ${viewerCount}`);
        console.log(`Available Sessions: ${this.sessionCookies.length}`);
        console.log(`==========================================\n`);

        if (viewerCount > this.sessionCookies.length) {
            console.log(`[WARNING] Requested ${viewerCount} viewers but only ${this.sessionCookies.length} sessions available`);
            viewerCount = this.sessionCookies.length;
        }

        for (let i = 0; i < viewerCount; i++) {
            const sessionData = this.sessionCookies[i];
            console.log(`[STARTING] Viewer ${i + 1} with session cookies...`);
            
            const viewer = await this.createViewer(sessionData, sessionId, i + 1);
            if (viewer) {
                this.activeViewers.push(viewer);
                
                // Random delay between viewers
                const delay = 3000 + Math.random() * 5000;
                console.log(`[DELAY] Waiting ${Math.floor(delay/1000)}s before next viewer...`);
                await new Promise(resolve => setTimeout(resolve, delay));
            }
        }

        console.log(`\n[COMPLETED] ${this.activeViewers.length}/${viewerCount} viewers started successfully!`);
        console.log(`[INFO] Viewers will continue running with boost manipulation`);
        console.log(`[INFO] Press Ctrl+C to stop all viewers`);

        // Keep alive
        process.on('SIGINT', async () => {
            console.log(`\n[CLEANUP] Closing all viewers...`);
            for (const viewer of this.activeViewers) {
                try {
                    await viewer.browser.close();
                } catch (e) {}
            }
            process.exit(0);
        });

        // Keep process alive
        setInterval(() => {
            console.log(`[ALIVE] ${this.activeViewers.length} viewers active`);
        }, 60000);
    }
}

// Main execution
async function main() {
    const args = process.argv.slice(2);
    
    if (args.length < 2) {
        console.log('Usage: node generatex_4c.js <session_id> <viewer_count>');
        console.log('Example: node generatex_4c.js 157658364 5');
        process.exit(1);
    }

    const sessionId = args[0];
    const viewerCount = parseInt(args[1]) || 2;

    const bot = new ShopeeViewerBot();
    await bot.startViewers(sessionId, viewerCount);
}

// Handle unhandled rejections
process.on('unhandledRejection', (reason, promise) => {
    console.log('[ERROR] Unhandled Rejection:', reason);
});

if (require.main === module) {
    main();
}

module.exports = ShopeeViewerBot;
