// Page Navigation
function showPage(pageId, ev) {
    // Hide all pages
    const pages = document.querySelectorAll('.page');
    pages.forEach(page => page.classList.add('hidden'));

    // Show selected page
    const target = document.getElementById(pageId);
    if (target) target.classList.remove('hidden');

    // Update navigation active state
    const navButtons = document.querySelectorAll('nav button');
    navButtons.forEach(btn => btn.classList.remove('text-green-600', 'font-bold'));

    // Add active state to current button (if event provided)
    if (ev && ev.currentTarget) {
        ev.currentTarget.classList.add('text-green-600', 'font-bold');
    }
}

// Attach showPage to existing inline onclick attributes by wrapping expected signature
window.showPage = function(pageId) { showPage(pageId, event); };

// Simulate progress animations
function animateProgress() {
    const progressBars = document.querySelectorAll('.progress-fill');
    progressBars.forEach(bar => {
        const width = bar.style.width || getComputedStyle(bar).width;
        const inlineWidth = bar.getAttribute('data-width');
        const finalWidth = inlineWidth || bar.style.width || '';
        bar.style.width = '0%';
        setTimeout(() => {
            if (finalWidth) bar.style.width = finalWidth;
        }, 100);
    });
}

// Initialize animations when page loads
document.addEventListener('DOMContentLoaded', function() {
    setTimeout(animateProgress, 500);
});

// Add click handlers for interactive elements
document.addEventListener('click', function(e) {
    const text = (e.target.textContent || '').trim();

    // Handle challenge completion
    if (text.includes('Mark as Complete')) {
        e.target.textContent = '✅ Completed!';
        e.target.classList.remove('bg-green-500', 'hover:bg-green-600');
        e.target.classList.add('bg-gray-400', 'cursor-not-allowed');

        // Show success message
        const successMsg = document.createElement('div');
        successMsg.className = 'fixed top-4 right-4 bg-green-500 text-white px-6 py-3 rounded-full font-bold z-50';
        successMsg.textContent = '🎉 +50 points earned!';
        document.body.appendChild(successMsg);

        setTimeout(() => successMsg.remove(), 3000);
    }

    // Handle challenge acceptance
    if (text.includes('Accept Challenge')) {
        e.target.textContent = '✅ Accepted!';
        e.target.classList.remove('bg-blue-500', 'hover:bg-blue-600', 'bg-green-500', 'hover:bg-green-600', 'bg-purple-500', 'hover:bg-purple-600');
        e.target.classList.add('bg-gray-400', 'cursor-not-allowed');

        const successMsg = document.createElement('div');
        successMsg.className = 'fixed top-4 right-4 bg-blue-500 text-white px-6 py-3 rounded-full font-bold z-50';
        successMsg.textContent = '🚀 Challenge accepted!';
        document.body.appendChild(successMsg);

        setTimeout(() => successMsg.remove(), 3000);
    }

    // Handle approvals
    if (text.includes('Approve')) {
        const parentDiv = e.target.closest('.bg-yellow-50');
        if (parentDiv) {
            parentDiv.classList.remove('bg-yellow-50', 'border-yellow-200');
            parentDiv.classList.add('bg-green-50', 'border-green-200');
            e.target.textContent = '✅ Approved';
            e.target.classList.remove('bg-green-500', 'hover:bg-green-600');
            e.target.classList.add('bg-gray-400', 'cursor-not-allowed');
        }
    }
});

// Add hover effects for cards (improve bubbling target detection)
document.addEventListener('mouseover', function(e) {
    const el = e.target.closest('.card-hover');
    if (el) el.style.transform = 'translateY(-5px)';
});

document.addEventListener('mouseout', function(e) {
    const el = e.target.closest('.card-hover');
    if (el) el.style.transform = 'translateY(0)';
});

// The following small snippet was originally injected (likely Cloudflare challenge iframe).
// It is preserved here, but commented out to avoid unexpected iframe/script injection.
/*
(function(){function c(){var b=a.contentDocument||a.contentWindow.document;if(b){var d=b.createElement('script');d.innerHTML="window.__CF$cv$params={r:'988b1ec055e1a7ce',t:'MTc1OTQ4MDY3My4wMDAwMDA='};var a=document.createElement('script');a.nonce='';a.src='/cdn-cgi/challenge-platform/scripts/jsd/main.js';document.getElementsByTagName('head')[0].appendChild(a);";b.getElementsByTagName('head')[0].appendChild(d)}}if(document.body){var a=document.createElement('iframe');a.height=1;a.width=1;a.style.position='absolute';a.style.top=0;a.style.left=0;a.style.border='none';a.style.visibility='hidden';document.body.appendChild(a);if('loading'!==document.readyState)c();else if(window.addEventListener)document.addEventListener('DOMContentLoaded',c);else{var e=document.onreadystatechange||function(){};document.onreadystatechange=function(b){e(b);'loading'!==document.readyState&&(document.onreadystatechange=e,c())}}}})();
*/
