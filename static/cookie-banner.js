(function() {
    function initCookieBanner() {
        const hasConsent = localStorage.getItem('neurovibe_cookie_consent');
        if (!hasConsent) {
            document.getElementById('cookie-banner').style.display = 'flex';
        } else {
            document.getElementById('cookie-banner').style.display = 'none';
        }
    }

    window.acceptCookies = function() {
        localStorage.setItem('neurovibe_cookie_consent', 'true');
        document.getElementById('cookie-banner').style.display = 'none';
    };

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initCookieBanner);
    } else {
        initCookieBanner();
    }
})();
