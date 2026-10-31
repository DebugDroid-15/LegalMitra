"""LegalMitra Interactive Web Workbench & Visual Legal Explorer (Phase 71).

A modern, responsive browser interface built on Streamlit providing:
1. Multi-turn Conversational Legal Assistant with IRAC prose rendering.
2. Verified Claim & Statutory Grounding Inspector.
3. Statutory Demand Notice Drafting Studio (NI 138, Arb 21, TPA 106, IBC 8).
4. Authoritative Knowledge Base & FTS Corpus Explorer.
"""

import os
import sys
import time
from datetime import date
from pathlib import Path

import streamlit as st

# Configure page metadata
st.set_page_config(
    page_title="LegalMitra — Indian Legal Intelligence",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Pipeline Imports
from legalmitra.drafting import (
    NoticeParty,
    NoticeType,
    StatutoryNoticeDraftingEngine,
)
from legalmitra.models.local_adapter import (
    LocalLegalModelAdapter,
    ModelAdapterConfig,
)
from legalmitra.orchestration.decision_policy import LegalResponseState
from legalmitra.orchestration.pipeline import LegalQueryPipeline

# Session State Initialization
if "session_id" not in st.session_state:
    st.session_state.session_id = f"web_session_{int(time.time())}"

if "messages" not in st.session_state:
    st.session_state.messages = []

if "pipeline" not in st.session_state:
    st.session_state.pipeline = LegalQueryPipeline()

if "model_mode" not in st.session_state:
    st.session_state.model_mode = "Deterministic Engine"


def update_pipeline_model(mode: str):
    """Update pipeline's model adapter according to selection."""
    if mode == "Neural LoRA (Kaggle Fine-Tuned)":
        adapter = LocalLegalModelAdapter()
        st.session_state.pipeline.model_adapter = adapter
        st.session_state.pipeline.answer_assembler.model_adapter = adapter
    elif mode == "Mock Neural (IRAC Simulator)":
        adapter = LocalLegalModelAdapter(ModelAdapterConfig(enable_mock_for_testing=True))
        st.session_state.pipeline.model_adapter = adapter
        st.session_state.pipeline.answer_assembler.model_adapter = adapter
    else:
        st.session_state.pipeline.model_adapter = None
        st.session_state.pipeline.answer_assembler.model_adapter = None


# --- SIDEBAR CONFIGURATION ---
with st.sidebar:
    st.title("⚖️ LegalMitra Core")
    st.markdown("**Enterprise Indian Legal Reasoning Engine**")
    st.divider()

    st.subheader("1. Synthesis Model and Perspective")
    chosen_mode = st.radio(
        "Response Generation Mode:",
        ["Deterministic Engine", "Mock Neural (IRAC Simulator)", "Neural LoRA (Kaggle Fine-Tuned)"],
        index=1,
    )
    audience_perspective = st.selectbox(
        "Target Audience View:",
        ["Dual-Layer (Plain English + Lawyer Analysis)", "Citizen Focus (Plain English First)", "Lawyer Focus (Strict Statutory IRAC)"],
        index=0,
    )
    if chosen_mode != st.session_state.model_mode:
        st.session_state.model_mode = chosen_mode
        update_pipeline_model(chosen_mode)

    st.divider()
    st.subheader("2. Temporal & Territorial Jurisdiction")
    selected_date = st.date_input("Point-in-Time Date:", value=date(2024, 9, 1))
    date_str = selected_date.isoformat() if selected_date else None

    jurisdiction_options = {
        "All India (Central / Supreme Court)": "IN",
        "Delhi (IN-DL)": "IN-DL",
        "Maharashtra (IN-MH)": "IN-MH",
        "Karnataka (IN-KA)": "IN-KA",
        "Tamil Nadu (IN-TN)": "IN-TN",
        "West Bengal (IN-WB)": "IN-WB",
    }
    selected_jur_label = st.selectbox("Territorial Jurisdiction:", list(jurisdiction_options.keys()))
    jur_code = jurisdiction_options[selected_jur_label]

    st.divider()
    if st.button("🔄 Reset Dialogue Memory", use_container_width=True):
        st.session_state.messages.clear()
        st.session_state.pipeline.dialogue_manager.get_or_create_session(st.session_state.session_id).reset()
        st.session_state.session_id = f"web_session_{int(time.time())}"
        st.rerun()

    # System Status Indicator
    adapter_available = LocalLegalModelAdapter().is_available
    st.markdown(
        f"**Local Adapter Status:** {'🟢 Ready (160MB)' if adapter_available else '🟡 Missing'}\n\n"
        f"**Corpus Units:** 1,515 authoritative chunks"
    )

# --- MAIN WORKBENCH TABS ---
tab_chat, tab_drafting, tab_corpus = st.tabs([
    "💬 Conversational Legal Assistant",
    "📝 Statutory Notice Drafting Studio",
    "📚 Knowledge Base & Corpus Explorer",
])

# ==============================================================================
# TAB 1: CONVERSATIONAL LEGAL ASSISTANT
# ==============================================================================
with tab_chat:
    st.markdown("### Interactive Indian Legal Consultation")
    st.caption("Answers are synthesized using strict 15-stage retrieval, temporal resolution, and claim verification.")

    # Render previous conversation turns
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if "claims" in msg and msg["claims"]:
                with st.expander(f"🔍 Grounded Claims & Citations ({len(msg['claims'])})"):
                    for c in msg["claims"]:
                        st.markdown(f"- **[{c['verdict']}]** `{c['id']}`: {c['text']}")
                    if msg.get("citations"):
                        st.markdown("**Formal Citations:**")
                        for cit in msg["citations"]:
                            st.markdown(f"- *{cit}*")

    # User input prompt
    if user_query := st.chat_input("Enter your Indian legal query (e.g. 'Can an interim injunction be granted in infrastructure contracts?')..."):
        # Display user message
        st.session_state.messages.append({"role": "user", "content": user_query})
        with st.chat_message("user"):
            st.markdown(user_query)

        # Execute Pipeline
        with st.chat_message("assistant"):
            with st.spinner("Executing 15-stage legal orchestration pipeline..."):
                t0 = time.time()
                resp = st.session_state.pipeline.execute(
                    query=user_query,
                    context_date=date_str,
                    jurisdiction=jur_code,
                    session_id=st.session_state.session_id,
                )
                duration_ms = round((time.time() - t0) * 1000.0, 2)

                # Render policy badge
                state_val = resp.response_state.value
                if state_val == "ANSWER_SUPPORTED":
                    st.success(f"DECISION STATE: {state_val} ({duration_ms} ms)")
                elif "QUALIFIED" in state_val or "CONDITIONAL" in state_val:
                    st.warning(f"DECISION STATE: {state_val} ({duration_ms} ms)")
                elif "CLARIFICATION" in state_val:
                    st.info(f"CLARIFICATION REQUIRED ({duration_ms} ms)")
                else:
                    st.error(f"ABSTENTION: {state_val} ({duration_ms} ms)")

                st.markdown(resp.answer_text)

                # Extract claims
                claims_payload = []
                if resp.assembled_answer and resp.assembled_answer.claims:
                    for clm in resp.assembled_answer.claims:
                        claims_payload.append({
                            "id": clm.claim_id,
                            "text": clm.claim_text,
                            "verdict": clm.validation_verdict,
                        })

                if claims_payload:
                    with st.expander(f"🔍 Grounded Claims & Citations ({len(claims_payload)})"):
                        for c in claims_payload:
                            st.markdown(f"- **[{c['verdict']}]** `{c['id']}`: {c['text']}")
                        if resp.citations:
                            st.markdown("**Formal Citations:**")
                            for cit in resp.citations:
                                st.markdown(f"- *{cit}*")

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": resp.answer_text,
                    "claims": claims_payload,
                    "citations": resp.citations,
                })


