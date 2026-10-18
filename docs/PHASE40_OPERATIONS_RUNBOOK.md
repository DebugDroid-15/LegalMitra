# PHASE 40 — OPERATIONS RUNBOOK

## 1. High Court Connectors Operation

### Running Discovery (Dry-Run Mode)
```bash
python -c "
from legalmitra.judicial.connectors import DelhiHighCourtConnector
conn = DelhiHighCourtConnector(dry_run=True)
docs = conn.discover_documents({'year': 2024, 'limit': 10})
print(f'Discovered {len(docs)} judgments for High Court of Delhi')
"
```

### Running Bombay High Court Multi-Bench Discovery
```bash
python -c "
from legalmitra.judicial.connectors import BombayHighCourtConnector
conn = BombayHighCourtConnector(dry_run=True)
for bench in ['OS', 'AS', 'NAG', 'AUR', 'GOA']:
    docs = conn.discover_documents({'year': 2023, 'bench_code': bench, 'limit': 5})
    print(f'Bench {bench}: {len(docs)} documents discovered')
"
```

---

## 2. eCourts CIS Ingestion & Validation

### Validating a CNR
```bash
python -c "
from legalmitra.judicial.ecourts_protocol import ECourtsProtocolValidator
validator = ECourtsProtocolValidator()
res = validator.validate_cnr('DLTH010012342023')
print('CNR Valid:', res.is_valid, 'State:', res.state_code, 'Year:', res.filing_year)
"
```

### Processing Ingestion Batch
```bash
python -c "
from legalmitra.judicial.ecourts_protocol import ECourtsProtocolValidator
validator = ECourtsProtocolValidator()
sample = {
    'cnr_number': 'MHCC020056782022',
    'state_name': 'Maharashtra',
    'district_name': 'Mumbai',
    'court_establishment': 'City Civil Court',
    'case_type': 'Summary Suit',
    'filing_number': '5678/2022',
    'registration_date': '2022-07-10',
    'petitioner': 'Bank A',
    'respondent': 'Company B',
    'governing_acts': ['CPC Order 37'],
    'order_date': '2023-05-18',
    'disposal_nature': 'DECREED',
    'raw_text': 'Commercial claim decreed under Order 37 CPC.'
}
rec = validator.process_record(sample)
print('Record Stage:', rec.stage.value, 'Retrieval Eligible:', rec.is_retrieval_eligible)
"
```

---

## 3. Devanagari OCR Normalization & QA

### Normalizing Hindi Text & Computing Quality Metrics
```bash
python -c "
from legalmitra.judicial.devanagari_ocr import DevanagariOCREngine
engine = DevanagariOCREngine()
text = 'उच्चतम न्यायालय ने जमानत प्रदान की ।'
res = engine.normalize(text)
print('Normalized:', res.normalized_text)
print('Legal Tokens:', res.legal_tokens_detected)
print('Requires Review:', res.requires_human_review)
"
```

---

## 4. Precedent Conflict Triage Management

### Resolving a Registered Conflict (Advocate Reviewers Only)
```bash
python -c "
from legalmitra.judicial.conflict_triage import PrecedentConflictTriageManager, TriageStatus
manager = PrecedentConflictTriageManager()
# Requires ADV-SHATRUJEET-01 or ADV-REGULATORY-LEAD
# manager.resolve_conflict(conflict_id='CONF-2026-003', reviewer_id='ADV-SHATRUJEET-01', resolution_status=TriageStatus.RESOLVED_FACTUALLY_DISTINGUISHED, rationale='Verified factual distinctions between lease and EPC contracts.')
"
```

---

## 5. Regression Testing & Invariant Audit
```bash
pytest -v tests/test_phase40_operational_infrastructure.py
python scripts/verify_freeze.py
python scripts/verify_review_packages.py
pytest -q
```
