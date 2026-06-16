/* ════════════════════════════════════════════════════════════════════════════
   ONTDEK AMSTERDAM — directory logic (NL)
   Loads data.json, renders a searchable / filterable / paginated directory.
   Industry photography via LoremFlickr CDN with a styled fallback per category.
   ════════════════════════════════════════════════════════════════════════════ */
(function () {
  'use strict';

  // Per-group presentation metadata: Dutch label, emoji, image keyword
  const META = {
    restaurant: { emoji: '🍽️', kw: 'restaurant,food', accent: '#e1562f' },
    cafe:       { emoji: '☕', kw: 'cafe,coffee', accent: '#b5742f' },
    bar:        { emoji: '🍺', kw: 'bar,pub', accent: '#c4452f' },
    bakkerij:   { emoji: '🥐', kw: 'bakery,pastry', accent: '#caa24a' },
    grooming:   { emoji: '💈', kw: 'barbershop,hairsalon', accent: '#3b6ea5' },
    fiets:      { emoji: '🚲', kw: 'bicycle,amsterdam', accent: '#1f9d6b' },
    coffeeshop: { emoji: '🌿', kw: 'cannabis,plant', accent: '#2f8f4e' },
    vervoer:    { emoji: '🚊', kw: 'tram,amsterdam', accent: '#7a6cc4' },
    overig:     { emoji: '🏬', kw: 'shop,store', accent: '#6b7079' }
  };
  const FLICKR = (kw, seed, w, h) =>
    `https://loremflickr.com/${w}/${h}/${encodeURIComponent(kw)}/all?lock=${seed}`;

  const PAGE = 24;
  let DATA = { groups: {}, items: [] };
  let filtered = [];
  let shown = 0;
  let activeGroup = 'all';
  let query = '';
  let sort = 'relevant';

  const $ = s => document.querySelector(s);
  const grid = $('#bizGrid');
  const countEl = $('#resultCount');
  const chipsEl = $('#chips');
  const loadWrap = $('#loadWrap');

  // small deterministic hash for stable image seeds per business
  function seed(str) {
    let h = 0;
    for (let i = 0; i < str.length; i++) h = (h * 31 + str.charCodeAt(i)) >>> 0;
    return h % 1000;
  }
  const esc = s => (s || '').replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));

  function applyFilters() {
    const q = query.trim().toLowerCase();
    filtered = DATA.items.filter(it => {
      if (activeGroup !== 'all' && it.g !== activeGroup) return false;
      if (q && !(it.n.toLowerCase().includes(q) || (it.s || '').toLowerCase().includes(q) || (it.c || '').toLowerCase().includes(q))) return false;
      return true;
    });
    if (sort === 'az') filtered.sort((a, b) => a.n.localeCompare(b.n, 'nl'));
    else if (sort === 'za') filtered.sort((a, b) => b.n.localeCompare(a.n, 'nl'));
    else if (sort === 'phone') filtered.sort((a, b) => (b.p ? 1 : 0) - (a.p ? 1 : 0));
    shown = 0;
    grid.innerHTML = '';
    renderMore();
    countEl.innerHTML = `<b>${filtered.length.toLocaleString('nl-NL')}</b> ${filtered.length === 1 ? 'bedrijf' : 'bedrijven'} gevonden`;
    if (!filtered.length) {
      grid.innerHTML = `<div class="empty" style="grid-column:1/-1"><div class="em">🔍</div><h3>Geen resultaten</h3><p>Probeer een andere zoekterm of categorie.</p></div>`;
    }
  }

  function cardHTML(it) {
    const m = META[it.g] || META.overig;
    const grp = (DATA.groups[it.g] || {}).nl || 'Bedrijf';
    const img = FLICKR(m.kw, seed(it.n), 600, 380);
    const tel = it.p ? it.p.replace(/\s+/g, '') : '';
    return `<article class="biz reveal">
      <div class="biz-thumb" style="background:${m.accent}1a">
        <span class="biz-badge">${esc(grp)}</span>
        <img loading="lazy" src="${img}" alt="${esc(it.n)}"
             onerror="this.replaceWith(Object.assign(document.createElement('div'),{className:'ph',textContent:'${m.emoji}'}))">
      </div>
      <div class="biz-body">
        <h3>${esc(it.n)}</h3>
        ${it.s ? `<div class="biz-row"><svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/></svg><span>${esc(it.s)}</span></div>` : ''}
        ${it.p ? `<div class="biz-row"><svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.8 19.8 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.12 4.18 2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.91.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92Z"/></svg><span>${esc(it.p)}</span></div>` : `<div class="biz-row" style="color:var(--line-2)"><span>Geen telefoonnummer bekend</span></div>`}
        <div class="biz-actions">
          <a class="btn btn-dark" href="${esc(it.u)}" target="_blank" rel="noopener">Op de kaart</a>
          ${tel ? `<a class="btn btn-ghost" href="tel:${esc(tel)}">Bellen</a>` : `<span class="btn btn-ghost" aria-disabled="true" style="opacity:.4;pointer-events:none">Bellen</span>`}
        </div>
      </div>
    </article>`;
  }

  function renderMore() {
    const slice = filtered.slice(shown, shown + PAGE);
    const frag = document.createElement('div');
    frag.innerHTML = slice.map(cardHTML).join('');
    const cards = [...frag.children];
    cards.forEach(c => grid.appendChild(c));
    requestAnimationFrame(() => cards.forEach(c => c.classList.add('in')));
    shown += slice.length;
    loadWrap.style.display = shown < filtered.length ? 'flex' : 'none';
    const btn = $('#loadBtn');
    if (btn) btn.textContent = `Meer laden (${(filtered.length - shown).toLocaleString('nl-NL')} resterend)`;
  }

  function buildChips() {
    const counts = {};
    DATA.items.forEach(it => { counts[it.g] = (counts[it.g] || 0) + 1; });
    let html = `<button class="chip active" data-g="all">Alles <span class="n">${DATA.items.length}</span></button>`;
    Object.keys(DATA.groups).forEach(g => {
      if (!counts[g]) return;
      html += `<button class="chip" data-g="${g}">${(META[g] || {}).emoji || ''} ${esc(DATA.groups[g].nl)} <span class="n">${counts[g]}</span></button>`;
    });
    chipsEl.innerHTML = html;
    chipsEl.querySelectorAll('.chip').forEach(ch => ch.addEventListener('click', () => {
      chipsEl.querySelectorAll('.chip').forEach(c => c.classList.remove('active'));
      ch.classList.add('active');
      activeGroup = ch.dataset.g;
      applyFilters();
      document.getElementById('gids').scrollIntoView({ behavior: 'smooth', block: 'start' });
    }));
  }

  function buildCategoryTiles() {
    const counts = {};
    DATA.items.forEach(it => { counts[it.g] = (counts[it.g] || 0) + 1; });
    const el = $('#catGrid');
    if (!el) return;
    el.innerHTML = Object.keys(DATA.groups).filter(g => counts[g]).map(g => {
      const m = META[g] || META.overig;
      return `<a class="cat-tile reveal" data-g="${g}" href="#gids">
        <img loading="lazy" src="${FLICKR(m.kw, 7, 500, 400)}" alt="${esc(DATA.groups[g].nl)}"
             onerror="this.replaceWith(Object.assign(document.createElement('div'),{className:'ph',style:'background:${m.accent};display:flex;align-items:center;justify-content:center;font-size:3rem',textContent:'${m.emoji}'}))">
        <div class="meta"><div class="emoji">${m.emoji}</div><h3>${esc(DATA.groups[g].nl)}</h3><span>${counts[g]} bedrijven</span></div>
      </a>`;
    }).join('');
    el.querySelectorAll('.cat-tile').forEach(t => t.addEventListener('click', () => {
      activeGroup = t.dataset.g;
      chipsEl.querySelectorAll('.chip').forEach(c => c.classList.toggle('active', c.dataset.g === activeGroup));
      applyFilters();
    }));
  }

  // ── wiring ──────────────────────────────────────────────────────────────
  function wire() {
    const heroInput = $('#heroSearch');
    const miniInput = $('#miniSearch');
    const sync = v => { query = v; if (heroInput) heroInput.value = v; if (miniInput) miniInput.value = v; applyFilters(); };
    if (heroInput) heroInput.addEventListener('input', e => sync(e.target.value));
    if (miniInput) miniInput.addEventListener('input', e => sync(e.target.value));
    const heroBtn = $('#heroBtn');
    if (heroBtn) heroBtn.addEventListener('click', () => document.getElementById('gids').scrollIntoView({ behavior: 'smooth' }));
    const sortSel = $('#sortSel');
    if (sortSel) sortSel.addEventListener('change', e => { sort = e.target.value; applyFilters(); });
    $('#loadBtn').addEventListener('click', renderMore);
  }

  // nav scroll + progress
  addEventListener('scroll', () => {
    const nav = $('#nav'); if (nav) nav.classList.toggle('scrolled', scrollY > 30);
    const p = $('#progress'); if (p) p.style.width = (scrollY / (document.body.scrollHeight - innerHeight) * 100) + '%';
  }, { passive: true });

  // reveal observer for static blocks
  const ro = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { e.target.classList.add('in'); ro.unobserve(e.target); } }), { threshold: .12 });

  fetch('assets/data.json').then(r => r.json()).then(d => {
    DATA = d;
    // hero stats
    $('#statBiz').textContent = d.items.length.toLocaleString('nl-NL');
    $('#statCat').textContent = Object.keys(d.groups).filter(g => d.items.some(i => i.g === g)).length;
    $('#statTel').textContent = d.items.filter(i => i.p).length.toLocaleString('nl-NL');
    buildChips();
    buildCategoryTiles();
    applyFilters();
    wire();
    document.querySelectorAll('.reveal').forEach(el => ro.observe(el));
  }).catch(() => {
    grid.innerHTML = `<div class="empty" style="grid-column:1/-1"><div class="em">⚠️</div><h3>Kon gegevens niet laden</h3><p>Ververs de pagina om het opnieuw te proberen.</p></div>`;
  });
})();
