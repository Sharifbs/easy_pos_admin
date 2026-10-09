// Clear older cache and network-first strategy
const CACHE_NAME = 'easy-pos-v2';

self.addEventListener('install', event => {
  self.skipWaiting();
});

self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cache => caches.delete(cache))
      );
    }).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', event => {
  // Always fetch fresh code from Vercel network first
  event.respondWith(
    fetch(event.request).catch(() => caches.match(event.request))
  );
});