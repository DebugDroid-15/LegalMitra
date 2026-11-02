/**
 * LegalMitra Modal Information Panel Controller
 * Handles interactive drawers/modals for landing page information CTAs without navigating away to /chat.
 */

const MODAL_DATA = {
  about: {
    badge: "ORIGIN & MISSION",
    badgeClass: "bg-brand-ashokaBlue text-white",
    title: "About LegalMitra",
    subtitle: "Sovereign AI for Indian Jurisprudence & Constitutional Literacy",
    content: `
      <div class="space-y-4 text-sm text-brand-ink">
        <p class="leading-relaxed">
          LegalMitra was conceived to bridge the vast informational asymmetry between complex Indian legal statutes and everyday citizens, litigators, and enterprises. By synthesizing verified bare acts from the Legislative Department, Supreme Court precedents, and Gazette notifications, LegalMitra provides authoritative, source-grounded answers without hallucination.
        </p>
        <div class="bg-brand-ivory p-3 rounded-lg border border-brand-ivoryBorder space-y-2">
          <div class="text-xs font-bold text-brand-navy uppercase">Core Commitments</div>
          <ul class="text-xs text-brand-slate space-y-1.5 list-disc list-inside">
            <li>Zero synthetic hallucination: every claim citations official Gazette or SCC reporter source.</li>
            <li>Dual-code transition coverage: full awareness of IPC-to-BNS, CrPC-to-BNSS, and IEA-to-BSS mappings.</li>
            <li>Plain-language simplification without sacrificing doctrinal precision or procedural nuance.</li>
          </ul>
        </div>
      </div>
    `,
    footerNote: "LegalMitra Republic of India Knowledge Initiative"
  },

  support: {
    badge: "ASSISTANCE & HELPDESK",
    badgeClass: "bg-brand-forest text-white",
    title: "Support & Citizen Helpdesk",
    subtitle: "Getting Guidance on Using the Platform",
    content: `
      <div class="space-y-4 text-sm text-brand-ink">
        <p class="leading-relaxed">
          Need help navigating legal features, reporting an erratum in a statute citation, or inquiring about research partnerships? Our support channels are accessible for citizens and legal academics.
        </p>
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 pt-2">
          <div class="p-3 bg-brand-ivory rounded-lg border border-brand-ivoryBorder">
            <div class="text-xs font-bold text-brand-navy">Technical & Platform Inquiries</div>
            <div class="text-xs text-brand-slate mt-1">support@legalmitra.org.in</div>
          </div>
          <div class="p-3 bg-brand-ivory rounded-lg border border-brand-ivoryBorder">
            <div class="text-xs font-bold text-brand-navy">Statute & Corpus Validation</div>
            <div class="text-xs text-brand-slate mt-1">registry@legalmitra.org.in</div>
          </div>
        </div>
      </div>
    `,
    footerNote: "Standard response timeline: 24-48 business hours"
  },

  partners: {
    badge: "ACADEMIC & INSTITUTIONAL",
    badgeClass: "bg-purple-700 text-white",
    title: "Research & Knowledge Partners",
    subtitle: "Collaborating with National Law Universities & Legal Tech Labs",
    content: `
      <div class="space-y-4 text-sm text-brand-ink">
        <p class="leading-relaxed">
          LegalMitra collaborates with legal research cells, law university clinical programmes, and open legal data initiatives across Bharat to evaluate retrieval accuracy and ensure constitutional conformity.
        </p>
        <div class="bg-brand-ivory p-3.5 rounded-lg border border-brand-ivoryBorder text-xs text-brand-slate space-y-2">
          <div class="font-bold text-brand-navy">Collaborative Areas:</div>
          <p>1. Empirical benchmarking of new criminal laws (BNS, BNSS, BSS).</p>
          <p>2. High Court jurisdiction mapping and local amendment tracking.</p>
          <p>3. Multilingual legal access for regional court litigants.</p>
        </div>
      </div>
    `,
    footerNote: "Open Academic Research Consortium"
  },

  responsible_ai: {
    badge: "ETHICS & GOVERNANCE",
    badgeClass: "bg-brand-navy text-white",
    title: "Responsible AI Architecture",
    subtitle: "Sovereign Grounding, Provenance & Non-Advisory Guardrails",
    content: `
      <div class="space-y-4 text-sm text-brand-ink">
        <p class="leading-relaxed">
          LegalMitra operates under strict responsible AI guidelines compliant with the Ministry of Electronics and Information Technology (MeitY) advisory on algorithmic accountability:
        </p>
        <div class="space-y-2 text-xs text-brand-slate">
          <div class="p-2.5 bg-brand-ivory rounded border border-brand-ivoryBorder">
            <span class="font-bold text-brand-navy">1. Source Determinism:</span> Outputs are anchored solely to verified parliamentary acts and judicial transcripts.
          </div>
          <div class="p-2.5 bg-brand-ivory rounded border border-brand-ivoryBorder">
            <span class="font-bold text-brand-navy">2. Non-Advisory Disclaimer:</span> Algorithmic outputs educate and inform; they do not substitute for licensed advocate counsel.
          </div>
          <div class="p-2.5 bg-brand-ivory rounded border border-brand-ivoryBorder">
            <span class="font-bold text-brand-navy">3. Auditability:</span> Every section cited includes its Gazette enactment number or Supreme Court case citation.
          </div>
        </div>
      </div>
    `,
    footerNote: "BCI & MeitY Framework Compliant"
  },

  // 1. Navigation & Header CTAs
  capabilities: {
    badge: "SYSTEM CAPABILITIES",
    badgeColor: "bg-brand-ashokaBlue text-white",
    title: "LegalMitra Intelligence Capabilities",
    subtitle: "Built specifically around Indian Law and the 2024–2025 Criminal Codes",
    sections: [
      {
        heading: "1. Natural Language Statutory Translation",
        body: "Translates technical legislative enactments (BNS, BNSS, BSA, Companies Act, DPDP) into structured, human-accessible language with essential ingredients, exceptions, and practical advice."
      },
      {
        heading: "2. Real-Time Emergency & Citizen Triage",
        body: "Instant detection of urgent scenarios (police detention, cyber financial fraud, illegal eviction, domestic violence) with actionable step-by-step guides and official 24/7 helplines (112, 1930, 1915, 15100)."
      },
      {
        heading: "3. Judicial Precedent & Ratio Extraction",
        body: "Retrieves landmark Supreme Court of India and High Court rulings, bench constitutions (Constitution Bench vs. Division Bench), and binding ratio decidendi under Article 141."
      },
      {
        heading: "4. Temporal Law & Commencement Tracking",
        body: "Automatically resolves whether legacy law (IPC, CrPC, IEA) or new statutory codes apply based on the exact date of incident, preventing retrospective confusion."
      }
    ],
    ctaText: "Start a Conversation",
    ctaLink: "/chat"
  },

  signin: {
    badge: "USER ACCESS",
    badgeColor: "bg-brand-navy text-white",
    title: "LegalMitra Sovereign Public Access",
    subtitle: "Zero-barrier access to Indian statutory intelligence",
    sections: [
      {
        heading: "Public Community Edition",
        body: "LegalMitra is currently operating in free, open public access mode. No credit card, subscription paywall, or user login is required to query Indian statutes, police procedures, consumer rights, or judicial precedents."
      },
      {
        heading: "Advocate & Researcher Workspace",
        body: "Advocate workspace features—including statutory PDF exports, local case briefing ledgers, and contract risk audits—run entirely in your browser session with complete client confidentiality."
      }
    ],
    ctaText: "Start a Conversation",
    ctaLink: "/chat"
  },

  // 2. Showcase Detail Modals
  showcase_statute: {
    badge: "BARE ACT CLAUSE",
    badgeColor: "bg-brand-ashokaBlue text-white",
    title: "Section 316, Bharatiya Nyaya Sanhita (BNS), 2023",
    subtitle: "Criminal Breach of Trust (Erstwhile Section 405 IPC)",
    sections: [
      {
        heading: "Verbatim Statutory Clause",
        body: "Whoever, being in any manner entrusted with property, or with any dominion over property, dishonestly misappropriates or converts to his own use that property, or dishonestly uses or disposes of that property in violation of any direction of law prescribing the mode in which such trust is to be discharged, or of any legal contract, express or implied, which he has made touching the discharge of such trust, or wilfully suffers any other person so to do, commits criminal breach of trust."
      },
      {
        heading: "Punishment (Section 316(2) BNS)",
        body: "Whoever commits criminal breach of trust shall be punished with imprisonment of either description for a term which may extend to five years, or with fine, or with both."
      },
      {
        heading: "Critical Judicial Test",
        body: "The Supreme Court in Dalip Kaur v. Jagnar Singh held that to constitute criminal breach of trust, entrustment must be admitted or proved, followed by subsequent dishonest conversion."
      }
    ],
    ctaText: "Ask About This Section",
    ctaLink: "/chat?q=Explain+Section+316+BNS+Criminal+Breach+of+Trust"
  },

  showcase_judgment: {
    badge: "LANDMARK RATIO",
    badgeColor: "bg-purple-700 text-white",
    title: "Arnesh Kumar v. State of Bihar & Anr. (2014) 8 SCC 273",
    subtitle: "Supreme Court Guidelines on Section 41 CrPC / Section 35 BNSS",
    sections: [
      {
        heading: "The Rule of Law on Arrest",
        body: "Arrest brings humiliation, curtails freedom, and casts scars forever. No arrest can be made in a routine manner on a mere allegation of commission of an offence punishable with imprisonment up to 7 years without satisfying Section 41(1)(b) CrPC (now Section 35 BNSS)."
      },
      {
        heading: "Mandatory Notice of Appearance",
        body: "Police officers must issue a Notice of Appearance under Section 41A CrPC (now Section 35(3) BNSS) within two weeks from the date of institution of the case, unless compelling recorded reasons necessitate physical detention."
      },
      {
        heading: "Strict Sanctions on Defaulting Officers",
        body: "Defaulting police officers are liable for contempt of court as well as departmental disciplinary action by the High Court."
      }
    ],
    ctaText: "Explore Precedent in Chat",
    ctaLink: "/chat?q=Arnesh+Kumar+guidelines+on+arrest+under+BNSS"
  },

  showcase_procedure: {
    badge: "STATUTORY PROCEDURE",
    badgeColor: "bg-emerald-700 text-white",
    title: "Section 173(4) & 175(3) BNSS: FIR Registration Hierarchy",
    subtitle: "Remedy against Police Inaction under 2023 Sanhitas",
    sections: [
      {
        heading: "Step 1: Written Representation to SP (Section 173(4) BNSS)",
        body: "Any person aggrieved by a refusal on the part of an officer-in-charge of a police station to record FIR may send the substance of such information in writing and by post to the Superintendent of Police concerned. The SP may investigate directly or depute an officer."
      },
      {
        heading: "Step 2: Judicial Application (Section 175(3) BNSS)",
        body: "If the SP fails to act, the complainant can file an application before the Judicial Magistrate supported by an affidavit and proof of prior representation to the SP. The Magistrate has statutory powers to direct the police to register the FIR and investigate."
      },
      {
        heading: "Emergency Dial 112",
        body: "Where an offence is in progress or imminent physical harm is threatened, immediate response must be requisitioned via the National Emergency Helpline 112."
      }
    ],
    ctaText: "Consult on FIR Refusal",
    ctaLink: "/chat?q=Police+refusing+to+register+my+FIR"
  },

  showcase_timeline: {
    badge: "COMMENCEMENT TIMELINE",
    badgeColor: "bg-amber-600 text-white",
    title: "Ministry of Home Affairs Notifications S.O. 848(E)–850(E)",
    subtitle: "Statutory Transition Boundary: 1 July 2024 Cutoff",
    sections: [
      {
        heading: "Appointed Date of Enforcement",
        body: "By notifications dated 23 February 2024, the Central Government appointed the 1st day of July 2024 as the date on which the Bharatiya Nyaya Sanhita, Bharatiya Nagarik Suraksha Sanhita, and Bharatiya Sakshya Adhiniyam came into force across India."
      },
      {
        heading: "Repeal and Savings (Section 531 BNSS)",
        body: "Notwithstanding the repeal of CrPC, any pending appeal, application, trial, inquiry, or investigation shall be disposed of, continued, held, or made in accordance with the provisions of the Code of Criminal Procedure, 1973 as if this Sanhita had not come into force."
      },
      {
        heading: "Section 106(2) BNS Stayed / Held in Abeyance",
        body: "Sub-section (2) of Section 106 BNS regarding ten-year imprisonment for hit-and-run drivers has not yet been notified and is held in abeyance pending stakeholder consultations."
      }
    ],
    ctaText: "Check Temporal Law in Chat",
    ctaLink: "/chat?q=Which+law+applies+IPC+or+BNS+based+on+date"
  },

  showcase_source: {
    badge: "PROVENANCE AUDIT",
    badgeColor: "bg-teal-700 text-white",
    title: "Universal Authority Provenance & Verification Model",
    subtitle: "Zero Hallucination Guarantee with Central Gazette Pinning",
    sections: [
      {
        heading: "68 Authenticated Primary Enactments",
        body: "All statutory texts are parsed directly from the Official Gazette of India (Extraordinary), containing the full legislative statement of objects, enabling sections, proviso conditions, and schedules."
      },
      {
        heading: "Reporter Cross-Validation",
        body: "Judicial propositions are verified against official Supreme Court Reports (SCR), Supreme Court Cases (SCC), and High Court reporters, ensuring no overturned precedents or dissenting dicta are cited as binding ratios."
      },
      {
        heading: "Synthetic Scaffold Quarantining",
        body: "Every response runs through an automated Proposition Provenance Auditor that quarantines unauthenticated synthetic assertions before token emission."
      }
    ],
    ctaText: "Audit Legal Sources",
    ctaLink: "/chat?q=Show+verified+statutory+sources"
  },

  // 3. Section 7 Source Cards
  source_dpdp: {
    badge: "ACT PROVISION",
    badgeColor: "bg-brand-ashokaBlue text-white",
    title: "Digital Personal Data Protection Act, 2023",
    subtitle: "Act No. 22 of 2023 • Section 6(1): Notice and Consent Safeguards",
    sections: [
      {
        heading: "Section 6(1) Statutory Requirement",
        body: "Every request for consent made to a Data Principal shall be accompanied or preceded by an itemised notice in clear and plain language, specifying the personal data sought to be processed, the exact purpose of processing, and how the citizen may exercise rights of withdrawal and grievance redressal."
      },
      {
        heading: "Multilingual Mandate",
        body: "The notice must provide the citizen the option to access the consent request in English or any of the 22 languages specified in the Eighth Schedule to the Constitution of India."
      },
      {
        heading: "Enforcement & Penalties",
        body: "Failure to provide adequate notice or breach of consent obligations can attract significant monetary penalties up to ₹250 crore adjudicated by the Data Protection Board of India."
      }
    ],
    ctaText: "Start a Conversation",
    ctaLink: "/chat"
  },

  source_puttaswamy: {
    badge: "SUPREME COURT JUDGMENT",
    badgeColor: "bg-brand-saffron text-white",
    title: "Justice K.S. Puttaswamy (Retd.) v. Union of India",
    subtitle: "(2017) 10 SCC 1 • 9-Judge Constitution Bench",
    sections: [
      {
        heading: "Fundamental Right to Privacy (Article 21)",
        body: "A unanimous 9-judge bench ruled that the right to privacy is an intrinsic part of the right to life and personal liberty under Article 21, and as a part of the freedoms guaranteed by Part III of the Constitution."
      },
      {
        heading: "The Three-Fold Proportionality Test",
        body: "Any state encroachment on personal privacy must satisfy three cumulative tests: (1) Legality: existence of an enabling law; (2) Need: a legitimate state aim; and (3) Proportionality: a rational nexus between the measure and the objective."
      },
      {
        heading: "Informational Privacy & Bodily Autonomy",
        body: "The Court held that informational privacy is a facet of privacy, safeguarding citizen autonomy against unauthorized surveillance and automated digital tracking."
      }
    ],
    ctaText: "Start a Conversation",
    ctaLink: "/chat"
  },

  source_gazette: {
    badge: "COMMENCEMENT GAZETTE",
    badgeColor: "bg-brand-forest text-white",
    title: "Official Gazette Notification: S.O. 848(E)",
    subtitle: "Ministry of Home Affairs • Appointed Date of Criminal Sanhitas",
    sections: [
      {
        heading: "Gazette Notification Details",
        body: "Published in Part II, Section 3, Sub-section (ii) of the Gazette of India Extraordinary on 23rd February 2024, notifying 1 July 2024 as the commencement date for the Bharatiya Nyaya Sanhita, 2023."
      },
      {
        heading: "Universal Jurisdiction Across Bharat",
        body: "The enactment extends to the whole of India, superseding the Indian Penal Code, 1860 for all offences committed on or after the appointed date."
      },
      {
        heading: "Statutory Exceptions",
        body: "Section 106(2) BNS concerning hit-and-run liabilities was explicitly excluded from enforcement under this notification until further notice."
      }
    ],
    ctaText: "Start a Conversation",
    ctaLink: "/chat"
  },

  // 4. Section 6: Six Sample Question Details
  sample_q1: {
    badge: "STATUTORY INTERPRETATION",
    badgeColor: "bg-brand-ashokaBlue text-white",
    title: "Interpreting Section 528, BNSS, 2023",
    subtitle: "Saving of Inherent Powers of High Court (Erstwhile Sec 482 CrPC)",
    sections: [
      {
        heading: "Scope of Inherent Powers",
        body: "Section 528 BNSS confirms that nothing in the Sanhita shall be deemed to limit or affect the inherent powers of the High Court to make such orders as may be necessary to give effect to any order, prevent abuse of the process of any court, or secure the ends of justice."
      },
      {
        heading: "Application to Commercial Disputes",
        body: "Where criminal proceedings (such as FIR under cheating or fraud) are launched as a coercive shortcut to resolve a purely commercial dispute, the High Court exercises Section 528 jurisdiction to quash the proceedings."
      }
    ],
    ctaText: "Start a Conversation",
    ctaLink: "/chat"
  },

  sample_q2: {
    badge: "LEGAL DEFINITION",
    badgeColor: "bg-brand-saffron text-white",
    title: "Doctrine of Mens Rea in Commercial Allegations",
    subtitle: "Guilty Mind vs. Mere Breach of Contract",
    sections: [
      {
        heading: "Essential Distinction",
        body: "Mens rea (guilty intention) must exist at the very inception of the contract to sustain a charge of cheating or fraud. A subsequent inability to perform or breach of warranty constitutes a civil wrong, not a criminal offence."
      },
      {
        heading: "Supreme Court Authorities",
        body: "In Hridaya Ranjan Prasad Verma v. State of Bihar, the Apex Court affirmed that the distinction between mere breach of contract and cheating depends upon the intention of the accused at the time of making the promise."
      }
    ],
    ctaText: "Start a Conversation",
    ctaLink: "/chat"
  },

  sample_q3: {
    badge: "EMPLOYMENT & CONTRACTS",
    badgeColor: "bg-brand-forest text-white",
    title: "Withholding Relieving Letters & Experience Certificates",
    subtitle: "Civil Rights, Service Deficiency & Labour Department Remedies",
    sections: [
      {
        heading: "Contractual & Service Remedies",
        body: "An employer cannot arbitrarily withhold earned relieving letters or experience certificates to force settlement of disputed claims. If notice period was duly served or bought out per the contract, withholding certificates constitutes unfair practice and breach of employment contract."
      },
      {
        heading: "Actionable Steps",
        body: "1. Send a formal legal demand letter via speed post citing contractual fulfillment.\\n2. Approach the State Labour Commissioner or file a summary suit / writ petition for mandatory delivery of records."
      }
    ],
    ctaText: "Start a Conversation",
    ctaLink: "/chat"
  },

  sample_q4: {
    badge: "COMPARATIVE ANALYSIS",
    badgeColor: "bg-brand-ashokaBlue text-white",
    title: "Comparative Transition: Section 482 CrPC vs Section 528 BNSS",
    subtitle: "Procedural Safeguards under Bharatiya Nagarik Suraksha Sanhita",
    sections: [
      {
        heading: "Textual & Substantive Parity",
        body: "Section 528 of BNSS preserves the foundational wording of erstwhile Section 482 CrPC, ensuring that decades of settled Supreme Court jurisprudence (including Bhajan Lal categories) remain fully operational."
      },
      {
        heading: "Electronic Case Filing Transition",
        body: "BNSS incorporates electronic filings and technological records, enabling digital verification of affidavits and lower court trial records during Section 528 quashing petitions."
      }
    ],
    ctaText: "Start a Conversation",
    ctaLink: "/chat"
  },

  sample_q5: {
    badge: "PRIMARY GAZETTE DISCOVERY",
    badgeColor: "bg-brand-forest text-white",
    title: "Locating Official Central Gazette Notifications",
    subtitle: "DPDP Act 2023 & Ministry Rules Publication Registry",
    sections: [
      {
        heading: "Official Publication Source",
        body: "The Digital Personal Data Protection Act, 2023 was published in the Gazette of India (Extraordinary, Part II—Section 1) on August 11, 2023 as Act No. 22 of 2023 after receiving Presidential assent."
      },
      {
        heading: "Enabling Section Commencement",
        body: "Under Section 1(2), different dates may be appointed for different provisions. Notifications are accessed via egazette.gov.in issued by the Ministry of Electronics and Information Technology (MeitY)."
      }
    ],
    ctaText: "Start a Conversation",
    ctaLink: "/chat"
  },

  sample_q6: {
    badge: "COMMENCEMENT STATUS",
    badgeColor: "bg-brand-saffron text-white",
    title: "Status of Section 106(2) BNS (Hit-and-Run Penalties)",
    subtitle: "Operative Status: Kept in Abeyance / Uncommenced",
    sections: [
      {
        heading: "Statutory Text & Proposed Penalty",
        body: "Section 106(2) BNS prescribes imprisonment up to 10 years and fine for drivers who cause death by rash and negligent driving and escape without reporting to a police officer."
      },
      {
        heading: "Current Legal Status",
        body: "Section 106(2) was NOT commenced on 1 July 2024. Following representations from transport associations, the Union Government affirmed that Section 106(2) will only be brought into force after further consultations. Predecessor standards under Section 106(1) BNS (punishable up to 5 years) apply currently."
      }
    ],
    ctaText: "Start a Conversation",
    ctaLink: "/chat"
  },

  // 5. Governance & Policy Modals
  privacy: {
    badge: "GOVERNANCE",
    badgeColor: "bg-brand-navy text-white",
    title: "Privacy & Client Confidentiality Policy",
    subtitle: "Local Sovereign Architecture Guarantee",
    sections: [
      {
        heading: "Zero Cloud Data Transmission",
        body: "LegalMitra is built as a local sovereign intelligence system. Your queries, legal memos, and research drafts are processed locally on your hardware with no tracking or remote ad logging."
      },
      {
        heading: "Attorney-Client Privilege Protection",
        body: "Because queries are not dispatched to third-party proprietary clouds, sensitive client matter facts remain strictly confidential within your local environment."
      }
    ],
    ctaText: "Start a Conversation",
    ctaLink: "/chat"
  },

  terms: {
    badge: "GOVERNANCE",
    badgeColor: "bg-brand-navy text-white",
    title: "Terms of Use & Research Standards",
    subtitle: "Empowering Citizen Rights & Academic Legal Research",
    sections: [
      {
        heading: "Public Legal Information Standard",
        body: "LegalMitra provides synthesized statutory and judicial intelligence for informational and educational purposes under the laws of the Republic of India."
      },
      {
        heading: "No Advocate-Client Relationship",
        body: "Using this platform does not create an advocate-client relationship. Actionable procedural timelines and court representation should always be verified with an advocate enrolled under the Advocates Act, 1961."
      }
    ],
    ctaText: "Start a Conversation",
    ctaLink: "/chat"
  },

  disclaimer: {
    badge: "LEGAL NOTICE",
    badgeColor: "bg-brand-ashokaBlue text-white",
    title: "Statutory Disclaimer & Verification Protocol",
    subtitle: "Compliance with Bar Council of India Guidelines",
    sections: [
      {
        heading: "Bar Council of India Compliance",
        body: "This service complies with Bar Council of India guidelines prohibiting advertisement and solicitation. LegalMitra provides unbiased primary source citations and procedural roadmaps without guaranteeing case outcomes."
      },
      {
        heading: "Emergency Contact",
        body: "For immediate physical safety, ongoing crimes, or life-threatening situations, always dial 112 directly."
      }
    ],
    ctaText: "Start a Conversation",
    ctaLink: "/chat"
  },

  methodology: {
    badge: "RESEARCH METHODOLOGY",
    badgeColor: "bg-brand-forest text-white",
    title: "15-Stage Deterministic Verification Engine",
    subtitle: "How LegalMitra Anchors Legal Output",
    sections: [
      {
        heading: "Stage 1–5: Query Parsing & Issue Mapping",
        body: "Queries are decomposed into candidate legal domains, material dates, territorial jurisdictions, and missing decisive facts."
      },
      {
        heading: "Stage 6–10: Gazette & Precedent Retrieval",
        body: "Primary Central Acts, delegated notifications, and Supreme Court ratio decidendi are retrieved with temporal relevance checks."
      },
      {
        heading: "Stage 11–15: Correctness Audit & Provenance Validation",
        body: "Claims undergo contradiction analysis and synthetic scaffold quarantine before being synthesized into human-accessible answers."
      }
    ],
    ctaText: "Start a Conversation",
    ctaLink: "/chat"
  }
};

