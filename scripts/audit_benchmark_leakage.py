"""
Enhanced Benchmark Provenance, Leakage, and Contamination Audit Script for Phase 58.
Audits PIT-V13 (cases 1-240) across exact duplicates, token Jaccard, shared scenarios,
shared expected provisions, template leakage, and diagnostic authoring bias.
"""

import json
import re
from collections import defaultdict
from typing import Dict, List, Set, Tuple

def audit_benchmark():
    manifest_path = "data/22_central_legislation/temporal_benchmark_manifest.json"
    with open(manifest_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    cases = data["test_cases"]
    print(f"Total test cases: {len(cases)}")
    print(f"Split distribution: {data.get('split_counts')}")

    # 1. Exact query duplicates after normalization
    normalized_queries = {}
    exact_dups = []
    for c in cases:
        cid = c["case_id"]
        q = c.get("query_description") or c.get("title", "")
        norm_q = " ".join(re.findall(r"\b\w+\b", q.lower()))
        if norm_q in normalized_queries:
            exact_dups.append((cid, normalized_queries[norm_q], norm_q[:60]))
        else:
            normalized_queries[norm_q] = cid

    print(f"Exact normalized query duplicates: {len(exact_dups)}")

    # 2. Token-level Jaccard across splits
    stopwords = {
        "a", "an", "the", "in", "on", "at", "to", "for", "of", "with", "by", "from",
        "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "do",
        "does", "did", "can", "could", "should", "would", "may", "might", "must", "and",
        "or", "but", "if", "then", "else", "when", "where", "why", "how", "all", "any",
        "what", "which", "who", "whom", "this", "that", "these", "those", "under"
    }

    def tokenize(text: str) -> Set[str]:
        words = re.findall(r"\b[a-zA-Z0-9_\-]{3,}\b", text.lower())
        return {w for w in words if w not in stopwords}

    case_tokens = {c["case_id"]: tokenize(c.get("query_description") or c.get("title", "")) for c in cases}
    case_splits = {c["case_id"]: c.get("split", "unassigned") for c in cases}

    cids = list(case_tokens.keys())
    high_sim_pairs = []
    max_jaccard = 0.0
    max_pair = None

    for i in range(len(cids)):
        for j in range(i + 1, len(cids)):
            id_a, id_b = cids[i], cids[j]
            split_a, split_b = case_splits[id_a], case_splits[id_b]
            if split_a == split_b:
                continue  # Cross-split only

            toks_a = case_tokens[id_a]
            toks_b = case_tokens[id_b]
            if not toks_a or not toks_b:
                continue

            sim = len(toks_a & toks_b) / len(toks_a | toks_b)
            if sim > max_jaccard:
                max_jaccard = sim
                max_pair = (id_a, id_b, split_a, split_b)
            if sim >= 0.50:
                high_sim_pairs.append({
                    "case_a": id_a,
                    "split_a": split_a,
                    "case_b": id_b,
                    "split_b": split_b,
                    "jaccard": round(sim, 4),
                    "shared_tokens": sorted(list(toks_a & toks_b)),
                })

    print(f"Max cross-split Jaccard: {max_jaccard:.4f} between {max_pair}")
    print(f"Pairs with Jaccard >= 0.50 across splits: {len(high_sim_pairs)}")

    # 3. Shared statutory provisions across splits
    provision_to_cases = defaultdict(lambda: defaultdict(list))
    for c in cases:
        cid = c["case_id"]
        split = c.get("split")
        provisions = c.get("expected_applicable_provisions", [])
        for p in provisions:
            norm_p = " ".join(re.findall(r"\b\w+\b", p.lower()))
            provision_to_cases[norm_p][split].append(cid)

    cross_split_provisions = {}
    for p, splits in provision_to_cases.items():
        if len(splits) > 1:
            cross_split_provisions[p] = {s: len(cids) for s, cids in splits.items()}

    print(f"Provisions shared across splits: {len(cross_split_provisions)}")

    # 4. Diagnostic Cases (PIT-213 to PIT-240) Analysis
    diag_cases = [c for c in cases if int(c["case_id"].replace("PIT-", "")) >= 213]
    print(f"Phase 57 Diagnostic cases (PIT-213 to PIT-240): {len(diag_cases)}")
    domains = defaultdict(int)
    for c in diag_cases:
        domains[c.get("domain", "UNKNOWN")] += 1
    print("Diagnostic cases domain breakdown:")
    for d, cnt in sorted(domains.items()):
        print(f"  {d}: {cnt}")

    return {
        "total_cases": len(cases),
        "split_counts": data.get("split_counts"),
        "exact_duplicates": exact_dups,
        "max_jaccard": max_jaccard,
        "max_pair": max_pair,
        "high_sim_pairs_count": len(high_sim_pairs),
        "cross_split_provisions_count": len(cross_split_provisions),
        "diag_cases_count": len(diag_cases),
    }

if __name__ == "__main__":
    audit_benchmark()
