// Phase 100: Guided Conversational Citizen Intake Wizard UI Controller
window.openCitizenIntakeWizard = function() {
    let modal = document.getElementById("modal-intake-wizard");
    if (!modal) {
        modal = document.createElement("div");
        modal.id = "modal-intake-wizard";
        modal.className = "fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4";
        modal.innerHTML = `
            <div class="bg-surface rounded-xl shadow-2xl max-w-2xl w-full p-6 flex flex-col max-h-[92vh] overflow-hidden border border-surface-container-high">
                <div class="flex items-center justify-between pb-3 border-b border-surface-container-high">
                    <div class="flex items-center gap-2">
                        <span class="material-symbols-outlined text-secondary text-[24px]">contact_support</span>
                        <h3 class="font-headline-sm font-bold text-primary">Guided Citizen Intake Wizard</h3>
                    </div>
                    <button onclick="document.getElementById('modal-intake-wizard').remove()" class="p-1 rounded hover:bg-surface-container-high text-outline hover:text-primary">
                        <span class="material-symbols-outlined">close</span>
                    </button>
                </div>
                
                <div class="py-3 space-y-4 overflow-y-auto flex-1 font-body-sm text-on-surface">
                    <p class="text-xs text-on-surface-variant">Don't know legal terminology? Just answer 3 simple questions in your own mother tongue, and LegalMitra will determine your legal rights, applicable laws, and next steps.</p>
                    
                    <!-- Question 1 -->
                    <div>
                        <label class="block font-label-md font-semibold text-primary mb-1">1. What happened? (साधेपणाने काय घडले ते सांगा / Describe in plain words)</label>
                        <textarea id="wizard-description" rows="3" class="w-full p-2.5 rounded border border-outline-variant bg-surface-container-lowest font-body-sm text-on-surface focus:outline-none focus:ring-1 focus:ring-primary" placeholder="उदा. पोलीस ठाण्यात चोरीची तक्रार दाखल करून घेण्यास नकार दिला... / Amazon वरून खराब फोन आला आणि रिफंड दिला नाही..."></textarea>
                    </div>

                    <!-- Question 2 -->
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
                        <div>
                            <label class="block font-label-md font-semibold text-primary mb-1">2. When did this happen? (घटना कधी घडली?)</label>
                            <input id="wizard-date" type="date" class="w-full p-2 rounded border border-outline-variant bg-surface-container-lowest font-body-sm text-on-surface" value="${new Date().toISOString().split('T')[0]}"/>
                            <span class="text-[11px] text-outline block mt-0.5">Determines if IPC (old) or BNS 2024 (new) applies.</span>
                        </div>
                        <div>
                            <label class="block font-label-md font-semibold text-primary mb-1">3. Where did this happen? (ठिकाण / शहर / राज्य)</label>
                            <input id="wizard-location" type="text" class="w-full p-2 rounded border border-outline-variant bg-surface-container-lowest font-body-sm text-on-surface" placeholder="e.g. Pune, Maharashtra / New Delhi" value="Pune, Maharashtra"/>
                            <span class="text-[11px] text-outline block mt-0.5">Maps local police jurisdiction &amp; court forum.</span>
                        </div>
                    </div>

                    <div class="flex items-center justify-between pt-1">
                        <button id="wizard-submit-btn" onclick="executeCitizenIntake()" class="px-5 py-2.5 rounded bg-primary text-on-primary font-label-md font-semibold hover:bg-primary-container transition-all flex items-center gap-1.5 shadow-sm">
                            <span class="material-symbols-outlined text-[18px]">psychology</span>
                            <span>Analyze My Legal Position</span>
                        </button>
                        <span id="wizard-status-msg" class="text-xs text-secondary font-medium"></span>
                    </div>

                    <!-- Results Card -->
                    <div id="wizard-result-box" class="hidden mt-3 p-4 rounded bg-surface-container-low border border-surface-container-high space-y-3">
                        <div class="flex items-center justify-between border-b border-surface-container-high pb-2">
                            <div>
                                <span id="wiz-res-domain" class="font-bold text-primary text-sm block"></span>
                                <span id="wiz-res-forum" class="text-xs text-secondary font-medium block"></span>
                            </div>
                            <span id="wiz-res-temporal" class="text-xs px-2.5 py-1 rounded bg-surface-container-highest font-mono text-primary font-semibold"></span>
                        </div>

                        <div>
                            <span class="font-label-md font-semibold text-primary block mb-1">Immediate Citizen Action Steps:</span>
                            <ul id="wiz-res-actions" class="text-xs space-y-1 list-disc pl-4 text-on-surface"></ul>
                        </div>

                        <div>
                            <span class="font-label-md font-semibold text-primary block mb-1">Applicable Statutory Enactments:</span>
                            <div id="wiz-res-statutes" class="flex flex-wrap gap-1.5"></div>
                        </div>

                        <div class="flex items-center gap-2 pt-2 border-t border-surface-container-high">
                            <button id="wiz-action-query" class="px-4 py-1.5 rounded bg-secondary text-on-secondary text-xs font-semibold hover:bg-secondary-fixed-variant transition-colors flex items-center gap-1">
                                <span class="material-symbols-outlined text-[16px]">chat</span> Ask Engine Full Question
                            </button>
                            <button id="wiz-action-notice" class="px-4 py-1.5 rounded bg-primary text-on-primary text-xs font-semibold hover:bg-primary-container transition-colors flex items-center gap-1">
                                <span class="material-symbols-outlined text-[16px]">description</span> Draft Legal Notice
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        `;
        document.body.appendChild(modal);
    }
};

