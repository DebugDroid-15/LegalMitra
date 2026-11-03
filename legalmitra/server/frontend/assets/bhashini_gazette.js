/**
 * Phase 104: Pinpoint Gazette Source Peek & Citation Inspector Modal Controller
 */
(function() {
    function initGazetteInspector() {
        if (document.getElementById('gazette-inspector-modal')) return;

        const modalHtml = `
        <div id="gazette-inspector-modal" class="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm hidden">
            <div class="bg-surface-elevated border border-border-default rounded-2xl p-6 w-full max-w-2xl shadow-2xl mx-4 max-h-[90vh] overflow-y-auto">
                <div class="flex items-center justify-between pb-4 border-b border-border-default">
                    <div class="flex items-center space-x-3">
                        <span class="material-symbols-outlined text-primary text-2xl">verified</span>
                        <div>
                            <h3 class="text-base font-semibold text-text-primary">Gazette of India Source Inspector</h3>
                            <p class="text-xs text-text-secondary">Zero-hallucination statutory verification with official digital provenance</p>
                        </div>
                    </div>
                    <button id="close-gazette-btn" class="text-text-secondary hover:text-text-primary">
                        <span class="material-symbols-outlined">close</span>
                    </button>
                </div>

                <div class="mt-4 space-y-4">
                    <div class="flex gap-2">
                        <input id="gazette-statute-input" type="text" placeholder="Statute (e.g. BNS)" value="BNS" class="w-1/3 bg-surface-base border border-border-default rounded-xl px-3 py-2 text-xs font-mono uppercase focus:outline-none focus:border-primary text-text-primary" />
                        <input id="gazette-section-input" type="text" placeholder="Section (e.g. 318)" value="318" class="w-1/3 bg-surface-base border border-border-default rounded-xl px-3 py-2 text-xs font-mono focus:outline-none focus:border-primary text-text-primary" />
                        <button id="gazette-verify-btn" class="w-1/3 bg-primary hover:bg-primary-hover text-white py-2 px-3 rounded-xl text-xs font-semibold flex items-center justify-center gap-1 transition-colors shrink-0">
                            <span class="material-symbols-outlined text-base">verified_user</span>
                            Verify Gazette
                        </button>
                    </div>

                    <div id="gazette-result-container" class="space-y-3 pt-2">
                        <div class="bg-surface-base p-4 rounded-xl border border-border-default space-y-2">
                            <div class="flex justify-between items-start">
                                <div>
                                    <span id="gazette-act-title" class="text-xs font-bold text-primary block"></span>
                                    <h4 id="gazette-section-title" class="text-sm font-bold text-text-primary mt-0.5"></h4>
                                </div>
                                <span class="px-2 py-0.5 text-[10px] font-semibold rounded bg-emerald-500/20 text-emerald-400">IN FORCE</span>
                            </div>
                            <div class="text-[11px] text-text-secondary grid grid-cols-2 gap-2 pt-2 border-t border-border-default/50">
                                <div><span class="font-medium text-text-primary">Gazette No:</span> <span id="gazette-notif-no"></span></div>
                                <div><span class="font-medium text-text-primary">Gazette Date:</span> <span id="gazette-pub-date"></span></div>
                                <div><span class="font-medium text-text-primary">Commenced:</span> <span id="gazette-commence"></span></div>
                                <div><span class="font-medium text-text-primary">SHA-256 Seal:</span> <span id="gazette-hash" class="font-mono text-[10px]"></span></div>
                            </div>
                        </div>

                        <div>
                            <h5 class="text-xs font-semibold uppercase text-text-secondary mb-1 flex items-center gap-1">
                                <span class="material-symbols-outlined text-xs text-primary">menu_book</span>
                                Verbatim Gazette Text
                            </h5>
                            <pre id="gazette-verbatim-text" class="bg-surface-base border border-border-default p-3 rounded-xl text-xs text-text-primary whitespace-pre-wrap font-sans leading-relaxed"></pre>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        `;

        document.body.insertAdjacentHTML('beforeend', modalHtml);

        const modal = document.getElementById('gazette-inspector-modal');
        const closeBtn = document.getElementById('close-gazette-btn');
        const verifyBtn = document.getElementById('gazette-verify-btn');
        const statuteInput = document.getElementById('gazette-statute-input');
        const sectionInput = document.getElementById('gazette-section-input');

        closeBtn.addEventListener('click', () => modal.classList.add('hidden'));

        verifyBtn.addEventListener('click', async () => {
            const statute = statuteInput.value.trim();
            const section = sectionInput.value.trim();
            if (!statute || !section) return;

            verifyBtn.disabled = true;
            verifyBtn.innerHTML = '<span class="material-symbols-outlined text-sm animate-spin">sync</span> Verifying...';

            try {
                const res = await fetch('/api/v1/corpus/gazette-inspect', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ statute, section })
                });
                const data = await res.json();
                if (!res.ok) throw new Error(data.detail || 'Verification error');

                document.getElementById('gazette-act-title').innerText = data.statute_code;
                document.getElementById('gazette-section-title').innerText = `${data.section}: ${data.official_title}`;
                document.getElementById('gazette-notif-no').innerText = data.gazette_notification_no;
                document.getElementById('gazette-pub-date').innerText = data.gazette_date;
                document.getElementById('gazette-commence').innerText = data.commencement_date;
                document.getElementById('gazette-hash').innerText = data.digital_signature_hash;
                document.getElementById('gazette-verbatim-text').innerText = data.verbatim_text;
            } catch (err) {
                alert(err.message);
            } finally {
                verifyBtn.disabled = false;
                verifyBtn.innerHTML = '<span class="material-symbols-outlined text-base">verified_user</span> Verify Gazette';
            }
        });

        window.openGazetteInspector = function(statute, section) {
            if (statute) statuteInput.value = statute;
            if (section) sectionInput.value = section;
            modal.classList.remove('hidden');
            verifyBtn.click();
        };
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initGazetteInspector);
    } else {
        initGazetteInspector();
    }
})();
