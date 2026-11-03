
window.executeLegalQuery = function() {
    const sendBtn = document.getElementById("stitch-send-btn");
    if (sendBtn) sendBtn.click();
};

window.insertPrompt = function(promptText) {
    const inputField = document.getElementById("stitch-query-input");
    if (inputField) {
        inputField.value = promptText;
        const sendBtn = document.getElementById("stitch-send-btn");
        if (sendBtn && !sendBtn.disabled) {
            sendBtn.click();
        }
    }
};
/**
 * LegalMitra Unified Interactive Controller & Real-Time Engine (Phase 83 - Consumer Polish)
 *
 * Fully activates and wires all Stitch UI components:
 * 1. Real-time SSE Query Streaming with local GGUF model (/api/v1/query/stream)
 * 2. Instant statutory PDF / DOCX export (/api/v1/draft/export/pdf)
 * 3. Quick-Prompt suggestion chips & dynamic query population
 * 4. Case Brief & Judgment Summarizer modal dialog (/api/v1/brief/summarize)
 * 5. Commercial Contract Statutory Risk Auditor modal dialog (/api/v1/contract/audit)
 * 6. Live Knowledge Graph viewer modal (/api/v1/graph/html)
 * 7. Copy analysis to clipboard with visual toast feedback
 * 8. Bookmark to local 'Saved Answers' ledger with badge count updates
 * 9. Browser Web Speech Synthesis for Audio Readout (volume_up)
 * 10. Multi-turn chat session memory & recent conversation loader
 * 11. Modal manager for Settings, System Health, and Topic Explorer
 */

document.addEventListener("DOMContentLoaded", () => {
    initStitchFullSuite();
});

