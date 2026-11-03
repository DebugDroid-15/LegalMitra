"""
Unit tests for Phase 108: Multi-Tenant Advocate Practice Management & Sovereign Vault.
"""
import pytest
from legalmitra.vault.practice_engine import practice_vault_engine

def test_practice_vault_matter_lifecycle():
    firm_id = "FIRM-TEST-DELHI"
    matter = practice_vault_engine.create_matter(
        tenant_firm_id=firm_id,
        client_name="Rajesh Exports Ltd",
        case_title="Rajesh Exports v. Commercial Freight Corp",
        court_jurisdiction="High Court of Delhi",
        dispute_category="Commercial Arbitration",
        lead_advocate="Adv. V. K. Tandon",
        cnr_number="DLHC010098762024"
    )

    assert matter.matter_id.startswith("MAT-")
    assert matter.tenant_firm_id == firm_id
    assert len(matter.timeline) == 1

    # Add hearing timeline entry
    updated = practice_vault_engine.add_timeline_entry(
        matter_id=matter.matter_id,
        stage_name="Notice of Motion Hearing",
        recorded_notes="Ad-interim injunction granted against bank guarantee encashment.",
        advocate_id="Adv. V. K. Tandon"
    )
    assert len(updated.timeline) == 2
    assert "injunction granted" in updated.timeline[1].recorded_notes

    # Upload encrypted document to vault
    doc = practice_vault_engine.upload_vault_document(
        matter_id=matter.matter_id,
        doc_title="Section 9 Arbitration Petition.pdf",
        category="Pleadings",
        raw_text_content="Confidential petition text with trade secrets and bank guarantee terms."
    )
    assert doc.doc_id.startswith("DOC-")
    assert "AES-256" in doc.encryption_cipher
    assert "SHA256:" in doc.sha256_checksum

    # List firm matters
    firm_matters = practice_vault_engine.list_firm_matters(firm_id)
    assert any(m.matter_id == matter.matter_id for m in firm_matters)
