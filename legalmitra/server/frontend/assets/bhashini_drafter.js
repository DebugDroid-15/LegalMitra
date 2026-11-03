// Phase 98: One-Click Statutory Notice & Representation Drafter UI Controller
window.openNoticeDrafterModal = function(initialData = {}) {
    let modal = document.getElementById("modal-notice-drafter");
    if (!modal) {
        modal = document.createElement("div");
        modal.id = "modal-notice-drafter";
        modal.className = "fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4";
        modal.innerHTML = `
            <div class="bg-surface rounded-xl shadow-2xl max-w-3xl w-full p-6 flex flex-col max-h-[92vh] overflow-hidden border border-surface-container-high">
                <div class="flex items-center justify-between pb-3 border-b border-surface-container-high">
                    <div class="flex items-center gap-2">
                        <span class="material-symbols-outlined text-secondary text-[24px]">description</span>
                        <h3 class="font-headline-sm font-bold text-primary">One-Click Statutory Notice & Representation Drafter</h3>
                    </div>
                    <button onclick="document.getElementById('modal-notice-drafter').remove()" class="p-1 rounded hover:bg-surface-container-high text-outline hover:text-primary">
                        <span class="material-symbols-outlined">close</span>
                    </button>
                </div>
                
                <div class="py-3 space-y-3 overflow-y-auto flex-1 font-body-sm text-on-surface">
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
                        <div>
                            <label class="block font-label-md font-semibold text-primary mb-1">Notice / Representation Template</label>
                            <select id="draft-template-type" class="w-full p-2 rounded border border-outline-variant bg-surface-container-lowest font-body-sm text-on-surface focus:outline-none focus:ring-1 focus:ring-primary">
                                <option value="police_fir_refusal_sp">Sec 173(4) BNSS - Police FIR Refusal (Representation to SP/DCP)</option>
                                <option value="cheque_dishonour_138">Sec 138 NI Act - Cheque Dishonour Demand Notice</option>
                                <option value="consumer_deficiency_notice">Sec 35 Consumer Protection Act - Deficiency Legal Notice</option>
                                <option value="tenant_eviction_notice">Sec 106 Transfer of Property Act - Lease Termination Notice</option>
                                <option value="general_legal_demand">General Contractual / Civil Legal Demand</option>
                            </select>
                        </div>
                        <div>
                            <label class="block font-label-md font-semibold text-primary mb-1">Incident / Cheque / Agreement Date</label>
                            <input id="draft-incident-date" type="text" class="w-full p-2 rounded border border-outline-variant bg-surface-container-lowest font-body-sm text-on-surface" value="${new Date().toLocaleDateString('en-GB')}"/>
                        </div>
                    </div>

                    <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
                        <div>
                            <label class="block font-label-md font-semibold text-primary mb-1">Your Full Name (Complainant / Client)</label>
                            <input id="draft-sender-name" type="text" class="w-full p-2 rounded border border-outline-variant bg-surface-container-lowest font-body-sm text-on-surface" placeholder="e.g. Rahul Sharma" value="Complainant / Citizen"/>
                        </div>
                        <div>
                            <label class="block font-label-md font-semibold text-primary mb-1">Your Postal Address & Phone</label>
                            <input id="draft-sender-address" type="text" class="w-full p-2 rounded border border-outline-variant bg-surface-container-lowest font-body-sm text-on-surface" placeholder="Address, City, State, PIN" value="Pune, Maharashtra"/>
                        </div>
                    </div>

                    <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
                        <div>
                            <label class="block font-label-md font-semibold text-primary mb-1">Opposite Party / Officer Name & Designation</label>
                            <input id="draft-recipient-name" type="text" class="w-full p-2 rounded border border-outline-variant bg-surface-container-lowest font-body-sm text-on-surface" placeholder="e.g. Superintendent of Police / Opposite Party" value="Superintendent of Police (SP)"/>
                        </div>
                        <div>
                            <label class="block font-label-md font-semibold text-primary mb-1">Opposite Party / Police Station Address</label>
                            <input id="draft-recipient-address" type="text" class="w-full p-2 rounded border border-outline-variant bg-surface-container-lowest font-body-sm text-on-surface" placeholder="Office / Police Station Address" value="District Headquarters / Police Commissionerate"/>
                        </div>
                    </div>

                    <div>
                        <label class="block font-label-md font-semibold text-primary mb-1">Brief Facts Disclosing Cause of Action</label>
                        <textarea id="draft-facts" rows="3" class="w-full p-2 rounded border border-outline-variant bg-surface-container-lowest font-body-sm text-on-surface focus:outline-none focus:ring-1 focus:ring-primary" placeholder="Describe the offence, refusal to register FIR, or unpaid debt...">${initialData.facts || "The local police officer refused to record information of a cognizable offence in violation of Section 173 BNSS."}</textarea>
                    </div>

                    <div class="flex items-center justify-between pt-2">
                        <button id="draft-execute-btn" onclick="executeStatutoryDraft()" class="px-5 py-2 rounded bg-primary text-on-primary font-label-md font-semibold hover:bg-primary-container transition-all flex items-center gap-1.5 shadow-sm">
                            <span class="material-symbols-outlined text-[18px]">gavel</span>
                            <span>Generate Formal Notice</span>
                        </button>
                        <span id="draft-status-msg" class="text-xs text-secondary font-medium"></span>
                    </div>

                    <!-- Output Area -->
                    <div id="draft-result-box" class="hidden mt-3 p-4 rounded bg-surface-container-low border border-surface-container-high space-y-2">
                        <div class="flex items-center justify-between">
                            <span id="draft-result-title" class="font-bold text-primary text-sm"></span>
                            <div class="flex items-center gap-2">
                                <a id="draft-download-pdf" href="#" download="Legal_Notice.pdf" class="px-3 py-1 text-xs rounded bg-red-700 text-white font-semibold flex items-center gap-1 shadow-sm hover:bg-red-800">
                                    <span class="material-symbols-outlined text-[14px]">picture_as_pdf</span> PDF
                                </a>
                                <a id="draft-download-docx" href="#" download="Legal_Notice.docx" class="px-3 py-1 text-xs rounded bg-blue-700 text-white font-semibold flex items-center gap-1 shadow-sm hover:bg-blue-800">
                                    <span class="material-symbols-outlined text-[14px]">description</span> Word (.docx)
                                </a>
                            </div>
                        </div>
                        <div id="draft-preview-content" class="text-xs max-h-52 overflow-y-auto p-3 bg-white rounded border border-surface-container-high whitespace-pre-wrap font-mono"></div>
                    </div>
                </div>
            </div>
        `;
        document.body.appendChild(modal);
    }
};

