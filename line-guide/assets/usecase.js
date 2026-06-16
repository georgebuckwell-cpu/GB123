/* ============================================================================
   LINE GUIDE — Use-case renderer
   Powers BOTH the index (#ucGrid) and the dynamic landing (#usecase?u=slug).
   Pulls related verified suppliers from the shared LG_SUPPLIERS dataset and
   hands every CTA into the brief builder / directory funnel.
   NOTE: injected markup avoids .reveal (observer runs before this) so all
   content renders visible; for production these should be pre-rendered to
   static HTML from this same data for full SEO.
   ========================================================================== */
(function () {
  'use strict';
  const $ = (s, c = document) => c.querySelector(s);
  const $$ = (s, c = document) => Array.from(c.querySelectorAll(s));
  const UC = window.LG_USECASES || [];
  const CASE_LABEL = { packing:'Packing', palletising:'Palletising', 'end-of-line':'End-of-line', filling:'Filling', inspection:'Inspection', manual:'Manual process' };

  const stars = (r) => {
    const f = Math.round(r); let o = '<span class="stars">';
    for (let i = 1; i <= 5; i++) o += `<svg width="12" height="12" viewBox="0 0 24 24" fill="${i <= f ? 'currentColor' : 'none'}" stroke="currentColor" stroke-width="1.5"><path d="M12 2l3 6.5 7 .9-5 4.9 1.2 7L12 18l-6.4 3.3L7 14.3 2 9.4l7-.9z"/></svg>`;
    return o + '</span>';
  };
  const arrow = '<svg class="arr" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M12 5l7 7-7 7"/></svg>';
  const check = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>';

  /* ── INDEX GRID ─────────────────────────────────────────────────────────── */
  const grid = $('#ucGrid');
  if (grid) {
    grid.innerHTML = UC.map((u, i) => `
      <a class="case" href="use-case-${u.slug}.html" style="animation:wzIn .4s var(--ease-out) ${Math.min(i*60,360)}ms both;text-decoration:none">
        <span class="case-tag">${u.facts.budget}</span>
        <div class="case-ico"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">${u.icon}</svg></div>
        <h4>${u.name}</h4>
        <p>${u.intro}</p>
        <div class="sup-foot" style="margin-top:1.1rem"><span class="mono-note">${u.facts.timeframe} · ${u.facts.lead}</span><span class="link" style="color:var(--green);font-weight:600;font-size:.84rem">Explore ${arrow}</span></div>
      </a>`).join('');
    return;
  }

  /* ── SINGLE LANDING ─────────────────────────────────────────────────────── */
  const root = $('#usecase');
  if (!root) return;
  const slug = new URLSearchParams(location.search).get('u');
  const u = UC.find(x => x.slug === slug) || UC[0];

  document.title = u.metaTitle;
  const md = $('meta[name="description"]'); if (md) md.setAttribute('content', u.metaDesc);

  const related = (window.LG_SUPPLIERS || [])
    .filter(s => s.cases.includes(u.case))
    .sort((a, b) => b.rating - a.rating).slice(0, 3);

  const relCards = related.map(s => `
    <article class="sup-card">
      <div class="sup-card-head">
        <div class="sup-logo">${s.monogram}</div>
        <div class="sup-id"><div class="sup-name">${s.name}</div><div class="sup-loc">${s.location}</div></div>
      </div>
      <div class="sup-rate">${stars(s.rating)} <b>${s.rating}</b> <span class="tier-pill ${s.tier==='Ultra'?'ultra':''}" style="margin-left:auto">${s.tier}</span></div>
      <p class="sup-blurb">${s.blurb}</p>
      <div class="sup-foot"><span></span><a class="link" href="supplier.html?s=${s.slug}">View profile ${arrow}</a></div>
    </article>`).join('');

  const relCases = u.related.map(rc => {
    const x = UC.find(y => y.case === rc); if (!x) return '';
    return `<a class="chip" href="use-case-${x.slug}.html" style="text-decoration:none">${x.name}</a>`;
  }).join('');

  root.innerHTML = `
    <a href="use-cases.html" class="wz-back" style="opacity:1;margin-bottom:1.6rem"><svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 12H5M12 19l-7-7 7-7"/></svg> All applications</a>

    <div style="max-width:720px;animation:wzIn .5s var(--ease-out) both">
      <div class="eyebrow">${u.eyebrow}</div>
      <h1 class="h-xl" style="font-size:clamp(2.2rem,5vw,3.4rem);margin-bottom:1.1rem">${u.h1.replace(/(\b\w+\b)$/, '<span class="gt">$1</span>')}</h1>
      <p class="lede" style="margin-bottom:1.8rem">${u.intro}</p>
      <div class="hero-actions" style="justify-content:flex-start;margin-bottom:0">
        <a href="brief.html" class="btn btn-primary btn-lg">Find suppliers for this ${arrow}</a>
        <a href="suppliers.html?case=${u.case}" class="btn btn-ghost btn-lg">Browse the directory</a>
      </div>
    </div>

    <div class="prof-stats" style="margin-top:3rem">
      <div class="pstat"><div class="n">${u.facts.budget}</div><div class="l">Typical budget</div></div>
      <div class="pstat"><div class="n">${u.facts.timeframe}</div><div class="l">Typical timeframe</div></div>
      <div class="pstat"><div class="n">${u.facts.throughput}</div><div class="l">Throughput</div></div>
      <div class="pstat"><div class="n">${u.facts.lead}</div><div class="l">Lead time</div></div>
    </div>

    <div class="prof-grid">
      <div>
        <div class="prof-block">
          <h3><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="12" cy="12" r="10"/><path d="M12 16v-4M12 8h.01"/></svg> The challenge</h3>
          <p>${u.challenge}</p>
        </div>
        <div class="prof-block">
          <h3><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M20 6L9 17l-5-5"/></svg> What to look for</h3>
          <ul>${u.lookFor.map(l => `<li style="display:flex;gap:11px;padding:.5rem 0;font-size:.92rem;color:var(--sub)"><span style="color:var(--green);flex-shrink:0;margin-top:2px">${check}</span>${l}</li>`).join('')}</ul>
        </div>
        <div class="prof-block" style="margin-bottom:0">
          <h3><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg> Questions to ask suppliers</h3>
          ${u.questions.map((q, i) => `<div class="cs-card"><div class="result"><span style="font-family:var(--font-display);font-weight:700;color:var(--green)">${String(i+1).padStart(2,'0')}</span> ${q}</div></div>`).join('')}
        </div>
      </div>

      <aside>
        <div class="prof-side">
          <h4>Top-rated for ${CASE_LABEL[u.case]}</h4>
          <div style="display:flex;flex-direction:column;gap:.7rem;margin-bottom:1rem">${relCards}</div>
          <a href="brief.html" class="btn btn-primary btn-block">Get my top 3 ${arrow}</a>
          <p class="mono-note" style="text-align:center;margin-top:.9rem">// free for buyers · 60-second brief</p>
        </div>
      </aside>
    </div>

    <div class="prof-block" style="margin-top:3rem">
      <h3><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M12 5v14M5 12h14"/></svg> Frequently asked</h3>
      <div class="faq" style="margin:0;max-width:none">
        ${u.faqs.map(f => `<div class="faq-item"><button class="faq-q">${f.q}<span class="ico"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4"><path d="M12 5v14M5 12h14"/></svg></span></button><div class="faq-a"><p>${f.a}</p></div></div>`).join('')}
      </div>
    </div>

    <div style="margin-top:3rem">
      <div class="mono-note" style="margin-bottom:.8rem">// related applications</div>
      <div class="wz-chips">${relCases}</div>
    </div>`;

  // wire FAQ accordion (app.js bound before this injected markup existed)
  $$('#usecase .faq-item').forEach(item => {
    const q = $('.faq-q', item), a = $('.faq-a', item);
    q.addEventListener('click', () => {
      const open = item.classList.contains('open');
      $$('#usecase .faq-item').forEach(i => { i.classList.remove('open'); $('.faq-a', i).style.maxHeight = null; });
      if (!open) { item.classList.add('open'); a.style.maxHeight = a.scrollHeight + 'px'; }
    });
  });
})();
