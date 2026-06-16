/* ============================================================================
   LINE GUIDE — Buyer Brief Builder
   A guided multi-step wizard that captures a full sourcing brief, then runs
   the matching engine to return the top 3 best-fit suppliers with a
   transparent per-signal fit breakdown and "request introduction" flow.
   ========================================================================== */
(function () {
  'use strict';
  const $  = (s, c = document) => c.querySelector(s);
  const $$ = (s, c = document) => Array.from(c.querySelectorAll(s));
  const clamp = (n, a, b) => Math.max(a, Math.min(b, n));
  const wizard = $('#wizard');
  if (!wizard) return;

  const TOTAL = 5;
  let cur = 1, atResults = false;

  /* ── STATE ──────────────────────────────────────────────────────────────── */
  const state = {
    useCase: null, format: null, env: 'ambient', throughput: 50,
    budget: 50, timeframe: null, region: null, must: new Set(),
    name: '', company: '', email: ''
  };
  const TF_LABEL = { asap: 'ASAP (<1 mo)', '1-3': '1–3 months', '3-6': '3–6 months', '6+': '6+ months' };
  const CASE_LABEL = { packing:'Packing', palletising:'Palletising', 'end-of-line':'End-of-line', filling:'Filling', inspection:'Inspection', manual:'Manual process' };

  /* ── SUPPLIER DATASET ───────────────────────────────────────────────────── */
  const SUPPLIERS = [
    { name:'Meridian Robotics',   rating:4.9, region:'uk', budget:'high', speed:9, cases:['packing','palletising','end-of-line'], formats:['cartons','trays','cans'],   env:['ambient','chilled','washdown'], certs:true,  cobot:true,  small:false, tags:['Robotics','High-speed','Turnkey'] },
    { name:'AxisFlow Automation', rating:4.8, region:'uk', budget:'mid',  speed:8, cases:['packing','filling','manual'],          formats:['pouches','bottles','cans'],  env:['ambient','chilled'],            certs:true,  cobot:true,  small:true,  tags:['Flexible','Quick install'] },
    { name:'Nordic Lineworks',    rating:4.7, region:'eu', budget:'high', speed:7, cases:['palletising','end-of-line','inspection'], formats:['cartons','trays'],         env:['ambient','frozen','washdown'],  certs:true,  cobot:false, small:false, tags:['End-of-line','Cold chain'] },
    { name:'Crisp Systems',       rating:4.6, region:'uk', budget:'mid',  speed:8, cases:['inspection','manual','packing'],       formats:['trays','pouches','bulk'],     env:['ambient','washdown'],           certs:true,  cobot:true,  small:true,  tags:['Vision','Quality'] },
    { name:'Pactura Engineering', rating:4.5, region:'eu', budget:'low',  speed:6, cases:['packing','filling','end-of-line'],     formats:['bottles','cans','bulk'],      env:['ambient','chilled'],            certs:false, cobot:false, small:true,  tags:['Value','Modular'] },
    { name:'Vanguard Cobotics',   rating:4.7, region:'uk', budget:'mid',  speed:9, cases:['manual','inspection','packing'],       formats:['pouches','cartons','trays'],  env:['ambient','chilled'],            certs:true,  cobot:true,  small:true,  tags:['Cobots','Retrofit','Fast ROI'] },
    { name:'Helix Process Co.',   rating:4.4, region:'eu', budget:'low',  speed:6, cases:['filling','manual','inspection'],       formats:['bottles','bulk','pouches'],   env:['ambient','washdown'],           certs:false, cobot:false, small:false, tags:['Filling','Dosing'] },
    { name:'Orbit Handling',      rating:4.6, region:'uk', budget:'high', speed:7, cases:['palletising','packing','end-of-line'], formats:['cartons','trays','cans'],     env:['ambient','frozen','chilled'],   certs:true,  cobot:false, small:false, tags:['Palletising','Conveying'] },
    { name:'BluePeak Systems',    rating:4.8, region:'eu', budget:'mid',  speed:8, cases:['inspection','packing','filling'],      formats:['pouches','bottles','trays'],  env:['ambient','chilled','washdown'], certs:true,  cobot:true,  small:true,  tags:['Inspection','Hygienic'] },
  ];
  const CLUSTER = { packing:'pack', palletising:'pack', 'end-of-line':'pack', filling:'proc', inspection:'proc', manual:'proc' };
  const BANDS = ['low','mid','high'];
  const budgetBand = v => v < 35 ? 'low' : v < 70 ? 'mid' : 'high';

  /* ── SCORING ────────────────────────────────────────────────────────────── */
  function evaluate(s) {
    // Use-case (with format + environment nudges)
    let uc = s.cases.includes(state.useCase) ? 92
           : (CLUSTER[state.useCase] && s.cases.some(c => CLUSTER[c] === CLUSTER[state.useCase])) ? 60 : 30;
    if (state.format && s.formats.includes(state.format)) uc += 8;
    if (state.env && s.env.includes(state.env)) uc += 4; else if (state.env) uc -= 6;
    uc = clamp(uc, 5, 100);

    // Rating
    const rt = clamp((s.rating - 4.3) / 0.7 * 100, 0, 100);

    // Budget alignment
    const band = budgetBand(state.budget);
    const gap = Math.abs(BANDS.indexOf(s.budget) - BANDS.indexOf(band));
    const bg = gap === 0 ? 100 : gap === 1 ? 62 : 28;

    // Speed vs timeframe + throughput
    const urgency = { asap:1, '1-3':0.8, '3-6':0.6, '6+':0.45 }[state.timeframe] ?? 0.8;
    const needed = 4 + state.throughput / 100 * 6;             // 4–10
    const speedGap = Math.max(0, needed - s.speed);
    let sp = (s.speed * 10) * urgency + (1 - urgency) * 75 - speedGap * 9;
    sp = clamp(sp, 0, 100);

    // Weighted overall
    let overall = uc * 0.45 + rt * 0.25 + bg * 0.18 + sp * 0.12;

    // Modifiers — region + must-haves
    if (state.region && state.region !== 'either') overall *= s.region === state.region ? 1.04 : 0.9;
    let met = 0;
    if (state.must.size) {
      const checks = { footprint: s.small, certs: s.certs, integration: true, support: s.rating >= 4.6, cobot: s.cobot };
      state.must.forEach(m => { if (checks[m]) met++; });
      overall *= 1 + (met / state.must.size - 0.5) * 0.12;
    }
    return { s, overall, uc, rt, bg, sp, met };
  }

  function computeMatches() {
    const ranked = SUPPLIERS.map(evaluate).sort((a, b) => b.overall - a.overall).slice(0, 3);
    const maxO = ranked[0].overall;
    ranked.forEach(r => { r.fit = Math.round(clamp(r.overall / maxO * 97, 62, 98)); });
    return ranked;
  }

  /* ── PROGRESS ───────────────────────────────────────────────────────────── */
  function updateProgress() {
    $$('.wz-pstep').forEach((el, i) => {
      const n = i + 1;
      el.classList.toggle('active', n === cur && !atResults);
      el.classList.toggle('done', n < cur || atResults);
    });
    $('#wzCount').textContent = atResults ? 'Results' : `Step ${cur} of ${TOTAL}`;
  }

  /* ── SUMMARY CHIPS ──────────────────────────────────────────────────────── */
  function renderSummary() {
    const bits = [];
    if (state.useCase) bits.push(['Need', CASE_LABEL[state.useCase]]);
    if (state.format)  bits.push(['Format', state.format]);
    if (state.env && cur > 1) bits.push(['Env', state.env]);
    if (cur >= 3) bits.push(['Budget', '£' + (state.budget * 4) + 'k']);
    if (state.timeframe) bits.push(['When', TF_LABEL[state.timeframe]]);
    if (state.region) bits.push(['Region', state.region.toUpperCase()]);
    if (state.must.size) bits.push(['Must-haves', state.must.size]);
    $('#wzSummary').innerHTML = bits.map(([k, v]) => `<span class="wz-sumchip">${k} <b>${v}</b></span>`).join('');
  }

  /* ── STEP NAVIGATION ────────────────────────────────────────────────────── */
  function showStep(n) {
    $$('.wz-step').forEach(s => s.classList.toggle('active', +s.dataset.step === n));
    $('#wzBack').toggleAttribute('disabled', n === 1);
    $('#wzNext').innerHTML = n === TOTAL
      ? 'See my matches <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M12 5l7 7-7 7"/></svg>'
      : 'Continue <svg class="arr" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M12 5l7 7-7 7"/></svg>';
    updateProgress(); renderSummary();
  }

  function validate(n) {
    const warn = $('#wzWarn');
    let ok = true, msg = '';
    if (n === 1 && !state.useCase) { ok = false; msg = 'Pick what you need to automate.'; }
    if (n === 2 && !state.format)  { ok = false; msg = 'Choose your primary product format.'; }
    if (n === 3 && !state.timeframe) { ok = false; msg = 'Select your install timeframe.'; }
    if (n === 4 && !state.region)  { ok = false; msg = 'Choose a preferred region.'; }
    if (n === 5) {
      state.name = $('#wzName').value.trim();
      state.company = $('#wzCompany').value.trim();
      state.email = $('#wzEmail').value.trim();
      const bad = [];
      if (!state.name) bad.push($('#wzName'));
      if (!state.company) bad.push($('#wzCompany'));
      if (!state.email.includes('@')) bad.push($('#wzEmail'));
      $$('.wz-input').forEach(i => i.classList.remove('err'));
      if (bad.length) { ok = false; msg = 'Add your name, company and a valid email.'; bad.forEach(i => i.classList.add('err')); bad[0].focus(); }
    }
    warn.classList.toggle('show', !ok);
    if (!ok) $('#wzWarnMsg').textContent = msg;
    return ok;
  }

  function next() {
    if (!validate(cur)) return;
    if (cur < TOTAL) { cur++; showStep(cur); scrollTop(); }
    else showResults();
  }
  function back() {
    $('#wzWarn').classList.remove('show');
    if (atResults) { atResults = false; wizard.classList.remove('results-mode'); $('#wzResultsPanel').classList.remove('active'); showStep(cur); }
    else if (cur > 1) { cur--; showStep(cur); }
    scrollTop();
  }
  function scrollTop() {
    const t = wizard.getBoundingClientRect().top + scrollY - 120;
    scrollTo({ top: t, behavior: 'smooth' });
  }

  /* ── RESULTS ────────────────────────────────────────────────────────────── */
  function showResults() {
    atResults = true;
    wizard.classList.add('results-mode');
    $$('.wz-step').forEach(s => s.classList.remove('active'));
    const panel = $('#wzResultsPanel');
    panel.classList.add('active');
    updateProgress(); scrollTop();

    const greet = state.name ? state.name.split(' ')[0] : 'there';
    $('#wzGreet').textContent = `Top matches for ${greet} · ${state.company || 'your line'}`;
    const wrap = $('#wzResults');
    wrap.innerHTML = '';

    // brief "calculating" beat, then reveal
    setTimeout(() => {
      const ranked = computeMatches();
      wrap.innerHTML = ranked.map((r, i) => `
        <div class="res-card ${i === 0 ? 'top' : ''}">
          <div class="res-ranktag">${i === 0 ? '★ Best fit' : 'Match #' + (i + 1)}</div>
          <div class="res-name">${r.s.name}
            <span class="verified" title="Verified supplier"><svg width="15" height="15" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2l2.6 1.9 3.2-.2 1 3.1 2.6 1.9-1 3.1 1 3.1-2.6 1.9-1 3.1-3.2-.2L12 22l-2.6-1.9-3.2.2-1-3.1L2.6 15.5l1-3.1-1-3.1 2.6-1.9 1-3.1 3.2.2z"/><path d="M10.5 13.2l-1.9-1.9-1.2 1.2 3.1 3.1 5.3-5.3-1.2-1.2z" fill="#141A16"/></svg></span>
          </div>
          <div class="res-meta">★ ${r.s.rating} · ${r.s.region.toUpperCase()} · ${r.s.budget} budget</div>
          <div class="res-fit"><span class="big">${r.fit}%</span><span class="lbl">overall fit</span></div>
          <div class="res-break">
            <div class="brk-row"><span class="brk-lbl">Use-case</span><span class="brk-track"><span class="brk-bar" style="--w:${Math.round(r.uc)}%"></span></span></div>
            <div class="brk-row"><span class="brk-lbl">Rating</span><span class="brk-track"><span class="brk-bar" style="--w:${Math.round(r.rt)}%"></span></span></div>
            <div class="brk-row"><span class="brk-lbl">Budget</span><span class="brk-track"><span class="brk-bar" style="--w:${Math.round(r.bg)}%"></span></span></div>
            <div class="brk-row"><span class="brk-lbl">Timeline</span><span class="brk-track"><span class="brk-bar" style="--w:${Math.round(r.sp)}%"></span></span></div>
          </div>
          <div class="res-tags">${r.s.tags.map(t => `<span class="res-tag">${t}</span>`).join('')}</div>
          <button class="btn btn-primary btn-block res-introbtn">Request introduction</button>
          <div class="res-intro"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg> Introduction requested</div>
        </div>`).join('');

      $$('.res-card', wrap).forEach((c, i) => setTimeout(() => c.classList.add('in'), 120 + i * 140));
      $$('.res-introbtn', wrap).forEach(btn => btn.addEventListener('click', () => {
        btn.style.display = 'none';
        btn.nextElementSibling.classList.add('show');
      }));
    }, 750);
  }

  /* ── INPUT WIRING ───────────────────────────────────────────────────────── */
  // option cards (single per group)
  $$('.opt').forEach(opt => opt.addEventListener('click', () => {
    const g = opt.dataset.group;
    $$(`.opt[data-group="${g}"]`).forEach(o => o.classList.remove('sel'));
    opt.classList.add('sel');
    state[g] = opt.dataset.val;
    $('#wzWarn').classList.remove('show');
    renderSummary();
  }));

  // chips (single or multi via data-multi)
  $$('.wz-chips .chip').forEach(chip => chip.addEventListener('click', () => {
    const g = chip.dataset.group;
    if (chip.dataset.multi) {
      chip.classList.toggle('sel');
      chip.classList.contains('sel') ? state.must.add(chip.dataset.val) : state.must.delete(chip.dataset.val);
    } else {
      $$(`.chip[data-group="${g}"]`).forEach(c => c.classList.remove('sel'));
      chip.classList.add('sel');
      state[g] = chip.dataset.val;
      $('#wzWarn').classList.remove('show');
    }
    renderSummary();
  }));

  // sliders
  const tput = $('#wzTput'), tputOut = $('#wzTputOut');
  if (tput) tput.addEventListener('input', () => {
    state.throughput = +tput.value;
    tput.style.setProperty('--pct', tput.value + '%');
    const upm = Math.round(20 + state.throughput / 100 * 580); // 20–600 units/min
    tputOut.innerHTML = `<em>${upm}</em> units/min`;
  });
  const bud = $('#wzBudget'), budOut = $('#wzBudgetOut');
  if (bud) bud.addEventListener('input', () => {
    state.budget = +bud.value;
    bud.style.setProperty('--pct', bud.value + '%');
    budOut.innerHTML = `£<em>${(state.budget * 4).toLocaleString()}k</em>`;
  });

  // nav buttons + keyboard
  $('#wzNext').addEventListener('click', next);
  $('#wzBack').addEventListener('click', back);
  $('#wzRestart').addEventListener('click', () => location.reload());
  document.addEventListener('keydown', e => {
    if (e.key === 'Enter' && !atResults && e.target.tagName !== 'TEXTAREA') { e.preventDefault(); next(); }
  });

  // init
  showStep(1);
})();
