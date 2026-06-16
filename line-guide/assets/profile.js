/* ============================================================================
   LINE GUIDE — Supplier Profile (dynamic)
   Reads ?s=slug, finds the supplier in the shared dataset and renders the
   full profile. Falls back to the first supplier if no/unknown slug.
   ========================================================================== */
(function () {
  'use strict';
  const $ = (s, c = document) => c.querySelector(s);
  const root = $('#profile');
  if (!root || !window.LG_SUPPLIERS) return;

  const CASE_LABEL = { packing:'Packing', palletising:'Palletising', 'end-of-line':'End-of-line', filling:'Filling', inspection:'Inspection', manual:'Manual process' };
  const slug = new URLSearchParams(location.search).get('s');
  const s = window.LG_SUPPLIERS.find(x => x.slug === slug) || window.LG_SUPPLIERS[0];

  document.title = `${s.name} — Line Guide`;

  const stars = (r, size = 14) => {
    const full = Math.round(r); let out = '<span class="stars">';
    for (let i = 1; i <= 5; i++) out += `<svg width="${size}" height="${size}" viewBox="0 0 24 24" fill="${i <= full ? 'currentColor' : 'none'}" stroke="currentColor" stroke-width="1.5"><path d="M12 2l3 6.5 7 .9-5 4.9 1.2 7L12 18l-6.4 3.3L7 14.3 2 9.4l7-.9z"/></svg>`;
    return out + '</span>';
  };
  const check = '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>';
  const verified = '<span class="verified" style="color:var(--green)"><svg width="22" height="22" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2l2.6 1.9 3.2-.2 1 3.1 2.6 1.9-1 3.1 1 3.1-2.6 1.9-1 3.1-3.2-.2L12 22l-2.6-1.9-3.2.2-1-3.1L2.6 15.5l1-3.1-1-3.1 2.6-1.9 1-3.1 3.2.2z"/><path d="M10.5 13.2l-1.9-1.9-1.2 1.2 3.1 3.1 5.3-5.3-1.2-1.2z" fill="#070A08"/></svg></span>';

  root.innerHTML = `
    <a href="suppliers.html" class="wz-back" style="opacity:1;margin-bottom:1.6rem"><svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 12H5M12 19l-7-7 7-7"/></svg> All suppliers</a>

    <div class="prof-head">
      <div class="sup-logo prof-logo">${s.monogram}</div>
      <div>
        <div class="prof-name">${s.name} ${verified}</div>
        <div class="prof-badges">
          ${stars(s.rating, 16)} <b style="color:var(--white);font-family:var(--font-display)">${s.rating}</b>
          <span style="color:var(--sub);font-size:.85rem">(${s.reviews} reviews)</span>
          <span class="tier-pill ${s.tier === 'Ultra' ? 'ultra' : ''}">${s.tier} member</span>
          <span class="sup-tag">${s.location}</span>
        </div>
      </div>
      <div class="prof-cta">
        <a href="brief.html" class="btn btn-primary btn-block">Request introduction</a>
        <a href="brief.html" class="btn btn-ghost btn-block">Add to my brief</a>
      </div>
    </div>

    <div class="prof-stats">
      <div class="pstat"><div class="n"><em>${s.projects}</em>+</div><div class="l">Projects delivered</div></div>
      <div class="pstat"><div class="n">${s.lead}</div><div class="l">Typical lead time</div></div>
      <div class="pstat"><div class="n">${s.response}</div><div class="l">Response time</div></div>
      <div class="pstat"><div class="n">${s.founded}</div><div class="l">Established</div></div>
    </div>

    <div class="prof-grid">
      <div>
        <div class="prof-block">
          <h3><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="12" cy="12" r="10"/><path d="M12 16v-4M12 8h.01"/></svg> About</h3>
          <p>${s.about}</p>
        </div>

        <div class="prof-block">
          <h3><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M12 2l2 5 5 .5-4 3.5 1 5-4-2.5L8 16l1-5L5 7.5 10 7z"/></svg> Capabilities</h3>
          <div class="cap-grid">${s.capabilities.map(c => `<span class="cap">${check} ${c}</span>`).join('')}</div>
        </div>

        <div class="prof-block">
          <h3><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><rect x="3" y="3" width="18" height="18" rx="2"/><path d="M3 9h18M9 21V9"/></svg> Applications served</h3>
          <div class="cap-grid">${s.cases.map(c => `<span class="cap">${CASE_LABEL[c]}</span>`).join('')} ${s.formats.map(f => `<span class="sup-tag" style="padding:8px 14px">${f}</span>`).join('')}</div>
        </div>

        <div class="prof-block">
          <h3><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6M9 13l2 2 4-4"/></svg> Case studies</h3>
          ${s.caseStudies.map(cs => `<div class="cs-card"><div class="sector">${cs.sector}</div><h4>${cs.title}</h4><div class="result"><svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><polyline points="22 7 13.5 15.5 8.5 10.5 2 17"/><polyline points="16 7 22 7 22 13"/></svg> ${cs.result}</div></div>`).join('')}
        </div>

        <div class="prof-block" style="margin-bottom:0">
          <h3><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg> Buyer reviews</h3>
          <div class="rate-summary">
            <div class="rate-big">${s.rating}</div>
            <div>${stars(s.rating, 18)}<div class="mono-note" style="margin-top:.4rem">Based on ${s.reviews} verified buyer reviews</div></div>
          </div>
          ${s.reviewList.map(r => `<div class="review">${stars(r.rating)}<p>“${r.text}”</p><div class="who"><b>${r.author}</b> · ${r.company}</div></div>`).join('')}
        </div>
      </div>

      <aside>
        <div class="prof-side">
          <h4>At a glance</h4>
          <div class="row"><span class="k">Tier</span><span class="v">${s.tier}</span></div>
          <div class="row"><span class="k">Region</span><span class="v">${s.region.toUpperCase()}</span></div>
          <div class="row"><span class="k">Team size</span><span class="v">${s.team}</span></div>
          <div class="row"><span class="k">Lead time</span><span class="v">${s.lead}</span></div>
          <div class="row"><span class="k">Environments</span><span class="v">${s.environments.join(', ')}</span></div>
          <div class="row"><span class="k">Certifications</span><span class="v">${s.certs.join(', ')}</span></div>
          <a href="brief.html" class="btn btn-primary btn-block" style="margin-top:1.3rem">Request introduction</a>
          <p class="mono-note" style="text-align:center;margin-top:.9rem">// free for buyers</p>
        </div>
      </aside>
    </div>`;
})();
