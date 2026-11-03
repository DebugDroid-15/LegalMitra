/**
 * Phase 103: Tri-Code Redline Diff & Statutory Transition Visualizer Modal Controller
 */
(function() {
    function initRedlineVisualizer() {
        if (document.getElementById('redline-diff-modal')) return;

        const modalHtml = `
        <div id="redline-diff-modal" class="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm hidden">
            <div class="bg-surface-elevated border border-border-default rounded-2xl p-6 w-full max-w-3xl shadow-2xl mx-4 max-h-[90vh] overflow-y-auto">
                <div class="flex items-center justify-between pb-4 border-b border-border-default">
                    <div class="flex items-center space-x-3">
                        <span class="material-symbols-outlined text-primary text-2xl">compare</span>
                        <div>
                            <h3 class="text-base font-semibold text-text-primary">Tri-Code Redline & Transition Visualizer</h3>
                            <p class="text-xs text-text-secondary">Side-by-side textual diffs: IPC ↔ BNS, CrPC ↔ BNSS, IEA ↔ BSA</p>
                        </div>
                    </div>
                    <button id="close-redline-btn" class="text-text-secondary hover:text-text-primary">
                        <span class="material-symbols-outlined">close</span>
                    </button>
                </div>

                <div class="mt-4 space-y-4">
                    <div class="grid grid-cols-2 gap-3">
                        <div class="space-y-1">
                            <label class="block text-xs font-semibold text-text-secondary uppercase">Legacy Section</label>
                            <select id="legacy-select" class="w-full bg-surface-base border border-border-default rounded-xl px-3 py-2 text-xs text-text-primary focus:outline-none">
                                <option value="IPC:420:BNS:318(4)">IPC 420 (Cheating) ➔ BNS 318(4)</option>
                                <option value="IPC:302:BNS:103(1)">IPC 302 (Murder) ➔ BNS 103(1)</option>
                                <option value="IPC:124A:BNS:152">IPC 124A (Sedition) ➔ BNS 152 (Sovereignty)</option>
                                <option value="CrPC:154:BNSS:173">CrPC 154 (FIR) ➔ BNSS 173 (e-FIR)</option>
                            </select>
                        </div>
                        <div class="flex items-end">
                            <button id="render-diff-btn" class="w-full bg-primary hover:bg-primary-hover text-white py-2 px-4 rounded-xl text-xs font-semibold flex items-center justify-center gap-1.5 transition-colors">
                                <span class="material-symbols-outlined text-base">difference</span>
                                Compare Redline
                            </button>
                        </div>
                    </div>

                    <div id="diff-results" class="hidden space-y-3 pt-3 border-t border-border-default">
                        <div class="flex items-center justify-between text-xs">
                            <span id="diff-badge" class="px-2.5 py-0.5 rounded-full font-semibold bg-emerald-500/20 text-emerald-400"></span>
                            <span class="text-text-secondary text-[11px]"><del class="text-red-400">Red Strikethrough</del> = Repealed | <ins class="text-emerald-400 no-underline font-semibold">Green</ins> = Added in 2024</span>
                        </div>

                        <div class="bg-surface-base p-4 rounded-xl border border-border-default text-xs leading-relaxed font-mono" id="diff-text-box">
                        </div>

                        <div>
                            <h5 class="text-xs font-semibold uppercase text-text-secondary mb-1">Substantive Reforms & Key Changes</h5>
                            <ul id="diff-changes-list" class="space-y-1 text-xs text-text-secondary list-disc pl-4"></ul>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        `;

        document.body.insertAdjacentHTML('beforeend', modalHtml);

        const modal = document.getElementById('redline-diff-modal');
        const closeBtn = document.getElementById('close-redline-btn');
        const renderBtn = document.getElementById('render-diff-btn');
        const select = document.getElementById('legacy-select');

        closeBtn.addEventListener('click', () => modal.classList.add('hidden'));

        renderBtn.addEventListener('click', async () => {
            const parts = select.value.split(':');
            renderBtn.disabled = true;
            renderBtn.innerHTML = '<span class="material-symbols-outlined text-sm animate-spin">sync</span> Diffing...';

            try {
                const res = await fetch('/api/v1/crosswalk/redline-diff', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        old_code: parts[0],
                        old_section: parts[1],
                        new_code: parts[2],
                        new_section: parts[3]
                    })
                });
                const data = await res.json();
                if (!res.ok) throw new Error(data.detail || 'Failed to compute diff');

                document.getElementById('diff-badge').innerText = `${data.old_code} §${data.old_section} ➔ ${data.new_code} §${data.new_section} (${data.equivalence_type})`;
                document.getElementById('diff-text-box').innerHTML = data.diff_html;

                const list = document.getElementById('diff-changes-list');
                list.innerHTML = '';
                data.key_substantive_changes.forEach(ch => {
                    const li = document.createElement('li');
                    li.innerText = ch;
                    list.appendChild(li);
                });

                document.getElementById('diff-results').classList.remove('hidden');
            } catch (err) {
                alert(err.message);
            } finally {
                renderBtn.disabled = false;
                renderBtn.innerHTML = '<span class="material-symbols-outlined text-base">difference</span> Compare Redline';
            }
        });

        window.openRedlineVisualizer = function() {
            modal.classList.remove('hidden');
            renderBtn.click();
        };
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initRedlineVisualizer);
    } else {
        initRedlineVisualizer();
    }
})();
