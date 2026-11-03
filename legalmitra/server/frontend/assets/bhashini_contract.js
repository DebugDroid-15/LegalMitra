/**
 * Phase 106: Commercial Contract Statutory Risk Auditor & Clause Redliner Modal Controller
 */
(function() {
    function initContractAuditor() {
        if (document.getElementById('contract-auditor-modal')) return;

        const modalHtml = `
        <div id="contract-auditor-modal" class="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm hidden">
            <div class="bg-surface-elevated border border-border-default rounded-2xl p-6 w-full max-w-4xl shadow-2xl mx-4 max-h-[92vh] overflow-y-auto">
                <div class="flex items-center justify-between pb-4 border-b border-border-default">
                    <div class="flex items-center space-x-3">
                        <span class="material-symbols-outlined text-primary text-2xl">description</span>
                        <div>
                            <h3 class="text-base font-semibold text-text-primary">Commercial Contract Risk Auditor & Redliner</h3>
                            <p class="text-xs text-text-secondary">Statutory checks under Indian Contract Act, Arbitration Act & DOCX track changes</p>
                        </div>
                    </div>
                    <button id="close-contract-btn" class="text-text-secondary hover:text-text-primary">
                        <span class="material-symbols-outlined">close</span>
                    </button>
                </div>

                <div class="mt-4 space-y-4">
                    <div class="space-y-2">
                        <div class="flex gap-2">
                            <input id="contract-title-input" type="text" class="w-full bg-surface-base border border-border-default rounded-xl px-3 py-2 text-xs text-text-primary focus:outline-none" value="Master Service Agreement (Vendor / Consultant)" placeholder="Contract Title" />
                        </div>
                        <textarea id="contract-raw-text" rows="5" class="w-full bg-surface-base border border-border-default rounded-xl p-3 text-xs text-text-primary font-mono focus:outline-none focus:border-primary" placeholder="Paste contract text or clauses here...">1. Non-compete: Consultant shall not directly or indirectly engage in any competing venture for 2 years post-termination.
2. Dispute Resolution: All disputes shall be settled by a sole arbitrator appointed solely and exclusively by the Company Managing Director.
3. Limitation: Any claims must be brought within 60 days of dispute, failing which right to sue is permanently waived.</textarea>
                        <div class="flex justify-between items-center pt-1">
                            <span class="text-[11px] text-text-secondary">Checks: Sec 27 (Non-compete), Sec 28 (Limitation bar), Perkins Eastman (Arbitrator bias), Sec 74 (Penalties)</span>
                            <button id="run-contract-audit-btn" class="bg-primary hover:bg-primary-hover text-white py-2 px-5 rounded-xl text-xs font-semibold flex items-center justify-center gap-1.5 transition-colors">
                                <span class="material-symbols-outlined text-base">rule</span>
                                Audit & Redline Contract
                            </button>
                        </div>
                    </div>

                    <div id="contract-audit-results" class="hidden space-y-4 pt-3 border-t border-border-default">
                        <div class="bg-surface-base p-4 rounded-xl border border-border-default flex justify-between items-center">
                            <div>
                                <span id="audit-verdict-badge" class="px-2.5 py-0.5 rounded-full text-xs font-bold bg-rose-500/20 text-rose-400"></span>
                                <h4 id="audit-title-display" class="text-sm font-bold text-text-primary mt-1"></h4>
                                <p id="audit-score-summary" class="text-xs text-text-secondary mt-0.5"></p>
                            </div>
                            <div id="audit-download-container" class="shrink-0">
                                <a id="audit-docx-download" href="#" target="_blank" class="bg-primary/20 hover:bg-primary/30 text-primary border border-primary/30 px-3 py-2 rounded-xl text-xs font-semibold flex items-center gap-1.5 transition-colors">
                                    <span class="material-symbols-outlined text-base">download</span>
                                    Download Redline DOCX
                                </a>
                            </div>
                        </div>

                        <div>
                            <h5 class="text-xs font-semibold uppercase text-text-secondary mb-2">Flagged Clauses & Balanced Counter-Proposals</h5>
                            <div id="audit-clauses-container" class="space-y-3"></div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        `;

        document.body.insertAdjacentHTML('beforeend', modalHtml);

        const modal = document.getElementById('contract-auditor-modal');
        const closeBtn = document.getElementById('close-contract-btn');
        const auditBtn = document.getElementById('run-contract-audit-btn');
        const titleInput = document.getElementById('contract-title-input');
        const textInput = document.getElementById('contract-raw-text');

        closeBtn.addEventListener('click', () => modal.classList.add('hidden'));

        auditBtn.addEventListener('click', async () => {
            const contract_text = textInput.value.trim();
            if (!contract_text) return;

            auditBtn.disabled = true;
            auditBtn.innerHTML = '<span class="material-symbols-outlined text-sm animate-spin">sync</span> Auditing Contract...';

            try {
                const res = await fetch('/api/v1/contract/audit-full', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        contract_text: contract_text,
                        contract_title: titleInput.value.trim(),
                        generate_docx: true
                    })
                });
                const data = await res.json();
                if (!res.ok) throw new Error(data.detail || 'Audit failed');

                document.getElementById('audit-verdict-badge').innerText = data.overall_compliance_verdict;
                document.getElementById('audit-title-display').innerText = data.contract_title;
                document.getElementById('audit-score-summary').innerText = `Risk Score: ${data.composite_risk_score}/100 | Critical Void: ${data.critical_risks_count} | High Risk: ${data.high_risks_count}`;

                if (data.docx_download_url) {
                    document.getElementById('audit-docx-download').href = data.docx_download_url;
                    document.getElementById('audit-download-container').classList.remove('hidden');
                }

                const clausesContainer = document.getElementById('audit-clauses-container');
                clausesContainer.innerHTML = '';

                data.analyzed_clauses.forEach(cl => {
                    const card = document.createElement('div');
                    card.className = 'bg-surface-base p-4 rounded-xl border border-border-default space-y-2';
                    const badgeColor = cl.risk_level === 'CRITICAL' ? 'bg-red-500/20 text-red-400' : 'bg-amber-500/20 text-amber-400';

                    card.innerHTML = `
                        <div class="flex justify-between items-start">
                            <span class="text-xs font-bold text-text-primary flex items-center gap-2">
                                <span class="px-2 py-0.5 rounded text-[10px] font-semibold ${badgeColor}">${cl.risk_level}</span>
                                ${cl.clause_title}
                            </span>
                            <span class="text-[11px] text-text-secondary font-mono">${cl.statutory_reference}</span>
                        </div>
                        <p class="text-[11px] text-text-secondary">${cl.risk_summary} <em>(${cl.judicial_authority})</em></p>
                        
                        <div class="pt-2 border-t border-border-default/40 space-y-1.5 text-xs">
                            <div class="p-2.5 rounded-lg bg-red-500/5 border border-red-500/20">
                                <span class="text-[10px] uppercase font-bold text-red-400 block mb-0.5">Original Vulnerable Clause:</span>
                                <del class="text-text-secondary line-through block font-mono text-[11px]">${cl.original_clause}</del>
                            </div>
                            <div class="p-2.5 rounded-lg bg-emerald-500/5 border border-emerald-500/20">
                                <span class="text-[10px] uppercase font-bold text-emerald-400 block mb-0.5">Recommended Statutory Replacement:</span>
                                <ins class="text-text-primary no-underline block font-mono text-[11px]">${cl.balanced_counter_clause}</ins>
                            </div>
                        </div>
                    `;
                    clausesContainer.appendChild(card);
                });

                document.getElementById('contract-audit-results').classList.remove('hidden');
            } catch (err) {
                alert(err.message);
            } finally {
                auditBtn.disabled = false;
                auditBtn.innerHTML = '<span class="material-symbols-outlined text-base">rule</span> Audit & Redline Contract';
            }
        });

        window.openContractAuditor = function() {
            modal.classList.remove('hidden');
        };
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initContractAuditor);
    } else {
        initContractAuditor();
    }
})();
