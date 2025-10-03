const CACHE_VERSION = 'v1';
const CACHE_NAME = `arvora-${CACHE_VERSION}`;
const OFFLINE_PAGE = '/offline.html';

// Assets to cache immediately on service worker install
const PRECACHE_URLS = [
    '/',
    '/index.html',
    '/styles.css',
    '/src/js/auth.js',
    '/src/js/eco.js',
    '/src/js/learning.js',
    '/src/js/social.js',
    '/src/js/analytics.js',
    '/src/js/ui.js',
    '/offline.html',
    '/images/logo.png'
];

// Install event - precache critical assets
self.addEventListener('install', event => {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(cache => cache.addAll(PRECACHE_URLS))
            .then(() => self.skipWaiting())
    );
});

// Activate event - clean up old caches
self.addEventListener('activate', event => {
    event.waitUntil(
        caches.keys().then(cacheNames => {
            return Promise.all(
                cacheNames
                    .filter(name => name.startsWith('arvora-') && name !== CACHE_NAME)
                    .map(name => caches.delete(name))
            );
        })
    );
});

// Fetch event - network-first strategy with fallback to cache
self.addEventListener('fetch', event => {
    // Skip non-GET requests
    if (event.request.method !== 'GET') return;

    // Handle API requests
    if (event.request.url.includes('/api/')) {
        event.respondWith(handleApiRequest(event.request));
        return;
    }

    // Handle static assets and pages
    event.respondWith(
        fetch(event.request)
            .then(response => {
                // Cache successful responses
                if (response.ok) {
                    const responseClone = response.clone();
                    caches.open(CACHE_NAME).then(cache => {
                        cache.put(event.request, responseClone);
                    });
                }
                return response;
            })
            .catch(async () => {
                const cachedResponse = await caches.match(event.request);
                if (cachedResponse) {
                    return cachedResponse;
                }
                // Return offline page if no cached response
                return caches.match(OFFLINE_PAGE);
            })
    );
});

// Handle API requests with network-first strategy
async function handleApiRequest(request) {
    try {
        const response = await fetch(request);
        // Don't cache if not successful
        if (!response.ok) throw new Error('Network response was not ok');
        return response;
    } catch (error) {
        const cachedResponse = await caches.match(request);
        if (cachedResponse) {
            return cachedResponse;
        }
        // Return a JSON error response if offline
        return new Response(
            JSON.stringify({
                error: 'You are offline. Please check your internet connection.'
            }),
            {
                status: 503,
                headers: { 'Content-Type': 'application/json' }
            }
        );
    }
}

// Push notification event
self.addEventListener('push', event => {
    const data = event.data.json();
    const options = {
        body: data.body,
        icon: '/images/logo.png',
        badge: '/images/badge.png',
        data: data.data
    };

    event.waitUntil(
        self.registration.showNotification(data.title, options)
    );
});

// Notification click event
self.addEventListener('notificationclick', event => {
    event.notification.close();
    
    // Handle notification click based on data
    if (event.notification.data) {
        const urlToOpen = new URL(event.notification.data.url, self.location.origin).href;
        
        event.waitUntil(
            clients.matchAll({ type: 'window' }).then(windowClients => {
                // Check if a window is already open
                for (const client of windowClients) {
                    if (client.url === urlToOpen) {
                        return client.focus();
                    }
                }
                // Open new window
                return clients.openWindow(urlToOpen);
            })
        );
    }
});