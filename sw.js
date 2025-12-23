const CACHE_NAME = 'chores-app-v2'; // Version erhöht, um alten Cache zu leeren

// Die Pfade müssen EXAKT mit deinen Dateien auf GitHub übereinstimmen
const ASSETS_TO_CACHE = [
    '/chores-app/',
    '/chores-app/index.html',
    '/chores-app/static/style.css',
    '/chores-app/static/icon.png',
    '/chores-app/manifest.json' // Korrigiert: manifest liegt im Hauptverzeichnis
];

// 1. Installation: Dateien in den Cache laden
self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME).then((cache) => {
            console.log('Caching assets...');
            // addAll schlägt fehl, wenn ein einziger Pfad falsch ist!
            return cache.addAll(ASSETS_TO_CACHE);
        })
    );
    self.skipWaiting(); // Erzwingt, dass der neue SW sofort aktiv wird
});

// 2. Aktivierung: Alte Caches löschen
self.addEventListener('activate', (event) => {
    event.waitUntil(
        caches.keys().then((cacheNames) => {
            return Promise.all(
                cacheNames.map((cache) => {
                    if (cache !== CACHE_NAME) {
                        console.log('Lösche alten Cache:', cache);
                        return caches.delete(cache);
                    }
                })
            );
        })
    );
    console.log('Service Worker aktiviert');
    return self.clients.claim(); // Übernimmt sofort die Kontrolle
});

// 3. Strategie: Cache First, falling back to Network
self.addEventListener('fetch', (event) => {
    event.respondWith(
        caches.match(event.request).then((response) => {
            return response || fetch(event.request);
        })
    );
});

