// Phase 101/102: Court Fee, MACT & RERA Compensation Estimator UI Controller
// Supports Multi-Framework Selection & Comparative Valuation

const FINANCIAL_FRAMEWORKS = [
    {
        id: "mact_accident_compensation",
        label: "MACT Motor Accident Compensation",
        statute: "Motor Vehicles Act, 1988 (Sarla Verma & Pranay Sethi)",
        badge: "Accident / MACT",
        icon: "directions_car"
    },
    {
        id: "civil_court_fee",
        label: "Ad-Valorem State Civil Court Fees",
        statute: "State Court Fees Act (Maharashtra / Delhi / Karnataka / UP / TN)",
        badge: "Court Fees",
        icon: "account_balance"
    },
    {
        id: "rera_delayed_possession",
        label: "RERA Delayed Flat Possession Refund & Interest",
        statute: "Real Estate (Regulation and Development) Act, 2016 (Sec 18)",
        badge: "Real Estate / RERA",
        icon: "home_work"
    },
    {
        id: "cheque_138_recovery",
        label: "Sec 138 NI Act Recovery Limits & Penal Fines",
        statute: "Negotiable Instruments Act, 1881 (2x Cheque Amount / 20% Interim)",
        badge: "Cheque Dishonour",
        icon: "payments"
    }
];

window.financialEstimatorState = {
    selectedFrameworks: ["mact_accident_compensation"],
    dropdownOpen: false
};

