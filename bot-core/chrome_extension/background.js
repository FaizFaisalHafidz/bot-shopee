// Background service worker for Manifest V3
console.log('[EXTENSION] Background service worker loaded');

// Generate unique device ID
function generateDeviceId() {
  const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
  let result = '';
  for (let i = 0; i < 32; i++) {
    result += chars.charAt(Math.floor(Math.random() * chars.length));
  }
  return result;
}

// Store device ID in storage
async function initializeDeviceId() {
  const result = await chrome.storage.local.get(['deviceId']);
  if (!result.deviceId) {
    const deviceId = generateDeviceId();
    await chrome.storage.local.set({ deviceId });
    console.log('[EXTENSION] Generated new device ID:', deviceId.slice(0, 8) + '...');
  }
}

// Initialize on extension startup
initializeDeviceId();

// Inject manipulation when tab loads Shopee
chrome.tabs.onUpdated.addListener(async (tabId, changeInfo, tab) => {
  if (changeInfo.status === 'complete' && tab.url && tab.url.includes('live.shopee.co.id')) {
    console.log('[EXTENSION] Shopee Live detected, injecting manipulation...');
    
    try {
      // Get stored device ID
      const result = await chrome.storage.local.get(['deviceId']);
      const deviceId = result.deviceId || generateDeviceId();
      
      // Inject the manipulation script
      await chrome.scripting.executeScript({
        target: { tabId: tabId },
        func: injectManipulation,
        args: [deviceId]
      });
      
      console.log('[EXTENSION] Successfully injected manipulation for device:', deviceId.slice(0, 8) + '...');
      
    } catch (error) {
      console.error('[EXTENSION] Failed to inject script:', error);
    }
  }
});

