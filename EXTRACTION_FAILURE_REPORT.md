# LegalMitra Extraction & Failure Diagnostic Report
**Generated at**: 2026-10-15 17:16:29 UTC

## Summary Metrics
- **Total Documents Processed**: 6
- **Successful Extractions**: 5
- **Failed / Unsupported Extractions**: 1
- **Success Rate**: 83.3%

## Extraction Failures and Unsupported Cases
| Document ID | Format | Failure Category | Suggested Remediation |
|---|---|---|---|
| `IND-UNSUPPORTED-001` | `.xyz` | **UNSUPPORTED_FORMAT** | Convert file from '.xyz' to standard PDF, DOCX, HTML, or TXT before ingestion. |

### Detailed Failure Logs

#### Case 1: IND-UNSUPPORTED-001
- **File Path**: `C:\PROJECTS\LegalMitra\data\01_raw\IND-UNSUPPORTED-001.xyz`
- **Failure Mode**: `UNSUPPORTED_FORMAT`
- **Error Diagnostic**: ```
No extractor registered for file extension: '.xyz'
```
- **Actionable Remediation**: Convert file from '.xyz' to standard PDF, DOCX, HTML, or TXT before ingestion.
