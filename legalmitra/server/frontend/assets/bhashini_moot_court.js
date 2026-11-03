/**
 * Phase 105: Multi-Agent Adversarial Moot Court Simulator Modal Controller
 */
(function() {
    function initMootCourtSimulator() {
        if (document.getElementById('moot-court-modal')) return;

        const modalHtml = `
        <div id="moot-court-modal" class="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm hidden">
            <div class="bg-surface-elevated border border-border-default rounded-2xl p-6 w-full max-w-4xl shadow-2xl mx-4 max-h-[92vh] overflow-y-auto">
                <div class="flex items-center justify-between pb-4 border-b border-border-default">
                    <div class="flex items-center space-x-3">
                        <span class="material-symbols-outlined text-primary text-2xl">gavel</span>
                        <div>
                            <h3 class="text-base font-semibold text-text-primary">Multi-Agent Adversarial "Moot Court" Simulator</h3>
                            <p class="text-xs text-text-secondary">Simulate Prosecution vs Defence arguments with Presiding Bench risk assessment</p>
                        </div>
                    </div>
                    <button id="close-moot-btn" class="text-text-secondary hover:text-text-primary">
                        <span class="material-symbols-outlined">close</span>
                    </button>
                </div>

                <div class="mt-4 space-y-4">
                    <div class="space-y-2">
                        <label class="block text-xs font-semibold text-text-secondary uppercase">Dispute Topic & Summary</label>
                        <select id="moot-category-select" class="w-full bg-surface-base border border-border-default rounded-xl px-3 py-2 text-xs text-text-primary focus:outline-none mb-2">
                            <option value="Criminal Breach & Cheating">Cheating & Financial Misappropriation (BNS 316 / 318)</option>
                            <option value="Cheque Dishonour 138 NI Act">Cheque Dishonour & Incomplete Funds (Section 138 NI Act)</option>
                            <option value="Contractual Dispute">Breach of Commercial Agreement & Injunction</option>
                        </select>
                        <textarea id="moot-facts-input" rows="2" class="w-full bg-surface-base border border-border-default rounded-xl p-3 text-xs text-text-primary focus:outline-none focus:border-primary" placeholder="Summarize facts (e.g. Accused collected advance payment for commercial consignment and ceased communications)...">Accused promised delivery of raw materials, accepted Rs 5,00,000 in bank transfer, but failed to deliver and blocked phone calls.</textarea>
                        <button id="run-moot-btn" class="bg-primary hover:bg-primary-hover text-white py-2.5 px-5 rounded-xl text-xs font-semibold flex items-center justify-center gap-1.5 transition-colors">
                            <span class="material-symbols-outlined text-base">balance</span>
                            Commence Moot Court Simulation
                        </button>
                    </div>

                    <div id="moot-results" class="hidden space-y-4 pt-3 border-t border-border-default">
                        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                            <!-- Petitioner Counsel -->
                            <div class="bg-surface-base p-4 rounded-xl border border-blue-500/20 space-y-2">
                                <div class="flex items-center gap-2 text-blue-400 font-bold text-xs uppercase">
                                    <span class="material-symbols-outlined text-sm">record_voice_over</span>
                                    <span id="petitioner-role-title">Petitioner Submissions</span>
                                </div>
                                <h5 id="petitioner-statute" class="text-xs font-bold text-text-primary"></h5>
                                <ul id="petitioner-submissions-list" class="space-y-1 text-xs text-text-secondary list-disc pl-4"></ul>
                                <div class="pt-2 border-t border-border-default/40">
                                    <span class="text-[10px] text-text-secondary uppercase font-semibold block">Precedents Relied On:</span>
                                    <div id="petitioner-precedents" class="text-[11px] text-blue-300 font-mono"></div>
                                </div>
                            </div>

                            <!-- Defence Counsel -->
                            <div class="bg-surface-base p-4 rounded-xl border border-amber-500/20 space-y-2">
                                <div class="flex items-center gap-2 text-amber-400 font-bold text-xs uppercase">
                                    <span class="material-symbols-outlined text-sm">shield</span>
                                    <span id="defence-role-title">Defence Rebuttal</span>
                                </div>
                                <h5 id="defence-statute" class="text-xs font-bold text-text-primary"></h5>
                                <ul id="defence-submissions-list" class="space-y-1 text-xs text-text-secondary list-disc pl-4"></ul>
                                <div class="pt-2 border-t border-border-default/40">
                                    <span class="text-[10px] text-text-secondary uppercase font-semibold block">Precedents Relied On:</span>
                                    <div id="defence-precedents" class="text-[11px] text-amber-300 font-mono"></div>
                                </div>
                            </div>
                        </div>

                        <!-- Presiding Bench -->
                        <div class="bg-primary/5 p-4 rounded-xl border border-primary/20 space-y-3">
                            <div class="flex justify-between items-center">
                                <div class="flex items-center gap-2 text-primary font-bold text-xs uppercase">
                                    <span class="material-symbols-outlined text-base">gavel</span>
                                    <span id="bench-name-title">Presiding Judicial Bench</span>
                                </div>
                                <span id="verdict-likelihood-badge" class="px-2.5 py-0.5 rounded-full text-xs font-bold bg-primary/20 text-primary"></span>
                            </div>
                            <p id="bench-findings-text" class="text-xs text-text-primary leading-relaxed"></p>

                            <div class="grid grid-cols-1 md:grid-cols-2 gap-3 pt-2 border-t border-border-default/40">
                                <div>
                                    <span class="text-[11px] text-rose-400 font-bold block mb-1">Critical Vulnerabilities:</span>
                                    <ul id="bench-vulnerabilities-list" class="space-y-1 text-xs text-text-secondary list-disc pl-4"></ul>
                                </div>
                                <div>
                                    <span class="text-[11px] text-emerald-400 font-bold block mb-1">Suggested Evidentiary Steps:</span>
                                    <ul id="bench-evidence-list" class="space-y-1 text-xs text-text-secondary list-disc pl-4"></ul>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        `;

        document.body.insertAdjacentHTML('beforeend', modalHtml);

        const modal = document.getElementById('moot-court-modal');
        const closeBtn = document.getElementById('close-moot-btn');
        const runBtn = document.getElementById('run-moot-btn');
        const categorySelect = document.getElementById('moot-category-select');
        const factsInput = document.getElementById('moot-facts-input');

        closeBtn.addEventListener('click', () => modal.classList.add('hidden'));

        runBtn.addEventListener('click', async () => {
            runBtn.disabled = true;
            runBtn.innerHTML = '<span class="material-symbols-outlined text-sm animate-spin">sync</span> Simulating Proceedings...';

            try {
                const res = await fetch('/api/v1/simulation/moot-court', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        fact_summary: factsInput.value.trim(),
                        dispute_category: categorySelect.value
                    })
                });
                const data = await res.json();
                if (!res.ok) throw new Error(data.detail || 'Simulation failed');

                // Render Petitioner
                const p = data.petitioner_submission;
                document.getElementById('petitioner-role-title').innerText = `${p.role} (${p.advocate_name})`;
                document.getElementById('petitioner-statute').innerText = p.primary_statutory_basis;
                const pList = document.getElementById('petitioner-submissions-list');
                pList.innerHTML = '';
                p.core_submissions.forEach(sub => {
                    const li = document.createElement('li');
                    li.innerText = sub;
                    pList.appendChild(li);
                });
                document.getElementById('petitioner-precedents').innerText = p.precedents_relied_on.join(' • ');

                // Render Defence
                const d = data.defence_rebuttal;
                document.getElementById('defence-role-title').innerText = `${d.role} (${d.advocate_name})`;
                document.getElementById('defence-statute').innerText = d.primary_statutory_basis;
                const dList = document.getElementById('defence-submissions-list');
                dList.innerHTML = '';
                d.core_submissions.forEach(sub => {
                    const li = document.createElement('li');
                    li.innerText = sub;
                    dList.appendChild(li);
                });
                document.getElementById('defence-precedents').innerText = d.precedents_relied_on.join(' • ');

                // Render Bench
                const b = data.bench_ruling;
                document.getElementById('bench-name-title').innerText = b.bench_name;
                document.getElementById('verdict-likelihood-badge').innerText = b.probable_verdict_likelihood;
                document.getElementById('bench-findings-text').innerText = b.preliminary_findings;

                const vList = document.getElementById('bench-vulnerabilities-list');
                vList.innerHTML = '';
                b.critical_vulnerabilities.forEach(v => {
                    const li = document.createElement('li');
                    li.innerText = v;
                    vList.appendChild(li);
                });

                const eList = document.getElementById('bench-evidence-list');
                eList.innerHTML = '';
                b.suggested_evidentiary_steps.forEach(e => {
                    const li = document.createElement('li');
                    li.innerText = e;
                    eList.appendChild(li);
                });

                document.getElementById('moot-results').classList.remove('hidden');
            } catch (err) {
                alert(err.message);
            } finally {
                runBtn.disabled = false;
                runBtn.innerHTML = '<span class="material-symbols-outlined text-base">balance</span> Commence Moot Court Simulation';
            }
        });

        window.openMootCourtSimulator = function() {
            modal.classList.remove('hidden');
        };
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initMootCourtSimulator);
    } else {
        initMootCourtSimulator();
    }
})();
