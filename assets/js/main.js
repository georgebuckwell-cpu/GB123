/* ════════════════════════════════════════════════════════════════════════════
   VELASYNC — INTERACTION LAYER
   Shared across all pages. Each block guards for missing elements,
   so the same file safely powers every page.
   ════════════════════════════════════════════════════════════════════════════ */
(function () {
  'use strict';

  /* ── LOADER ──────────────────────────────────────────────────────────── */
  window.addEventListener('load', () => {
    const l = document.getElementById('loader');
    if (l) setTimeout(() => l.classList.add('out'), 250);
  });

  /* ── CURSOR GLOW (desktop) ───────────────────────────────────────────── */
  const glow = document.getElementById('cursorGlow');
  if (glow && window.matchMedia('(min-width:1025px)').matches) {
    let ax = innerWidth / 2, ay = innerHeight / 2, cx = ax, cy = ay;
    addEventListener('mousemove', e => { ax = e.clientX; ay = e.clientY; });
    (function loop() {
      cx += (ax - cx) * 0.08; cy += (ay - cy) * 0.08;
      glow.style.left = cx + 'px'; glow.style.top = cy + 'px';
      requestAnimationFrame(loop);
    })();
  }

  /* ── NAV SCROLL + PROGRESS ───────────────────────────────────────────── */
  const nav = document.getElementById('nav');
  const prog = document.getElementById('progress');
  const mobileCta = document.getElementById('mobileCta');
  addEventListener('scroll', () => {
    const sy = scrollY;
    if (nav) nav.classList.toggle('scrolled', sy > 40);
    if (prog) prog.style.width = (sy / (document.body.scrollHeight - innerHeight) * 100) + '%';
    if (mobileCta) mobileCta.classList.toggle('visible', sy > 500);
  }, { passive: true });

  /* ── HAMBURGER ───────────────────────────────────────────────────────── */
  const hbg = document.getElementById('hamburger');
  const mm = document.getElementById('mobileMenu');
  if (hbg && mm) {
    hbg.addEventListener('click', () => {
      hbg.classList.toggle('open');
      mm.classList.toggle('open');
      document.body.style.overflow = mm.classList.contains('open') ? 'hidden' : '';
    });
    mm.querySelectorAll('a').forEach(a => a.addEventListener('click', () => {
      hbg.classList.remove('open'); mm.classList.remove('open'); document.body.style.overflow = '';
    }));
  }

  /* ── REVEAL ON SCROLL ────────────────────────────────────────────────── */
  const revObs = new IntersectionObserver(es => {
    es.forEach(e => { if (e.isIntersecting) { e.target.classList.add('in'); revObs.unobserve(e.target); } });
  }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
  document.querySelectorAll('.reveal, .stagger').forEach(el => revObs.observe(el));

  /* ── COUNTERS ────────────────────────────────────────────────────────── */
  function animCount(el, target, dur = 1700) {
    let start = null;
    const step = ts => {
      if (!start) start = ts;
      const p = Math.min((ts - start) / dur, 1);
      const ease = 1 - Math.pow(1 - p, 3);
      el.textContent = Math.round(ease * target).toLocaleString();
      if (p < 1) requestAnimationFrame(step); else el.textContent = target.toLocaleString();
    };
    requestAnimationFrame(step);
  }
  const cObs = new IntersectionObserver(es => {
    es.forEach(e => {
      if (e.isIntersecting) {
        const t = parseInt(e.target.dataset.target);
        if (!isNaN(t)) { animCount(e.target, t); cObs.unobserve(e.target); }
      }
    });
  }, { threshold: 0.5 });
  document.querySelectorAll('[data-target]').forEach(el => cObs.observe(el));

  /* ── TIMELINE FILL + ACTIVE STEPS ────────────────────────────────────── */
  const timeline = document.querySelector('.timeline');
  if (timeline) {
    const fill = timeline.querySelector('.fill');
    const steps = timeline.querySelectorAll('.tl-step');
    const tObs = new IntersectionObserver(es => {
      es.forEach(e => {
        if (e.isIntersecting) {
          if (fill) fill.style.width = 'calc(75% - 0px)';
          steps.forEach((s, i) => setTimeout(() => s.classList.add('active'), i * 280));
          tObs.disconnect();
        }
      });
    }, { threshold: 0.4 });
    tObs.observe(timeline);
  }

  /* ── SKILL BARS ──────────────────────────────────────────────────────── */
  const skillWrap = document.querySelector('.team-body');
  document.querySelectorAll('.skill-fill').forEach(bar => {
    const sObs = new IntersectionObserver(es => {
      es.forEach(e => { if (e.isIntersecting) { bar.style.width = bar.dataset.level + '%'; sObs.unobserve(bar); } });
    }, { threshold: 0.5 });
    sObs.observe(bar);
  });

  /* ── FAQ ACCORDION ───────────────────────────────────────────────────── */
  document.querySelectorAll('.faq-item').forEach(item => {
    const q = item.querySelector('.faq-q');
    const a = item.querySelector('.faq-a');
    q.addEventListener('click', () => {
      const open = item.classList.contains('open');
      document.querySelectorAll('.faq-item').forEach(i => { i.classList.remove('open'); i.querySelector('.faq-a').style.maxHeight = null; });
      if (!open) { item.classList.add('open'); a.style.maxHeight = a.scrollHeight + 'px'; }
    });
  });

  /* ── PORTFOLIO FILTER ────────────────────────────────────────────────── */
  const filterRow = document.querySelector('.filter-row');
  if (filterRow) {
    const cards = document.querySelectorAll('.work-card');
    filterRow.querySelectorAll('.filter-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        filterRow.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        const f = btn.dataset.filter;
        cards.forEach(c => {
          const show = f === 'all' || c.dataset.cat === f;
          c.classList.toggle('hide', !show);
        });
      });
    });
  }

  /* ── PACKAGE BUILDER ─────────────────────────────────────────────────── */
  const builder = document.getElementById('builder');
  if (builder) {
    const fmt = n => '£' + n.toLocaleString();
    const opts = builder.querySelectorAll('.opt');
    const sumLines = document.getElementById('sumLines');
    const sumTotal = document.getElementById('sumTotal');
    const sumMo = document.getElementById('sumMo');

    function recalc() {
      let oneOff = 0, monthly = 0;
      const chosen = [];
      opts.forEach(o => {
        if (o.classList.contains('sel')) {
          oneOff += +o.dataset.price;
          monthly += +(o.dataset.mo || 0);
          chosen.push({ name: o.dataset.name, price: +o.dataset.price, mo: +(o.dataset.mo || 0) });
        }
      });
      sumLines.innerHTML = chosen.length
        ? chosen.map(c => `<div class="sum-line"><span>${c.name}</span><b>${fmt(c.price)}${c.mo ? ' + ' + fmt(c.mo) + '/mo' : ''}</b></div>`).join('')
        : '<div class="sum-line empty">Select options to build your package…</div>';
      sumTotal.querySelector('.big').textContent = fmt(oneOff);
      sumMo.querySelector('b').textContent = fmt(monthly) + '/mo';
    }

    opts.forEach(o => {
      o.addEventListener('click', () => {
        if (o.classList.contains('locked')) return;
        // radio group (base package) — only one base selectable
        if (o.dataset.group) {
          builder.querySelectorAll(`.opt[data-group="${o.dataset.group}"]`).forEach(g => g.classList.remove('sel'));
          o.classList.add('sel');
        } else {
          o.classList.toggle('sel');
        }
        recalc();
      });
    });
    recalc();
  }

  /* ── ROI CALCULATOR ──────────────────────────────────────────────────── */
  const calc = document.getElementById('calc');
  if (calc) {
    const visitors = document.getElementById('cVisitors');
    const value = document.getElementById('cValue');
    const rate = document.getElementById('cRate');
    const fmt = n => '£' + Math.round(n).toLocaleString();

    function paint(el) {
      const min = +el.min, max = +el.max, v = +el.value;
      const pct = ((v - min) / (max - min)) * 100;
      el.style.background = `linear-gradient(90deg,var(--teal) 0%,var(--teal) ${pct}%,var(--surf-3) ${pct}%)`;
    }
    function update() {
      const vis = +visitors.value, val = +value.value, rt = +rate.value;
      document.getElementById('vVisitors').textContent = vis.toLocaleString();
      document.getElementById('vValue').textContent = '£' + val;
      document.getElementById('vRate').textContent = rt + '%';
      const monthlyRevenue = vis * (rt / 100) * val;
      const yearly = monthlyRevenue * 12;
      const cost = 400 + 50 * 12; // basic package year-one
      const roi = cost > 0 ? ((yearly - cost) / cost) * 100 : 0;
      document.getElementById('roiMonthly').textContent = fmt(monthlyRevenue);
      document.getElementById('roiYearly').textContent = fmt(yearly);
      document.getElementById('roiX').textContent = (yearly / cost).toFixed(1) + '×';
      [visitors, value, rate].forEach(paint);
    }
    [visitors, value, rate].forEach(el => el.addEventListener('input', update));
    update();
  }

  /* ── CONTACT FORM (demo handler) ─────────────────────────────────────── */
  const form = document.getElementById('contactForm');
  if (form) {
    form.addEventListener('submit', e => {
      e.preventDefault();
      const ok = document.getElementById('formSuccess');
      if (ok) { ok.classList.add('show'); ok.scrollIntoView({ behavior: 'smooth', block: 'center' }); }
      form.reset();
    });
  }

  /* ── PREFILL PACKAGE FROM URL (?plan=) ───────────────────────────────── */
  const params = new URLSearchParams(location.search);
  const plan = params.get('plan');
  if (plan) {
    const sel = document.getElementById('cf-package');
    if (sel) sel.value = plan;
  }
})();
