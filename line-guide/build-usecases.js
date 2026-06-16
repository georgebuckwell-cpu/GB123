#!/usr/bin/env node
/* ============================================================================
   LINE GUIDE — Static pre-render for use-case landing pages
   Reads assets/usecases.js + assets/data.js and emits a fully static
   use-case-<slug>.html per application, with title/meta/body baked into the
   initial HTML payload for full SEO. Re-run after editing the content data:
       node build-usecases.js
   ========================================================================== */
const fs = require('fs');
const path = require('path');
const vm = require('vm');

const DIR = __dirname;
const ctx = { window: {} };
vm.createContext(ctx);
vm.runInContext(fs.readFileSync(path.join(DIR, 'assets/usecases.js'), 'utf8'), ctx);
vm.runInContext(fs.readFileSync(path.join(DIR, 'assets/data.js'), 'utf8'), ctx);
const UC = ctx.window.LG_USECASES || [];
const SUP = ctx.window.LG_SUPPLIERS || [];
const CASE_LABEL = { packing:'Packing', palletising:'Palletising', 'end-of-line':'End-of-line', filling:'Filling', inspection:'Inspection', manual:'Manual process' };

const esc = s => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
const arrow = '<svg class="arr" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M12 5l7 7-7 7"/></svg>';
const check = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>';
const stars = r => { const f = Math.round(r); let o = '<span class="stars">'; for (let i = 1; i <= 5; i++) o += `<svg width="12" height="12" viewBox="0 0 24 24" fill="${i<=f?'currentColor':'none'}" stroke="currentColor" stroke-width="1.5"><path d="M12 2l3 6.5 7 .9-5 4.9 1.2 7L12 18l-6.4 3.3L7 14.3 2 9.4l7-.9z"/></svg>`; return o + '</span>'; };

