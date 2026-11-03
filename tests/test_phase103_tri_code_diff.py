"""
Unit tests for Phase 103: Tri-Code Redline Diff & Statutory Transition Visualizer.
"""
import pytest
from legalmitra.corpus.redline_engine import tri_code_redline_engine

def test_compare_sections_ipc_bns_cheating():
    res = tri_code_redline_engine.compare_sections("IPC", "420", "BNS", "318(4)")
    assert res.old_code == "IPC"
    assert res.new_code == "BNS"
    assert len(res.diff_blocks) > 0
    assert "ins" in res.diff_html
    assert len(res.key_substantive_changes) > 0

def test_compare_sections_crpc_bnss_fir():
    res = tri_code_redline_engine.compare_sections("CrPC", "154", "BNSS", "173")
    assert res.old_section == "154"
    assert res.new_section == "173"
    assert "del" in res.diff_html
    assert any("electronic" in c.lower() for c in res.key_substantive_changes)
