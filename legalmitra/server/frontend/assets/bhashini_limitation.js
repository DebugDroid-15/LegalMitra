// Phase 99: Statutory Limitation & Procedural Timeline Calculator UI Controller
window.openLimitationModal = function(initialCategory = "cheque_dishonour_138") {
    let modal = document.getElementById("modal-limitation-calculator");
    if (!modal) {
        modal = document.createElement("div");
        modal.id = "modal-limitation-calculator";
        modal.className = "fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4";
        modal.innerHTML = `
            <div class="bg-surface rounded-xl shadow-2xl max-w-3xl w-full p-6 flex flex-col max-h-[92vh] overflow-hidden border border-surface-container-high">
                <div class="flex items-center justify-between pb-3 border-b border-surface-container-high">
                    <div class="flex items-center gap-2">
                        <span class="material-symbols-outlined text-secondary text-[24px]">event_repeat</span>
                        <h3 class="font-headline-sm font-bold text-primary">Statutory Limitation & Procedural Timeline Calculator</h3>
                    </div>
                    <button onclick="document.getElementById('modal-limitation-calculator').remove()" class="p-1 rounded hover:bg-surface-container-high text-outline hover:text-primary">
                        <span class="material-symbols-outlined">close</span>
                    </button>
                </div>
                
                <div class="py-3 space-y-3 overflow-y-auto flex-1 font-body-sm text-on-surface">
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
                        <div>
                            <label class="block font-label-md font-semibold text-primary mb-1">Dispute / Proceeding Category</label>
                            <select id="lim-category" class="w-full p-2 rounded border border-outline-variant bg-surface-container-lowest font-body-sm text-on-surface focus:outline-none focus:ring-1 focus:ring-primary">
                                <option value="cheque_dishonour_138">Sec 138 NI Act - Cheque Dishonour (30-15-30 Triad)</option>
                                <option value="consumer_complaint">Consumer Protection Act 2019 (2-Year Limitation)</option>
                                <option value="arbitration_award_challenge">Sec 34 Arbitration Act (Strict 3 Months + 30 Days)</option>
                                <option value="high_court_appeal_civil">Civil First Appeal to High Court (90 Days - Art 116)</option>
                                <option value="money_recovery_debt">Civil Suit for Money Recovery (3 Years - Art 19-21)</option>
                            </select>
                        </div>
                        <div>
                            <label class="block font-label-md font-semibold text-primary mb-1">Cause of Action / Incident / Memo Date</label>
                            <input id="lim-date" type="date" class="w-full p-2 rounded border border-outline-variant bg-surface-container-lowest font-body-sm text-on-surface" value="${new Date().toISOString().split('T')[0]}"/>
                        </div>
                    </div>

                    <div class="flex items-center justify-between pt-1">
                        <button id="lim-run-btn" onclick="executeLimitationCalculation()" class="px-5 py-2 rounded bg-primary text-on-primary font-label-md font-semibold hover:bg-primary-container transition-all flex items-center gap-1.5 shadow-sm">
                            <span class="material-symbols-outlined text-[18px]">calendar_month</span>
                            <span>Calculate Deadlines</span>
                        </button>
                        <span id="lim-status-msg" class="text-xs text-secondary font-medium"></span>
                    </div>

                    <!-- Result Card -->
                    <div id="lim-result-box" class="hidden mt-3 p-4 rounded bg-surface-container-low border border-surface-container-high space-y-3">
                        <div class="flex items-center justify-between">
                            <div>
                                <span id="lim-res-cat" class="font-bold text-primary text-sm block"></span>
                                <span id="lim-res-statute" class="text-xs text-outline block"></span>
                            </div>
                            <div id="lim-badge-status" class="px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider"></div>
                        </div>

                        <!-- Days Remaining Highlight -->
                        <div class="grid grid-cols-2 md:grid-cols-4 gap-2 text-center">
                            <div class="p-2 rounded bg-white border border-surface-container-high">
                                <span class="text-xs text-outline block">Cause Date</span>
                                <span id="lim-card-start" class="font-bold text-primary text-xs"></span>
                            </div>
                            <div class="p-2 rounded bg-white border border-surface-container-high">
                                <span class="text-xs text-outline block">Final Expiry</span>
                                <span id="lim-card-expiry" class="font-bold text-primary text-xs"></span>
                            </div>
                            <div class="p-2 rounded bg-white border border-surface-container-high">
                                <span class="text-xs text-outline block">Days Remaining</span>
                                <span id="lim-card-days" class="font-bold text-lg"></span>
                            </div>
                            <div class="p-2 rounded bg-white border border-surface-container-high">
                                <span class="text-xs text-outline block">Condonation</span>
                                <span id="lim-card-condonation" class="font-bold text-xs"></span>
                            </div>
                        </div>

                        <!-- Stepper Milestones -->
                        <div>
                            <span class="font-label-md font-semibold text-primary block mb-2">Statutory Milestone Progression</span>
                            <div id="lim-milestones-list" class="space-y-2"></div>
                        </div>

                        <!-- Advocate Advice -->
                        <div class="p-3 bg-amber-50 rounded border border-amber-200 text-xs text-amber-900 leading-relaxed">
                            <span class="font-bold block mb-1">Judicial Note &amp; Section 5 Guidance:</span>
                            <span id="lim-adv-advice"></span>
                        </div>
                    </div>
                </div>
            </div>
        `;
        document.body.appendChild(modal);
    }
    if (initialCategory) {
        const sel = document.getElementById("lim-category");
        if (sel) sel.value = initialCategory;
    }
};

