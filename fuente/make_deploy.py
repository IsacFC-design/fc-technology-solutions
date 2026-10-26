import json
URL='https://fc-technology-solutions.vercel.app'   # cambia aquí si tu proyecto de Vercel tiene otro nombre
import os
HERE=os.path.dirname(os.path.abspath(__file__))
D=os.path.dirname(HERE)+'/'   # raíz del proyecto (lo que se publica)
new=open(HERE+'/portafolio-vista-previa.html',encoding='utf8').read()
body=new[new.index('<title>'):]
body=body.replace('<meta name="claude:viewport-fit-sides" content="cover">\n','')
head=f'''<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="description" content="Desarrollo de páginas web, apps PWA y sistemas a medida para negocios y colegios en Perú. Cotiza en un minuto y escribe por WhatsApp.">
<meta name="theme-color" content="#040705">
<link rel="canonical" href="{URL}/">
<link rel="alternate" hreflang="es" href="{URL}/">
<link rel="alternate" hreflang="en" href="{URL}/?lang=en">
<link rel="alternate" hreflang="x-default" href="{URL}/">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32.png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/manifest.webmanifest">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="FC Tech">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta property="og:type" content="website">
<meta property="og:locale" content="es_PE">
<meta property="og:site_name" content="FC Technology Solutions">
<meta property="og:title" content="FC Technology Solutions · Webs, apps y sistemas a medida">
<meta property="og:description" content="Convierto hojas de Excel y procesos manuales en sistemas que tu equipo usa todos los días. Cotiza en línea.">
<meta property="og:url" content="{URL}/">
<meta property="og:image" content="{URL}/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="FC Technology Solutions: webs, apps y sistemas que trabajan por tu negocio">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="FC Technology Solutions · Webs, apps y sistemas a medida">
<meta name="twitter:description" content="Convierto hojas de Excel y procesos manuales en sistemas que tu equipo usa todos los días.">
<meta name="twitter:image" content="{URL}/og-image.png">
<script type="application/ld+json">{json.dumps({"@context":"https://schema.org","@type":"ProfessionalService","name":"FC Technology Solutions","url":URL+"/","image":URL+"/og-image.png","telephone":"+51945872089","areaServed":"PE","founder":{"@type":"Person","name":"Isac David Fuentes Calixto"},"description":"Páginas web, apps PWA y sistemas a medida para negocios y colegios."},ensure_ascii=False)}</script>
'''
open(D+'index.html','w',encoding='utf8').write(head+body.rstrip()+('\n</body>\n</html>\n' if '</html>' not in body else '\n'))

# --- Imágenes: se sacan del HTML a /img/ (nombres con hash, se guardan en caché un año) ---
import re, hashlib, os, base64
os.makedirs(D+'img', exist_ok=True)
for f in os.listdir(D+'img'): os.remove(D+'img/'+f)
_h = open(D+'index.html', encoding='utf8').read()
def _ext(m):
    kind, b64 = m.group(1), m.group(2)
    if len(b64) < 1500: return m.group(0)
    raw = base64.b64decode(b64)
    ext = 'jpg' if kind == 'jpeg' else kind
    if kind == 'png':
        try:
            from PIL import Image; import io
            im = Image.open(io.BytesIO(raw)); out = io.BytesIO(); im.save(out, 'WEBP', quality=85, method=6)
            if out.tell() < len(raw) * 0.85: raw, ext = out.getvalue(), 'webp'
        except Exception: pass
    name = hashlib.sha1(raw).hexdigest()[:12] + '.' + ext
    open(D+'img/'+name, 'wb').write(raw)
    return '/img/' + name
_h2 = re.sub(r'data:image/(\w+);base64,([A-Za-z0-9+/=]+)', _ext, _h)
open(D+'index.html', 'w', encoding='utf8').write(_h2)
print('index.html', len(_h)//1024, 'KB ->', len(_h2)//1024, 'KB;', len(os.listdir(D+'img')), 'imágenes')
open(D+'robots.txt','w').write(f'User-agent: *\nAllow: /\n\nSitemap: {URL}/sitemap.xml\n')
open(D+'sitemap.xml','w').write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n  <url><loc>{URL}/</loc></url>\n</urlset>\n')
import time
MAN={"id":"/","name":"FC Technology Solutions","short_name":"FC Tech","description":"Webs, apps y sistemas a medida. Cotiza en línea y escribe por WhatsApp.","lang":"es","start_url":"/?source=pwa","scope":"/","display":"standalone","orientation":"portrait-primary","background_color":"#040705","theme_color":"#040705","categories":["business","productivity"],
 "icons":[{"src":"/icon-192.png","sizes":"192x192","type":"image/png","purpose":"any"},{"src":"/icon-512.png","sizes":"512x512","type":"image/png","purpose":"any"},{"src":"/icon-maskable-192.png","sizes":"192x192","type":"image/png","purpose":"maskable"},{"src":"/icon-maskable-512.png","sizes":"512x512","type":"image/png","purpose":"maskable"}],
 "shortcuts":[{"name":"Cotizar un proyecto","short_name":"Cotizar","url":"/?source=shortcut#cotizador","icons":[{"src":"/icon-192.png","sizes":"192x192"}]},{"name":"Ver proyectos","short_name":"Proyectos","url":"/?source=shortcut#proyectos","icons":[{"src":"/icon-192.png","sizes":"192x192"}]}]}
open(D+'manifest.webmanifest','w').write(json.dumps(MAN,indent=1,ensure_ascii=False))
SW="""/* Service worker de FC Technology Solutions. Cambia VERSION para forzar que se actualice el contenido guardado. */
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
"""
open(D+'sw.js','w').write(SW)
CSP = "; ".join([
 "default-src 'self'",
 "script-src 'self' 'unsafe-inline' https://cdnjs.cloudflare.com",
 "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com",
 "font-src 'self' data: https://fonts.gstatic.com",
 "img-src 'self' data: blob:",
 "connect-src 'self' https://*.supabase.co https://cdnjs.cloudflare.com https://fonts.googleapis.com https://fonts.gstatic.com",
 "worker-src 'self'", "manifest-src 'self'", "object-src 'none'",
 "base-uri 'self'", "form-action 'self'", "frame-ancestors 'none'", "upgrade-insecure-requests"])
H = lambda k, v: {"key": k, "value": v}
open(D+'vercel.json','w').write(json.dumps({"cleanUrls":True,"headers":[
 {"source":"/(.*)","headers":[
  H("Content-Security-Policy", CSP),
  H("Strict-Transport-Security", "max-age=63072000; includeSubDomains; preload"),
  H("X-Content-Type-Options", "nosniff"),
  H("Referrer-Policy", "strict-origin-when-cross-origin"),
  H("X-Frame-Options", "DENY"),
  H("Permissions-Policy", "camera=(), microphone=(), geolocation=(), payment=(), usb=(), interest-cohort=()"),
  H("Cross-Origin-Opener-Policy", "same-origin")]},
 {"source":"/sw.js","headers":[H("Cache-Control","no-cache")]},
 {"source":"/img/(.*)","headers":[H("Cache-Control","public, max-age=31536000, immutable")]},
 {"source":"/(.*)\\.(png|ico|webmanifest)","headers":[H("Cache-Control","public, max-age=86400")]},
 {"source":"/img/(.*)","headers":[H("Cache-Control","public, max-age=31536000, immutable")]}]},indent=1))
