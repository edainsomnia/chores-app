const CACHE_NAME = 'chores-app-v1';
const ASSETS_TO_CACHE = [
    '/',
    '/static/style.css',
    '/static/icon.png',
    '/static/manifest.json'
];

// 1. Installation: Dateien in den Cache laden
self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME).then((cache) => {
            console.log('Caching assets...');
            return cache.addAll(ASSETS_TO_CACHE);
        })
    );
});

// 2. Aktivierung: Alte Caches löschen (falls du die App updatest)
self.addEventListener('activate', (event) => {
    console.log('Service Worker aktiviert');
});

// 3. Strategie: Cache First, then Network
// Das macht die App blitzschnell
self.addEventListener('fetch', (event) => {
    event.respondWith(
        caches.match(event.request).then((response) => {
            return response || fetch(event.request);
        })
    );
});