# ==============================================================================
# TAB 2: STATUTORY NOTICE DRAFTING STUDIO
# ==============================================================================
with tab_drafting:
    st.markdown("### Statutory Demand Notice Generator")
    st.caption("Generates legally compliant, court-ready demand notices strictly enforcing mandatory statutory cure periods.")

    col_type, col_date = st.columns([3, 1])
    with col_type:
        notice_choice = st.selectbox(
            "Select Statutory Notice Category:",
            [
                "Section 138 Negotiable Instruments Act (Cheque Dishonour Demand)",
                "Section 21 Arbitration & Conciliation Act (Notice of Invocation)",
                "Section 106 Transfer of Property Act (Tenancy Termination / Quit)",
                "Section 8 Insolvency & Bankruptcy Code (Operational Creditor Form 3)",
                "General Cease & Desist / Breach of Contract Demand",
            ]
        )
    with col_date:
        notice_date = st.date_input("Notice Date:", value=date.today())

    st.subheader("1. Parties Details")
    col_sender, col_recip = st.columns(2)
    with col_sender:
        s_name = st.text_input("Sender / Complainant Name:", "ABC Corporation Limited")
        s_addr = st.text_input("Sender Address:", "123 Barakhamba Road, Connaught Place, New Delhi")
        s_adv = st.text_input("Advocate Name:", "Advocate R. Sharma")
        s_enr = st.text_input("Bar Enrollment Number:", "D/1234/2015")

    with col_recip:
        r_name = st.text_input("Recipient / Opposite Party Name:", "XYZ Enterprises Private Limited")
        r_addr = st.text_input("Recipient Address:", "Plot 45, Udyog Vihar Phase 4, Gurugram, HR")

    st.subheader("2. Factual Particulars")
    facts_dict = {}

    if "Section 138" in notice_choice:
        col_c1, col_c2, col_c3 = st.columns(3)
        with col_c1:
            facts_dict["cheque_number"] = st.text_input("Cheque Number:", "458901")
            facts_dict["cheque_date"] = st.text_input("Cheque Date (YYYY-MM-DD):", "2024-05-10")
        with col_c2:
            facts_dict["cheque_amount"] = st.text_input("Cheque Amount (INR):", "5,00,000")
            facts_dict["bank_name"] = st.text_input("Drawee Bank & Branch:", "HDFC Bank, K.G. Marg")
        with col_c3:
            facts_dict["return_memo_date"] = st.text_input("Return Memo Date:", "2024-05-15")
            facts_dict["dishonour_reason"] = st.selectbox("Reason for Dishonour:", ["Funds Insufficient", "Exceeds Arrangement", "Account Closed", "Stop Payment"])
        target_ntype = NoticeType.CHEQUE_BOUNCE_NI_ACT_138

    elif "Arbitration" in notice_choice:
        col_a1, col_a2 = st.columns(2)
        with col_a1:
            facts_dict["contract_title"] = st.text_input("Contract Title:", "EPC Commercial Construction Agreement")
            facts_dict["contract_date"] = st.text_input("Contract Date:", "2022-03-15")
            facts_dict["arbitration_clause"] = st.text_input("Arbitration Clause:", "Clause 21.2 (Arbitration)")
        with col_a2:
            facts_dict["claim_amount"] = st.text_input("Estimated Claim Amount:", "2,50,00,000")
            facts_dict["proposed_arbitrator"] = st.text_input("Proposed Arbitrator:", "Justice (Retd.) S.K. Kaul")
            facts_dict["nature_of_disputes"] = st.text_area("Nature of Disputes:", "Unpaid milestone invoices and unlawful termination")
        target_ntype = NoticeType.ARBITRATION_INVOCATION_SEC_21

    elif "Section 106" in notice_choice:
        col_t1, col_t2 = st.columns(2)
        with col_t1:
            facts_dict["property_address"] = st.text_input("Demised Premises Address:", "Shop 4, MI Road, Jaipur, Rajasthan")
            facts_dict["lease_date"] = st.text_input("Lease Date:", "2021-01-01")
        with col_t2:
            facts_dict["monthly_rent"] = st.text_input("Monthly Rent (INR):", "35,000")
            facts_dict["ground_for_eviction"] = st.text_area("Ground for Eviction:", "Non-payment of rent for 6 consecutive months")
        target_ntype = NoticeType.TENANCY_TERMINATION_TPA_106

    elif "Insolvency" in notice_choice:
        col_i1, col_i2 = st.columns(2)
        with col_i1:
            facts_dict["debt_amount"] = st.text_input("Operational Debt Amount (INR):", "1,20,00,000")
            facts_dict["default_date"] = st.text_input("Date of Default:", "2024-01-15")
        with col_i2:
            facts_dict["invoices"] = st.text_input("Invoice Numbers:", "INV-101, INV-102, INV-108")
        target_ntype = NoticeType.IBC_OPERATIONAL_CREDITOR_SEC_8

    else:
        facts_dict["subject"] = st.text_input("Notice Subject:", "Legal Demand for Performance of Contract")
        facts_dict["grievance"] = st.text_area("Grievance Details:", "Breach of contractual delivery schedule")
        facts_dict["demand_text"] = st.text_input("Specific Demand:", "Complete pending deliverables immediately")
        facts_dict["cure_days"] = st.number_input("Cure Days:", value=15)
        target_ntype = NoticeType.GENERAL_LEGAL_DEMAND

    if st.button("📄 Generate Statutory Legal Notice", type="primary", use_container_width=True):
        sender_obj = NoticeParty(name=s_name, address=s_addr, advocate_name=s_adv, advocate_enrollment=s_enr)
        recip_obj = NoticeParty(name=r_name, address=r_addr)

        draft = StatutoryNoticeDraftingEngine.draft_notice(
            notice_type=target_ntype,
            sender=sender_obj,
            recipient=recip_obj,
            facts=facts_dict,
            as_of_date=notice_date.isoformat(),
        )

        st.success(f"Draft Generated Successfully! Mandatory Cure Window: {draft.mandatory_cure_period_days} Days.")
        st.markdown(draft.full_notice_markdown)
        st.download_button(
            label="💾 Download Notice (.md)",
            data=draft.full_notice_markdown,
            file_name=f"legal_notice_{target_ntype.value.lower()}.md",
            mime="text/markdown",
            use_container_width=True,
        )