window.executeCitizenIntake = async function() {
    const btn = document.getElementById("wizard-submit-btn");
    const resultBox = document.getElementById("wizard-result-box");
    const statusMsg = document.getElementById("wizard-status-msg");

    const desc = document.getElementById("wizard-description").value.trim();
    if (!desc) {
        alert("Please describe your problem in simple words.");
        return;
    }

    btn.disabled = true;
    btn.innerHTML = '<span class="material-symbols-outlined text-[18px] animate-spin">sync</span> Evaluating...';

    const payload = {
        incident_description: desc,
        incident_date: document.getElementById("wizard-date").value,
        state_or_city: document.getElementById("wizard-location").value,
        language: "mr"
    };

    try {
        const res = await fetch("/api/v1/intake/resolve", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });
        const data = await res.json();
        if (data.success) {
            resultBox.classList.remove("hidden");
            document.getElementById("wiz-res-domain").innerText = `Domain: ${data.broad_domain}`;
            document.getElementById("wiz-res-forum").innerText = `Competent Forum: ${data.competent_forum}`;
            document.getElementById("wiz-res-temporal").innerText = data.statutory_governance_framework.includes("2023") ? "2024 New Codes (BNS/BNSS)" : "Legacy Codes (IPC/CrPC)";

            const actionsList = document.getElementById("wiz-res-actions");
            actionsList.innerHTML = data.immediate_citizen_actions.map(act => `<li>${act}</li>`).join("");

            const statutesBox = document.getElementById("wiz-res-statutes");
            statutesBox.innerHTML = data.suggested_statutes.map(st => `<span class="px-2 py-0.5 rounded bg-white border border-surface-container-high text-[11px] font-semibold text-primary">${st}</span>`).join("");

            // Wire instant buttons
            document.getElementById("wiz-action-query").onclick = () => {
                document.getElementById("modal-intake-wizard").remove();
                if (window.insertPrompt) {
                    window.insertPrompt(data.synthesized_legal_query);
                }
            };

            document.getElementById("wiz-action-notice").onclick = () => {
                document.getElementById("modal-intake-wizard").remove();
                if (window.openNoticeDrafterModal) {
                    window.openNoticeDrafterModal({ facts: data.synthesized_legal_query });
                }
            };
        }
    } catch (e) {
        if (statusMsg) statusMsg.innerText = "Error: " + e.message;
    } finally {
        btn.disabled = false;
        btn.innerHTML = '<span class="material-symbols-outlined text-[18px]">psychology</span> Analyze My Legal Position';
    }
};
