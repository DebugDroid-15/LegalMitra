# LegalMitra Phase 43 — Operations Runbook

**Date:** October 19, 2026  
**Audience:** Pipeline Engineers, Systems Operators, and Corpus Auditors  

---

## 1. Daily Invariant & System Integrity Verification

Execute prior to committing or tagging any release:

```powershell
# 1. Verify Phase 9 Freeze Snapshot Files
python scripts/verify_freeze.py

# 2. Verify Advocate Review Packages & Tracking Register
python scripts/verify_review_packages.py

# 3. Evaluate Real-World Scanned Hindi OCR Benchmark
python scripts/evaluate_real_world_ocr.py

# 4. Reconcile Multi-Layer Corpus & Database Separation
python scripts/reconcile_phase42_corpus.py

# 5. Run Full Test Suite
pytest -q
```

---

## 2. Auditing Scanned Hindi OCR with Micro and Macro Metrics

To audit OCR error rates across authentic vernacular legal pages:

```powershell
python scripts/evaluate_real_world_ocr.py
```
Expected production thresholds:
- Macro Normalized CER: $\le 1.50\%$ (measured 1.42%)
- Micro Normalized CER: $\le 1.50\%$ (measured 1.46%)
- Macro Normalized WER: $\le 3.00\%$ (measured 2.64%)
- Micro Normalized WER: $\le 3.00\%$ (measured 2.76%)
- Legal Token Recall: $\ge 98.00\%$ (measured 100.00%)

---

## 3. Verifying Whitelist-Protected Anusvara Normalization

Test normalization of legal terms alongside tadbhav words:

```powershell
python -c "
from legalmitra.judicial.devanagari_ocr import DevanagariOCREngine
engine = DevanagariOCREngine()
# Tadbhav words with genuine Chandrabindu must be preserved
print('Tadbhav preservation:', engine.normalize('गाँव में पाँच लोग रहते हैं।').normalized_text)
# Tatsama legal terms with OCR noise must be normalized
print('Legal normalization :', engine.normalize('सँविधान के अनुच्छेद 226 के अधीन सँरक्षण।').normalized_text)
"
```
