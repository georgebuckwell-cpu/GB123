/* ============================================================================
   LINE GUIDE — Interaction & Motion
   Loader · cursor glow · scroll progress · nav · mobile menu · reveal ·
   counters · tabs · FAQ · waitlist · particle field · live matching engine
   ========================================================================== */
(function () {
  'use strict';
  const $  = (s, c = document) => c.querySelector(s);
  const $$ = (s, c = document) => Array.from(c.querySelectorAll(s));
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ── LOADER ─────────────────────────────────────────────────────────────── */
  window.addEventListener('load', () => {
    const l = $('#loader');
    if (l) setTimeout(() => l.classList.add('out'), 350);
  });

  /* ── CURSOR GLOW ────────────────────────────────────────────────────────── */
  const glow = $('#cursorGlow');
  if (glow && window.innerWidth > 1024 && !reduce) {
    let ax = innerWidth / 2, ay = innerHeight / 2, cx = ax, cy = ay;
    addEventListener('mousemove', e => { ax = e.clientX; ay = e.clientY; });
    (function loop() {
      cx += (ax - cx) * .09; cy += (ay - cy) * .09;
      glow.style.left = cx + 'px'; glow.style.top = cy + 'px';
      requestAnimationFrame(loop);
    })();
  }

  /* ── NAV + PROGRESS ─────────────────────────────────────────────────────── */
  const nav = $('#nav'), prog = $('#progress');
  addEventListener('scroll', () => {
    if (nav) nav.classList.toggle('scrolled', scrollY > 30);
    if (prog) prog.style.width = (scrollY / (document.body.scrollHeight - innerHeight) * 100) + '%';
  }, { passive: true });

  /* ── MOBILE MENU ────────────────────────────────────────────────────────── */
  const burger = $('#hamburger'), menu = $('#mobileMenu');
  if (burger && menu) {
    const toggle = (open) => {
      burger.classList.toggle('open', open);
      menu.classList.toggle('open', open);
      document.body.style.overflow = open ? 'hidden' : '';
    };
    burger.addEventListener('click', () => toggle(!menu.classList.contains('open')));
    $$('a', menu).forEach(a => a.addEventListener('click', () => toggle(false)));
  }

  /* ── REVEAL ON SCROLL ───────────────────────────────────────────────────── */
  const revObs = new IntersectionObserver((es) => {
    es.forEach(e => { if (e.isIntersecting) { e.target.classList.add('in'); revObs.unobserve(e.target); } });
  }, { threshold: .12, rootMargin: '0px 0px -40px 0px' });
  $$('.reveal, .stagger').forEach(el => revObs.observe(el));

  /* ── COUNTERS ───────────────────────────────────────────────────────────── */
  function countUp(el, target, dur = 1700) {
    if (reduce) { el.textContent = target.toLocaleString(); return; }
    let start = null;
    const step = (t) => {
      if (!start) start = t;
      const p = Math.min((t - start) / dur, 1);
      const e = 1 - Math.pow(1 - p, 3);
      el.textContent = Math.round(e * target).toLocaleString();
      if (p < 1) requestAnimationFrame(step); else el.textContent = target.toLocaleString();
    };
    requestAnimationFrame(step);
  }
  const cntObs = new IntersectionObserver((es) => {
    es.forEach(e => {
      if (e.isIntersecting) {
        const t = parseFloat(e.target.dataset.count);
        if (!isNaN(t)) { countUp(e.target, t); cntObs.unobserve(e.target); }
      }
    });
  }, { threshold: .6 });
  $$('[data-count]').forEach(el => cntObs.observe(el));

  /* ── RATING BARS ────────────────────────────────────────────────────────── */
  const barObs = new IntersectionObserver((es) => {
    es.forEach(e => { if (e.isIntersecting) { e.target.style.width = e.target.dataset.w + '%'; barObs.unobserve(e.target); } });
  }, { threshold: .5 });
  $$('.rate-bar').forEach(el => barObs.observe(el));

  /* ── TABS (How it works) ────────────────────────────────────────────────── */
  $$('[data-tabs]').forEach(group => {
    const tabs = $$('.tab', group);
    const pill = $('.tab-pill', group);
    const panels = $$('.tab-panel', group.closest('[data-tabgroup]') || document);
    const move = (tab) => { if (pill) { pill.style.left = tab.offsetLeft + 'px'; pill.style.width = tab.offsetWidth + 'px'; } };
    const activate = (tab) => {
      tabs.forEach(t => t.classList.remove('active'));
      tab.classList.add('active'); move(tab);
      const key = tab.dataset.tab;
      panels.forEach(p => p.classList.toggle('active', p.dataset.panel === key));
    };
    tabs.forEach(t => t.addEventListener('click', () => activate(t)));
    const init = tabs.find(t => t.classList.contains('active')) || tabs[0];
    if (init) requestAnimationFrame(() => move(init));
    addEventListener('resize', () => { const a = tabs.find(t => t.classList.contains('active')); if (a) move(a); });
  });

  /* ── FAQ ACCORDION ──────────────────────────────────────────────────────── */
  $$('.faq-item').forEach(item => {
    const q = $('.faq-q', item), a = $('.faq-a', item);
    q.addEventListener('click', () => {
      const open = item.classList.contains('open');
      $$('.faq-item').forEach(i => { i.classList.remove('open'); $('.faq-a', i).style.maxHeight = null; });
      if (!open) { item.classList.add('open'); a.style.maxHeight = a.scrollHeight + 'px'; }
    });
  });

  /* ── WAITLIST FORM ──────────────────────────────────────────────────────── */
  $$('.waitlist').forEach(form => {
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      const input = $('input', form);
      if (!input.value || !input.value.includes('@')) { input.focus(); input.style.borderColor = '#ff6b6b'; return; }
      const ok = form.parentElement.querySelector('.waitlist-ok');
      form.style.display = 'none';
      if (ok) { ok.classList.add('show'); ok.querySelector('span').textContent = "You're on the list — we'll be in touch soon."; }
    });
  });

  /* ── PARTICLE FIELD (animated technical backdrop) ───────────────────────── */
  const cv = $('#fx-canvas');
  if (cv && !reduce) {
    const ctx = cv.getContext('2d');
    let w, h, pts = [], DPR = Math.min(devicePixelRatio || 1, 2);
    const resize = () => {
      w = cv.width = innerWidth * DPR; h = cv.height = innerHeight * DPR;
      cv.style.width = innerWidth + 'px'; cv.style.height = innerHeight + 'px';
      const count = Math.min(70, Math.floor(innerWidth / 22));
      pts = Array.from({ length: count }, () => ({
        x: Math.random() * w, y: Math.random() * h,
        vx: (Math.random() - .5) * .22 * DPR, vy: (Math.random() - .5) * .22 * DPR
      }));
    };
    resize(); addEventListener('resize', resize);
    const LINK = 130 * DPR;
    (function draw() {
      ctx.clearRect(0, 0, w, h);
      for (const p of pts) {
        p.x += p.vx; p.y += p.vy;
        if (p.x < 0 || p.x > w) p.vx *= -1;
        if (p.y < 0 || p.y > h) p.vy *= -1;
      }
      for (let i = 0; i < pts.length; i++) {
        for (let j = i + 1; j < pts.length; j++) {
          const dx = pts[i].x - pts[j].x, dy = pts[i].y - pts[j].y;
          const d = Math.hypot(dx, dy);
          if (d < LINK) {
            ctx.strokeStyle = `rgba(25,205,106,${(1 - d / LINK) * .22})`;
            ctx.lineWidth = DPR;
            ctx.beginPath(); ctx.moveTo(pts[i].x, pts[i].y); ctx.lineTo(pts[j].x, pts[j].y); ctx.stroke();
          }
        }
      }
      ctx.fillStyle = 'rgba(25,205,106,.55)';
      for (const p of pts) { ctx.beginPath(); ctx.arc(p.x, p.y, 1.4 * DPR, 0, 6.283); ctx.fill(); }
      requestAnimationFrame(draw);
    })();
  }

  /* ── LIVE MATCHING ENGINE ───────────────────────────────────────────────── */
  /* A working demo of the core product: pick a use case, budget & timeframe,
     and the engine ranks the 3 most suitable suppliers by a weighted fit score. */
  const matcher = $('#matcher');
  if (matcher) {
    // Supplier dataset — each tagged with strengths the engine scores against.
    const SUPPLIERS = [
      { name: 'Meridian Robotics',   rating: 4.9, cases: ['packing','palletising','end-of-line'], speed: 9, budget: 'high',   region: 'UK',  tier: 'Ultra'   },
      { name: 'AxisFlow Automation', rating: 4.8, cases: ['packing','filling','manual'],          speed: 8, budget: 'mid',    region: 'UK',  tier: 'Premium' },
      { name: 'Nordic Lineworks',    rating: 4.7, cases: ['palletising','end-of-line','inspection'], speed: 7, budget: 'high', region: 'EU',  tier: 'Ultra'   },
      { name: 'Crisp Systems',       rating: 4.6, cases: ['inspection','quality','manual'],        speed: 8, budget: 'mid',   region: 'UK',  tier: 'Premium' },
      { name: 'Pactura Engineering', rating: 4.5, cases: ['packing','filling','end-of-line'],      speed: 6, budget: 'low',   region: 'EU',  tier: 'Basic'   },
      { name: 'Vanguard Cobotics',   rating: 4.7, cases: ['manual','inspection','packing'],        speed: 9, budget: 'mid',   region: 'UK',  tier: 'Premium' },
      { name: 'Helix Process Co.',   rating: 4.4, cases: ['filling','quality','manual'],           speed: 6, budget: 'low',   region: 'EU',  tier: 'Basic'   },
      { name: 'Orbit Handling',      rating: 4.6, cases: ['palletising','packing','end-of-line'],  speed: 7, budget: 'high',  region: 'UK',  tier: 'Ultra'   },
    ];
    const state = { useCase: 'packing', budget: 50, timeframe: 1 }; // budget 0-100 (k£), timeframe idx
    const TIMEFRAMES = ['ASAP (< 1 mo)', '1–3 months', '3–6 months', '6+ months'];

    function budgetBand(v) { return v < 35 ? 'low' : v < 70 ? 'mid' : 'high'; }

    function score(s) {
      let pts = 0;
      // Use-case fit (most important)
      if (s.cases.includes(state.useCase)) pts += 45;
      else if (s.cases.some(c => ['packing','palletising','end-of-line'].includes(c) && ['packing','palletising','end-of-line'].includes(state.useCase))) pts += 18;
      // Rating
      pts += (s.rating - 4.3) * 40;          // ~0–24
      // Budget alignment
      const band = budgetBand(state.budget);
      pts += s.budget === band ? 18 : (Math.abs(['low','mid','high'].indexOf(s.budget) - ['low','mid','high'].indexOf(band)) === 1 ? 8 : 0);
      // Timeframe vs delivery speed (urgent → reward faster suppliers)
      const urgency = 3 - state.timeframe;   // 3 = ASAP ... 0 = relaxed
      pts += (s.speed / 10) * (8 + urgency * 4);
      return pts;
    }

    function render() {
      const ranked = SUPPLIERS.map(s => ({ s, p: score(s) })).sort((a, b) => b.p - a.p).slice(0, 3);
      const max = ranked[0].p;
      const wrap = $('#matchResults');
      wrap.innerHTML = ranked.map((r, i) => {
        const fit = Math.round(72 + (r.p / max) * 26); // normalised 72-98%
        return `
        <div class="match" style="--fit:${fit}%">
          <div class="match-rank">${i + 1}</div>
          <div class="match-body">
            <div class="match-name">${r.s.name}
              <span class="verified" title="Verified supplier">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2l2.6 1.9 3.2-.2 1 3.1 2.6 1.9-1 3.1 1 3.1-2.6 1.9-1 3.1-3.2-.2L12 22l-2.6-1.9-3.2.2-1-3.1L2.6 15.5l1-3.1-1-3.1 2.6-1.9 1-3.1 3.2.2z"/><path d="M10.5 13.2l-1.9-1.9-1.2 1.2 3.1 3.1 5.3-5.3-1.2-1.2z" fill="#0a0e0c"/></svg>
              </span>
            </div>
            <div class="match-meta">★ ${r.s.rating} · ${r.s.region} · ${r.s.tier} listing · ${r.s.cases.slice(0,2).join(', ')}</div>
          </div>
          <div class="match-fit">
            <div class="fit-pct">${fit}%</div>
            <div class="fit-cap">fit</div>
          </div>
          <div class="fit-bar"></div>
        </div>`;
      }).join('');
      // re-trigger entry animation
      requestAnimationFrame(() => $$('.match', wrap).forEach((m, i) => setTimeout(() => m.classList.add('in'), i * 90)));
    }

    // Wire controls
    $$('#matcher [data-case]').forEach(chip => chip.addEventListener('click', () => {
      $$('#matcher [data-case]').forEach(c => c.classList.remove('sel'));
      chip.classList.add('sel'); state.useCase = chip.dataset.case; render();
    }));
    const budget = $('#mBudget'), budgetOut = $('#mBudgetOut');
    if (budget) budget.addEventListener('input', () => {
      state.budget = +budget.value;
      budget.style.setProperty('--pct', budget.value + '%');
      budgetOut.innerHTML = `£<em>${(state.budget * 4).toLocaleString()}k</em>`;
      render();
    });
    const tf = $('#mTime'), tfOut = $('#mTimeOut');
    if (tf) tf.addEventListener('input', () => {
      state.timeframe = +tf.value;
      tf.style.setProperty('--pct', (state.timeframe / 3 * 100) + '%');
      tfOut.textContent = TIMEFRAMES[state.timeframe];
      render();
    });

    // Initial paint when scrolled into view
    let painted = false;
    new IntersectionObserver((es) => {
      es.forEach(e => { if (e.isIntersecting && !painted) { painted = true; render(); } });
    }, { threshold: .3 }).observe(matcher);
  }

  /* ── MAGNETIC BUTTONS (subtle) ──────────────────────────────────────────── */
  if (!reduce && window.innerWidth > 1024) {
    $$('.btn-primary').forEach(btn => {
      btn.addEventListener('mousemove', e => {
        const r = btn.getBoundingClientRect();
        btn.style.transform = `translate(${(e.clientX - r.left - r.width / 2) * .12}px, ${(e.clientY - r.top - r.height / 2) * .18}px)`;
      });
      btn.addEventListener('mouseleave', () => { btn.style.transform = ''; });
    });
  }
})();
