self.addEventListener('install', event => {
    event.waitUntil(
        caches.open('travelslasher-v1').then(cache => {
            return cache.addAll([
                '/', '/index.html', '/styles.css', '/script.js', '/manifest.json'
            ]);
        })
    );
});

self.addEventListener('fetch', event => {
    event.respondWith(
        caches.match(event.request).then(response => response || fetch(event.request))
    );
});