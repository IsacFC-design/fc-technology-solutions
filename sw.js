/* Service worker de FC Technology Solutions. Cambia VERSION para forzar que se actualice el contenido guardado. */
const VERSION = 'fc-v2';
const SHELL = ['/', '/index.html', '/manifest.webmanifest', '/favicon-32.png', '/icon-192.png', '/icon-512.png', '/og-image.png'];

self.addEventListener('install', (e) => {
  e.waitUntil(caches.open(VERSION).then((c) => c.addAll(SHELL)).then(() => self.skipWaiting()));
});

self.addEventListener('activate', (e) => {
  e.waitUntil(caches.keys().then((keys) => Promise.all(keys.filter((k) => k !== VERSION).map((k) => caches.delete(k)))).then(() => self.clients.claim()));
});

self.addEventListener('fetch', (e) => {
  const req = e.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);
  if (!/^https?:$/.test(url.protocol)) return;
  if (/supabase\.co$/.test(url.hostname)) return;            // los datos de Supabase siempre van a la red

  // Páginas: primero la red (siempre lo último), y si no hay conexión, la copia guardada
  if (req.mode === 'navigate') {
    e.respondWith(fetch(req).then((res) => {
      const copy = res.clone(); caches.open(VERSION).then((c) => c.put('/index.html', copy)); return res;
    }).catch(() => caches.match('/index.html')));
    return;
  }

  // Todo lo demás: responde con lo guardado y se actualiza en segundo plano
  e.respondWith(caches.open(VERSION).then((cache) => cache.match(req).then((hit) => {
    const net = fetch(req).then((res) => { if (res && (res.ok || res.type === 'opaque')) cache.put(req, res.clone()); return res; }).catch(() => hit);
    return hit || net;
  })));
});
