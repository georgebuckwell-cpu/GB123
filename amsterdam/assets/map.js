/* ════════════════════════════════════════════════════════════════════════════
   ONTDEK AMSTERDAM — Locatiekaart
   Loads data.json, geocodes each business address in the browser (no API key),
   caches results in localStorage, and plots category-coloured, clustered pins.

   Geocoding: PDOK Locatieserver (Dutch national address service, CORS, free)
   with an OpenStreetMap Nominatim fallback. Map tiles: CARTO Voyager (OSM data).
   ════════════════════════════════════════════════════════════════════════════ */
(function () {
  'use strict';

  // category presentation — mirrors the directory's META (label comes from data.json)
  const META = {
    restaurant: { emoji: '🍽️', accent: '#e1562f' },
    cafe:       { emoji: '☕', accent: '#b5742f' },
    bar:        { emoji: '🍺', accent: '#c4452f' },
    bakkerij:   { emoji: '🥐', accent: '#caa24a' },
    grooming:   { emoji: '💈', accent: '#3b6ea5' },
    fiets:      { emoji: '🚲', accent: '#1f9d6b' },
    coffeeshop: { emoji: '🌿', accent: '#2f8f4e' },
    vervoer:    { emoji: '🚊', accent: '#7a6cc4' },
    overig:     { emoji: '🏬', accent: '#6b7079' }
  };
  const AMS = [52.3676, 4.9041];
  const CACHE_KEY = 'oa_geo_v2';

  const $ = s => document.querySelector(s);
  const esc = s => (s || '').replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));

  let DATA = { groups: {}, items: [] };
  let activeGroup = 'all';
  let query = '';
  let map, cluster;

  // persistent geocode cache: { "<street>": [lat,lng] | null }
  let cache = {};
  try { cache = JSON.parse(localStorage.getItem(CACHE_KEY) || '{}'); } catch (e) { cache = {}; }
  let cacheDirty = false;
  function saveCache() {
    if (!cacheDirty) return;
    try { localStorage.setItem(CACHE_KEY, JSON.stringify(cache)); cacheDirty = false; } catch (e) {}
  }
  setInterval(saveCache, 2500);
  addEventListener('beforeunload', saveCache);

  // small deterministic jitter (~a few metres) so businesses sharing a street
  // don't stack on a single pixel; keeps cluster counts meaningful.
  function jitter(str) {
    let h = 0; for (let i = 0; i < str.length; i++) h = (h * 31 + str.charCodeAt(i)) >>> 0;
    const a = (h % 1000) / 1000, b = ((h >> 10) % 1000) / 1000;
    return [(a - 0.5) * 0.00045, (b - 0.5) * 0.00045];
  }

  function icon(group) {
    const m = META[group] || META.overig;
    return L.divIcon({
      className: 'oa-pin',
      html: `<div class="oa-pin-dot" style="--c:${m.accent}"><span>${m.emoji}</span></div>`,
      iconSize: [30, 30], iconAnchor: [15, 30], popupAnchor: [0, -30]
    });
  }

  function popupHTML(it) {
    const grp = (DATA.groups[it.g] || {}).nl || it.c || 'Bedrijf';
    const tel = it.p ? it.p.replace(/\s+/g, '') : '';
    return `<div class="pop">
      <h3>${esc(it.n)}</h3>
      <div class="pop-cat">${esc(grp)}</div>
      ${it.s ? `<div class="pop-row"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/></svg><span>${esc(it.s)}</span></div>` : ''}
      ${it.p ? `<div class="pop-row"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.8 19.8 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.12 4.18 2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.91.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92Z"/></svg><span>${esc(it.p)}</span></div>` : ''}
      <div class="pop-actions">
        <a class="gm" href="${esc(it.u)}" target="_blank" rel="noopener">Google Maps</a>
        ${tel ? `<a class="tel" href="tel:${esc(tel)}">Bellen</a>` : ''}
      </div>
    </div>`;
  }

  // ── geocoders (browser-side, no key) ──────────────────────────────────────
  async function pdok(street) {
    const q = encodeURIComponent(street + ', Amsterdam');
    const url = `https://api.pdok.nl/bzk/locatieserver/search/v3_1/free?q=${q}&rows=1&fl=centroide_ll`;
    const r = await fetch(url);
    if (!r.ok) throw new Error('pdok ' + r.status);
    const j = await r.json();
    const d = j && j.response && j.response.docs && j.response.docs[0];
    const m = d && /POINT\(([-\d.]+)\s+([-\d.]+)\)/.exec(d.centroide_ll);
    return m ? [+m[2], +m[1]] : null;
  }
  async function nominatim(street) {
    const q = encodeURIComponent(street + ', Amsterdam, Netherlands');
    const url = `https://nominatim.openstreetmap.org/search?format=json&limit=1&q=${q}`;
    const r = await fetch(url, { headers: { 'Accept-Language': 'nl' } });
    if (!r.ok) throw new Error('nominatim ' + r.status);
    const j = await r.json();
    return (j && j[0]) ? [+j[0].lat, +j[0].lon] : null;
  }
  async function geocode(street) {
    try { return await pdok(street); }
    catch (e) {
      try { return await nominatim(street); }
      catch (e2) { throw e2; }
    }
  }

  // ── pipeline ──────────────────────────────────────────────────────────────
  const geoText = $('#geoText'), geoBar = $('#geoBar');
  let placed = 0, totalGeo = 0, networkOff = false;

  function setProgress() {
    const pct = totalGeo ? Math.round(placed / totalGeo * 100) : 100;
    if (geoBar) geoBar.style.width = pct + '%';
    if (placed >= totalGeo) {
      geoText.innerHTML = `<span class="done">✓ ${placed.toLocaleString('nl-NL')} bedrijven op de kaart</span>`;
      setTimeout(() => { const s = $('#geoStatus'); if (s) s.style.opacity = '.65'; }, 1500);
    } else {
      geoText.textContent = `Locaties laden… ${placed.toLocaleString('nl-NL')} / ${totalGeo.toLocaleString('nl-NL')}`;
    }
  }

  function place(it, ll) {
    const [dy, dx] = jitter(it.n + it.s);
    it._ll = [ll[0] + dy, ll[1] + dx];
    const mk = L.marker(it._ll, { icon: icon(it.g) });
    mk.bindPopup(popupHTML(it), { minWidth: 210 });
    mk.on('click', () => highlightList(it));
    it._marker = mk;
    if (visible(it)) cluster.addLayer(mk);
    placed++;
    setProgress();
  }

  function placeStreet(street, ll) {
    // place every business on this street (or count failures so progress completes)
    DATA.items.forEach(it => {
      if (it.s !== street || it._marker) return;
      if (ll) place(it, ll); else placed++;
    });
    setProgress();
  }

  async function run() {
    totalGeo = DATA.items.filter(it => it.s).length;

    // group businesses by unique street → geocode each street once
    const streets = [...new Set(DATA.items.filter(it => it.s).map(it => it.s))];

    // 1) instant placement from cache; queue the unknowns
    const pending = [];
    streets.forEach(st => {
      const c = cache[st];
      if (c === undefined) pending.push(st);
      else placeStreet(st, c);           // cached coords, or null (known failure)
    });
    refreshList();

    // 2) geocode the rest with a small, polite concurrency pool
    let i = 0;
    const POOL = 8;
    async function worker() {
      while (i < pending.length && !networkOff) {
        const st = pending[i++];
        let ll = null, failed = false;
        try { ll = await geocode(st); }
        catch (e) { failed = true; }
        if (failed) {                     // network unreachable → stop hammering
          networkOff = true;
          geoText.textContent = `${placed.toLocaleString('nl-NL')} geplaatst · netwerk niet bereikbaar`;
          break;
        }
        cache[st] = ll; cacheDirty = true;
        placeStreet(st, ll);
        if (i % 20 === 0) refreshList();
      }
    }
    await Promise.all(Array.from({ length: POOL }, worker));
    saveCache();
    refreshList();
  }

  // ── filtering / list ───────────────────────────────────────────────────────
  function visible(it) {
    if (activeGroup !== 'all' && it.g !== activeGroup) return false;
    if (query) {
      const q = query.toLowerCase();
      if (!(it.n.toLowerCase().includes(q) || (it.s || '').toLowerCase().includes(q) || (it.c || '').toLowerCase().includes(q))) return false;
    }
    return true;
  }

  function applyFilters() {
    cluster.clearLayers();
    const layers = [];
    DATA.items.forEach(it => { if (it._marker && visible(it)) layers.push(it._marker); });
    cluster.addLayers(layers);
    refreshList();
  }

  const listBody = $('#listBody'), listHead = $('#listHead');
  let activeRow = null;
  function refreshList() {
    const matches = DATA.items.filter(visible);
    const onMap = matches.filter(it => it._marker).length;
    listHead.innerHTML = `<b>${matches.length.toLocaleString('nl-NL')}</b> ${matches.length === 1 ? 'bedrijf' : 'bedrijven'}` +
      (onMap < matches.length ? ` · ${onMap.toLocaleString('nl-NL')} op de kaart` : '');

    if (!matches.length) { listBody.innerHTML = `<div class="empty">Geen bedrijven gevonden. Probeer een andere zoekterm of categorie.</div>`; return; }

    // cap the rendered rows for performance; map still shows everything
    const CAP = 300;
    const rows = matches.slice(0, CAP).map(it => {
      const m = META[it.g] || META.overig;
      const grp = (DATA.groups[it.g] || {}).nl || it.c || '';
      return `<div class="mli" data-id="${it._id}">
        <div class="dot" style="--c:${m.accent}">${m.emoji}</div>
        <div class="mli-b">
          <h4>${esc(it.n)}</h4>
          <span class="cat">${esc(grp)}</span>
          ${it.s ? `<div class="addr">${esc(it.s)}</div>` : ''}
        </div>
      </div>`;
    }).join('');
    listBody.innerHTML = rows + (matches.length > CAP ? `<div class="empty">+ ${(matches.length - CAP).toLocaleString('nl-NL')} meer — verfijn met zoeken of een filter.</div>` : '');
  }

  function highlightList(it) {
    if (activeRow) activeRow.classList.remove('active');
    const row = listBody.querySelector(`.mli[data-id="${it._id}"]`);
    if (row) { row.classList.add('active'); activeRow = row; row.scrollIntoView({ block: 'nearest' }); }
  }

  listBody.addEventListener('click', e => {
    const row = e.target.closest('.mli'); if (!row) return;
    const it = DATA.items[+row.dataset.id];
    if (!it) return;
    if (it._marker && it._ll) {
      if (activeRow) activeRow.classList.remove('active');
      row.classList.add('active'); activeRow = row;
      map.flyTo(it._ll, Math.max(map.getZoom(), 16), { duration: .6 });
      cluster.zoomToShowLayer(it._marker, () => it._marker.openPopup());
    }
  });

  // ── chips ───────────────────────────────────────────────────────────────
  function buildChips() {
    const counts = {};
    DATA.items.forEach(it => { counts[it.g] = (counts[it.g] || 0) + 1; });
    const el = $('#mapChips');
    let html = `<button class="map-chip active" data-g="all">Alles <span class="n">${DATA.items.length}</span></button>`;
    Object.keys(DATA.groups).forEach(g => {
      if (!counts[g]) return;
      const m = META[g] || META.overig;
      html += `<button class="map-chip" data-g="${g}"><span class="swatch" style="--c:${m.accent}"></span>${esc(DATA.groups[g].nl)} <span class="n">${counts[g]}</span></button>`;
    });
    el.innerHTML = html;
    el.querySelectorAll('.map-chip').forEach(ch => ch.addEventListener('click', () => {
      el.querySelectorAll('.map-chip').forEach(c => c.classList.remove('active'));
      ch.classList.add('active');
      activeGroup = ch.dataset.g;
      applyFilters();
    }));
  }

  // ── init ────────────────────────────────────────────────────────────────
  function initMap() {
    map = L.map('map', { center: AMS, zoom: 12, scrollWheelZoom: true, preferCanvas: true });
    L.tileLayer('https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png', {
      maxZoom: 19, subdomains: 'abcd',
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> &copy; <a href="https://carto.com/attributions">CARTO</a> · Adressen via <a href="https://www.pdok.nl">PDOK</a>'
    }).addTo(map);
    cluster = L.markerClusterGroup({ maxClusterRadius: 50, chunkedLoading: true, showCoverageOnHover: false });
    map.addLayer(cluster);
  }

  function wire() {
    const s = $('#mapSearch');
    let t;
    s.addEventListener('input', e => { query = e.target.value.trim(); clearTimeout(t); t = setTimeout(applyFilters, 200); });
    addEventListener('scroll', () => { const p = $('#progress'); if (p) p.style.width = (scrollY / Math.max(1, document.body.scrollHeight - innerHeight) * 100) + '%'; }, { passive: true });
  }

  initMap();
  wire();

  fetch('assets/data.json').then(r => r.json()).then(d => {
    DATA = d;
    DATA.items.forEach((it, idx) => { it._id = idx; });
    buildChips();
    refreshList();
    run();
  }).catch(() => {
    geoText.textContent = 'Kon de bedrijfsgegevens niet laden — ververs de pagina.';
    listBody.innerHTML = `<div class="empty">⚠️ Gegevens niet beschikbaar.</div>`;
  });
})();