window.openFinancialEstimatorModal = function(initialType = "mact_accident_compensation") {
    let modal = document.getElementById("modal-financial-estimator");
    if (modal) modal.remove();

    window.financialEstimatorState.selectedFrameworks = [initialType];
    window.financialEstimatorState.dropdownOpen = false;

    modal = document.createElement("div");
    modal.id = "modal-financial-estimator";
    modal.className = "fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-3 sm:p-4";
    modal.innerHTML = `
        <div class="bg-surface rounded-xl shadow-2xl max-w-4xl w-full p-5 sm:p-6 flex flex-col max-h-[92vh] overflow-hidden border border-surface-container-high transition-all">
            <!-- Modal Header -->
            <div class="flex items-center justify-between pb-3 border-b border-surface-container-high">
                <div class="flex items-center gap-2.5">
                    <div class="w-9 h-9 rounded-lg bg-primary/10 flex items-center justify-center text-primary">
                        <span class="material-symbols-outlined text-[22px]">calculate</span>
                    </div>
                    <div>
                        <h3 class="font-headline-sm font-bold text-primary leading-tight">Court Fee &amp; Statutory Compensation Estimator</h3>
                        <p class="text-[11px] text-outline">Multi-framework calculator under Supreme Court precedents &amp; Indian statutory schedules</p>
                    </div>
                </div>
                <button onclick="document.getElementById('modal-financial-estimator').remove()" class="p-1.5 rounded-lg hover:bg-surface-container-high text-outline hover:text-primary transition-colors">
                    <span class="material-symbols-outlined text-[20px]">close</span>
                </button>
            </div>
            
            <div class="py-3.5 space-y-4 overflow-y-auto flex-1 font-body-sm text-on-surface custom-scrollbar">
                <!-- Framework & Jurisdiction Selection Grid -->
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <!-- Multi-Select Frameworks -->
                    <div class="relative">
                        <div class="flex items-center justify-between mb-1">
                            <label class="block font-label-md font-semibold text-primary">Calculator Framework(s)</label>
                            <span class="text-[11px] text-secondary font-medium">Select one or multiple</span>
                        </div>
                        
                        <!-- Custom Multi-Select Dropdown Button -->
                        <div id="fin-framework-btn" onclick="toggleFrameworkDropdown(event)" class="w-full min-h-[42px] p-2 rounded-lg border border-outline-variant bg-surface-container-lowest font-body-sm text-on-surface cursor-pointer flex items-center justify-between gap-2 hover:border-primary transition-all">
                            <div id="fin-selected-tags" class="flex flex-wrap gap-1.5 items-center flex-1">
                                <!-- Tags injected via renderFrameworkTags() -->
                            </div>
                            <span class="material-symbols-outlined text-outline text-[20px] transition-transform duration-200" id="fin-dropdown-arrow">expand_more</span>
                        </div>

                        <!-- Dropdown Menu with Checkboxes -->
                        <div id="fin-framework-menu" class="hidden absolute top-[calc(100%+4px)] left-0 right-0 z-30 bg-surface-container-lowest rounded-lg border border-surface-container-high shadow-xl p-2 space-y-1 max-h-64 overflow-y-auto custom-scrollbar">
                            <div class="flex items-center justify-between px-2 py-1 text-[11px] text-outline font-semibold uppercase tracking-wider border-b border-surface-container-high mb-1">
                                <span>Available Calculators</span>
                                <button type="button" onclick="selectAllFrameworks(event)" class="text-secondary hover:underline normal-case">Select All</button>
                            </div>
                            ${FINANCIAL_FRAMEWORKS.map(fw => `
                                <label class="flex items-start gap-2.5 p-2 rounded-md hover:bg-surface-container-high cursor-pointer transition-colors text-xs text-on-surface">
                                    <input type="checkbox" value="${fw.id}" onchange="onFrameworkCheckboxChange(this)" class="mt-0.5 rounded border-outline-variant text-primary focus:ring-primary w-4 h-4 cursor-pointer" />
                                    <div class="flex-1">
                                        <div class="font-semibold text-primary flex items-center gap-1.5">
                                            <span>${fw.label}</span>
                                        </div>
                                        <div class="text-[11px] text-outline mt-0.5">${fw.statute}</div>
                                    </div>
                                </label>
                            `).join("")}
                        </div>
                    </div>

                    <!-- State Jurisdiction -->
                    <div>
                        <div class="flex items-center justify-between mb-1">
                            <label class="block font-label-md font-semibold text-primary">State / Territorial Jurisdiction</label>
                            <span class="text-[11px] text-outline">Governs State Court Fees</span>
                        </div>
                        <select id="fin-state" class="w-full h-[42px] px-3 py-2 rounded-lg border border-outline-variant bg-surface-container-lowest font-body-sm text-on-surface focus:outline-none focus:ring-1 focus:ring-primary">
                            <option value="maharashtra">Maharashtra (Bombay Court Fees Act, 1959)</option>
                            <option value="delhi">Delhi NCT (Court Fees Act, 1870 as applicable to Delhi)</option>
                            <option value="karnataka">Karnataka (Karnataka Court Fees &amp; Suits Valuation Act)</option>
                            <option value="tamil_nadu">Tamil Nadu (TN Court Fees &amp; Suits Valuation Act)</option>
                            <option value="uttar_pradesh">Uttar Pradesh (UP Court Fees Act)</option>
                            <option value="all_india_default">All-India / Central Jurisdiction Schedule</option>
                        </select>
                    </div>
                </div>

                <!-- Active Dynamic Parameter Panels -->
                <div id="fin-parameters-container" class="space-y-3">
                    <!-- MACT Parameters -->
                    <div id="panel-mact" class="p-3.5 bg-surface-container-low rounded-lg border border-surface-container-high space-y-2">
                        <div class="flex items-center gap-2 text-xs font-bold text-primary uppercase tracking-wider">
                            <span class="material-symbols-outlined text-[16px] text-secondary">directions_car</span>
                            <span>MACT Accident Compensation Parameters</span>
                        </div>
                        <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
                            <div>
                                <label class="block text-xs font-semibold text-on-surface-variant mb-1">Victim Age (Years)</label>
                                <input id="fin-mact-age" type="number" min="1" max="100" class="w-full p-2 rounded-md border border-outline-variant bg-white text-xs font-medium focus:ring-1 focus:ring-primary" value="32"/>
                            </div>
                            <div>
                                <label class="block text-xs font-semibold text-on-surface-variant mb-1">Monthly Income (INR)</label>
                                <input id="fin-mact-income" type="number" min="0" step="500" class="w-full p-2 rounded-md border border-outline-variant bg-white text-xs font-medium focus:ring-1 focus:ring-primary" value="45000"/>
                            </div>
                            <div>
                                <label class="block text-xs font-semibold text-on-surface-variant mb-1">Number of Dependents</label>
                                <input id="fin-mact-dependents" type="number" min="0" max="20" class="w-full p-2 rounded-md border border-outline-variant bg-white text-xs font-medium focus:ring-1 focus:ring-primary" value="3"/>
                            </div>
                        </div>
                        <div class="flex items-center gap-2 pt-1 text-xs text-outline">
                            <input id="fin-mact-employed" type="checkbox" checked class="rounded border-outline-variant text-primary focus:ring-primary w-3.5 h-3.5 cursor-pointer"/>
                            <label for="fin-mact-employed" class="cursor-pointer">Permanently employed / established income (Pranay Sethi future prospects addition)</label>
                        </div>
                    </div>

                    <!-- Monetary Claim Amount (Court Fee & Cheque 138) -->
                    <div id="panel-claim-amount" class="p-3.5 bg-surface-container-low rounded-lg border border-surface-container-high space-y-2">
                        <div class="flex items-center gap-2 text-xs font-bold text-primary uppercase tracking-wider">
                            <span class="material-symbols-outlined text-[16px] text-secondary">currency_rupee</span>
                            <span id="panel-claim-title">Suit Valuation / Cheque Recovery Amount</span>
                        </div>
                        <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
                            <div>
                                <label id="fin-claim-amount-label" class="block text-xs font-semibold text-on-surface-variant mb-1">Suit Valuation / Cheque Value (INR)</label>
                                <input id="fin-claim-amount" type="number" min="0" step="1000" class="w-full p-2 rounded-md border border-outline-variant bg-white text-xs font-medium focus:ring-1 focus:ring-primary" value="1500000"/>
                            </div>
                            <div class="flex flex-col justify-center text-xs text-outline leading-tight">
                                <span class="font-semibold text-primary mb-0.5">Statutory Ceilings &amp; Rates:</span>
                                <span>• Civil Court Fee: Ad-valorem graduated tariff (Max ₹3 Lakh in MH).</span>
                                <span>• NI Act 138: Penal fine up to 2× cheque value &amp; 20% interim relief.</span>
                            </div>
                        </div>
                    </div>

                    <!-- RERA Parameters -->
                    <div id="panel-rera" class="p-3.5 bg-surface-container-low rounded-lg border border-surface-container-high space-y-2">
                        <div class="flex items-center gap-2 text-xs font-bold text-primary uppercase tracking-wider">
                            <span class="material-symbols-outlined text-[16px] text-secondary">home_work</span>
                            <span>RERA Real Estate Delayed Possession Parameters</span>
                        </div>
                        <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
                            <div>
                                <label class="block text-xs font-semibold text-on-surface-variant mb-1">Total Amount Paid to Promoter/Builder (INR)</label>
                                <input id="fin-rera-paid" type="number" min="0" step="10000" class="w-full p-2 rounded-md border border-outline-variant bg-white text-xs font-medium focus:ring-1 focus:ring-primary" value="5000000"/>
                            </div>
                            <div>
                                <label class="block text-xs font-semibold text-on-surface-variant mb-1">Delay in Possession (Months)</label>
                                <input id="fin-rera-delay" type="number" min="1" max="240" class="w-full p-2 rounded-md border border-outline-variant bg-white text-xs font-medium focus:ring-1 focus:ring-primary" value="18"/>
                            </div>
                        </div>
                        <div class="text-[11px] text-outline">
                            Governed by Section 18 RERA: Prescribed statutory interest benchmarked at SBI Marginal Cost of Lending Rate (MCLR) + 2%.
                        </div>
                    </div>
                </div>

                <!-- Action Button & Calculation Status -->
                <div class="flex flex-col sm:flex-row items-center justify-between gap-3 pt-2">
                    <button id="fin-run-btn" onclick="executeFinancialCalculation()" class="w-full sm:w-auto px-6 py-2.5 rounded-lg bg-primary text-on-primary font-label-md font-semibold hover:bg-primary-container transition-all flex items-center justify-center gap-2 shadow-sm">
                        <span class="material-symbols-outlined text-[18px]">currency_rupee</span>
                        <span id="fin-calc-btn-text">Calculate Selected Frameworks</span>
                    </button>
                    <span id="fin-status-msg" class="text-xs text-secondary font-medium"></span>
                </div>

                <!-- Multi-Framework Results Container -->
                <div id="fin-result-box" class="hidden space-y-4 pt-1">
                    <div class="flex items-center justify-between border-b border-surface-container-high pb-2">
                        <div>
                            <span class="font-bold text-primary text-base block">Statutory Compensation &amp; Fee Results</span>
                            <span class="text-xs text-outline block">Calculated across selected frameworks</span>
                        </div>
                        <button onclick="copyAllEstimatorResults()" class="text-xs text-secondary hover:text-primary font-medium flex items-center gap-1">
                            <span class="material-symbols-outlined text-[16px]">content_copy</span>
                            <span>Copy Summary</span>
                        </button>
                    </div>

                    <!-- Dynamic Cards Generated Here -->
                    <div id="fin-results-grid" class="space-y-4"></div>
                </div>
            </div>
        </div>
    `;

    document.body.appendChild(modal);

    // Initial render of tags and panels
    renderFrameworkTags();
    syncFrameworkCheckboxes();
    updatePanelVisibility();

    // Close dropdown on outside click
    document.addEventListener("click", function handleOutsideClick(e) {
        const btn = document.getElementById("fin-framework-btn");
        const menu = document.getElementById("fin-framework-menu");
        if (menu && !menu.contains(e.target) && btn && !btn.contains(e.target)) {
            closeFrameworkDropdown();
        }
    });
};

