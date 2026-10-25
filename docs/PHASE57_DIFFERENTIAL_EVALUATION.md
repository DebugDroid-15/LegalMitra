# Phase 57 Differential Evaluation Engine

**Component:** `legalmitra.evaluation.differential_evaluator`  
**Classification:** PROPRIETARY AND CONFIDENTIAL  

---

## 1. Differential Analysis Between PIT-V12 and PIT-V13

The `DifferentialEvaluator` tracks performance deltas across benchmark iterations:
- **Baseline Run**: PIT-V12 (212 test cases)
- **Candidate Run**: PIT-V13 (240 test cases)

### Key Metrics Tracked
1. **Both Passed Count**: Cases passing in both baseline and candidate.
2. **Improvements Count**: Cases failing in baseline that pass in candidate.
3. **Regressions Count**: Cases passing in baseline that fail in candidate.
4. **Critical Safety Regressions**: Regressions involving quarantined scaffolds, fabricated citations, or overruled precedents.
5. **State Transition Matrix**: Mapping disposition shifts across model runs.
