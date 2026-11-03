/**
 * Phase 102: e-Courts & NJDG Live CNR Case Tracker Modal Controller
 */
(function() {
    function initECourtsTracker() {
        if (document.getElementById('ecourts-tracker-modal')) return;

        const modalHtml = `
        <div id="ecourts-tracker-modal" class="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm hidden">
            <div class="bg-surface-elevated border border-border-default rounded-2xl p-6 w-full max-w-2xl shadow-2xl mx-4 max-h-[90vh] overflow-y-auto">
                <div class="flex items-center justify-between pb-4 border-b border-border-default">
                    <div class="flex items-center space-x-3">
                        <span class="material-symbols-outlined text-primary text-2xl">account_balance</span>
                        <div>
                            <h3 class="text-base font-semibold text-text-primary">e-Courts & NJDG Realtime Case Tracker</h3>
                            <p class="text-xs text-text-secondary">Instant status & AI order explainer across Indian Courts</p>
                        </div>
                    </div>
                    <button id="close-ecourts-btn" class="text-text-secondary hover:text-text-primary">
                        <span class="material-symbols-outlined">close</span>
                    </button>
                </div>

                <div class="mt-4 space-y-4">
                    <div>
                        <label class="block text-xs font-semibold text-text-secondary uppercase mb-1">16-Character CNR Number</label>
                        <div class="flex gap-2">
                            <input id="cnr-input" type="text" maxlength="16" placeholder="e.g. MHAU010012342023" class="w-full bg-surface-base border border-border-default rounded-xl px-4 py-2.5 text-sm font-mono tracking-wider focus:outline-none focus:border-primary text-text-primary uppercase" />
                            <button id="cnr-search-btn" class="bg-primary hover:bg-primary-hover text-white px-5 py-2.5 rounded-xl text-sm font-semibold flex items-center gap-1.5 transition-colors shrink-0">
                                <span class="material-symbols-outlined text-lg">search</span>
                                Track
                            </button>
                        </div>
                        <p class="text-[11px] text-text-secondary mt-1">Found on the top right of any High Court / District Court summons or receipt.</p>
                    </div>

                    <div id="cnr-result-container" class="hidden space-y-4 pt-3 border-t border-border-default">
                        <div class="bg-surface-base p-4 rounded-xl border border-border-default space-y-2">
                            <div class="flex justify-between items-start">
                                <div>
                                    <span id="case-badge" class="px-2 py-0.5 text-xs font-semibold rounded-md bg-primary/20 text-primary"></span>
                                    <h4 id="case-court" class="text-sm font-bold text-text-primary mt-1"></h4>
                                    <p id="case-parties" class="text-xs text-text-secondary mt-0.5 font-medium"></p>
                                </div>
                                <div class="text-right">
                                    <span class="text-[11px] text-text-secondary block">Next Hearing</span>
                                    <span id="case-next-date" class="text-xs font-bold text-amber-500"></span>
                                </div>
                            </div>
                        </div>

                        <div>
                            <h5 class="text-xs font-semibold uppercase text-text-secondary mb-1 flex items-center gap-1">
                                <span class="material-symbols-outlined text-sm text-primary">psychology</span>
                                Citizen Plain-Language Explanation
                            </h5>
                            <div id="case-plain-summary" class="bg-primary/5 border border-primary/20 p-3.5 rounded-xl text-xs text-text-primary leading-relaxed font-sans">
                            </div>
                        </div>

                        <div>
                            <h5 class="text-xs font-semibold uppercase text-text-secondary mb-1">Next Action Checklist</h5>
                            <ul id="case-advice-list" class="space-y-1.5 text-xs text-text-secondary list-disc pl-4"></ul>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        `;

        document.body.insertAdjacentHTML('beforeend', modalHtml);

        const modal = document.getElementById('ecourts-tracker-modal');
        const closeBtn = document.getElementById('close-ecourts-btn');
        const searchBtn = document.getElementById('cnr-search-btn');
        const cnrInput = document.getElementById('cnr-input');

        closeBtn.addEventListener('click', () => modal.classList.add('hidden'));

        searchBtn.addEventListener('click', async () => {
            const cnr = cnrInput.value.trim();
            if (cnr.length !== 16) {
                alert('Please enter a valid 16-character CNR number.');
                return;
            }
            searchBtn.disabled = true;
            searchBtn.innerHTML = '<span class="material-symbols-outlined text-lg animate-spin">sync</span> Tracking...';

            try {
                const res = await fetch('/api/v1/cases/track-cnr', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ cnr: cnr, target_lang: 'en' })
                });
                const data = await res.json();
                if (!res.ok) throw new Error(data.detail || 'Failed to track case');

                const c = data.case;
                document.getElementById('case-badge').innerText = c.case_type;
                document.getElementById('case-court').innerText = c.court_name;
                document.getElementById('case-parties').innerText = `${c.petitioner} vs ${c.respondent}`;
                document.getElementById('case-next-date').innerText = `${c.next_hearing_date} (${c.next_hearing_purpose})`;
                document.getElementById('case-plain-summary').innerText = c.plain_language_summary.en;

                const adviceList = document.getElementById('case-advice-list');
                adviceList.innerHTML = '';
                c.procedural_advice.forEach(adv => {
                    const li = document.createElement('li');
                    li.innerText = adv;
                    adviceList.appendChild(li);
                });

                document.getElementById('cnr-result-container').classList.remove('hidden');
            } catch (err) {
                alert(err.message);
            } finally {
                searchBtn.disabled = false;
                searchBtn.innerHTML = '<span class="material-symbols-outlined text-lg">search</span> Track';
            }
        });

        window.openECourtsTracker = function() {
            modal.classList.remove('hidden');
            cnrInput.focus();
        };
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initECourtsTracker);
    } else {
        initECourtsTracker();
    }
})();