window.toggleFrameworkDropdown = function(e) {
    if (e) e.stopPropagation();
    const menu = document.getElementById("fin-framework-menu");
    const arrow = document.getElementById("fin-dropdown-arrow");
    if (!menu) return;

    window.financialEstimatorState.dropdownOpen = !window.financialEstimatorState.dropdownOpen;
    if (window.financialEstimatorState.dropdownOpen) {
        menu.classList.remove("hidden");
        arrow.style.transform = "rotate(180deg)";
    } else {
        menu.classList.add("hidden");
        arrow.style.transform = "rotate(0deg)";
    }
};

window.closeFrameworkDropdown = function() {
    const menu = document.getElementById("fin-framework-menu");
    const arrow = document.getElementById("fin-dropdown-arrow");
    if (menu) menu.classList.add("hidden");
    if (arrow) arrow.style.transform = "rotate(0deg)";
    window.financialEstimatorState.dropdownOpen = false;
};

window.renderFrameworkTags = function() {
    const tagsBox = document.getElementById("fin-selected-tags");
    if (!tagsBox) return;

    const selected = window.financialEstimatorState.selectedFrameworks;
    if (selected.length === 0) {
        tagsBox.innerHTML = '<span class="text-outline text-xs italic">Select at least one framework...</span>';
        return;
    }

    tagsBox.innerHTML = selected.map(id => {
        const fw = FINANCIAL_FRAMEWORKS.find(f => f.id === id);
        if (!fw) return "";
        return `
            <span class="inline-flex items-center gap-1 px-2 py-0.5 rounded bg-primary/10 text-primary text-xs font-semibold">
                <span>${fw.badge}</span>
                <button type="button" onclick="removeFramework('${fw.id}', event)" class="hover:text-red-700 text-[14px] leading-none">&times;</button>
            </span>
        `;
    }).join("");

    const btnText = document.getElementById("fin-calc-btn-text");
    if (btnText) {
        btnText.innerText = `Calculate (${selected.length} Framework${selected.length > 1 ? 's' : ''})`;
    }
};