# ==============================================================================
# TAB 3: KNOWLEDGE BASE & CORPUS EXPLORER
# ==============================================================================
with tab_corpus:
    st.markdown("### Authoritative Legal Knowledge Base")
    st.caption("Inspect indexed statutory chunks, commencement dates, and search index reconciliation health.")

    kb = st.session_state.pipeline.kb
    audit = kb.audit_search_index()

    col_m1, col_m2, col_m3 = st.columns(3)
    col_m1.metric("Indexed Chunks (KB)", audit.get("main_chunks_count", 1515))
    col_m2.metric("FTS Search Index Chunks", audit.get("fts_chunks_count", 1515))
    col_m3.metric("FTS Synchronization", "100% Synchronized" if audit.get("is_synchronized", True) else "Desynchronized")

    st.subheader("Full-Text Search (FTS5) Query Explorer")
    search_query = st.text_input("Enter search keywords across the Indian legal corpus:", "Section 20A Specific Relief")
    if search_query:
        results = kb.search(search_query, limit=5)
        st.write(f"Found {len(results)} authoritative chunks:")
        for r in results:
            title = r.act_or_case_title or "Statutory Law"
            ref = r.provision_or_para_ref or (f"Section {r.section_number}" if r.section_number else "")
            with st.expander(f"📌 {title} {('— ' + ref) if ref else ''}"):
                st.markdown(f"**Chunk ID:** `{r.chunk_id}` | **Date:** `{r.effective_date or r.document_date or 'N/A'}` | **Jurisdiction:** `{r.jurisdiction}`")
                st.text(r.content[:400] + ("..." if len(r.content) > 400 else ""))