function inner(u) {
  const related = SUP.filter(s => s.cases.includes(u.case)).sort((a, b) => b.rating - a.rating).slice(0, 3);
  const relCards = related.map(s => `
        <article class="sup-card">
          <div class="sup-card-head"><div class="sup-logo">${s.monogram}</div><div class="sup-id"><div class="sup-name">${esc(s.name)}</div><div class="sup-loc">${esc(s.location)}</div></div></div>
          <div class="sup-rate">${stars(s.rating)} <b>${s.rating}</b> <span class="tier-pill ${s.tier==='Ultra'?'ultra':''}" style="margin-left:auto">${s.tier}</span></div>
          <p class="sup-blurb">${esc(s.blurb)}</p>
          <div class="sup-foot"><span></span><a class="link" href="supplier.html?s=${s.slug}">View profile ${arrow}</a></div>
        </article>`).join('');
  const relCases = u.related.map(rc => { const x = UC.find(y => y.case === rc); return x ? `<a class="chip" href="use-case-${x.slug}.html" style="text-decoration:none">${esc(x.name)}</a>` : ''; }).join('');
  const h1 = esc(u.h1).replace(/(\b[\w-]+\b)(\.?)$/, '<span class="gt">$1$2</span>');

  return `
      <a href="use-cases.html" class="wz-back" style="opacity:1;margin-bottom:1.6rem"><svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 12H5M12 19l-7-7 7-7"/></svg> All applications</a>

      <div style="max-width:720px">
        <div class="eyebrow">${esc(u.eyebrow)}</div>
        <h1 class="h-xl" style="font-size:clamp(2.2rem,5vw,3.4rem);margin-bottom:1.1rem">${h1}</h1>
        <p class="lede" style="margin-bottom:1.8rem">${esc(u.intro)}</p>
        <div class="hero-actions" style="justify-content:flex-start;margin-bottom:0">
          <a href="brief.html" class="btn btn-primary btn-lg">Find suppliers for this ${arrow}</a>
          <a href="suppliers.html?case=${u.case}" class="btn btn-ghost btn-lg">Browse the directory</a>
        </div>
      </div>

      <div class="prof-stats" style="margin-top:3rem">
        <div class="pstat"><div class="n">${esc(u.facts.budget)}</div><div class="l">Typical budget</div></div>
        <div class="pstat"><div class="n">${esc(u.facts.timeframe)}</div><div class="l">Typical timeframe</div></div>
        <div class="pstat"><div class="n">${esc(u.facts.throughput)}</div><div class="l">Throughput</div></div>
        <div class="pstat"><div class="n">${esc(u.facts.lead)}</div><div class="l">Lead time</div></div>
      </div>

      <div class="prof-grid">
        <div>
          <div class="prof-block">
            <h3><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="12" cy="12" r="10"/><path d="M12 16v-4M12 8h.01"/></svg> The challenge</h3>
            <p>${esc(u.challenge)}</p>
          </div>
          <div class="prof-block">
            <h3><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M20 6L9 17l-5-5"/></svg> What to look for</h3>
            <ul>${u.lookFor.map(l => `<li style="display:flex;gap:11px;padding:.5rem 0;font-size:.92rem;color:var(--sub)"><span style="color:var(--green);flex-shrink:0;margin-top:2px">${check}</span>${esc(l)}</li>`).join('')}</ul>
          </div>
          <div class="prof-block" style="margin-bottom:0">
            <h3><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg> Questions to ask suppliers</h3>
            ${u.questions.map((q, i) => `<div class="cs-card"><div class="result"><span style="font-family:var(--font-display);font-weight:700;color:var(--green)">${String(i+1).padStart(2,'0')}</span> ${esc(q)}</div></div>`).join('')}
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
          ${u.faqs.map(f => `<div class="faq-item"><button class="faq-q">${esc(f.q)}<span class="ico"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4"><path d="M12 5v14M5 12h14"/></svg></span></button><div class="faq-a"><p>${esc(f.a)}</p></div></div>`).join('')}
        </div>
      </div>

      <div style="margin-top:3rem">
        <div class="mono-note" style="margin-bottom:.8rem">// related applications</div>
        <div class="wz-chips">${relCases}</div>
      </div>`;
}

function page(u) {
  return `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>${esc(u.metaTitle)}</title>
<meta name="description" content="${esc(u.metaDesc)}">
<link rel="canonical" href="use-case-${u.slug}.html">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/styles.css">
</head>
<body>

<canvas id="fx-canvas"></canvas>
<div id="progress"></div>
<div class="cursor-glow" id="cursorGlow"></div>
<div id="loader"><div class="loader-brand"><span>LG</span></div></div>

<div class="announce"><span class="rocket">🚀</span> Free for buyers, always <span class="sep">|</span> <a href="brief.html">Get matched →</a></div>

<nav class="nav" id="nav">
  <div class="container">
    <a href="index.html" class="brand"><span class="brand-frame"><span>LG</span></span><span class="brand-word">Line<b>·</b>Guide</span></a>
    <div class="nav-links">
      <a href="how-it-works.html">How it works</a>
      <a href="use-cases.html" class="active">Use cases</a>
      <a href="suppliers.html">Suppliers</a>
      <a href="for-buyers.html">For buyers</a>
      <a href="for-suppliers.html">For suppliers</a>
    </div>
    <div class="nav-right">
      <a href="use-cases.html" class="link-quiet desktop-only">All applications</a>
      <a href="brief.html" class="btn btn-primary">Get matched ${arrow}</a>
    </div>
    <button class="hamburger" id="hamburger" aria-label="Menu"><span></span><span></span><span></span></button>
  </div>
</nav>

<div class="mobile-menu" id="mobileMenu">
  <a href="how-it-works.html">How it works</a>
  <a href="use-cases.html">Use cases</a>
  <a href="suppliers.html">Suppliers</a>
  <a href="for-buyers.html">For buyers</a>
  <a href="for-suppliers.html">For suppliers</a>
  <a href="brief.html" class="btn btn-primary btn-block">Get matched</a>
</div>

<main class="page">
  <section class="section" style="padding-top:48px">
    <div class="container">
      <div id="usecase">${inner(u)}
      </div>
    </div>
  </section>

  <section class="cta">
    <div class="cta-glow"></div>
    <div class="container"><div class="cta-inner">
      <div class="eyebrow center">Ready when you are</div>
      <h2 class="h-lg">Get your <span class="gt">top 3 matches.</span></h2>
      <p class="lede center">Describe your line in about a minute and we'll rank the best-fit verified suppliers — free, no obligation.</p>
      <a href="brief.html" class="btn btn-primary btn-lg">Build my brief ${arrow}</a>
    </div></div>
  </section>
</main>

<footer class="footer">
  <div class="container">
    <div class="footer-bot" style="border-top:none;padding-top:0">
      <a href="index.html" class="brand"><span class="brand-frame"><span>LG</span></span><span class="brand-word">Line<b>·</b>Guide</span></a>
      <div>© 2026 Line Guide · The new way to buy automation equipment</div>
      <a href="use-cases.html" class="link-quiet">← All applications</a>
    </div>
  </div>
</footer>

<script src="assets/app.js"></script>
</body>
</html>
`;
}

let n = 0;
for (const u of UC) {
  const file = path.join(DIR, `use-case-${u.slug}.html`);
  fs.writeFileSync(file, page(u));
  console.log('  wrote use-case-' + u.slug + '.html');
  n++;
}
console.log(`Done — pre-rendered ${n} use-case page(s).`);