window.syncFrameworkCheckboxes = function() {
    const checkboxes = document.querySelectorAll("#fin-framework-menu input[type='checkbox']");
    checkboxes.forEach(cb => {
        cb.checked = window.financialEstimatorState.selectedFrameworks.includes(cb.value);
    });
};

window.onFrameworkCheckboxChange = function(cb) {
    const val = cb.value;
    let list = window.financialEstimatorState.selectedFrameworks;
    if (cb.checked) {
        if (!list.includes(val)) list.push(val);
    } else {
        list = list.filter(item => item !== val);
    }
    window.financialEstimatorState.selectedFrameworks = list;
    renderFrameworkTags();
    updatePanelVisibility();
};

window.removeFramework = function(id, e) {
    if (e) e.stopPropagation();
    let list = window.financialEstimatorState.selectedFrameworks;
    list = list.filter(item => item !== id);
    window.financialEstimatorState.selectedFrameworks = list;
    syncFrameworkCheckboxes();
    renderFrameworkTags();
    updatePanelVisibility();
};

window.selectAllFrameworks = function(e) {
    if (e) e.stopPropagation();
    window.financialEstimatorState.selectedFrameworks = FINANCIAL_FRAMEWORKS.map(f => f.id);
    syncFrameworkCheckboxes();
    renderFrameworkTags();
    updatePanelVisibility();
};