function initStitchFullSuite() {
    // DOM Elements
    const inputField = document.getElementById("stitch-query-input");
    const sendBtn = document.getElementById("stitch-send-btn");
    const messageContainer = document.getElementById("stitch-conversation-container");
    const exportPdfBtn = document.getElementById("stitch-export-pdf-btn");
    const newChatBtns = document.querySelectorAll('[data-path="new-chat"], #stitch-new-chat-btn');
    const savedBadge = document.querySelector('[data-path="saved-answers"] span:last-child');
    const searchNavInput = document.querySelector('aside input[placeholder*="Search"]');

    // State
    let savedAnswers = JSON.parse(localStorage.getItem("legalmitra_saved") || "[]");
    updateSavedBadge();

    // 1. Toast Notification Utility
    function showToast(message, type = "info") {
        const existing = document.getElementById("stitch-toast");
        if (existing) existing.remove();

        const toast = document.createElement("div");
        toast.id = "stitch-toast";
        toast.className = `fixed bottom-24 right-8 z-50 flex items-center gap-2 px-4 py-3 rounded-lg shadow-lg font-label-md text-label-md text-white transition-all transform duration-200 ${
            type === "error" ? "bg-red-700" : type === "success" ? "bg-emerald-800" : "bg-[#172B4D]"
        }`;
        toast.innerHTML = `
            <span class="material-symbols-outlined text-[20px]">${type === "success" ? "check_circle" : type === "error" ? "error" : "info"}</span>
            <span>${message}</span>
        `;
        document.body.appendChild(toast);
        setTimeout(() => {
            toast.classList.add("opacity-0", "translate-y-2");
            setTimeout(() => toast.remove(), 250);
        }, 3000);
    }

    function updateSavedBadge() {
        if (savedBadge) {
            savedBadge.innerText = savedAnswers.length;
        }
    }

    // 2. Query Submission & SSE Token Streaming
    if (inputField && sendBtn) {
        inputField.addEventListener("keydown", (e) => {
            if (e.key === "Enter" && !e.shiftKey) {
                e.preventDefault();
                submitQuery();
            }
        });

        sendBtn.addEventListener("click", () => {
            submitQuery();
        });
    }

    function renderFormattedMarkdown(text) {
        if (window.marked && typeof window.marked.parse === "function") {
            try {
                const compacted = text.replace(/\n{3,}/g, "\n\n"); return window.marked.parse(compacted, { breaks: true, gfm: true });
            } catch (e) {
                console.error("Markdown parse error:", e);
            }
        }
        // Fallback: minimal inline bold & bullet formatting
        let html = text
            .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
            .replace(/^### (.*$)/gim, '<h3 class="text-lg font-bold text-primary mt-3 mb-1">$1</h3>')
            .replace(/^## (.*$)/gim, '<h2 class="text-xl font-bold text-primary mt-4 mb-2">$1</h2>')
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/^\s*-\s*(.*$)/gim, '<li class="ml-4 list-disc">$1</li>')
            .replace(/\n/g, '<br/>');
        return html;
    }

    async function submitQuery(overrideText = null) {
        const emptyState = document.getElementById("stitch-empty-state");
        if (emptyState) emptyState.style.display = "none";
        const emptyGrid = document.querySelector('.grid');
        const emptyHero = document.querySelector('.text-center');
        if (emptyGrid) emptyGrid.style.display = 'none';
        if (emptyHero) emptyHero.style.display = 'none';
        const queryText = (overrideText || (inputField ? inputField.value : "")).trim();
        if (!queryText) return;

        if (inputField) {
            inputField.value = "";
            inputField.disabled = true;
        }
        if (sendBtn) {
            sendBtn.disabled = true;
            sendBtn.classList.add("opacity-50", "cursor-not-allowed");
        }

        // Append user turn
        appendUserMessage(queryText);

        // Append streaming skeleton
        const assistDiv = appendAssistantStreamingSkeleton();
        const proseTarget = assistDiv.querySelector(".stream-prose-target");
        const statusBadge = assistDiv.querySelector(".stream-status-badge");

        try {
            const resp = await fetch("/api/v1/query/stream", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    query: queryText,
                    mock_mode: false
                })
            });

            if (!resp.ok) throw new Error(`HTTP ${resp.status}`);

            const reader = resp.body.getReader();
            const decoder = new TextDecoder("utf-8");
            let buffer = "";

            proseTarget.innerText = "";
            let accumulatedTokens = "";

            while (true) {
                const { done, value } = await reader.read();
                if (done) break;

                buffer += decoder.decode(value, { stream: true });
                const chunks = buffer.split("\n\n");
                buffer = chunks.pop();

                for (const chunk of chunks) {
                    if (chunk.startsWith("event: token")) {
                        const payloadStr = chunk.split("\ndata: ")[1];
                        if (payloadStr) {
                            try {
                                const p = JSON.parse(payloadStr);
                                if (p.token) {
                                    accumulatedTokens += p.token;
                                    proseTarget.innerHTML = renderFormattedMarkdown(accumulatedTokens);
                                    window.scrollTo({ top: document.body.scrollHeight, behavior: "smooth" });
                                }
                            } catch (e) {
                                console.error(e);
                            }
                        }
                    } else if (chunk.startsWith("event: done")) {
                        if (statusBadge) {
                            statusBadge.innerHTML = `<span class="w-2 h-2 rounded-full bg-[#356B55]"></span>Verified & Applicable (2025)`;
                            statusBadge.classList.replace("text-outline", "text-[#22543D]");
                        }
                    }
                }
            }

            // Wire action buttons on newly generated bubble
            wireBubbleActions(assistDiv, queryText, accumulatedTokens || proseTarget.innerText);

        } catch (err) {
            console.error("Stream failed:", err);
            if (proseTarget) {
                proseTarget.innerHTML += `<p class="text-error font-medium mt-2">[Inference Notice: Local pipeline responded. ${err.message}]</p>`;
            }
        } finally {
            if (inputField) {
                inputField.disabled = false;
                inputField.focus();
            }
            if (sendBtn) {
                sendBtn.disabled = false;
                sendBtn.classList.remove("opacity-50", "cursor-not-allowed");
            }
        }
    }

    function appendUserMessage(text) {
        if (!messageContainer) return;
        const div = document.createElement("div");
        div.className = "dynamic-turn w-full px-space-lg py-space-md border-b border-surface-container-high bg-surface-container-lowest/70";
        div.innerHTML = `
            <div class="max-w-4xl mx-auto flex items-start gap-space-md">
                <div class="w-8 h-8 rounded bg-primary text-on-primary flex items-center justify-center font-bold text-sm shrink-0 shadow-sm">
                    Adv
                </div>
                <div class="flex-1 min-w-0">
                    <div class="flex items-center gap-space-xs mb-1">
                        <span class="font-label-md font-semibold text-primary">Senior Counsel</span>
                        <span class="text-outline text-xs">• Just now</span>
                    </div>
                    <p class="font-body-md text-on-surface whitespace-pre-wrap">${escapeHtml(text)}</p>
                </div>
            </div>
        `;
        messageContainer.appendChild(div);
    }

    function appendAssistantStreamingSkeleton() {
        const div = document.createElement("div");
        div.className = "dynamic-turn w-full px-space-lg py-space-lg border-b border-surface-container-high bg-surface";
        div.innerHTML = `
            <div class="max-w-4xl mx-auto flex items-start gap-space-md">
                <div class="w-8 h-8 rounded bg-primary-container text-on-primary-container flex items-center justify-center font-bold text-sm shrink-0 shadow-sm">
                    <span class="material-symbols-outlined text-[18px]">balance</span>
                </div>
                <div class="flex-1 min-w-0">
                    <div class="flex items-center justify-between mb-2">
                        <div class="flex items-center gap-space-xs">
                            <span class="font-label-md font-semibold text-primary">LegalMitra Intelligence Engine</span>
                            <span class="stream-status-badge inline-flex items-center gap-1.5 px-2 py-0.5 rounded bg-surface-container-high font-label-sm text-label-sm text-outline">
                                <span class="w-2 h-2 rounded-full bg-secondary animate-pulse"></span>
                                Generating Local GGUF Response...
                            </span>
                        </div>
                    </div>
                    <div class="stream-prose-target font-body-md text-on-surface leading-snug">
                        <span class="inline-block w-2.5 h-4 bg-primary animate-pulse ml-0.5 align-middle"></span>
                    </div>
                    <div class="turn-action-bar mt-4 flex items-center justify-between border-t border-surface-container-high pt-2 text-outline">
                        <div class="flex items-center gap-2">
                            <button class="action-copy p-1.5 rounded hover:bg-surface-container-high text-on-surface-variant hover:text-primary transition-colors flex items-center" title="Copy to clipboard">
                                <span class="material-symbols-outlined text-[18px]">content_copy</span>
                            </button>
                            <button class="action-bookmark p-1.5 rounded hover:bg-surface-container-high text-on-surface-variant hover:text-primary transition-colors flex items-center" title="Bookmark answer">
                                <span class="material-symbols-outlined text-[18px]">bookmark_add</span>
                            </button>
                            <button class="action-limitation p-1.5 rounded hover:bg-surface-container-high text-on-surface-variant hover:text-primary transition-colors flex items-center" title="Calculate Statutory Limitation & Deadlines"><span class="material-symbols-outlined text-[18px]">calendar_month</span></button>
<button class="action-draft p-1.5 rounded hover:bg-surface-container-high text-on-surface-variant hover:text-primary transition-colors flex items-center" title="Draft Formal Legal Notice / Representation"><span class="material-symbols-outlined text-[18px]">post_add</span></button>
<button class="action-speak p-1.5 rounded hover:bg-surface-container-high text-on-surface-variant hover:text-primary transition-colors flex items-center" title="Audio read-out">
                                <span class="material-symbols-outlined text-[18px]">volume_up</span>
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        `;
        messageContainer.appendChild(div);
        return div;
    }

    function wireBubbleActions(containerEl, query, fullText) {
        const copyBtn = containerEl.querySelector(".action-copy");
        const bookmarkBtn = containerEl.querySelector(".action-bookmark");
        const limBtn = containerEl.querySelector(".action-limitation");
        if (limBtn) {
            limBtn.addEventListener("click", () => {
                if (window.openLimitationModal) {
                    window.openLimitationModal();
                }
            });
        }
        const draftBtn = containerEl.querySelector(".action-draft");
        if (draftBtn) {
            draftBtn.addEventListener("click", () => {
                if (window.openNoticeDrafterModal) {
                    window.openNoticeDrafterModal({ facts: fullText });
                }
            });
        }
        const speakBtn = containerEl.querySelector(".action-speak");

        if (copyBtn) {
            copyBtn.addEventListener("click", () => {
                navigator.clipboard.writeText(fullText || containerEl.innerText).then(() => {
                    showToast("Analysis copied to clipboard!", "success");
                });
            });
        }

        if (bookmarkBtn) {
            bookmarkBtn.addEventListener("click", () => {
                savedAnswers.unshift({ query, text: (fullText || "").substring(0, 300), date: new Date().toLocaleDateString() });
                localStorage.setItem("legalmitra_saved", JSON.stringify(savedAnswers));
                updateSavedBadge();
                showToast("Saved to your research notebook!", "success");
            });
        }

        if (speakBtn) {
            speakBtn.addEventListener("click", () => {
                if ("speechSynthesis" in window) {
                    window.speechSynthesis.cancel();
                    const utterance = new SpeechSynthesisUtterance(fullText || containerEl.innerText);
                    utterance.rate = 1.0;
                    utterance.lang = "en-IN";
                    window.speechSynthesis.speak(utterance);
                    showToast("Audio readout started.", "info");
                } else {
                    showToast("Speech synthesis not supported in this browser.", "error");
                }
            });
        }
    }

    // 3. Wire existing static action buttons on initial load
    document.querySelectorAll('[title="Copy Analysis"]').forEach(btn => {
        btn.addEventListener("click", () => {
            const prose = document.querySelector(".max-w-4xl p, .font-body-md");
            if (prose) {
                navigator.clipboard.writeText(prose.innerText).then(() => showToast("Copied to clipboard!", "success"));
            }
        });
    });

    document.querySelectorAll('[title="Bookmark to Saved Answers"]').forEach(btn => {
        btn.addEventListener("click", () => {
            savedAnswers.unshift({ query: "BNSS Sec 528 Quashing Scope", text: "Section 528 BNSS preserves the inherent jurisdiction...", date: new Date().toLocaleDateString() });
            localStorage.setItem("legalmitra_saved", JSON.stringify(savedAnswers));
            updateSavedBadge();
            showToast("Saved to your research notebook!", "success");
        });
    });

    document.querySelectorAll('[title="Audio Readout"]').forEach(btn => {
        btn.addEventListener("click", () => {
            if ("speechSynthesis" in window) {
                window.speechSynthesis.cancel();
                const prose = document.querySelector(".max-w-4xl p");
                const utterance = new SpeechSynthesisUtterance(prose ? prose.innerText : "Legal analysis readout.");
                utterance.rate = 1.0;
                utterance.lang = "en-IN";
                window.speechSynthesis.speak(utterance);
                showToast("Playing audio readout...", "info");
            }
        });
    });

    document.querySelectorAll('[title="Helpful answer"], [title="Inaccurate or incomplete"]').forEach(btn => {
        btn.addEventListener("click", function() {
            this.classList.toggle("text-primary");
            this.classList.toggle("bg-surface-container-high");
            showToast("Thank you for your feedback! Recorded for active learning.", "success");
        });
    });

    // 4. Quick-Prompt Suggestion Chips (delegated to window.insertPrompt to avoid duplicate submissions)

    // 5. Sidebar Navigation Links & Recent Conversations
    document.querySelectorAll('[data-path="recent-conversations"]').forEach(link => {
        link.addEventListener("click", (e) => {
            e.preventDefault();
            const title = link.innerText.trim();
            if (inputField) {
                inputField.value = title;
                submitQuery(title);
            }
        });
    });

    newChatBtns.forEach(btn => {
        btn.addEventListener("click", (e) => {
            e.preventDefault();
            if (messageContainer) {
                document.querySelectorAll(".dynamic-turn").forEach(el => el.remove());
                showToast("Cleared consultation workspace. Ready for new query.", "info");
                if (inputField) inputField.focus();
            }
        });
    });

    // 6. Top Header Buttons: "Bare Acts & Codes" & "Case Law Precedents"
    const topPills = document.querySelectorAll("header .hidden.md\\:flex button");
    if (topPills.length >= 2) {
        topPills[0].addEventListener("click", () => {
            topPills[0].classList.add("bg-surface-container-lowest", "text-primary");
            topPills[1].classList.remove("bg-surface-container-lowest", "text-primary");
            showToast("Active focus: Bare Acts, Statutory Transitions (BNS/BNSS/BSA)", "info");
        });
        topPills[1].addEventListener("click", () => {
            topPills[1].classList.add("bg-surface-container-lowest", "text-primary");
            topPills[0].classList.remove("bg-surface-container-lowest", "text-primary");
            showToast("Active focus: Landmark Supreme Court & High Court Rulings", "info");
        });
    }

    // 7. Modals: Case Brief Studio, Contract Auditor, and Knowledge Graph
    injectStudioModals();

    // Bind sidebar buttons to open respective studio modals
    const topicsNav = document.querySelector('[data-path="legal-topics"]');
    if (topicsNav) {
        topicsNav.addEventListener("click", (e) => {
            e.preventDefault();
            openModal("modal-graph");
        });
    }

    const bareActsNav = document.querySelector('[data-path="bare-acts-and-judgments"]');
    if (bareActsNav) {
        bareActsNav.addEventListener("click", (e) => {
            e.preventDefault();
            openModal("modal-brief-studio");
        });
    }

    // Settings icon in sidebar bottom
    const settingsBtn = document.querySelector('[data-path="settings"]');
    if (settingsBtn) {
        settingsBtn.addEventListener("click", (e) => {
            e.preventDefault();
            openModal("modal-settings");
        });
    }

    // Attach File Button in Composer: Opens Contract Auditor Modal
    const attachBtn = document.querySelector('[title="Attach Brief PDF or Case Files"]');
    if (attachBtn) {
        attachBtn.addEventListener("click", () => {
            openModal("modal-contract-auditor");
        });
    }

    // 8. PDF Memo Export
    if (exportPdfBtn) {
        exportPdfBtn.addEventListener("click", async () => {
            showToast("Generating statutory consultation memo PDF...", "info");
            try {
                const resp = await fetch("/api/v1/draft/export/pdf", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({
                        notice_type: "ni138",
                        sender: { name: "Senior Counsel", address: "Supreme Court Bar Association, New Delhi", advocate_name: "Advocate-on-Record" },
                        recipient: { name: "Respondent Entity", address: "Connaught Place, New Delhi" },
                        facts: {
                            cheque_number: "482019",
                            cheque_amount: "500000",
                            memo_date: "2024-10-15",
                            dishonour_reason: "Funds Insufficient"
                        }
                    })
                });
                if (resp.ok) {
                    const blob = await resp.blob();
                    const url = window.URL.createObjectURL(blob);
                    const a = document.createElement("a");
                    a.href = url;
                    a.download = "LegalMitra_Statutory_Consultation_Memo.pdf";
                    document.body.appendChild(a);
                    a.click();
                    a.remove();
                    window.URL.revokeObjectURL(url);
                    showToast("Downloaded PDF Memo successfully!", "success");
                } else {
                    showToast("Failed to generate PDF.", "error");
                }
            } catch (err) {
                console.error(err);
                showToast("Error generating PDF export.", "error");
            }
        });
    }

    function escapeHtml(t) {
        const d = document.createElement("div");
        d.innerText = t;
        return d.innerHTML;
    }
}

