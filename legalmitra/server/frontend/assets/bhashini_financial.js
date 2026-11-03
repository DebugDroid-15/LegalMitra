// Phase 101: Court Fee, MACT & RERA Compensation Estimator UI Controller
window.openFinancialEstimatorModal = function(initialType = "mact_accident_compensation") {
    let modal = document.getElementById("modal-financial-estimator");
    if (!modal) {
        modal = document.createElement("div");
        modal.id = "modal-financial-estimator";
        modal.className = "fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4";
        modal.innerHTML = `
            <div class="bg-surface rounded-xl shadow-2xl max-w-3xl w-full p-6 flex flex-col max-h-[92vh] overflow-hidden border border-surface-container-high">
                <div class="flex items-center justify-between pb-3 border-b border-surface-container-high">
                    <div class="flex items-center gap-2">
                        <span class="material-symbols-outlined text-secondary text-[24px]">calculate</span>
                        <h3 class="font-headline-sm font-bold text-primary">Court Fee &amp; Statutory Compensation Estimator</h3>
                    </div>
                    <button onclick="document.getElementById('modal-financial-estimator').remove()" class="p-1 rounded hover:bg-surface-container-high text-outline hover:text-primary">
                        <span class="material-symbols-outlined">close</span>
                    </button>
                </div>
                
                <div class="py-3 space-y-3 overflow-y-auto flex-1 font-body-sm text-on-surface">
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
                        <div>
                            <label class="block font-label-md font-semibold text-primary mb-1">Calculator Framework</label>
                            <select id="fin-calc-type" onchange="toggleFinancialInputs(this.value)" class="w-full p-2 rounded border border-outline-variant bg-surface-container-lowest font-body-sm text-on-surface focus:outline-none focus:ring-1 focus:ring-primary">
                                <option value="mact_accident_compensation">MACT Motor Accident Compensation (Sarla Verma &amp; Pranay Sethi)</option>
                                <option value="civil_court_fee">Ad-Valorem State Civil Court Fees (Maharashtra / Delhi)</option>
                                <option value="rera_delayed_possession">RERA Delayed Flat Possession Refund &amp; Interest (Sec 18)</option>
                                <option value="cheque_138_recovery">Sec 138 NI Act Recovery Limits (2x Cheque Amount)</option>
                            </select>
                        </div>
                        <div>
                            <label class="block font-label-md font-semibold text-primary mb-1">State / Jurisdiction</label>
                            <select id="fin-state" class="w-full p-2 rounded border border-outline-variant bg-surface-container-lowest font-body-sm text-on-surface">
                                <option value="maharashtra">Maharashtra</option>
                                <option value="delhi">Delhi (NCT)</option>
                                <option value="karnataka">Karnataka</option>
                                <option value="tamil_nadu">Tamil Nadu</option>
                                <option value="uttar_pradesh">Uttar Pradesh</option>
                            </select>
                        </div>
                    </div>

                    <!-- Dynamic Inputs: MACT Container -->
                    <div id="fin-mact-inputs" class="grid grid-cols-1 md:grid-cols-3 gap-3 p-3 bg-surface-container-low rounded border border-surface-container-high">
                        <div>
                            <label class="block text-xs font-semibold text-primary mb-1">Victim Age (Years)</label>
                            <input id="fin-mact-age" type="number" class="w-full p-1.5 rounded border border-outline-variant bg-white text-xs" value="32"/>
                        </div>
                        <div>
                            <label class="block text-xs font-semibold text-primary mb-1">Monthly Income (INR)</label>
                            <input id="fin-mact-income" type="number" class="w-full p-1.5 rounded border border-outline-variant bg-white text-xs" value="45000"/>
                        </div>
                        <div>
                            <label class="block text-xs font-semibold text-primary mb-1">Number of Dependents</label>
                            <input id="fin-mact-dependents" type="number" class="w-full p-1.5 rounded border border-outline-variant bg-white text-xs" value="3"/>
                        </div>
                    </div>

                    <!-- Dynamic Inputs: Civil / RERA Container -->
                    <div id="fin-generic-inputs" class="hidden grid grid-cols-1 md:grid-cols-2 gap-3 p-3 bg-surface-container-low rounded border border-surface-container-high">
                        <div>
                            <label id="fin-amount-label" class="block text-xs font-semibold text-primary mb-1">Claim Amount / Suit Valuation (INR)</label>
                            <input id="fin-claim-amount" type="number" class="w-full p-1.5 rounded border border-outline-variant bg-white text-xs" value="1500000"/>
                        </div>
                        <div id="fin-rera-months-container" class="hidden">
                            <label class="block text-xs font-semibold text-primary mb-1">Months of Delay in Flat Possession</label>
                            <input id="fin-delay-months" type="number" class="w-full p-1.5 rounded border border-outline-variant bg-white text-xs" value="18"/>
                        </div>
                    </div>

                    <div class="flex items-center justify-between pt-1">
                        <button id="fin-run-btn" onclick="executeFinancialCalculation()" class="px-5 py-2 rounded bg-primary text-on-primary font-label-md font-semibold hover:bg-primary-container transition-all flex items-center gap-1.5 shadow-sm">
                            <span class="material-symbols-outlined text-[18px]">currency_rupee</span>
                            <span>Calculate Compensation &amp; Fees</span>
                        </button>
                        <span id="fin-status-msg" class="text-xs text-secondary font-medium"></span>
                    </div>

                    <!-- Results Card -->
                    <div id="fin-result-box" class="hidden mt-3 p-4 rounded bg-surface-container-low border border-surface-container-high space-y-3">
                        <div class="flex items-center justify-between border-b border-surface-container-high pb-2">
                            <div>
                                <span id="fin-res-title" class="font-bold text-primary text-sm block"></span>
                                <span id="fin-res-enactment" class="text-xs text-outline block"></span>
                            </div>
                            <div class="text-right">
                                <span class="text-[11px] text-outline block">Statutory Total</span>
                                <span id="fin-res-total" class="font-bold text-lg text-emerald-800"></span>
                            </div>
                        </div>

                        <div>
                            <span class="font-label-md font-semibold text-primary block mb-1">Itemized Statutory Heads:</span>
                            <div id="fin-res-heads" class="space-y-1.5"></div>
                        </div>

                        <div class="p-3 bg-blue-50 rounded border border-blue-200 text-xs text-blue-950 leading-relaxed">
                            <span class="font-bold block mb-1">Judicial Guidance &amp; Precedent:</span>
                            <span id="fin-res-guidance"></span>
                        </div>
                    </div>
                </div>
            </div>
        `;
        document.body.appendChild(modal);
    }
};