window.updatePanelVisibility = function() {
    const selected = window.financialEstimatorState.selectedFrameworks;
    const mactPanel = document.getElementById("panel-mact");
    const claimPanel = document.getElementById("panel-claim-amount");
    const reraPanel = document.getElementById("panel-rera");
    const claimTitle = document.getElementById("panel-claim-title");
    const claimLabel = document.getElementById("fin-claim-amount-label");

    if (mactPanel) {
        mactPanel.style.display = selected.includes("mact_accident_compensation") ? "block" : "none";
    }

    const needsClaim = selected.includes("civil_court_fee") || selected.includes("cheque_138_recovery");
    if (claimPanel) {
        claimPanel.style.display = needsClaim ? "block" : "none";
        if (selected.includes("civil_court_fee") && selected.includes("cheque_138_recovery")) {
            claimTitle.innerText = "Suit Valuation & Cheque Amount";
            claimLabel.innerText = "Claim Amount / Suit Valuation / Cheque Value (INR)";
        } else if (selected.includes("cheque_138_recovery")) {
            claimTitle.innerText = "Cheque Dishonour Face Value";
            claimLabel.innerText = "Bounced Cheque Face Value (INR)";
        } else {
            claimTitle.innerText = "Civil Suit Valuation";
            claimLabel.innerText = "Civil Suit Claim Amount / Valuation (INR)";
        }
    }

    if (reraPanel) {
        reraPanel.style.display = selected.includes("rera_delayed_possession") ? "block" : "none";
    }
};

