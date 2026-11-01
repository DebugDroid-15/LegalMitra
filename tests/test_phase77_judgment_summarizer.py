"""Tests for Phase 77: Automated Case Brief & Judicial Judgment Summarizer Engine."""

import pytest
from legalmitra.caselaw.brief_engine import (
    JudgmentSummarizerEngine,
    CaseBrief,
    JudicialMetadata,
)

SAMPLE_SUPREME_COURT_JUDGMENT = """
IN THE SUPREME COURT OF INDIA
CRIMINAL APPELLATE JURISDICTION

CRIMINAL APPEAL NO. 1420 OF 2023

Vikram Singh & Anr.                     ...Appellants
                                Versus
State of Punjab & Ors.                  ...Respondents

CORAM:
HON'BLE MR. JUSTICE ABHAY S. OKA
HON'BLE MR. JUSTICE UJJAL BHUYAN

JUDGMENT

1. This appeal arises out of the conviction recorded under Section 302 of the IPC and Section 41A of the CrPC.
The prosecution alleged that the appellants were involved in an altercation resulting in fatal injuries.

2. Learned counsel for the appellant placed reliance on Arnesh Kumar v. State of Bihar (2014) 8 SCC 273,
contending that mandatory statutory arrest procedures under Section 41 of the CrPC were flagrantly violated.

3. We have carefully examined the records and statutory mandates.
We hold that strict compliance with procedural safeguards prior to arrest is an integral component of Article 21.
Where the police officer fails to record reasons in terms of Section 41A of the CrPC, the detention is vitiated in law.

4. It may be observed that administrative circulars issued by state director generals cannot override statutory provisions.

5. In view of the above discussion, the criminal appeal is allowed. The impugned judgment of conviction is set aside.
The appellants are directed to be released forthwith.
"""

SAMPLE_HIGH_COURT_BAIL_ORDER = """
IN THE HIGH COURT OF DELHI AT NEW DELHI
BAIL APPLN. 2891/2024

Rohit Sharma                            ...Petitioner
                                Versus
State (NCT of Delhi)                    ...Respondent

BEFORE:
HON'BLE MR. JUSTICE ANUP JAIRAM BHAMBHANI

ORDER

1. The applicant seeks regular bail under Section 439 of the CrPC in connection with FIR registered under Section 420 of the IPC.
2. The dispute arises primarily out of a commercial agreement. It is settled law that criminal proceedings cannot be used as a recovery mechanism.
3. Bail application allowed. The applicant is directed to be released on bail on furnishing a personal bond of Rs. 50,000/- with one surety.
"""


class TestPhase77JudgmentSummarizer:
    """Test suite certifying Case Brief & Judgment Summarizer Engine."""

    def test_extract_court_name(self):
        """Test identification of Supreme Court and High Courts."""
        sc_court = JudgmentSummarizerEngine.extract_court_name(SAMPLE_SUPREME_COURT_JUDGMENT)
        assert sc_court == "Supreme Court of India"

        delhi_court = JudgmentSummarizerEngine.extract_court_name(SAMPLE_HIGH_COURT_BAIL_ORDER)
        assert "High Court of Delhi" in delhi_court

    def test_extract_case_title(self):
        """Test extraction of petitioner vs respondent header."""
        sc_title = JudgmentSummarizerEngine.extract_case_title(SAMPLE_SUPREME_COURT_JUDGMENT)
        assert "Vikram Singh" in sc_title
        assert "State of Punjab" in sc_title

    def test_extract_coram_bench(self):
        """Test extraction of presiding judges."""
        coram = JudgmentSummarizerEngine.extract_bench_coram(SAMPLE_SUPREME_COURT_JUDGMENT)
        assert any("Abhay S. Oka" in j for j in coram)
        assert any("Ujjal Bhuyan" in j for j in coram)

    def test_extract_disposition(self):
        """Test final outcome classification (Appeal Allowed, Bail Granted)."""
        disp_sc = JudgmentSummarizerEngine.extract_disposition(SAMPLE_SUPREME_COURT_JUDGMENT)
        assert "Appeal Allowed" in disp_sc

        disp_bail = JudgmentSummarizerEngine.extract_disposition(SAMPLE_HIGH_COURT_BAIL_ORDER)
        assert "Bail Application Allowed" in disp_bail

    def test_detect_statutory_transitions_bns_bnss(self):
        """Verify cross-mapping of legacy IPC/CrPC sections to 2024 BNS/BNSS codes."""
        transitions = JudgmentSummarizerEngine.detect_statutory_transitions(SAMPLE_SUPREME_COURT_JUDGMENT)
        
        acts = [t.modern_act for t in transitions]
        sections = [t.modern_section for t in transitions]

        # IPC 302 -> BNS 103
        assert any("Bharatiya Nyaya Sanhita" in act for act in acts)
        assert any("Section 103" in sec for sec in sections)

        # CrPC 41A -> BNSS 35(3)
        assert any("Bharatiya Nagarik Suraksha Sanhita" in act for act in acts)
        assert any("Section 35" in sec for sec in sections)

    def test_extract_precedents_relied(self):
        """Verify citation detection of landmark precedents."""
        precedents = JudgmentSummarizerEngine.extract_precedents_relied(SAMPLE_SUPREME_COURT_JUDGMENT)
        assert any("Arnesh Kumar" in p for p in precedents)

    def test_full_case_brief_generation(self):
        """Verify end-to-end Markdown brief compilation."""
        brief = JudgmentSummarizerEngine.summarize_judgment(SAMPLE_SUPREME_COURT_JUDGMENT)
        assert isinstance(brief, CaseBrief)
        assert "Supreme Court of India" in brief.full_brief_markdown
        assert "Ratio Decidendi" in brief.full_brief_markdown
        assert "Statutory Transition Notice" in brief.full_brief_markdown
        assert "Appeal Allowed" in brief.full_brief_markdown
