from pathlib import Path

p = Path("tests/test_phase56_multi_authority_synthesis.py")
content = p.read_text(encoding="utf-8").replace("\r\n", "\n")

old_test = """    def test_empty_retrieval_returns_calibrated_abstention(self, pipeline):
        # Completely nonexistent legal subject
        q = "What is the legal process under Indian interplanetary Martian mining statute 9999?"
        resp = pipeline.execute(q)
        assert resp.response_state == LegalResponseState.ABSTAIN_INSUFFICIENT_EVIDENCE
        assert "INSUFFICIENT" in resp.answer_text
        assert resp.telemetry.abstention_triggered is True"""

new_test = """    def test_empty_retrieval_returns_calibrated_abstention(self):
        # Empty knowledge base returns deterministic ABSTAIN_INSUFFICIENT_EVIDENCE
        empty_kb = LegalKnowledgeBase(db_path=":memory:")
        empty_pipe = LegalQueryPipeline(kb=empty_kb)
        resp = empty_pipe.execute("What is the legal process under interplanetary Martian mining statute 9999?")
        assert resp.response_state == LegalResponseState.ABSTAIN_INSUFFICIENT_EVIDENCE
        assert "INSUFFICIENT" in resp.answer_text
        assert resp.telemetry.abstention_triggered is True"""

assert old_test in content, "old_test not found"
content = content.replace(old_test, new_test, 1)
p.write_text(content, encoding="utf-8")
print("Updated successfully.")