window.executeFinancialCalculation = async function() {
    const selected = window.financialEstimatorState.selectedFrameworks;
    if (selected.length === 0) {
        alert("Please select at least one calculator framework.");
        return;
    }

    const btn = document.getElementById("fin-run-btn");
    const resultBox = document.getElementById("fin-result-box");
    const resultsGrid = document.getElementById("fin-results-grid");
    const statusMsg = document.getElementById("fin-status-msg");

    btn.disabled = true;
    btn.innerHTML = '<span class="material-symbols-outlined text-[18px] animate-spin">sync</span> Calculating...';
    statusMsg.innerText = `Executing ${selected.length} calculation${selected.length > 1 ? 's' : ''}...`;

    const commonPayload = {
        state: document.getElementById("fin-state").value,
        claim_amount: parseFloat(document.getElementById("fin-claim-amount")?.value || 0),
        victim_age: parseInt(document.getElementById("fin-mact-age")?.value || 30),
        monthly_income: parseFloat(document.getElementById("fin-mact-income")?.value || 30000),
        dependents_count: parseInt(document.getElementById("fin-mact-dependents")?.value || 3),
        is_permanent_employed: document.getElementById("fin-mact-employed")?.checked ?? true,
        total_amount_paid_to_builder: parseFloat(document.getElementById("fin-rera-paid")?.value || 5000000),
        delay_months: parseInt(document.getElementById("fin-rera-delay")?.value || 12)
    };

    try {
        const promises = selected.map(calcType => {
            const body = Object.assign({}, commonPayload, { calc_type: calcType });
            return fetch("/api/v1/calculators/court-fee", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(body)
            }).then(r => r.json());
        });

        const results = await Promise.all(promises);

        resultBox.classList.remove("hidden");
        statusMsg.innerText = "Calculation complete.";

        resultsGrid.innerHTML = results.map(data => {
            if (!data.success) {
                return `
                    <div class="p-3 bg-red-50 text-red-700 rounded-lg border border-red-200 text-xs">
                        Error calculating ${data.calc_type}: ${data.error || 'Statutory calculation failed'}
                    </div>
                `;
            }

            return `
                <div class="p-4 rounded-xl bg-surface-container-low border border-surface-container-high space-y-3 shadow-sm">
                    <div class="flex flex-col sm:flex-row sm:items-center justify-between border-b border-surface-container-high pb-2.5 gap-2">
                        <div>
                            <span class="font-bold text-primary text-sm flex items-center gap-1.5">
                                <span class="material-symbols-outlined text-[18px] text-secondary">check_circle</span>
                                <span>${data.calc_type}</span>
                            </span>
                            <span class="text-xs text-outline block mt-0.5">${data.primary_enactment} (${data.landmark_precedent || 'Statutory Schedule'})</span>
                        </div>
                        <div class="sm:text-right">
                            <span class="text-[11px] text-outline block">Statutory Total / Entitlement</span>
                            <span class="font-bold text-lg text-emerald-800">${data.formatted_total_inr}</span>
                        </div>
                    </div>

                    <div>
                        <span class="font-label-md font-semibold text-primary block mb-1.5 text-xs">Itemized Statutory Heads:</span>
                        <div class="space-y-1.5">
                            ${data.breakdown_heads.map(h => `
                                <div class="p-2.5 bg-white rounded-lg border border-surface-container-high">
                                    <div class="flex items-center justify-between">
                                        <span class="font-semibold text-xs text-primary">${h.head_name}</span>
                                        <span class="font-bold text-xs text-emerald-800">INR ${h.amount_inr.toLocaleString('en-IN')}</span>
                                    </div>
                                    <div class="text-[11px] text-outline mt-0.5">${h.statutory_governance}</div>
                                    <div class="text-[11px] text-on-surface-variant mt-0.5 italic">${h.calculation_breakdown}</div>
                                </div>
                            `).join("")}
                        </div>
                    </div>

                    <div class="p-3 bg-blue-50 rounded-lg border border-blue-200 text-xs text-blue-950 leading-relaxed">
                        <span class="font-bold block mb-1">Judicial Guidance &amp; Precedent:</span>
                        <span>${data.practical_guidance}</span>
                    </div>
                </div>
            `;
        }).join("");

        // Scroll to results cleanly
        resultBox.scrollIntoView({ behavior: 'smooth', block: 'start' });

    } catch (e) {
        alert("Calculation error: " + e.message);
        statusMsg.innerText = "Error during calculation.";
    } finally {
        btn.disabled = false;
        const count = selected.length;
        btn.innerHTML = `<span class="material-symbols-outlined text-[18px]">currency_rupee</span> <span>Calculate (${count} Framework${count > 1 ? 's' : ''})</span>`;
    }
};

window.copyAllEstimatorResults = function() {
    const resultsGrid = document.getElementById("fin-results-grid");
    if (!resultsGrid) return;
    const text = resultsGrid.innerText;
    navigator.clipboard.writeText(text).then(() => {
        alert("Calculation summary copied to clipboard!");
    }).catch(err => {
        alert("Failed to copy: " + err);
    });
};
