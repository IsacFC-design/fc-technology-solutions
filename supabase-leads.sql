-- FC Technology Solutions: tabla de contactos (leads)
-- Ejecuta este archivo en Supabase > SQL Editor.

create table if not exists public.leads (
  id          bigint generated always as identity primary key,
  created_at  timestamptz not null default now(),
  source      text,          -- 'cotizador' o 'contacto'
  name        text,
  business    text,
  contact     text,          -- WhatsApp o correo que dejó el cliente
  project     text,
  modules     text,
  users       text,
  speed       text,
  price_min   integer,
  price_max   integer,
  weeks_min   integer,
  weeks_max   integer,
  details     text,
  message     text,
  status      text not null default 'nuevo'   -- nuevo, contactado, cotizado, ganado, perdido
);

alter table public.leads enable row level security;

-- La página (clave anon) solo puede INSERTAR. Nadie puede leer, editar ni borrar la tabla desde la web.
drop policy if exists "anon puede insertar leads" on public.leads;
create policy "anon puede insertar leads"
  on public.leads for insert
  to anon
  with check (
    status = 'nuevo'
    and source in ('cotizador', 'contacto')
    and char_length(coalesce(name, ''))     <= 120
    and char_length(coalesce(business, '')) <= 160
    and char_length(coalesce(contact, ''))  <= 160
    and char_length(coalesce(project, ''))  <= 160
    and char_length(coalesce(modules, ''))  <= 600
    and char_length(coalesce(users, ''))    <= 120
    and char_length(coalesce(speed, ''))    <= 120
    and char_length(coalesce(details, ''))  <= 4000
    and char_length(coalesce(message, ''))  <= 4000
    and coalesce(price_min, 0) between 0 and 1000000
    and coalesce(price_max, 0) between 0 and 1000000
    and coalesce(weeks_min, 0) between 0 and 520
    and coalesce(weeks_max, 0) between 0 and 520
  );

-- Quitar permisos que no se necesitan: la clave anon NO debe leer, editar ni borrar.
revoke all on public.leads from anon;
grant insert on public.leads to anon;
revoke all on public.leads from authenticated;

-- Freno básico contra spam: máximo 30 contactos por minuto en total.
create or replace function public.leads_rate_limit() returns trigger
language plpgsql security definer set search_path = public as $$
begin
  if (select count(*) from public.leads where created_at > now() - interval '1 minute') >= 30 then
    raise exception 'demasiados envíos, intenta en un minuto';
  end if;
  return new;
end $$;
drop trigger if exists leads_rate_limit on public.leads;
create trigger leads_rate_limit before insert on public.leads
  for each row execute function public.leads_rate_limit();

-- Tú ves los contactos en Supabase > Table Editor (el panel usa otro rol y no depende de esta política).

-- Función mínima para el cronjob "keep-alive" (GitHub Actions): ejecuta una consulta real
-- y así Supabase (plan gratis) no pausa el proyecto por inactividad. No lee ni expone datos.
create or replace function public.ping() returns text
language sql stable as $$ select 'ok'::text $$;
revoke all on function public.ping() from public;
grant execute on function public.ping() to anon;
