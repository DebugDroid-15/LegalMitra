const SHOWCASE_DATA = [
  {
    id: "statute",
    modalKey: "showcase_statute",
    tagText: "ACT ANALYSIS",
    tagClass: "bg-brand-ashokaBlue text-white",
    actTitle: "Bharatiya Nyaya Sanhita, 2023 (BNS)",
    statusDot: "bg-brand-forest",
    statusText: "Commenced: 1 July 2024",
    statusTextClass: "text-brand-forest font-semibold",
    sectionMono: "SECTION 316 BNS • ERSTWHILE SEC 405 IPC",
    title: "Criminal Breach of Trust",
    headingLabel: "Plain-Language Meaning",
    description: "Criminal Breach of Trust occurs when an individual is entrusted with property or dominion over property, and subsequently dishonestly misappropriates, converts to their own use, or disposes of that property in violation of law or legal contract.",
    leftBoxTitle: "Essential Ingredients",
    leftBoxContent: `
      <ul class="text-xs text-brand-slate space-y-1 list-disc list-inside">
        <li>Actual entrustment of property or control</li>
        <li>Dishonest intention at the moment of conversion</li>
        <li>Violation of lawful direction or express trust</li>
      </ul>
    `,
    rightBoxTitle: "Doctrinal Distinction",
    rightBoxContent: `
      <p class="text-xs text-brand-slate leading-relaxed">
        Distinct from Cheating (Sec 318): In Breach of Trust, entrustment is innocent at inception; dishonest mens rea develops subsequently.
      </p>
    `,
    sourceGazette: "The Gazette of India: Act No. 45 of 2023",
    sourceSub: "Ministry of Law and Justice • Universal Jurisdiction Across Bharat",
    actionLabel: "Inspect Bare Act Clause"
  },
  {
    id: "judgment",
    modalKey: "showcase_judgment",
    tagText: "JUDICIAL PRECEDENT",
    tagClass: "bg-purple-700 text-white",
    actTitle: "Supreme Court of India (Constitution Bench)",
    statusDot: "bg-purple-600",
    statusText: "Binding Article 141 Precedent",
    statusTextClass: "text-purple-700 font-semibold",
    sectionMono: "ARNESH KUMAR V. STATE OF BIHAR • (2014) 8 SCC 273",
    title: "Mandatory Safeguards Against Arbitrary Arrest",
    headingLabel: "Ratio Decidendi (Binding Principle)",
    description: "Police officers cannot automatically arrest an accused merely because an FIR has been lodged under an offence carrying punishment up to seven years. The officer must satisfy and record the specific conditions under Section 41 CrPC (now Section 35 BNSS).",
    leftBoxTitle: "Checklist of Mandatory Criteria",
    leftBoxContent: `
      <ul class="text-xs text-brand-slate space-y-1 list-disc list-inside">
        <li>Necessity to prevent the person from committing further offence</li>
        <li>Proper investigation requirement with recorded reasons</li>
        <li>Prevention of evidence tampering or witness intimidation</li>
      </ul>
    `,
    rightBoxTitle: "Judicial Disciplinary Scope",
    rightBoxContent: `
      <p class="text-xs text-brand-slate leading-relaxed">
        Magistrates authorizing detention without recording reasoned satisfaction are liable for departmental disciplinary action by the High Court.
      </p>
    `,
    sourceGazette: "Supreme Court Reports • (2014) 8 SCC 273",
    sourceSub: "Criminal Appellate Jurisdiction • Coram: Chandramauli Kr. Prasad & P.C. Ghose, JJ.",
    actionLabel: "Query Precedent Ratio"
  },
  {
    id: "procedure",
    modalKey: "showcase_procedure",
    tagText: "PROCEDURAL ROADMAP",
    tagClass: "bg-emerald-700 text-white",
    actTitle: "Bharatiya Nagarik Suraksha Sanhita, 2023 (BNSS)",
    statusDot: "bg-emerald-600",
    statusText: "Active Procedural Standard",
    statusTextClass: "text-emerald-700 font-semibold",
    sectionMono: "SECTION 173(4) & 175(3) BNSS • ERSTWHILE SEC 154 & 156(3) CRPC",
    title: "Remedies When Police Refuse to Register FIR",
    headingLabel: "Step-by-Step Statutory Hierarchy",
    description: "When an Officer-in-Charge of a police station refuses to register information regarding a cognizable offence, a citizen has a clear two-tier statutory remedy to compel registration and judicial inquiry.",
    leftBoxTitle: "Tier 1: Representation to SP",
    leftBoxContent: `
      <ul class="text-xs text-brand-slate space-y-1 list-disc list-inside">
        <li>Send written complaint by registered post to Superintendent of Police (SP)</li>
        <li>SP can personally investigate or direct subordinate investigation</li>
        <li>Retain postal receipt and tracking acknowledgment as legal proof</li>
      </ul>
    `,
    rightBoxTitle: "Tier 2: Judicial Magistrate",
    rightBoxContent: `
      <p class="text-xs text-brand-slate leading-relaxed">
        If SP does not act, file an application before Judicial Magistrate under Section 175(3) BNSS accompanied by an affidavit verifying Tier 1 exhaustion.
      </p>
    `,
    sourceGazette: "The Gazette of India: Act No. 46 of 2023",
    sourceSub: "Code of Criminal Procedure Replacement Code",
    actionLabel: "View Procedural Hierarchy"
  },
  {
    id: "timeline",
    modalKey: "showcase_timeline",
    tagText: "TRANSITION TIMELINE",
    tagClass: "bg-amber-600 text-white",
    actTitle: "Ministry of Home Affairs Notifications S.O. 848(E)-850(E)",
    statusDot: "bg-amber-500",
    statusText: "Operational July 1, 2024",
    statusTextClass: "text-amber-700 font-semibold",
    sectionMono: "SECTION 531 BNSS & SECTION 358 BSS • SAVINGS CLAUSE RULES",
    title: "Applicability Rules for Ongoing Proceedings",
    headingLabel: "Critical Date of Offence Rule",
    description: "Offences committed prior to 1 July 2024 remain governed substantively by the Indian Penal Code, 1860. The Bharatiya Nyaya Sanhita applies strictly to acts committed on or after 1 July 2024.",
    leftBoxTitle: "Substantive Law Rule",
    leftBoxContent: `
      <p class="text-xs text-brand-slate leading-relaxed">
        Article 20(1) Constitution prohibits ex post facto criminal law. Charge-sheets for pre-July 2024 offences cite IPC sections even if filed today.
      </p>
    `,
    rightBoxTitle: "Procedural Transition (Sec 531)",
    rightBoxContent: `
      <p class="text-xs text-brand-slate leading-relaxed">
        Pending investigations, inquiries, or appeals instituted before 1 July 2024 continue under CrPC 1973 as if BNSS had not come into force.
      </p>
    `,
    sourceGazette: "Gazette Notification S.O. 848(E) • 23 February 2024",
    sourceSub: "Enforcement date notification for BNS, BNSS, and BSS",
    actionLabel: "Inspect Savings Provisions"
  },
  {
    id: "source",
    modalKey: "showcase_source",
    tagText: "VERIFIED CORPUS",
    tagClass: "bg-blue-800 text-white",
    actTitle: "Legislative Department, Ministry of Law and Justice",
    statusDot: "bg-blue-600",
    statusText: "Primary Sovereign Corpus",
    statusTextClass: "text-blue-800 font-semibold",
    sectionMono: "AUTHENTICATED SCR & SCC LAW REPOSITORIES",
    title: "Zero-Hallucination Source Verification Graph",
    headingLabel: "Rigorous Grounding Guarantee",
    description: "Every statement emitted by LegalMitra is cross-referenced with official Gazette printouts and Supreme Court Reports. No ungrounded synthetic speculation is admitted into legal analyses.",
    leftBoxTitle: "Statutory Provenance",
    leftBoxContent: `
      <ul class="text-xs text-brand-slate space-y-1 list-disc list-inside">
        <li>Direct parsing from official egazette.gov.in publications</li>
        <li>Sub-clause pin-pointing with exact sub-section text</li>
        <li>Corpus synchronized with published legislative amendments</li>
      </ul>
    `,
    rightBoxTitle: "Case Law Lineage",
    rightBoxContent: `
      <p class="text-xs text-brand-slate leading-relaxed">
        Judicial ratios verified against Supreme Court Case citation standards (SCC, SCR) with quorum details and affirming/dissenting bench records.
      </p>
    `,
    sourceGazette: "Statutory Registry & Provenance Graph: 68 Authentic Enactments",
    sourceSub: "National Judicial Data Model & Supreme Court Case Ledger",
    actionLabel: "Verify Sources Details"
  }
];

