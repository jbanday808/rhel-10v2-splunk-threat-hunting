"use strict";
(() => {
  const $ = (q, base = document) => base.querySelector(q);
  const $$ = (q, base = document) => [...base.querySelectorAll(q)];
  const escape = value => String(value ?? "").replace(/[&<>"']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
  const source = (path, anchor = "") => `${LAB.repo}/blob/${LAB.commit}/${path}${anchor ? "#" + anchor : ""}`;
  const key = "banday-network-workbench-v1";
  const statuses = ["Pending", "Passed", "Blocked", "Failed"];
  const defaultRecord = () => ({checks: {}, reviewed: {}});
  let storageAvailable = true;
  let records = defaultRecord();
  try {
    const stored = JSON.parse(localStorage.getItem(key));
    if (stored && typeof stored === "object") {
      LAB.checks.forEach(c => {
        const v = stored.checks?.[c.id];
        if (v && typeof v === "object") records.checks[c.id] = {status: statuses.includes(v.status) ? v.status : "Pending", note: typeof v.note === "string" ? v.note.slice(0, 1200) : "", updated: typeof v.updated === "string" ? v.updated.slice(0, 50) : ""};
      });
      LAB.phases.forEach(p => { if (stored.reviewed?.[p.id] === true) records.reviewed[p.id] = true; });
    }
  } catch { storageAvailable = false; }

  const icons = {
    network:'<rect x="8" y="2" width="8" height="6" rx="1"/><path d="M12 8v5M4 13h16M4 13v3m16-3v3"/><rect x="1" y="16" width="6" height="5" rx="1"/><rect x="17" y="16" width="6" height="5" rx="1"/>',
    layers:'<path d="m12 3 10 5-10 5L2 8l10-5ZM2 12l10 5 10-5M2 16l10 5 10-5"/>',
    flow:'<path d="M3 6h17m-4-4 4 4-4 4M21 18H4m4-4-4 4 4 4"/>',
    steps:'<path d="M4 4h3v3H4zM11 5h9M4 11h3v3H4zM11 12h9M4 18h3v3H4zM11 19h9"/>',
    check:'<rect x="3" y="3" width="18" height="18" rx="4"/><path d="m7 12 3 3 7-7"/>',
    server:'<rect x="3" y="3" width="18" height="7" rx="2"/><rect x="3" y="14" width="18" height="7" rx="2"/><path d="M7 6h.01M7 17h.01M12 6h5M12 17h5"/>',
    flag:'<path d="M5 22V3m0 1c5-4 9 5 15 0v10c-6 5-10-4-15 0"/>',
    lock:'<rect x="5" y="10" width="14" height="11" rx="2"/><path d="M8 10V6a4 4 0 0 1 8 0v4M12 14v3"/>',
    monitor:'<rect x="2" y="3" width="20" height="14" rx="2"/><path d="M8 22h8m-4-5v5"/>',
    window:'<path d="M3 4h8v8H3zM14 4h7v8h-7zM3 15h8v6H3zM14 15h7v6h-7z"/>',
    shield:'<path d="M12 2 3 6v6c0 5 9 10 9 10s9-5 9-10V6l-9-4Z"/><path d="m8 12 3 3 5-6"/>',
    terminal:'<rect x="2" y="4" width="20" height="16" rx="3"/><path d="m6 9 4 3-4 3m7 0h5"/>',
    eye:'<path d="M1 12s4-7 11-7 11 7 11 7-4 7-11 7S1 12 1 12Z"/><circle cx="12" cy="12" r="3"/>',
    search:'<circle cx="10" cy="10" r="7"/><path d="m15 15 6 6"/>',
    info:'<circle cx="12" cy="12" r="10"/><path d="M12 10v7m0-11v1"/>',
    download:'<path d="M12 2v13m-5-5 5 5 5-5M3 16v6h18v-6"/>'
  };
  function hydrateIcons(base = document) {
    $$('[data-icon]', base).forEach(el => { el.innerHTML = `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${icons[el.dataset.icon] || icons.layers}</svg>`; });
  }
  let toastTimer;
  function toast(message) {
    const el = $('#toast'); el.textContent = message; el.hidden = false;
    clearTimeout(toastTimer); toastTimer = setTimeout(() => { el.hidden = true; }, 3500);
  }
  function persist() {
    try { localStorage.setItem(key, JSON.stringify(records)); storageAvailable = true; }
    catch { storageAvailable = false; toast("Browser storage is unavailable. Export to keep your progress."); }
  }
  function counts() {
    return Object.fromEntries(statuses.map(s => [s, LAB.checks.filter(c => (records.checks[c.id]?.status || "Pending") === s).length]));
  }
  function updateProgress() {
    const c = counts();
    $('#sidebar-passed').textContent = c.Passed;
    $('#sidebar-total').textContent = LAB.checks.length;
    $('#sidebar-bar').style.width = `${100 * c.Passed / LAB.checks.length}%`;
    const reviewed = LAB.phases.filter(p => records.reviewed[p.id]).length;
    $('#phase-progress').textContent = `${reviewed} of ${LAB.phases.length} phases reviewed`;
    $('#phase-bar').style.width = `${100 * reviewed / LAB.phases.length}%`;
    $('#validation-stats').innerHTML = statuses.map(s => `<div class="validation-stat"><span>${s}</span><strong>${c[s]}</strong></div>`).join("");
  }
  const names = {architecture:"Architecture",tools:"Tool library",traffic:"Traffic explorer",deployment:"Deployment",validation:"Validation",screenshots:"Screenshots"};
  let currentView;
  function navigate() {
    const candidate = location.hash.slice(1);
    const view = Object.hasOwn(names, candidate) ? candidate : "architecture";
    $$('.view').forEach(s => { s.hidden = s.id !== `view-${view}`; });
    $$('nav [data-view]').forEach(a => {
      a.classList.toggle('active', a.dataset.view === view);
      if (a.dataset.view === view) a.setAttribute('aria-current', 'page'); else a.removeAttribute('aria-current');
    });
    $('#breadcrumb').textContent = names[view];
    document.title = "TraceVector | James Banday";
    if (currentView && currentView !== view) { window.scrollTo({top:0,behavior:"instant"}); $('#main').focus({preventScroll:true}); }
    currentView = view;
  }
  window.addEventListener('hashchange', navigate);

  function showNode(id) {
    const n = LAB.nodes[id]; if (!n) return;
    $$('[data-node]').forEach(b => { b.classList.toggle('selected', b.dataset.node === id); b.setAttribute('aria-pressed', String(b.dataset.node === id)); });
    $('#node-detail').innerHTML = `<div class="eyebrow">${escape(n.label)}</div><h3>${escape(n.name)}</h3><span class="address-tag">${escape(n.ip)}</span><p class="node-description">${escape(n.description)}</p><div class="detail-label">ROLE & CONNECTIONS</div>${n.connections.map(([role, value]) => `<div class="connection-item"><span>${escape(role)}</span><code>${escape(value)}</code></div>`).join('')}<a class="text-link" href="${source(n.source)}" target="_blank" rel="noopener noreferrer">View source guide <span aria-hidden="true">↗</span></a>`;
  }
  $$('[data-node]').forEach(b => b.addEventListener('click', () => showNode(b.dataset.node)));
  function makeChips(target, options, selected, onChange) {
    target.innerHTML = options.map(label => `<button class="chip${label === selected ? ' active' : ''}" aria-pressed="${label === selected}" type="button" data-value="${escape(label)}">${escape(label)}</button>`).join('');
    $$('button', target).forEach(b => b.addEventListener('click', () => onChange(b.dataset.value)));
  }

  let toolFilter = "All tools", toolQuery = "";
  function renderTools() {
    makeChips($('#tool-filters'), ['All tools','Packets','Metadata','Alerts','Sessions','Files','Queries','SIEM'], toolFilter, value => { toolFilter = value; renderTools(); });
    const list = LAB.tools.filter(t => (toolFilter === 'All tools' || t.category === toolFilter) && `${t.name} ${t.role} ${t.output} ${t.category} ${t.install.text} ${t.configure.text} ${t.validate.text}`.toLowerCase().includes(toolQuery));
    $('#tool-results').textContent = `${list.length} OF ${LAB.tools.length} TOOLS${toolQuery ? ' · FILTERED RESULTS' : ' · EXPLORE A PERSPECTIVE'}`;
    $('#tool-grid').innerHTML = list.length ? list.map(t => `<button class="tool-card" data-tool="${t.id}" aria-label="Open ${escape(t.name)} setup and validation"><span class="tool-card-top"><span class="tool-mark">${escape(t.mark)}</span><span class="tool-category">${escape(t.category.toUpperCase())}</span></span><h2>${escape(t.name)}</h2><p>${escape(t.role)}</p><span class="tool-output"><span>${escape(t.output)}</span><span aria-hidden="true">↗</span></span></button>`).join('') : '<div class="empty-state">No tools match this search.<br><button class="outline-button" id="clear-tools">Clear filters</button></div>';
    $$('[data-tool]').forEach(b => b.addEventListener('click', () => openTool(b.dataset.tool)));
    $('#clear-tools')?.addEventListener('click', () => { toolFilter = 'All tools'; toolQuery = ''; $('#tool-search').value = ''; renderTools(); });
  }
  $('#tool-search').addEventListener('input', e => { toolQuery = e.target.value.trim().toLowerCase(); renderTools(); });

  let activeTool, activeStage = 'install';
  function openTool(id) { activeTool = LAB.tools.find(t => t.id === id); activeStage = 'install'; renderToolDialog(); $('#tool-dialog').showModal(); }
  function guideAnchor(step) {
    const anchors = {1:'step-1--confirm-the-vm-and-network',4:'step-4--generate-two-harmless-in-scope-dns-packets',5:'step-5--inspect-the-offline-packets',7:'step-7--install-the-official-zeek-container',9:'step-9--inspect-the-rules-and-confirm-the-kali-configuration',12:'step-12--prepare-docker-resources-and-the-example',20:'step-20--test-a-benign-marker-and-negative-control',21:'step-21--install-sigma-and-its-splunk-backend-in-an-isolated-environment',23:'step-23--prove-the-capture-point',25:'step-25--deploy-a-live-idsmetadata-sensor-only-after-review'};
    return anchors[step] || '';
  }
  function renderToolDialog() {
    const t = activeTool, stage = t[activeStage];
    $('#tool-dialog-body').innerHTML = `<div class="dialog-tool-heading"><span class="tool-mark">${escape(t.mark)}</span><div><h2 id="tool-dialog-title">${escape(t.name)}</h2><p>${escape(t.output)}</p></div></div><p class="dialog-description">${escape(t.role)}</p><div class="dialog-tabs" aria-label="Tool reference sections">${[['install','Installation'],['configure','Configuration'],['validate','Validation']].map(([id,label]) => `<button class="dialog-tab${activeStage === id ? ' active' : ''}" data-stage="${id}" aria-pressed="${activeStage === id}">${label}</button>`).join('')}</div><div class="tool-stage"><h3>${escape(stage.title)}</h3><p>${escape(stage.text)}</p><div class="code-box"><button class="copy-button" id="copy-command">${escape(stage.copyLabel || "Copy command")}</button><pre><code>${escape(stage.code)}</code></pre></div><p>${stage.context ? escape(stage.context) : 'Run in a Kali Bash terminal. Commands using <code>$LAB</code> and <code>$REPO</code> depend on the private workspace defined in runbook Step 3.'}</p></div><div class="tool-limit">${escape(t.limit)}</div><div class="dialog-source"><a class="text-link" href="${source(stage.source || t.source,stage.source ? "" : guideAnchor(t.step))}" target="_blank" rel="noopener noreferrer">Read the complete procedure ↗</a><a class="text-link" href="#validation" id="dialog-validation">Go to checklist ↗</a></div>`;
    $$('[data-stage]').forEach(b => b.addEventListener('click', () => { activeStage = b.dataset.stage; renderToolDialog(); $(`[data-stage="${activeStage}"]`).focus(); }));
    $('#copy-command').addEventListener('click', async e => {
      try { await navigator.clipboard.writeText(stage.code); e.target.textContent = 'Copied'; toast('Command copied. Review the source procedure before running.'); }
      catch { toast('Clipboard unavailable. Select and copy the command text.'); }
    });
    $('#dialog-validation').addEventListener('click', () => $('#tool-dialog').close());
  }
  $('#close-dialog').addEventListener('click', () => $('#tool-dialog').close());
  $('#tool-dialog').addEventListener('click', e => { if (e.target === $('#tool-dialog')) { const r=e.target.getBoundingClientRect(); if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom)e.target.close(); } });


  let attackStatus = 'Candidate';
  function renderAttack() {
    makeChips($('#attack-filters'), LAB.attack.examples.map(e => e.status), attackStatus, value => { attackStatus = value; renderAttack(); $(`#attack-filters [data-value="${attackStatus}"]`).focus(); });
    const e = LAB.attack.examples.find(e => e.status === attackStatus);
    $('#attack-example').innerHTML = `<div class="eyebrow">${escape(e.status.toUpperCase())} / SOURCE EXAMPLE</div><h3>${escape(e.name)}</h3><dl><dt>Hunt hypothesis</dt><dd>${escape(e.hypothesis)}</dd><dt>Required telemetry</dt><dd>${escape(e.telemetry)}</dd><dt>Coverage boundary</dt><dd>${escape(e.limit)}</dd></dl>${e.hunt ? `<a class="text-link" href="${source(e.hunt)}" target="_blank" rel="noopener noreferrer">Review the candidate SPL ↗</a>` : ''}`;
    $$('[data-source]').forEach(a => { a.href = source(a.dataset.source); });
  }

  let flowKind = 'All paths', flowProtocol = 'all', selectedFlow = 'forward';
  function renderFlows() {
    makeChips($('#traffic-kinds'), ['All paths','Documented lab','Offline exercise','Planned'], flowKind, value => { flowKind=value; renderFlows(); });
    const flows = LAB.flows.filter(f => (flowKind==='All paths'||f.kind===flowKind)&&(flowProtocol==='all'||f.protocol===flowProtocol));
    if (!flows.some(f => f.id === selectedFlow)) selectedFlow = flows[0]?.id;
    $('#flow-list').innerHTML = flows.length ? flows.map(f => `<button class="flow-item${f.id===selectedFlow?' active':''}" data-flow="${f.id}" aria-pressed="${f.id===selectedFlow}"><span class="flow-item-top"><span>${escape(f.title)}</span><span class="flow-port">${escape(f.port)}</span></span><small>${escape(f.from)} → ${escape(f.to)}</small><small class="kind-tag">${escape(f.kind)}</small></button>`).join('') : '<div class="empty-state">No paths match these filters.</div>';
    $$('[data-flow]').forEach(b => b.addEventListener('click', () => { selectedFlow=b.dataset.flow; renderFlows(); }));
    const f = LAB.flows.find(item => item.id === selectedFlow);
    $('#flow-detail').innerHTML = f ? `<div class="eyebrow">${escape(f.kind.toUpperCase())} / ${escape(f.port)}</div><h2>${escape(f.title)}</h2><div class="flow-pair"><div><strong>${escape(f.from)}</strong><span>${escape(f.fromName)}</span></div><span aria-hidden="true">→</span><div><strong>${escape(f.to)}</strong><span>${escape(f.toName)}</span></div></div><p>${escape(f.purpose)}</p><h3>WHAT TO VERIFY</h3><ul>${f.checks.map(c=>`<li>${escape(c)}</li>`).join('')}</ul><p class="inline-warning">${escape(f.limit)}</p><a class="text-link" href="${source(f.source)}" target="_blank" rel="noopener noreferrer">Open the source guide ↗</a>` : '<div class="eyebrow">NO MATCHING CONNECTION</div><h2>Adjust the filters.</h2><p>Try another traffic type or choose All protocols.</p>';
  }
  $('#protocol-filter').addEventListener('change', e => { flowProtocol=e.target.value; renderFlows(); });

  let phaseFilter = 'All phases';
  function renderPhases() {
    makeChips($('#phase-filters'), ['All phases','Prepare','Analyze','Optional live','Review'], phaseFilter, value => { phaseFilter=value; renderPhases(); });
    const openIds = new Set($$('.phase[open]').map(e=>e.dataset.phase));
    const list = LAB.phases.filter(p=>phaseFilter==='All phases'||p.stage===phaseFilter);
    $('#phase-list').innerHTML = list.map(p=>`<details class="phase" data-phase="${p.id}"${openIds.has(p.id)?' open':''}><summary><span class="phase-number">${p.number}</span><span class="phase-title"><strong>${escape(p.title)}</strong><small>${escape(p.steps)}</small></span><span class="phase-badge">${records.reviewed[p.id]?'Reviewed':escape(p.stage)}</span><span class="phase-chevron" aria-hidden="true">+</span></summary><div class="phase-content"><p>${escape(p.description)}</p><ul>${p.tasks.map(t=>`<li>${escape(t)}</li>`).join('')}</ul><p><strong>Accept when:</strong> ${escape(p.accept)}</p><div class="phase-actions"><label class="review-toggle"><input type="checkbox" data-reviewed="${p.id}"${records.reviewed[p.id]?' checked':''}>I reviewed this phase</label><a class="text-link" href="${source(LAB.guide,guideAnchor(p.step))}" target="_blank" rel="noopener noreferrer">Open source step ↗</a></div></div></details>`).join('');
    $$('[data-reviewed]').forEach(input=>input.addEventListener('change',()=>{records.reviewed[input.dataset.reviewed]=input.checked;persist();updateProgress();input.closest('.phase').querySelector('.phase-badge').textContent=input.checked?'Reviewed':LAB.phases.find(p=>p.id===input.dataset.reviewed).stage;}));
  }

  let validationFilter='All checks';
  function renderValidation() {
    makeChips($('#validation-filters'), ['All checks',...statuses], validationFilter, value=>{validationFilter=value;renderValidation();});
    const list=LAB.checks.filter(c=>validationFilter==='All checks'||(records.checks[c.id]?.status||'Pending')===validationFilter);
    $('#validation-list').innerHTML = list.length ? list.map(c=>{
      const v=records.checks[c.id]||{status:'Pending',note:'',updated:''};
      return `<article class="validation-item"><div class="validation-row"><span class="validation-index">${String(LAB.checks.indexOf(c)+1).padStart(2,'0')}</span><div class="validation-main"><h3>${escape(c.title)}</h3><p>${escape(c.detail)}</p><button class="validation-note-toggle" data-note-toggle="${c.id}" aria-expanded="false" aria-controls="note-${c.id}">${v.note?'Edit observation':'Add observation'} +</button></div><select class="status-select" data-check="${c.id}" data-status="${v.status}" aria-label="Status: ${escape(c.title)}">${statuses.map(s=>`<option${s===v.status?' selected':''}>${s}</option>`).join('')}</select></div><div class="note-editor" id="note-${c.id}" hidden><label for="input-${c.id}">Sanitized observation · versions, expected/actual result, private evidence reference</label><textarea id="input-${c.id}" data-note="${c.id}" maxlength="1200" placeholder="Record what you observed. Leave credentials and raw logs out.">${escape(v.note)}</textarea><div class="note-meta"><span data-save="${c.id}">${v.updated?'Last edited '+escape(new Date(v.updated).toLocaleString()):'No observation recorded'}</span><span>1,200 characters max</span></div></div></article>`;
    }).join('') : '<div class="empty-state">No checks with this status. Choose another filter.</div>';
    $$('[data-note-toggle]').forEach(b=>b.addEventListener('click',()=>{const editor=$(`#note-${b.dataset.noteToggle}`);editor.hidden=!editor.hidden;b.setAttribute('aria-expanded',String(!editor.hidden));if(!editor.hidden)$('textarea',editor).focus();}));
    $$('[data-check]').forEach(select=>select.addEventListener('change',()=>{
      const id=select.dataset.check;
      records.checks[id]={note:records.checks[id]?.note||'',status:select.value,updated:new Date().toISOString()};
      select.dataset.status=select.value;persist();updateProgress();
      if(validationFilter!=='All checks')renderValidation();
      toast(`Recorded as ${select.value.toLowerCase()}. ${storageAvailable?'Saved in this browser.':'Export to keep your progress.'}`);
    }));
    $$('[data-note]').forEach(textarea=>textarea.addEventListener('input',()=>{
      const id=textarea.dataset.note;
      records.checks[id]={status:records.checks[id]?.status||'Pending',note:textarea.value,updated:new Date().toISOString()};
      persist();$(`[data-save="${id}"]`).textContent=storageAvailable?'Saved in this browser':'Not saved · use Export checklist';
    }));
  }
  $('#export-validation').addEventListener('click',()=>{
    const content={lab:'RHEL 10.2 Splunk network defense lab',source_repository:LAB.repo,source_commit:LAB.commit,exported_at:new Date().toISOString(),record_type:'User-entered browser-local observations; not independently verified',checks:LAB.checks.map(c=>({id:c.id,title:c.title,expected:c.detail,status:records.checks[c.id]?.status||'Pending',observation:records.checks[c.id]?.note||'',updated_at:records.checks[c.id]?.updated||null})),reviewed_phases:LAB.phases.filter(p=>records.reviewed[p.id]).map(p=>p.title)};
    const url=URL.createObjectURL(new Blob([JSON.stringify(content,null,2)],{type:'application/json'}));
    const a=document.createElement('a');a.href=url;a.download=`network-lab-checklist-${new Date().toISOString().slice(0,10)}.json`;document.body.append(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),10000);toast('Checklist exported as JSON.');
  });
  $('#reset-validation').addEventListener('click',()=>$('#reset-dialog').showModal());
  $('#cancel-reset').addEventListener('click',()=>$('#reset-dialog').close());
  $('#confirm-reset').addEventListener('click',()=>{records.checks={};persist();updateProgress();renderValidation();$('#reset-dialog').close();toast('Validation statuses and notes reset.');});

  $('#top-repo').href=LAB.repo;
  $('#evidence-link').href=source(LAB.evidence);
  $('#snapshot-link').href=`${LAB.repo}/commit/${LAB.commit}`;
  $('#deployment-source').href=source(LAB.guide);
  hydrateIcons();showNode('splunk');renderTools();renderAttack();renderFlows();renderPhases();renderValidation();updateProgress();navigate();
})();