window.executeLimitationCalculation = async function() {
    const btn = document.getElementById("lim-run-btn");
    const resultBox = document.getElementById("lim-result-box");
    const statusMsg = document.getElementById("lim-status-msg");

    btn.disabled = true;
    btn.innerHTML = '<span class="material-symbols-outlined text-[18px] animate-spin">sync</span> Calculating...';

    const payload = {
        category: document.getElementById("lim-category").value,
        incident_date: document.getElementById("lim-date").value
    };

    try {
        const res = await fetch("/api/v1/calculators/limitation", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });
        const data = await res.json();
        if (data.success) {
            resultBox.classList.remove("hidden");
            document.getElementById("lim-res-cat").innerText = data.dispute_category;
            document.getElementById("lim-res-statute").innerText = `${data.primary_enactment} (${data.statutory_citation})`;

            const badge = document.getElementById("lim-badge-status");
            if (data.is_time_barred) {
                badge.className = "px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider bg-red-100 text-red-800 border border-red-300";
                badge.innerText = "Time Barred";
            } else if (data.days_remaining <= 15) {
                badge.className = "px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider bg-amber-100 text-amber-800 border border-amber-300";
                badge.innerText = "Expiring Soon";
            } else {
                badge.className = "px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider bg-emerald-100 text-emerald-800 border border-emerald-300";
                badge.innerText = "Within Limitation";
            }

            document.getElementById("lim-card-start").innerText = data.start_event_date;
            document.getElementById("lim-card-expiry").innerText = data.final_limitation_expiry_date;
            
            const daysEl = document.getElementById("lim-card-days");
            daysEl.innerText = `${data.days_remaining} Days`;
            daysEl.className = data.is_time_barred ? "font-bold text-lg text-red-700" : (data.days_remaining <= 15 ? "font-bold text-lg text-amber-700" : "font-bold text-lg text-emerald-700");

            const condEl = document.getElementById("lim-card-condonation");
            condEl.innerText = data.is_condonation_of_delay_permissible ? "Permissible (Sec 5)" : "Strict Bar";
            condEl.className = data.is_condonation_of_delay_permissible ? "font-bold text-xs text-emerald-700" : "font-bold text-xs text-red-700";

            // Render milestones
            const mList = document.getElementById("lim-milestones-list");
            mList.innerHTML = data.milestones.map(m => `
                <div class="p-2.5 bg-white rounded border border-surface-container-high flex items-start gap-3">
                    <div class="w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold shrink-0 ${
                        m.status === 'COMPLETED' ? 'bg-emerald-100 text-emerald-800' : (m.status === 'ACTIVE_ACTION_REQUIRED' ? 'bg-amber-100 text-amber-800 animate-pulse' : (m.status === 'TIME_BARRED' ? 'bg-red-100 text-red-800' : 'bg-surface-container text-outline'))
                    }">
                        ${m.step_number}
                    </div>
                    <div class="flex-1">
                        <div class="flex items-center justify-between">
                            <span class="font-semibold text-primary text-xs">${m.title}</span>
                            <span class="text-xs font-mono font-semibold text-secondary">Deadline: ${m.statutory_deadline_date}</span>
                        </div>
                        <div class="text-[11px] text-outline mt-0.5">${m.governing_section}</div>
                        <div class="text-xs text-on-surface mt-1">${m.instruction}</div>
                    </div>
                </div>
            `).join("");

            document.getElementById("lim-adv-advice").innerText = data.practical_advocate_advice;
        }
    } catch (e) {
        if (statusMsg) statusMsg.innerText = "Error: " + e.message;
    } finally {
        btn.disabled = false;
        btn.innerHTML = '<span class="material-symbols-outlined text-[18px]">calendar_month</span> Calculate Deadlines';
    }
};
