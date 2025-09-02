// Inject script - injected directly ke page context
(function() {
  const script = document.querySelector('[data-device-id]');
  const DEVICE_ID = script?.dataset?.deviceId || generateDeviceId();
  
  function generateDeviceId() {
    const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
    let result = '';
    for (let i = 0; i < 32; i++) {
      result += chars.charAt(Math.floor(Math.random() * chars.length));
    }
    return result;
  }
  
  console.log('[INJECT] Advanced device fingerprint injection:', DEVICE_ID.slice(0,8) + '...');
  
  // Advanced fingerprint manipulation
  window.customDeviceId = DEVICE_ID;
  
  // Override canvas fingerprinting
  const originalToDataURL = HTMLCanvasElement.prototype.toDataURL;
  HTMLCanvasElement.prototype.toDataURL = function(...args) {
    const result = originalToDataURL.apply(this, args);
    return result + DEVICE_ID.slice(-8); // Unique canvas fingerprint
  };
  
  // Override audio context fingerprinting
  if (window.AudioContext || window.webkitAudioContext) {
    const AudioContextConstructor = window.AudioContext || window.webkitAudioContext;
    const originalCreateOscillator = AudioContextConstructor.prototype.createOscillator;
    AudioContextConstructor.prototype.createOscillator = function() {
      const oscillator = originalCreateOscillator.call(this);
      oscillator.frequency.value += parseInt(DEVICE_ID.slice(0, 2), 36) / 1000;
      return oscillator;
    };
  }
  
  // Override screen properties
  Object.defineProperty(screen, 'availWidth', {get: () => 1920 + parseInt(DEVICE_ID.slice(2, 4), 36) % 100});
  Object.defineProperty(screen, 'availHeight', {get: () => 1080 + parseInt(DEVICE_ID.slice(4, 6), 36) % 100});
  
  console.log('[INJECT] All fingerprints overridden with device:', DEVICE_ID.slice(0,8));
})();