// Function to inject into page (will be stringified and executed)
function injectManipulation(deviceId) {
  console.log('[INJECT] Starting Shopee manipulation with device:', deviceId.slice(0, 8) + '...');
  
  const VIEWER_BOOST = 50;
  const RANDOM_BOOST = 20;
  
  // Set device fingerprint
  window.customDeviceId = deviceId;
  localStorage.setItem('device_id', deviceId);
  localStorage.setItem('browser_id', deviceId.slice(0, 16));
  sessionStorage.setItem('session_device_id', deviceId);
  
  // Override navigator properties
  Object.defineProperty(navigator, 'deviceMemory', {
    get: () => 8,
    configurable: true
  });
  
  Object.defineProperty(navigator, 'hardwareConcurrency', {
    get: () => 8,
    configurable: true
  });
  
  // Override WebGL fingerprint
  try {
    const getParameter = WebGLRenderingContext.prototype.getParameter;
    WebGLRenderingContext.prototype.getParameter = function(parameter) {
      if (parameter === 37445) return 'Intel Inc. Custom ' + deviceId.slice(0, 8);
      if (parameter === 37446) return 'Intel HD Graphics Custom ' + deviceId.slice(8, 16);
      return getParameter.call(this, parameter);
    };
  } catch (e) {
    console.log('[INJECT] WebGL override failed:', e);
  }
  
  // Network request manipulation
  const originalFetch = window.fetch;
  window.fetch = function(...args) {
    const url = args[0];
    const options = args[1] || {};
    
    // Add custom headers for device ID
    options.headers = {
      ...options.headers,
      'X-Device-ID': deviceId,
      'X-Browser-ID': deviceId.slice(0, 16),
      'X-Session-ID': deviceId.slice(16)
    };
    
    return originalFetch(url, options).then(async response => {
      // Manipulate viewer count responses
      if (url.includes('viewer') || url.includes('count') || url.includes('live')) {
        try {
          const clonedResponse = response.clone();
          const data = await clonedResponse.json();
          
          if (manipulateViewerData(data)) {
            console.log('[INJECT] Viewer data manipulated in API response');
            return new Response(JSON.stringify(data), {
              status: response.status,
              statusText: response.statusText,
              headers: response.headers
            });
          }
        } catch (e) {
          // If not JSON, return original
        }
      }
      return response;
    });
  };
  
  // XMLHttpRequest manipulation
  const originalXHROpen = XMLHttpRequest.prototype.open;
  XMLHttpRequest.prototype.open = function(method, url, ...args) {
    this.setRequestHeader = function(name, value) {
      XMLHttpRequest.prototype.setRequestHeader.call(this, name, value);
      // Add device headers
      XMLHttpRequest.prototype.setRequestHeader.call(this, 'X-Device-ID', deviceId);
      XMLHttpRequest.prototype.setRequestHeader.call(this, 'X-Browser-ID', deviceId.slice(0, 16));
    };
    
    this.addEventListener('readystatechange', function() {
      if (this.readyState === 4 && this.responseText) {
        try {
          const data = JSON.parse(this.responseText);
          if (manipulateViewerData(data)) {
            Object.defineProperty(this, 'responseText', {
              value: JSON.stringify(data),
              writable: false,
              configurable: true
            });
          }
        } catch (e) {
          // Not JSON, ignore
        }
      }
    });
    
    return originalXHROpen.call(this, method, url, ...args);
  };
  
  function manipulateViewerData(data) {
    let modified = false;
    
    function recursiveManipulate(obj) {
      if (typeof obj === 'object' && obj !== null) {
        for (let key in obj) {
          const value = obj[key];
          if (typeof value === 'number') {
            const keyLower = key.toLowerCase();
            if (keyLower.includes('viewer') || keyLower.includes('count') || keyLower.includes('audience')) {
              if (value > 0 && value < 50000) { // Reasonable viewer count
                const boost = VIEWER_BOOST + Math.floor(Math.random() * RANDOM_BOOST);
                obj[key] = value + boost;
                modified = true;
                console.log('[INJECT] Boosted', key, 'from', value, 'to', obj[key]);
              }
            }
          } else if (typeof value === 'object') {
            recursiveManipulate(value);
          }
        }
      }
    }
    
    recursiveManipulate(data);
    return modified;
  }
  
  // DOM manipulation for visible viewer counts
  function manipulateDOM() {
    const selectors = [
      '[class*="viewer"]',
      '[class*="count"]', 
      '[class*="audience"]',
      '[data-testid*="viewer"]',
      '[data-testid*="count"]',
      'span:contains("viewer")',
      'div:contains("viewer")',
      'span',
      'div'
    ];
    
    selectors.forEach(selector => {
      try {
        const elements = document.querySelectorAll(selector);
        elements.forEach(el => {
          const text = el.textContent || el.innerText || '';
          const numbers = text.match(/\b\d{1,6}\b/g); // Find numbers 1-6 digits
          
          if (numbers) {
            numbers.forEach(numStr => {
              const num = parseInt(numStr);
              if (num > 0 && num < 50000) { // Reasonable viewer range
                const boost = VIEWER_BOOST + Math.floor(Math.random() * RANDOM_BOOST);
                const newNum = num + boost;
                const newText = text.replace(numStr, newNum.toString());
                
                if (el.textContent) el.textContent = newText;
                if (el.innerText) el.innerText = newText;
                
                console.log('[INJECT] DOM boosted viewer count:', num, '→', newNum);
              }
            });
          }
        });
      } catch (e) {
        // Selector might not be supported, ignore
      }
    });
  }
  
  // Run DOM manipulation periodically
  setInterval(manipulateDOM, 3000);
  
  // Initial DOM manipulation
  setTimeout(manipulateDOM, 1000);
  
  console.log('[SUCCESS] Shopee Live manipulation fully activated!');
  console.log('[INFO] Device ID:', deviceId.slice(0, 8) + '...' + deviceId.slice(-4));
  console.log('[INFO] Viewer boost: +' + VIEWER_BOOST + ' base + random up to +' + RANDOM_BOOST);
}