function switchShowcaseTab(index) {
  const data = SHOWCASE_DATA[index];
  if (!data) return;

  const previewContainer = document.getElementById("showcase-preview-container") || document.querySelector(".lg\\:col-span-8");
  const tabButtons = document.querySelectorAll("#showcase button[onclick*='switchShowcaseTab'], .lg\\:col-span-4 button");

  // 1. Update button visual states
  if (tabButtons && tabButtons.length) {
    tabButtons.forEach((btn, i) => {
      const iconBox = btn.querySelector("div:first-child");
      if (i === index) {
        btn.className = "w-full text-left p-4 rounded-xl border-2 border-brand-navy bg-white shadow-sm transition-all flex items-start space-x-3 group";
        if (iconBox) {
          iconBox.className = "w-8 h-8 rounded-lg bg-brand-navy text-white flex items-center justify-center flex-shrink-0 mt-0.5";
        }
      } else {
        btn.className = "w-full text-left p-4 rounded-xl border border-brand-ivoryBorder bg-white/70 hover:bg-white hover:border-brand-ashokaBlue/40 transition-all flex items-start space-x-3 group";
        if (iconBox) {
          iconBox.className = "w-8 h-8 rounded-lg bg-brand-ivoryDim text-brand-navy flex items-center justify-center flex-shrink-0 mt-0.5";
        }
      }
    });
  }

  // 2. Render content into preview container with openInfoModal modalKey trigger
  if (previewContainer) {
    previewContainer.innerHTML = `
      <!-- Viewport Header Bar -->
      <div class="flex flex-wrap items-center justify-between pb-4 border-b border-brand-ivoryBorder gap-2">
        <div class="flex items-center space-x-2">
          <span class="px-2 py-0.5 rounded text-[11px] font-bold ${data.tagClass}">${data.tagText}</span>
          <span class="text-xs font-semibold text-brand-slate">${data.actTitle}</span>
        </div>
        <div class="flex items-center space-x-2 text-xs">
          <span class="w-2 h-2 rounded-full ${data.statusDot}"></span>
          <span class="${data.statusTextClass}">${data.statusText}</span>
        </div>
      </div>

      <!-- Section Identity -->
      <div>
        <div class="text-xs font-mono text-brand-slate uppercase tracking-wide">${data.sectionMono}</div>
        <h3 class="font-heading font-bold text-2xl text-brand-navy mt-1">${data.title}</h3>
      </div>

      <!-- Plain-Language Explanation -->
      <div class="space-y-2">
        <h4 class="text-xs font-bold text-brand-navy uppercase tracking-wider">${data.headingLabel}</h4>
        <p class="text-sm text-brand-ink leading-relaxed">
          ${data.description}
        </p>
      </div>

      <!-- Statutory Scope & Core Elements Grid -->
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <div class="bg-brand-ivory p-4 rounded-lg border border-brand-ivoryBorder space-y-1.5">
          <span class="text-xs font-bold text-brand-navy">${data.leftBoxTitle}</span>
          ${data.leftBoxContent}
        </div>

        <div class="bg-brand-ivory p-4 rounded-lg border border-brand-ivoryBorder space-y-1.5">
          <span class="text-xs font-bold text-brand-navy">${data.rightBoxTitle}</span>
          ${data.rightBoxContent}
        </div>
      </div>

      <!-- Source Citation Footer Inside Showcase (Opens in-page Modal, never navigates to /chat) -->
      <div class="bg-brand-ashokaLight/60 border border-brand-ashokaBlue/20 rounded-xl p-4 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3">
        <div class="space-y-0.5">
          <div class="text-[11px] font-bold text-brand-navy flex items-center space-x-1.5">
            <svg class="w-3.5 h-3.5 text-brand-ashokaBlue" fill="currentColor" viewBox="0 0 20 20"><path d="M4 4a2 2 0 012-2h4.586A2 2 0 0112 2.586L15.414 6A2 2 0 0116 7.414V16a2 2 0 01-2 2H6a2 2 0 01-2-2V4z"/></svg>
            <span>${data.sourceGazette}</span>
          </div>
          <div class="text-[11px] text-brand-slate">${data.sourceSub}</div>
        </div>
        <button onclick="openInfoModal('${data.modalKey}')" class="text-xs font-bold text-brand-ashokaBlue hover:underline flex items-center space-x-1 flex-shrink-0 cursor-pointer">
          <span>${data.actionLabel}</span>
          <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"/></svg>
        </button>
      </div>
    `;
  }
}

// Expose globally to window
window.switchShowcaseTab = switchShowcaseTab;

// Self-init on load
if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", () => switchShowcaseTab(0));
} else {
  switchShowcaseTab(0);
}
