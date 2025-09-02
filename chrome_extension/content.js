// Content script for additional DOM manipulation
console.log('[EXTENSION] Content script loaded on Shopee Live');

// Wait for page to load
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initializeExtension);
} else {
  initializeExtension();
}

function initializeExtension() {
  console.log('[CONTENT] Initializing Shopee Live manipulation...');
  
  // Additional DOM monitoring for dynamic content
  const observer = new MutationObserver(function(mutations) {
    mutations.forEach(function(mutation) {
      if (mutation.type === 'childList') {
        mutation.addedNodes.forEach(function(node) {
          if (node.nodeType === 1) { // Element node
            manipulateNewElements(node);
          }
        });
      }
    });
  });
  
  // Start observing
  observer.observe(document.body, {
    childList: true,
    subtree: true
  });
  
  // Manipulate any newly added elements
  function manipulateNewElements(element) {
    const viewerElements = element.querySelectorAll ? 
      element.querySelectorAll('*') : [];
      
    [element, ...viewerElements].forEach(el => {
      if (el && el.textContent) {
        const text = el.textContent;
        const numbers = text.match(/\b\d{1,6}\b/g);
        
        if (numbers) {
          numbers.forEach(numStr => {
            const num = parseInt(numStr);
            if (num > 0 && num < 50000) {
              const boost = 50 + Math.floor(Math.random() * 20);
              const newNum = num + boost;
              const newText = text.replace(numStr, newNum.toString());
              
              try {
                if (el.textContent) el.textContent = newText;
                if (el.innerText) el.innerText = newText;
              } catch (e) {
                // Element might be read-only, ignore
              }
            }
          });
        }
      }
    });
  }
  
  console.log('[CONTENT] DOM observer activated for dynamic content');
}
