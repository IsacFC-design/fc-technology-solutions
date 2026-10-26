# FC Technology Solutions

Portafolio y sitio de negocio de Isac David Fuentes Calixto: páginas web, apps PWA y sistemas a medida.
Sitio estático (sin build en Vercel): la raíz de este repositorio es lo que se publica.

## Publicar
1. Sube TODO este contenido a un repositorio de GitHub (nombre sugerido: `fc-technology-solutions`).
2. En vercel.com/new importa el repositorio. Framework: **Other**. Build Command y Output Directory vacíos.
3. Nombre del proyecto: `fc-technology-solutions` → https://fc-technology-solutions.vercel.app

`.vercelignore` evita que Vercel publique la carpeta `fuente/` y este README.

## Contacto en Supabase (opcional)
Ejecuta `supabase-leads.sql` en Supabase > SQL Editor y pega la URL y la clave *anon* en `fuente/template.html`
(bloque `SUPABASE = { url: '', anonKey: '' }`), luego regenera el sitio.

## Seguir editando
Todo el contenido (textos, precios, proyectos, caso Barnard, paquetes, FAQ, juego) está en `fuente/template.html`.
Con Python 3 (y Pillow: `pip install pillow`), desde la raíz del proyecto:

    python fuente/build.py          # arma fuente/portafolio-vista-previa.html
    python fuente/make_deploy.py    # regenera index.html, img/, sw.js, vercel.json, manifest, robots y sitemap

Si tu proyecto de Vercel tiene otro nombre, cambia `URL` al inicio de `fuente/make_deploy.py`.
Después sube los cambios a GitHub y Vercel publica solo.

## Pendientes de contenido (hoy son ejemplos)
Tarifas reales, condiciones de pago y soporte, resultados reales de Barnard, un testimonio real, URL y clave de Supabase.

## Cronjob "keep-alive"
`.github/workflows/keep-alive.yml` corre cada día en GitHub Actions: visita el sitio y, si existe, consulta Supabase
para que el plan gratuito no se pause. Para activar la parte de Supabase: ejecuta de nuevo `supabase-leads.sql`
(crea la función `ping`) y en GitHub > Settings > Secrets and variables > Actions crea los secrets
`SUPABASE_URL` y `SUPABASE_ANON_KEY`. Nota: GitHub desactiva los cron de repos sin actividad por 60 días; si pasa, pulsa "Enable workflow" en la pestaña Actions.
