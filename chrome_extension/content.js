// Content script untuk manipulasi DOM
console.log('[EXTENSION] Content script loaded');

// Get device ID dari background script
const deviceId = document.currentScript?.dataset?.deviceId || generateDeviceId();

function generateDeviceId() {
  const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
  let result = '';
  for (let i = 0; i < 32; i++) {
    result += chars.charAt(Math.floor(Math.random() * chars.length));
  }
  return result;
}

// Inject manipulation script
const script = document.createElement('script');
script.textContent = `
(function() {
  const DEVICE_ID = '${deviceId}';
  const VIEWER_BOOST = 50;
  
  console.log('[INJECT] Device manipulation active:', DEVICE_ID.slice(0,8) + '...' + DEVICE_ID.slice(-4));
  
  // Override navigator properties
  Object.defineProperty(navigator, 'deviceMemory', {get: () => 8});
  Object.defineProperty(navigator, 'hardwareConcurrency', {get: () => 8});
  
  // Override WebGL fingerprint
  const getParameter = WebGLRenderingContext.prototype.getParameter;
  WebGLRenderingContext.prototype.getParameter = function(parameter) {
    if (parameter === 37445) return 'Intel Inc. Custom ' + DEVICE_ID.slice(0,8);
    if (parameter === 37446) return 'Intel(R) HD Graphics Custom ' + DEVICE_ID.slice(8,16);
    return getParameter.call(this, parameter);
  };
  
  // Set device fingerprint in storage
  localStorage.setItem('device_id', DEVICE_ID);
  localStorage.setItem('browser_id', DEVICE_ID.slice(0,16));
  sessionStorage.setItem('session_device_id', DEVICE_ID);
  
  // Manipulasi network requests
  const originalFetch = window.fetch;
  window.fetch = function(...args) {
    const url = args[0];
    const options = args[1] || {};
    
    // Add custom headers
    options.headers = {
      ...options.headers,
      'X-Device-ID': DEVICE_ID,
      'X-Browser-ID': DEVICE_ID.slice(0,16),
      'X-Custom-Session': DEVICE_ID.slice(16)
    };
    
    return originalFetch(url, options).then(response => {
      // Manipulasi response jika mengandung viewer data
      if (url.includes('viewer') || url.includes('count')) {
        return response.clone().json().then(data => {
          // Boost viewer count
          if (data && typeof data === 'object') {
            manipulateViewerData(data);
            return new Response(JSON.stringify(data), {
              status: response.status,
              statusText: response.statusText,
              headers: response.headers
            });
          }
          return response;
        }).catch(() => response);
      }
      return response;
    });
  };
  
  // Manipulasi XMLHttpRequest
  const originalXHROpen = XMLHttpRequest.prototype.open;
  XMLHttpRequest.prototype.open = function(method, url, ...args) {
    this.addEventListener('readystatechange', function() {
      if (this.readyState === 4 && this.responseText) {
        try {
          const data = JSON.parse(this.responseText);
          if (manipulateViewerData(data)) {
            Object.defineProperty(this, 'responseText', {
              value: JSON.stringify(data),
              writable: false
            });
          }
        } catch(e) {}
      }
    });
    
    return originalXHROpen.call(this, method, url, ...args);
  };
  
  function manipulateViewerData(data) {
    let modified = false;
    
    function recursiveManipulate(obj) {
      if (typeof obj === 'object' && obj !== null) {
        for (let key in obj) {
          if (typeof obj[key] === 'number' && (key.toLowerCase().includes('viewer') || key.toLowerCase().includes('count'))) {
            if (obj[key] > 0 && obj[key] < 10000) { // Reasonable viewer count
              obj[key] += VIEWER_BOOST + Math.floor(Math.random() * 20);
              modified = true;
              console.log('[BOOST] Viewer count boosted:', key, obj[key]);
            }
          } else if (typeof obj[key] === 'object') {
            recursiveManipulate(obj[key]);
          }
        }
      }
    }
    
    recursiveManipulate(data);
    return modified;
  }
  
  // DOM manipulation untuk viewer count yang tampil di UI
  setInterval(() => {
    const viewerElements = document.querySelectorAll('[class*="viewer"], [class*="count"], [data-testid*="viewer"], [class*="audience"]');
    
    viewerElements.forEach(el => {
      const text = el.textContent || el.innerText;
      if (text && /\\d+/.test(text)) {
        const numbers = text.match(/\\d+/g);
        if (numbers) {
          numbers.forEach(num => {
            const currentCount = parseInt(num);
            if (currentCount > 0 && currentCount < 10000) {
              const newCount = currentCount + VIEWER_BOOST + Math.floor(Math.random() * 20);
              el.textContent = text.replace(num, newCount.toString());
              el.innerText = text.replace(num, newCount.toString());
            }
          });
        }
      }
    });
  }, 3000);
  
  console.log('[SUCCESS] Shopee viewer manipulation active!');
})();
`;

(document.head || document.documentElement).appendChild(script);
script.remove();