window.toggleFinancialInputs = function(type) {
    const mactBox = document.getElementById("fin-mact-inputs");
    const genBox = document.getElementById("fin-generic-inputs");
    const reraBox = document.getElementById("fin-rera-months-container");
    const amtLabel = document.getElementById("fin-amount-label");

    if (type === "mact_accident_compensation") {
        if (mactBox) mactBox.classList.remove("hidden");
        if (genBox) genBox.classList.add("hidden");
    } else {
        if (mactBox) mactBox.classList.add("hidden");
        if (genBox) genBox.classList.remove("hidden");
        if (type === "rera_delayed_possession") {
            if (reraBox) reraBox.classList.remove("hidden");
            if (amtLabel) amtLabel.innerText = "Total Amount Paid to Promoter/Builder (INR)";
        } else {
            if (reraBox) reraBox.classList.add("hidden");
            if (amtLabel) amtLabel.innerText = "Claim Amount / Suit Valuation / Cheque Value (INR)";
        }
    }
};

window.executeFinancialCalculation = async function() {
    const btn = document.getElementById("fin-run-btn");
    const resultBox = document.getElementById("fin-result-box");
    const calcType = document.getElementById("fin-calc-type").value;

    btn.disabled = true;
    btn.innerHTML = '<span class="material-symbols-outlined text-[18px] animate-spin">sync</span> Calculating...';

    const payload = {
        calc_type: calcType,
        state: document.getElementById("fin-state").value,
        claim_amount: parseFloat(document.getElementById("fin-claim-amount").value || 0),
        victim_age: parseInt(document.getElementById("fin-mact-age").value || 30),
        monthly_income: parseFloat(document.getElementById("fin-mact-income").value || 30000),
        dependents_count: parseInt(document.getElementById("fin-mact-dependents").value || 3),
        total_amount_paid_to_builder: parseFloat(document.getElementById("fin-claim-amount").value || 5000000),
        delay_months: parseInt(document.getElementById("fin-delay-months").value || 12)
    };

    try {
        const res = await fetch("/api/v1/calculators/court-fee", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });
        const data = await res.json();
        if (data.success) {
            resultBox.classList.remove("hidden");
            document.getElementById("fin-res-title").innerText = data.calc_type;
            document.getElementById("fin-res-enactment").innerText = `${data.primary_enactment} (${data.landmark_precedent || 'Statutory Schedule'})`;
            document.getElementById("fin-res-total").innerText = data.formatted_total_inr;

            const headsBox = document.getElementById("fin-res-heads");
            headsBox.innerHTML = data.breakdown_heads.map(h => `
                <div class="p-2.5 bg-white rounded border border-surface-container-high">
                    <div class="flex items-center justify-between">
                        <span class="font-semibold text-xs text-primary">${h.head_name}</span>
                        <span class="font-bold text-xs text-emerald-800">INR ${h.amount_inr.toLocaleString('en-IN')}</span>
                    </div>
                    <div class="text-[11px] text-outline mt-0.5">${h.statutory_governance}</div>
                    <div class="text-[11px] text-on-surface-variant mt-0.5 italic">${h.calculation_breakdown}</div>
                </div>
            `).join("");

            document.getElementById("fin-res-guidance").innerText = data.practical_guidance;
        }
    } catch (e) {
        alert("Calculation error: " + e.message);
    } finally {
        btn.disabled = false;
        btn.innerHTML = '<span class="material-symbols-outlined text-[18px]">currency_rupee</span> Calculate Compensation & Fees';
    }
};
