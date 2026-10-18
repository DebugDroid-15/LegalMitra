"""
CLI Reference Generator for LegalMitra README Appendix D.
Provides exhaustive parameter and usage documentation for all primary operational scripts.
"""

def generate_detailed_cli_reference() -> str:
    cli_tools = [
        ("scripts/verify_freeze.py",
         "python scripts/verify_freeze.py",
         "Cryptographically asserts that all 6 Phase 9 frozen review artifacts remain 100% bitwise identical to their locked SHA-256 signatures, all 20 records remain strictly in pending_legal_review, and zero references to quarantined scaffold IND-JUD-DEL-2024-BAIL exist.",
         "None (Non-interactive strict assertion).",
         "Exit 0: All 6 files pass bitwise hash check and quarantine rules.\nExit 1: Hash mismatch or quarantine leakage detected.",
         "```powershell\npython scripts/verify_freeze.py\n```"),

        ("scripts/verify_review_packages.py",
         "python scripts/verify_review_packages.py",
         "Validates Package A (Pilot 20 frozen snapshot), Package B (Batch 01 candidate expansion), and review_tracking_register.json to verify that exactly 40 records are tracked, all 40 remain in pending_legal_review, and no automated approval occurred.",
         "None (Strict assertion).",
         "Exit 0: Package A, Package B, and tracking register verified.\nExit 1: Tracking drift or schema violation.",
         "```powershell\npython scripts/verify_review_packages.py\n```"),

        ("scripts/run_phase35_small_model_regression.py",
         "python scripts/run_phase35_small_model_regression.py",
         "Executes 50-step regression pretraining of the 1,069,824-parameter causal Transformer on Manifest v4. Measures initial loss, final loss, training throughput (tokens/sec), VRAM utilization, and exports checkpoint hash.",
         "Optional: `--device {cuda|cpu}`, `--batch-size INT` (default 32), `--steps INT` (default 50).",
         "Exit 0: Model trained, loss converged, and checkpoint saved.\nExit 1: Loss divergence or hardware exception.",
         "```powershell\npython scripts/run_phase35_small_model_regression.py\n```"),

        ("scripts/reproduce_phase35_small_model_regression.py",
         "python scripts/reproduce_phase35_small_model_regression.py",
         "Reloads the saved Phase 35 checkpoint (phase35_1m_baseline_regression.pt) and re-evaluates validation loss on held-out text to assert exact bitwise reproduction (Val Loss: 5.6607).",
         "None.",
         "Exit 0: EXACT_MATCH confirmed (loss delta == 0.0).\nExit 1: Validation loss mismatch or corrupted weights.",
         "```powershell\npython scripts/reproduce_phase35_small_model_regression.py\n```"),

        ("scripts/train_and_audit_tokenizer_v2.py",
         "python scripts/train_and_audit_tokenizer_v2.py",
         "Trains IndianLegalTokenizerV2 from scratch on bilingual corpus, saves vocabulary and 1,811 merges to tokenizer_v2.json, and executes comparative empirical audit against Tokenizer v1.",
         "Optional: `--vocab-size INT` (default 2048), `--corpus-dir PATH`.",
         "Exit 0: Tokenizer serialized and audit JSON generated.\nExit 1: Training convergence error.",
         "```powershell\npython scripts/train_and_audit_tokenizer_v2.py\n```"),

        ("scripts/build_benchmark_v9.py",
         "python scripts/build_benchmark_v9.py",
         "Compiles and serializes the 96-case Benchmark v9 dataset across 15 legal categories into data/20_evaluation/evaluation_cases_v9.json, computing SHA-256 dataset integrity manifests.",
         "None.",
         "Exit 0: 96 cases validated and manifest_v9.json written.\nExit 1: Duplicate eval_id or schema violation.",
         "```powershell\npython scripts/build_benchmark_v9.py\n```"),

        ("scripts/audit_custom_questions.py",
         "python scripts/audit_custom_questions.py",
         "Executes Benchmark v9 test cases against the RAG pipeline, recording latency, citation recall, claim support, and triggering automated failure attribution for any failing questions.",
         "Optional: `--cases PATH`, `--output PATH`, `--offline {0|1}`.",
         "Exit 0: Evaluation report and traces exported.\nExit 1: Execution failure.",
         "```powershell\n$env:LEGALMITRA_OFFLINE_EVAL = '1'\npython scripts/audit_custom_questions.py\n```"),

        ("scripts/populate_unified_source_registry.py",
         "python scripts/populate_unified_source_registry.py",
         "Audits and compiles unified_source_registry.json, integrating 111 tracked national sources, resolving lifecycle states, and computing derived passage counts.",
         "None.",
         "Exit 0: Registry written and reconciled.\nExit 1: Unresolved source duplicate.",
         "```powershell\npython scripts/populate_unified_source_registry.py\n```"),

        ("scripts/generate_source_eligibility_ledger.py",
         "python scripts/generate_source_eligibility_ledger.py",
         "Produces source_eligibility_ledger.json, reconciling exactly why 111 sources are tracked (33 eligible, 67 backlog catalog, 10 discovery, 1 quarantined fixture).",
         "None.",
         "Exit 0: Ledger generated and reconciled.\nExit 1: Ledger discrepancy.",
         "```powershell\npython scripts/generate_source_eligibility_ledger.py\n```"),

        ("scripts/corpus_coverage_report.py",
         "python scripts/corpus_coverage_report.py",
         "Computes and prints a detailed console audit of national legal coverage across Central Acts, State Acts, and High Court judgments.",
         "None.",
         "Exit 0: Summary printed and JSON report exported.",
         "```powershell\npython scripts/corpus_coverage_report.py\n```"),

        ("scripts/national_coverage_report.py",
         "python scripts/national_coverage_report.py",
         "Generates machine-readable CSV and JSON coverage reports in data/09_national_corpus/ for all 101 mapped universe instruments.",
         "None.",
         "Exit 0: coverage_report.json and coverage_report.csv updated.",
         "```powershell\npython scripts/national_coverage_report.py\n```"),

        ("scripts/ingest_hindi_statutes.py",
         "python scripts/ingest_hindi_statutes.py",
         "Ingests authentic Hindi legal texts from official Gazette publications under Article 394A, verifying Devanagari Unicode sequences and extracting 8,617 tokens.",
         "Optional: `--source-dir PATH`.",
         "Exit 0: Hindi chunks extracted and stored in KB.",
         "```powershell\npython scripts/ingest_hindi_statutes.py\n```"),

        ("scripts/build_phase34_datasets.py",
         "python scripts/build_phase34_datasets.py",
         "Builds pretraining partitions (train: 304K, val: 3.9K, test: 34.7K) using source-grouped splitting and exports dataset_manifest_v4.json with SHA-256 trees.",
         "None.",
         "Exit 0: Manifest v4 compiled and SHA-256 locked.",
         "```powershell\npython scripts/build_phase34_datasets.py\n```"),

        ("scripts/profile_compute_feasibility.py",
         "python scripts/profile_compute_feasibility.py",
         "Profiles local CPU and GPU hardware, measuring tensor throughput, memory bandwidth, and computing scaling feasibility curves for 10M-parameter models.",
         "None.",
         "Exit 0: compute_profile_v1.json exported.",
         "```powershell\npython scripts/profile_compute_feasibility.py\n```"),

        ("scripts/review_status_summary.py",
         "python scripts/review_status_summary.py",
         "Prints high-level management dashboard showing review status of all 40 candidate records across Package A and Package B.",
         "None.",
         "Exit 0: Status breakdown printed to console.",
         "```powershell\npython scripts/review_status_summary.py\n```"),

        ("scripts/build_batch_01_bundle.py",
         "python scripts/build_batch_01_bundle.py",
         "Generates Package B review candidate bundle (20 real-world commercial examples), exports CSV review sheet, and updates tracking register.",
         "None.",
         "Exit 0: Batch 01 bundle serialized in data/07_batches/review/.",
         "```powershell\npython scripts/build_batch_01_bundle.py\n```"),

        ("scripts/import_advocate_review.py",
         "python scripts/import_advocate_review.py",
         "Validates and imports completed advocate review sheets, verifying advocate digital signature, bar enrollment number, and updating review state.",
         "`--input-csv PATH`: Path to signed review CSV.\n`--advocate-id STR`: Enrolled advocate bar registration number.",
         "Exit 0: Reviews ingested and state transitioned.\nExit 1: Validation or signature failure.",
         "```powershell\npython scripts/import_advocate_review.py --input-csv path/to/review.csv --advocate-id D/1234/2018\n```"),

        ("scripts/validate_review_submission.py",
         "python scripts/validate_review_submission.py",
         "Pre-import integrity checker verifying that review scores, comments, and decision fields conform to Pydantic review rubric.",
         "`--file PATH`: Review sheet file to validate.",
         "Exit 0: Review submission valid.\nExit 1: Form validation errors detected.",
         "```powershell\npython scripts/validate_review_submission.py --file data/07_batches/review/batch_01_review_sheet.csv\n```")
    ]

    lines = [
        "### 23.4 Comprehensive CLI Scripts & Operational Tools Reference (Primary Utilities)\n",
        "The following operational guide provides detailed execution syntax, CLI arguments, expected return codes, and PowerShell invocation examples for the primary scripts in `scripts/`:\n"
    ]

    for name, cmd, desc, args, returns, example in cli_tools:
        lines.append(f"#### Script: `{name}`")
        lines.append(f"- **Standard Invocation**: `{cmd}`")
        lines.append(f"- **Functional Responsibility**: {desc}")
        lines.append(f"- **CLI Arguments & Options**: {args}")
        lines.append(f"- **Exit Codes & Behavior**:\n{returns}")
        lines.append(f"- **Execution Example**:\n{example}")
        lines.append("")

    return "\n".join(lines)
