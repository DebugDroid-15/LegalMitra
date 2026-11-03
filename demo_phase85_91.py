"""
Interactive LegalMitra Test & Demonstration CLI
Quick test runner for the Sovereign AI Kosh Mega Knowledge Base (Phases 85-91).
"""

import sys
from legalmitra.corpus.tri_code_crosswalk import ExtendedTriCodeKnowledgeGraph
from legalmitra.evaluation.phase91_adversarial_hardening import AdversarialBenchmarkHarness
from legalmitra.multilingual.bhashini_pipeline import BhashiniIndicLegalBridge, IndicLanguageCode
from legalmitra.retrieval.mega_hybrid_engine import MegaHybridRetrievalEngine
from legalmitra.training.aikosh_finetuner import AIKoshLegalFineTuner


def run_interactive_demo():
    print("=" * 80)
    print("      LEGALMITRA SOVEREIGN MEGA KNOWLEDGE BASE (PHASES 85-91) DEMO")
    print("=" * 80)

    # 1. Tri-Code Crosswalk & Precedent Lineage
    print("\n[1] TESTING TRI-CODE CROSSWALK & TEMPORAL SAVINGS (Phase 87):")
    graph = ExtendedTriCodeKnowledgeGraph()
    print("  -> Querying IPC Section 420 (Cheating)...")
    matches = graph.lookup_old_provision("IPC", "420")
    if matches:
        m = matches[0]
        print(f"     Successor: {m.new_code} {m.new_section} - {m.new_title}")
        print(f"     Landmark Precedent Lineage: {', '.join(m.landmark_judgments)}")

    print("\n  -> Testing Article 20(1) Date Routing for Offence on '2024-03-15':")
    dec_old = graph.route_by_incident_date("2024-03-15")
    print(f"     Regime: {dec_old.regime.value} | Governed Substantively by: {dec_old.substantive_code}")

    print("\n  -> Testing Date Routing for Offence on '2024-09-01':")
    dec_new = graph.route_by_incident_date("2024-09-01")
    print(f"     Regime: {dec_new.regime.value} | Governed Substantively by: {dec_new.substantive_code}")

    # 2. Mega Hybrid Retrieval Engine
    print("\n" + "-" * 80)
    print("[2] TESTING MEGA HYBRID RETRIEVAL & CITATION PINNING (Phase 88):")
    engine = MegaHybridRetrievalEngine()
    test_q = "Section 316 BNS Criminal Breach of Trust"
    print(f"  -> Hybrid Search Query: '{test_q}'")
    hits = engine.search_hybrid(test_q, limit=2)
    for i, h in enumerate(hits, 1):
        print(f"     Hit {i}: {h.citation} (Combined Score: {h.combined_score:.4f}, Pinned: {h.citation_pinned})")

    # 3. AI Kosh Fine-Tuned Model Inference
    print("\n" + "-" * 80)
    print("[3] TESTING AI KOSH FINE-TUNED LEGAL LLM INFERENCE (Phase 89):")
    finetuner = AIKoshLegalFineTuner()
    prompt = "police station refuses to register my FIR"
    print(f"  -> User Prompt: '{prompt}'")
    answer = finetuner.generate_response(prompt)
    print(f"     Model Response (First 250 chars):\n     {answer[:250]}...")

    # 4. Multilingual Translation & Citation Shielding
    print("\n" + "-" * 80)
    print("[4] TESTING BHASHINI 22 INDIC MULTILINGUAL TRANSLATION (Phase 90):")
    bridge = BhashiniIndicLegalBridge()
    sample_text = "To file an Anticipatory Bail petition regarding Cheating, apply under Section 482 BNSS."
    print(f"  -> English Source: '{sample_text}'")
    
    # Translate to Hindi
    hi_res = bridge.translate_legal_text(sample_text, IndicLanguageCode.HINDI)
    print(f"     Hindi Output  : {hi_res.translated_text.encode('ascii', 'backslashreplace').decode('ascii')}")
    
    # Translate to Marathi
    mr_res = bridge.translate_legal_text(sample_text, IndicLanguageCode.MARATHI)
    print(f"     Marathi Output: {mr_res.translated_text.encode('ascii', 'backslashreplace').decode('ascii')}")

    # 5. Adversarial Guardrails
    print("\n" + "-" * 80)
    print("[5] TESTING ADVERSARIAL BENCHMARK & GUARDRAILS (Phase 91):")
    harness = AdversarialBenchmarkHarness()
    summary = harness.run_full_benchmark()
    print(f"     Adversarial Test Suite: {summary['passed']}/{summary['total_cases']} Passed ({summary['adversarial_accuracy_pct']}%)")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    run_interactive_demo()

