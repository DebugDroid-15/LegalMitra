# LEGALMITRA — PHASE 44 OPERATIONS RUNBOOK
## Runbooks 19 through 23: OCR Normalization, Quality Gating, RAG Validation & Preflight

**Audit Date:** 2026-10-19T11:34:30+05:30  
**Target Repository:** `https://github.com/DebugDroid-15/LegalMitra`  
**Workspace:** `C:\PROJECTS\LegalMitra`  
**Auditor:** Shatrujeet Audit & Infrastructure Engineering Team  
**Classification:** PROPRIETARY AND CONFIDENTIAL  

---

### Runbook 19: Daily Invariant & Frozen Asset Audit

**Objective:** Verify that no baseline frozen files or advocate review candidates have drifted.

```powershell
# 1. Verify Phase 9 frozen files (must return 100% match on all 6 SHA-256 hashes)
python scripts/verify_freeze.py

# 2. Verify advocate review package candidates (must confirm all 40 are pending_legal_review)
python scripts/verify_review_packages.py

# 3. Verify physical database separation and scaffold quarantine
python -c "
import sqlite3
kb = sqlite3.connect('data/legalmitra_kb.db')
scaff = kb.cursor().execute('SELECT count(*) FROM legal_chunks WHERE is_synthetic_scaffold=1').fetchone()[0]
kb.close()
assert scaff == 6, f'Expected 6 quarantined scaffold chunks, found {scaff}'
print('[OK] Scaffold isolation verified: 6 quarantined chunks.')
"
```

---

### Runbook 20: OCR Normalization & Tadbhav Preservation Verification

**Objective:** Verify that Devanagari OCR normalization correctly protects tadbhav inflections while converting OCR noise in tatsama terms.

```powershell
python -c "
from legalmitra.judicial.devanagari_ocr import DevanagariOCREngine
engine = DevanagariOCREngine()

# 1. Test tadbhav inflections
tadbhav = 'गाँवों में पाँचों व्यक्ति अपनी आँखों से जाँच-पड़ताल देख रहे थे।'
res_tadbhav = engine.normalize(tadbhav)
assert res_tadbhav.normalized_text == tadbhav
print('[OK] Tadbhav inflections preserved 100%:', res_tadbhav.normalized_text)

# 2. Test tatsama normalization
tatsama = 'सँविधान के अनुच्छेद 226 के अधीन सँरक्षण और सँख्या।'
res_tatsama = engine.normalize(tatsama)
assert res_tatsama.normalized_text == 'संविधान के अनुच्छेद 226 के अधीन संरक्षण और संख्या।'
print('[OK] Tatsama normalization verified 100%:', res_tatsama.normalized_text)
"
```

---

### Runbook 21: OCR Quality Gate Operational Evaluation

**Objective:** Evaluate an unindexed scanned Hindi document against the fail-closed quality gate.

```powershell
python -c "
from legalmitra.judicial.ocr_quality_gate import OCRQualityGate, OCRQualityState
gate = OCRQualityGate()

metadata = {
    'page_id': 'INSPECT-001',
    'court_or_source': 'IND-HC-ALL',
    'source_url': 'https://example.gov.in/order.pdf',
    'raw_ocr_text_hash': 'a'*64,
    'scan_resolution_dpi': 300,
}

raw_text = 'उच्च न्यायालय इलाहाबाद द्वारा आपराधिक प्रकीर्ण जमानत याचिका स्वीकार की गई। यह आदेश धारा 439 के अधीन पारित किया गया।'
assessment = gate.evaluate_page(raw_text, metadata=metadata)
print(f'Quality State: {assessment.state.value}')
print(f'Retrieval Eligible: {assessment.is_retrieval_eligible}')
print(f'Heuristic Confidence: {assessment.heuristic_confidence}')
print(f'Detected Sections: {assessment.metrics[\"sections_detected\"]}')
"
```

---

### Runbook 22: End-to-End Failure Scenario Testing

**Objective:** Execute the 10 legal failure scenarios through `OCRRAGValidator`.

```powershell
python -c "
from legalmitra.judicial.ocr_rag_validator import OCRRAGValidator
validator = OCRRAGValidator()
results = validator.evaluate_10_failure_scenarios()
print(f'Evaluated {len(results)} failure scenarios.')
assert all(r.passed for r in results), 'One or more failure scenarios failed validation!'
assert all(r.retrieval_safe for r in results), 'Unsafe retrieval detected in failure scenarios!'
print('[OK] All 10 legal failure scenarios handled safely with zero false advice.')
"
```

---

### Runbook 23: Preflight Connector Security & Credential Audit

**Objective:** Execute preflight checks before any connector dry-run without printing secrets.

```powershell
python scripts/run_controlled_high_court_pilot.py
```

