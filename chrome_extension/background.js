// Background script untuk intercept network requests
chrome.webRequest.onBeforeRequest.addListener(
  function(details) {
    console.log('[EXTENSION] Intercepting request:', details.url);
    return {cancel: false};
  },
  {urls: ["https://live.shopee.co.id/*"]},
  ["blocking"]
);

chrome.webRequest.onResponseStarted.addListener(
  function(details) {
    console.log('[EXTENSION] Response intercepted:', details.url);
  },
  {urls: ["https://live.shopee.co.id/*"]}
);

// Inject device ID manipulation
chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  if (changeInfo.status === 'complete' && tab.url && tab.url.includes('live.shopee.co.id')) {
    
    // Generate unique device ID
    const deviceId = generateDeviceId();
    
    chrome.scripting.executeScript({
      target: { tabId: tabId },
      func: injectDeviceManipulation,
      args: [deviceId]
    });
  }
});

function generateDeviceId() {
  const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
  let result = '';
  for (let i = 0; i < 32; i++) {
    result += chars.charAt(Math.floor(Math.random() * chars.length));
  }
  return result;
}

function injectDeviceManipulation(deviceId) {
  // Inject script ke page
  const script = document.createElement('script');
  script.src = chrome.runtime.getURL('inject.js');
  script.dataset.deviceId = deviceId;
  (document.head || document.documentElement).appendChild(script);
  script.remove();
}