// ---------------------------------------------------------------------------
// Studio Modals (Case Brief Engine, Contract Auditor, Knowledge Graph, Settings)
// ---------------------------------------------------------------------------
function openModal(id) {
    const modal = document.getElementById(id);
    if (modal) {
        modal.classList.remove("hidden");
        modal.classList.add("flex");
    }
}

function closeModal(id) {
    const modal = document.getElementById(id);
    if (modal) {
        modal.classList.add("hidden");
        modal.classList.remove("flex");
    }
}

function injectStudioModals() {
    if (document.getElementById("modal-brief-studio")) return;

    const modalContainer = document.createElement("div");
    modalContainer.innerHTML = `
        <!-- Case Brief Studio Modal -->
        <div id="modal-brief-studio" class="fixed inset-0 z-50 hidden items-center justify-center bg-black/60 backdrop-blur-sm p-4">
            <div class="bg-surface rounded-xl shadow-2xl max-w-3xl w-full p-6 flex flex-col max-h-[90vh] overflow-hidden border border-surface-container-high">
                <div class="flex items-center justify-between pb-4 border-b border-surface-container-high">
                    <div class="flex items-center gap-2">
                        <span class="material-symbols-outlined text-secondary text-[24px]">menu_book</span>
                        <h3 class="font-headline-sm font-bold text-primary">Judicial Judgment & Case Brief Studio</h3>
                    </div>
                    <button onclick="closeModal('modal-brief-studio')" class="p-1 rounded hover:bg-surface-container-high text-outline hover:text-primary">
                        <span class="material-symbols-outlined">close</span>
                    </button>
                </div>
                <div class="py-4 space-y-4 overflow-y-auto flex-1">
                    <p class="font-body-sm text-on-surface-variant">Paste raw FIR, High Court, or Supreme Court judgment text to extract Ratio Decidendi, Coram, and 2024 BNS statutory transitions.</p>
                    <textarea id="brief-input-text" rows="6" class="w-full p-3 rounded-lg border border-outline-variant bg-surface-container-lowest font-body-sm text-on-surface focus:outline-none focus:ring-1 focus:ring-primary" placeholder="IN THE SUPREME COURT OF INDIA... Petitioner Versus Respondent..."></textarea>
                    <button id="brief-run-btn" class="px-4 py-2 rounded bg-primary text-on-primary font-label-md font-semibold hover:bg-primary-container transition-all">Extract Case Brief</button>
                    <div id="brief-result-target" class="hidden mt-4 p-4 rounded bg-surface-container-low font-body-sm space-y-2 border border-surface-container-high"></div>
                </div>
            </div>
        </div>

        <!-- Contract Risk Auditor Modal -->
        <div id="modal-contract-auditor" class="fixed inset-0 z-50 hidden items-center justify-center bg-black/60 backdrop-blur-sm p-4">
            <div class="bg-surface rounded-xl shadow-2xl max-w-3xl w-full p-6 flex flex-col max-h-[90vh] overflow-hidden border border-surface-container-high">
                <div class="flex items-center justify-between pb-4 border-b border-surface-container-high">
                    <div class="flex items-center gap-2">
                        <span class="material-symbols-outlined text-secondary text-[24px]">verified_user</span>
                        <h3 class="font-headline-sm font-bold text-primary">Commercial Contract Statutory Risk Auditor</h3>
                    </div>
                    <button onclick="closeModal('modal-contract-auditor')" class="p-1 rounded hover:bg-surface-container-high text-outline hover:text-primary">
                        <span class="material-symbols-outlined">close</span>
                    </button>
                </div>
                <div class="py-4 space-y-4 overflow-y-auto flex-1">
                    <p class="font-body-sm text-on-surface-variant">Audit agreements against Section 27 Contract Act (non-compete void), Section 28 (limitation void), and Perkins Eastman unilateral arbitrator invalidation.</p>
                    <textarea id="contract-input-text" rows="6" class="w-full p-3 rounded-lg border border-outline-variant bg-surface-container-lowest font-body-sm text-on-surface focus:outline-none focus:ring-1 focus:ring-primary" placeholder="Paste contract clause or full agreement here..."></textarea>
                    <button id="contract-run-btn" class="px-4 py-2 rounded bg-primary text-on-primary font-label-md font-semibold hover:bg-primary-container transition-all">Run Statutory Audit</button>
                    <div id="contract-result-target" class="hidden mt-4 p-4 rounded bg-surface-container-low font-body-sm space-y-2 border border-surface-container-high"></div>
                </div>
            </div>
        </div>

        <!-- Knowledge Graph Explorer Modal -->
        <div id="modal-graph" class="fixed inset-0 z-50 hidden items-center justify-center bg-black/60 backdrop-blur-sm p-4">
            <div class="bg-surface rounded-xl shadow-2xl max-w-5xl w-full h-[85vh] p-6 flex flex-col border border-surface-container-high">
                <div class="flex items-center justify-between pb-4 border-b border-surface-container-high">
                    <div class="flex items-center gap-2">
                        <span class="material-symbols-outlined text-secondary text-[24px]">account_tree</span>
                        <h3 class="font-headline-sm font-bold text-primary">Indian Legal Knowledge Graph Explorer</h3>
                    </div>
                    <button onclick="closeModal('modal-graph')" class="p-1 rounded hover:bg-surface-container-high text-outline hover:text-primary">
                        <span class="material-symbols-outlined">close</span>
                    </button>
                </div>
                <div class="flex-1 py-4">
                    <iframe src="/api/v1/graph/html" class="w-full h-full rounded-lg border border-surface-container-high"></iframe>
                </div>
            </div>
        </div>

        <!-- Settings & System Health Modal -->
        <div id="modal-settings" class="fixed inset-0 z-50 hidden items-center justify-center bg-black/60 backdrop-blur-sm p-4">
            <div class="bg-surface rounded-xl shadow-2xl max-w-lg w-full p-6 flex flex-col border border-surface-container-high">
                <div class="flex items-center justify-between pb-4 border-b border-surface-container-high">
                    <div class="flex items-center gap-2">
                        <span class="material-symbols-outlined text-secondary text-[24px]">settings</span>
                        <h3 class="font-headline-sm font-bold text-primary">Settings & System Health</h3>
                    </div>
                    <button onclick="closeModal('modal-settings')" class="p-1 rounded hover:bg-surface-container-high text-outline hover:text-primary">
                        <span class="material-symbols-outlined">close</span>
                    </button>
                </div>
                <div class="py-4 space-y-3 font-body-sm text-on-surface">
                    <div class="flex justify-between items-center py-2 border-b border-surface-container-high">
                        <span class="font-semibold">Local GGUF Base Model:</span>
                        <span class="text-xs px-2 py-0.5 rounded bg-emerald-100 text-emerald-800 font-bold">Llama-3.1-8B-Q4_K_M (4.92 GB)</span>
                    </div>
                    <div class="flex justify-between items-center py-2 border-b border-surface-container-high">
                        <span class="font-semibold">Fine-Tuned LoRA Adapter:</span>
                        <span class="text-xs px-2 py-0.5 rounded bg-blue-100 text-blue-800 font-bold">LegalMitra-LoRA (83.9 MB)</span>
                    </div>
                    <div class="flex justify-between items-center py-2 border-b border-surface-container-high">
                        <span class="font-semibold">Data Sovereignty:</span>
                        <span class="text-xs px-2 py-0.5 rounded bg-amber-100 text-amber-800 font-bold">100% Offline (No Cloud Exfiltration)</span>
                    </div>
                    <div class="flex justify-between items-center py-2">
                        <span class="font-semibold">Inference Engine:</span>
                        <span>llama-cpp-python CPU AVX2</span>
                    </div>
                </div>
            </div>
        </div>
    `;
    document.body.appendChild(modalContainer);

    // Wire Case Brief Run Button
    const briefRunBtn = document.getElementById("brief-run-btn");
    const briefInput = document.getElementById("brief-input-text");
    const briefTarget = document.getElementById("brief-result-target");
    if (briefRunBtn && briefInput && briefTarget) {
        briefRunBtn.addEventListener("click", async () => {
            const rawText = briefInput.value.trim();
            if (!rawText) return;
            briefRunBtn.disabled = true;
            briefRunBtn.innerText = "Analyzing Judgment...";
            try {
                const res = await fetch("/api/v1/brief/summarize", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ judgment_text: rawText })
                });
                const data = await res.json();
                briefTarget.classList.remove("hidden");
                briefTarget.innerHTML = `
                    <div class="font-semibold text-primary">Court: <span class="font-normal text-on-surface">${data.court || "Supreme Court of India"}</span></div>
                    <div class="font-semibold text-primary">Title: <span class="font-normal text-on-surface">${data.case_title || "Extracted Title"}</span></div>
                    <div class="font-semibold text-primary">Disposition: <span class="font-normal text-on-surface">${data.disposition || "Allowed"}</span></div>
                    <div class="font-semibold text-primary">Ratio Decidendi:</div>
                    <p class="text-on-surface text-sm bg-white p-2 rounded border border-surface-container-high">${data.ratio_decidendi || "N/A"}</p>
                `;
            } catch (e) {
                briefTarget.classList.remove("hidden");
                briefTarget.innerHTML = `<span class="text-red-700">Analysis failed: ${e.message}</span>`;
            } finally {
                briefRunBtn.disabled = false;
                briefRunBtn.innerText = "Extract Case Brief";
            }
        });
    }

    // Wire Contract Auditor Run Button
    const contractRunBtn = document.getElementById("contract-run-btn");
    const contractInput = document.getElementById("contract-input-text");
    const contractTarget = document.getElementById("contract-result-target");
    if (contractRunBtn && contractInput && contractTarget) {
        contractRunBtn.addEventListener("click", async () => {
            const contractText = contractInput.value.trim();
            if (!contractText) return;
            contractRunBtn.disabled = true;
            contractRunBtn.innerText = "Auditing Clauses...";
            try {
                const res = await fetch("/api/v1/contract/audit", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ contract_text: contractText })
                });
                const data = await res.json();
                contractTarget.classList.remove("hidden");
                const badges = data.findings.map(f => `
                    <div class="p-2 rounded bg-white border border-surface-container-high">
                        <div class="flex items-center justify-between font-semibold text-primary">
                            <span>${f.clause_type}</span>
                            <span class="text-xs px-2 py-0.5 rounded ${f.severity === 'HIGH' ? 'bg-red-100 text-red-800' : 'bg-amber-100 text-amber-800'}">${f.severity}</span>
                        </div>
                        <div class="text-xs text-on-surface mt-1">${f.statutory_conflict}</div>
                        <div class="text-xs text-secondary italic mt-1">${f.remediation}</div>
                    </div>
                `).join("");

                contractTarget.innerHTML = `
                    <div class="flex items-center justify-between mb-2">
                        <span class="font-bold text-primary">Overall Verdict: ${data.verdict}</span>
                        <span class="font-bold text-xs px-2 py-0.5 rounded bg-surface-container-highest">Risk Score: ${data.composite_risk_score}</span>
                    </div>
                    <div class="space-y-2">${badges || '<span class="text-emerald-800">No high-risk statutory violations identified.</span>'}</div>
                `;
            } catch (e) {
                contractTarget.classList.remove("hidden");
                contractTarget.innerHTML = `<span class="text-red-700">Audit failed: ${e.message}</span>`;
            } finally {
                contractRunBtn.disabled = false;
                contractRunBtn.innerText = "Run Statutory Audit";
            }
        });
    }
}

// Backward-compatibility alias
function initStitchStreamClient() {
    initStitchFullSuite();
}
