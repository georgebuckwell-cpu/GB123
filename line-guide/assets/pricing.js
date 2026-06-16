/* ============================================================================
   LINE GUIDE — Pricing page
   Billing toggle (monthly / annual = 2 months free) + interactive ROI
   calculator framed around supplier project value and matched pipeline.
   ========================================================================== */
(function () {
  'use strict';
  const $ = (s, c = document) => c.querySelector(s);
  const $$ = (s, c = document) => Array.from(c.querySelectorAll(s));
  const fmt = n => n.toLocaleString('en-GB');

  const TIERS = { Basic: 149, Premium: 399, Ultra: 899 };
  let annual = false;

  /* ── BILLING TOGGLE ─────────────────────────────────────────────────────── */
  const sw = $('#billSwitch');
  function paintPrices() {
    $$('[data-tier-price]').forEach(el => {
      const m = TIERS[el.dataset.tierPrice];
      const perMonth = annual ? Math.round(m * 10 / 12) : m;
      el.querySelector('.amt').textContent = perMonth;
      const sub = el.querySelector('.sub-bill');
      if (sub) sub.textContent = annual ? `£${fmt(m * 10)} billed yearly · save £${fmt(m * 2)}` : 'billed monthly · cancel anytime';
    });
    $('#billMonthly').classList.toggle('on', !annual);
    $('#billAnnual').classList.toggle('on', annual);
    // table header prices
    $$('[data-th-tier]').forEach(el => {
      const m = TIERS[el.dataset.thTier];
      const perMonth = annual ? Math.round(m * 10 / 12) : m;
      el.querySelector('.pp').textContent = `£${perMonth}/mo`;
    });
    calc();
  }
  if (sw) sw.addEventListener('click', () => { annual = !annual; sw.classList.toggle('annual', annual); paintPrices(); });
  $('#billMonthly')?.addEventListener('click', () => { if (annual) sw.click(); });
  $('#billAnnual')?.addEventListener('click', () => { if (!annual) sw.click(); });

  /* ── ROI CALCULATOR ─────────────────────────────────────────────────────── */
  const state = { value: 150, wins: 1, tier: 'Premium' }; // value in £k, wins per month

  const valEl = $('#roiValue'), winsEl = $('#roiWins');
  const outValue = $('#roiValueOut'), outWins = $('#roiWinsOut');

  function calc() {
    if (!$('#roiROI')) return;
    const m = TIERS[state.tier];
    const monthlyCost = annual ? m * 10 / 12 : m;
    const annualCost = annual ? m * 10 : m * 12;
    const projectVal = state.value * 1000;
    const monthlyPipeline = projectVal * state.wins;

    const roi = monthlyPipeline / monthlyCost;                 // £ pipeline per £1 spent
    const sharePct = monthlyCost / projectVal * 100;           // membership as % of one project
    const breakeven = annualCost / projectVal;                 // projects/yr to cover cost

    $('#roiROI').textContent = '£' + fmt(Math.round(roi));
    $('#roiShare').textContent = (sharePct < 1 ? sharePct.toFixed(2) : sharePct.toFixed(1)) + '%';
    $('#roiBreak').textContent = breakeven < 1
      ? (breakeven * 12 < 1 ? '< 1 project / yr' : (breakeven).toFixed(2).replace(/\.?0+$/, '') + ' projects / yr')
      : breakeven.toFixed(1) + ' / yr';
  }

  if (valEl) valEl.addEventListener('input', () => {
    state.value = +valEl.value;
    valEl.style.setProperty('--pct', ((valEl.value - valEl.min) / (valEl.max - valEl.min) * 100) + '%');
    outValue.innerHTML = `£<em>${fmt(state.value)}k</em>`;
    calc();
  });
  if (winsEl) winsEl.addEventListener('input', () => {
    state.wins = +winsEl.value;
    winsEl.style.setProperty('--pct', ((winsEl.value - winsEl.min) / (winsEl.max - winsEl.min) * 100) + '%');
    outWins.innerHTML = `<em>${state.wins}</em> / month`;
    calc();
  });
  $$('.roi-tier').forEach(t => t.addEventListener('click', () => {
    $$('.roi-tier').forEach(x => x.classList.remove('sel'));
    t.classList.add('sel'); state.tier = t.dataset.tier; calc();
  }));

  // FAQ accordion is static markup → bound by app.js (avoid double-binding here)

  paintPrices();
})();