window.executeStatutoryDraft = async function() {
    const btn = document.getElementById("draft-execute-btn");
    const statusMsg = document.getElementById("draft-status-msg");
    const resultBox = document.getElementById("draft-result-box");

    btn.disabled = true;
    btn.innerHTML = '<span class="material-symbols-outlined text-[18px] animate-spin">sync</span> Drafting...';
    if (statusMsg) statusMsg.innerText = "Applying statutory templates & court formatting...";

    const payload = {
        template_type: document.getElementById("draft-template-type").value,
        sender_name: document.getElementById("draft-sender-name").value,
        sender_address: document.getElementById("draft-sender-address").value,
        recipient_name: document.getElementById("draft-recipient-name").value,
        recipient_designation: "Authorized Officer / Respondent",
        recipient_address: document.getElementById("draft-recipient-address").value,
        incident_date: document.getElementById("draft-incident-date").value,
        cause_of_action_facts: document.getElementById("draft-facts").value,
        claim_amount: "50,000"
    };

    try {
        const res = await fetch("/api/v1/draft/generate", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });
        const data = await res.json();
        if (data.success) {
            resultBox.classList.remove("hidden");
            document.getElementById("draft-result-title").innerText = data.title;
            document.getElementById("draft-preview-content").innerText = data.full_text_markdown;

            if (data.pdf_base64) {
                const pdfLink = document.getElementById("draft-download-pdf");
                pdfLink.href = "data:application/pdf;base64," + data.pdf_base64;
                pdfLink.download = `${data.template_type}_Notice.pdf`;
            }
            if (data.docx_base64) {
                const docxLink = document.getElementById("draft-download-docx");
                docxLink.href = "data:application/vnd.openxmlformats-officedocument.wordprocessingml.document;base64," + data.docx_base64;
                docxLink.download = `${data.template_type}_Notice.docx`;
            }
            if (statusMsg) statusMsg.innerText = "Drafting successful!";
        }
    } catch (e) {
        if (statusMsg) statusMsg.innerText = "Error: " + e.message;
    } finally {
        btn.disabled = false;
        btn.innerHTML = '<span class="material-symbols-outlined text-[18px]">gavel</span> Generate Formal Notice';
    }
};
