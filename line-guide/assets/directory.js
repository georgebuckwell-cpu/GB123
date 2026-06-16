/* ============================================================================
   LINE GUIDE — Supplier Directory
   Search, filter (application + region), sort and render the verified supplier
   grid from the shared dataset. Cards deep-link to supplier.html?s=slug.
   ========================================================================== */
(function () {
  'use strict';
  const $  = (s, c = document) => c.querySelector(s);
  const $$ = (s, c = document) => Array.from(c.querySelectorAll(s));
  const grid = $('#dirGrid');
  if (!grid || !window.LG_SUPPLIERS) return;

  const CASE_LABEL = { packing:'Packing', palletising:'Palletising', 'end-of-line':'End-of-line', filling:'Filling', inspection:'Inspection', manual:'Manual process' };
  const state = { q: '', useCase: 'all', region: 'all', sort: 'rating' };

  function stars(r) {
    const full = Math.round(r);
    let out = '<span class="stars">';
    for (let i = 1; i <= 5; i++) out += `<svg width="13" height="13" viewBox="0 0 24 24" fill="${i <= full ? 'currentColor' : 'none'}" stroke="currentColor" stroke-width="1.5"><path d="M12 2l3 6.5 7 .9-5 4.9 1.2 7L12 18l-6.4 3.3L7 14.3 2 9.4l7-.9z"/></svg>`;
    return out + '</span>';
  }

  function filtered() {
    let list = window.LG_SUPPLIERS.filter(s => {
      if (state.useCase !== 'all' && !s.cases.includes(state.useCase)) return false;
      if (state.region !== 'all' && s.region !== state.region) return false;
      if (state.q) {
        const hay = (s.name + ' ' + s.blurb + ' ' + s.tags.join(' ') + ' ' + s.capabilities.join(' ') + ' ' + s.location).toLowerCase();
        if (!hay.includes(state.q.toLowerCase())) return false;
      }
      return true;
    });
    const TIER_RANK = { Ultra: 3, Premium: 2, Basic: 1 };
    list.sort((a, b) =>
      state.sort === 'projects' ? b.projects - a.projects :
      state.sort === 'name'     ? a.name.localeCompare(b.name) :
      state.sort === 'tier'     ? TIER_RANK[b.tier] - TIER_RANK[a.tier] || b.rating - a.rating :
      /* rating */                b.rating - a.rating
    );
    return list;
  }

  function render() {
    const list = filtered();
    $('#dirCount').textContent = `${list.length} supplier${list.length === 1 ? '' : 's'}`;
    $('#dirEmpty').classList.toggle('show', list.length === 0);
    grid.innerHTML = list.map((s, i) => `
      <article class="sup-card" style="animation-delay:${Math.min(i * 50, 400)}ms">
        <div class="sup-card-head">
          <div class="sup-logo">${s.monogram}</div>
          <div class="sup-id">
            <div class="sup-name">${s.name} <span class="verified" title="Verified"><svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2l2.6 1.9 3.2-.2 1 3.1 2.6 1.9-1 3.1 1 3.1-2.6 1.9-1 3.1-3.2-.2L12 22l-2.6-1.9-3.2.2-1-3.1L2.6 15.5l1-3.1-1-3.1 2.6-1.9 1-3.1 3.2.2z"/><path d="M10.5 13.2l-1.9-1.9-1.2 1.2 3.1 3.1 5.3-5.3-1.2-1.2z" fill="#141A16"/></svg></span></div>
            <div class="sup-loc">${s.location}</div>
          </div>
        </div>
        <div class="sup-rate">${stars(s.rating)} <b>${s.rating}</b> <span>(${s.reviews})</span> <span class="tier-pill ${s.tier === 'Ultra' ? 'ultra' : ''}" style="margin-left:auto">${s.tier}</span></div>
        <p class="sup-blurb">${s.blurb}</p>
        <div class="sup-tags">${s.tags.map(t => `<span class="sup-tag">${t}</span>`).join('')}</div>
        <div class="sup-foot">
          <span class="mono-note">${s.cases.map(c => CASE_LABEL[c]).slice(0, 2).join(' · ')}</span>
          <a class="link" href="supplier.html?s=${s.slug}">View profile <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M12 5l7 7-7 7"/></svg></a>
        </div>
      </article>`).join('');
  }

  // wire controls
  const search = $('#dirSearch');
  if (search) search.addEventListener('input', () => { state.q = search.value; render(); });
  $$('#dirFilters .chip').forEach(chip => chip.addEventListener('click', () => {
    $$('#dirFilters .chip').forEach(c => c.classList.remove('sel'));
    chip.classList.add('sel'); state.useCase = chip.dataset.case; render();
  }));
  const region = $('#dirRegion'); if (region) region.addEventListener('change', () => { state.region = region.value; render(); });
  const sort = $('#dirSort'); if (sort) sort.addEventListener('change', () => { state.sort = sort.value; render(); });

  // deep-link: ?case= preselects a filter (e.g. from use-case landing pages)
  const params = new URLSearchParams(location.search);
  const pc = params.get('case');
  if (pc && CASE_LABEL[pc]) {
    const chip = $(`#dirFilters .chip[data-case="${pc}"]`);
    if (chip) { $$('#dirFilters .chip').forEach(c => c.classList.remove('sel')); chip.classList.add('sel'); state.useCase = pc; }
  }

  render();
})();