/**
 * Open Modal Information Panel
 */
function openInfoModal(modalKey) {
  const data = MODAL_DATA[modalKey];
  if (!data) return;

  let modalEl = document.getElementById("legalmitra-info-modal");
  if (!modalEl) {
    modalEl = document.createElement("div");
    modalEl.id = "legalmitra-info-modal";
    modalEl.className = "fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm transition-opacity duration-200";
    document.body.appendChild(modalEl);
  }

  const sectionsHtml = data.sections.map(s => `
    <div class="space-y-1.5 p-4 rounded-lg bg-brand-ivory border border-brand-ivoryBorder">
      <h4 class="font-heading font-bold text-sm text-brand-navy">${s.heading}</h4>
      <p class="text-xs text-brand-slate leading-relaxed whitespace-pre-wrap">${s.body}</p>
    </div>
  `).join("");

  modalEl.innerHTML = `
    <div class="bg-white rounded-2xl shadow-2xl border border-brand-ivoryBorder max-w-2xl w-full max-h-[85vh] flex flex-col overflow-hidden animate-in fade-in zoom-in-95 duration-150">
      
      <!-- Modal Header -->
      <div class="px-6 py-5 border-b border-brand-ivoryBorder flex items-start justify-between gap-4 bg-brand-ivory/40">
        <div class="space-y-1">
          <span class="px-2.5 py-0.5 rounded text-[10px] font-bold tracking-wider uppercase ${data.badgeColor}">
            ${data.badge}
          </span>
          <h3 class="font-heading font-bold text-xl text-brand-navy mt-1">${data.title}</h3>
          <p class="text-xs text-brand-slate">${data.subtitle}</p>
        </div>
        <button onclick="closeInfoModal()" class="w-8 h-8 rounded-full bg-brand-ivoryDim hover:bg-brand-ivoryBorder text-brand-navy flex items-center justify-center transition-colors flex-shrink-0" title="Close Panel">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>
        </button>
      </div>

      <!-- Modal Body (Scrollable) -->
      <div class="p-6 overflow-y-auto space-y-4">
        ${sectionsHtml}
      </div>

      <!-- Modal Footer -->
      <div class="px-6 py-4 bg-brand-ivory/60 border-t border-brand-ivoryBorder flex items-center justify-between gap-3">
        <button onclick="closeInfoModal()" class="px-4 py-2 rounded-lg border border-brand-ivoryBorder hover:bg-white text-brand-slate text-xs font-semibold transition-colors">
          Close Panel
        </button>
        <a href="${data.ctaLink}" class="inline-flex items-center space-x-1.5 px-5 py-2.5 rounded-lg bg-brand-navy hover:bg-brand-ashokaBlue text-white text-xs font-bold transition-all shadow-sm">
          <span>${data.ctaText}</span>
          <svg class="w-3.5 h-3.5 text-brand-saffron" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"/></svg>
        </a>
      </div>

    </div>
  `;

  modalEl.style.display = "flex";
  document.body.style.overflow = "hidden";

  // Close on outside click
  modalEl.onclick = (e) => {
    if (e.target === modalEl) closeInfoModal();
  };
}

function closeInfoModal() {
  const modalEl = document.getElementById("legalmitra-info-modal");
  if (modalEl) {
    modalEl.style.display = "none";
  }
  document.body.style.overflow = "auto";
}

// Global exposure
window.openInfoModal = openInfoModal;
window.closeInfoModal = closeInfoModal;
