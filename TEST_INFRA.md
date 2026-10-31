# Testing Infrastructure & E2E Deliverables Verification Suite
**Project:** TPI Primavera 2026 — Comprensión Visual de Escenas  
**Course:** Cátedra de Inteligencia Artificial — Universidad Tecnológica Nacional (UTN FRC)  
**Group:** 21 (Curso 5k2 / 5K3A)  
**Artifact:** `TEST_INFRA.md`  
**Automated Harness:** `test_e2e_deliverables.py`  

---

## 1. Executive Summary & Philosophy

The verification framework for the Visual Scene Understanding deliverables implements an **opaque-box, multi-tier audit pipeline**. Unlike unit tests that verify internal algorithmic details, this harness verifies deliverables against formal academic specifications, visual publishing constraints, notebook ground-truth execution logs, and theoretical foundations.

### Core Principles
1. **Opaque-Box Auditing**: Deliverables are audited strictly via external contracts (file existence, section topology, PDF geometry, text extraction, metric accuracy, and cross-document metadata consistency) without assuming internal implementation details.
2. **Progressive Testability**: Tests fail cleanly with actionable, diagnostic assertion messages when deliverables are missing or partially complete, guiding parallel workers (`worker_m1`, `worker_m2`, `worker_m3`) through milestone completion.
3. **Zero Facade Testing**: No mock or always-passing tests. Every assertion verifies real observable logic against authoritative data oracles.
4. **Binary Gatekeeper**: The test suite exits with return code `0` if and only if 100% of all checks pass across all 4 tiers.

---

## 2. The 4-Tier Verification Hierarchy

```
+-------------------------------------------------------------------------+
|                  TIER 4: REAL-WORLD ACCEPTANCE                          |
|  - Cross-module author/group synchronization (Grupo 21, 5 students)     |
|  - Institutional consistency (UTN FRC, Cátedra IA, Course metadata)     |
|  - End-to-end acceptance certification & audit readiness                |
+-------------------------------------------------------------------------+
                                    ^
+-------------------------------------------------------------------------+
|             TIER 3: CROSS-FEATURE & QUANTITATIVE INTEGRITY              |
|  - Baseline metrics matching (Box F1 0.6464, Mask 0.6132, QA 0.6053)     |
|  - Improved V3 metrics matching (Box F1 0.6722, Mask 0.6351, QA 0.7895) |
|  - Refuted hypotheses (pad_fix 0.0000, OWLv2 Large, SAM2 multimask)    |
|  - Deep Learning theoretical grounding (convolución, receptive field)   |
|  - Non-technical document anti-jargon enforcement (no LaTeX math)       |
+-------------------------------------------------------------------------+
                                    ^
+-------------------------------------------------------------------------+
|                 TIER 2: BOUNDARY & QUALITY CONSTRAINTS                  |
|  - PDF page count verification (>= 15 pages)                             |
|  - PDF geometry & mediabox compliance (A4: 595.28 x 841.89 pt ± 5pt)     |
|  - Font encoding & character integrity (no \ufffd, valid Spanish diacritics)|
|  - Asset integrity & broken link auditing (local figures & logo exist)   |
|  - Clean build script execution (`python build_pdf.py` exits code 0)    |
+-------------------------------------------------------------------------+
                                    ^
+-------------------------------------------------------------------------+
|                      TIER 1: FEATURE COVERAGE                           |
|  - Presence of all 3 primary deliverables (Report, Non-Tech, Oral Guide)|
|  - 6 mandatory academic sections in informe_tecnico_tpi.md              |
|  - 5 conceptual stages in documento_explicativo_no_tecnico.md           |
|  - 10-minute presentation structure & Q&A bank in oral defense guide    |
+-------------------------------------------------------------------------+
```

---

## 3. Test Suite Inventory

The automated test harness is located at `test_e2e_deliverables.py` and contains 16 granular test cases across 4 test classes:

| # | Test Method | Target Class | Scope & Objective | Authoritative Oracle |
|---|---|---|---|---|
| **T1.1** | `test_t1_1_primary_deliverables_exist` | `TestTier1DeliverablesCoverage` | Verifies presence and non-zero size of 6 primary files: `informe_tecnico_tpi.pdf`, `.html`, `.md`, `build_pdf.py`, `documento_explicativo_no_tecnico.md`, `guia_defensa_oral_tpi.md`. | `PROJECT.md` Code Layout |
| **T1.2** | `test_t1_2_technical_report_six_mandatory_sections` | `TestTier1DeliverablesCoverage` | Verifies existence of the 6 mandatory academic sections in `informe_tecnico_tpi.md`: 1. Portada, 2. EDA, 3. Metodología, 4. Resultados, 5. Discusión, 6. Conclusiones. | `ORIGINAL_REQUEST.md` R1 |
| **T1.3** | `test_t1_3_non_technical_document_pipeline_stages` | `TestTier1DeliverablesCoverage` | Verifies `documento_explicativo_no_tecnico.md` covers all 5 pipeline stages: Percepción, Segmentación, Representación, Razonamiento, Interacción. | Guidelines Section 2.1 |
| **T1.4** | `test_t1_4_oral_defense_guide_structure` | `TestTier1DeliverablesCoverage` | Verifies `guia_defensa_oral_tpi.md` details the 10-minute presentation breakdown and comprehensive Q&A bank. | Guidelines Section 2.5 |
| **T2.1** | `test_t2_1_pdf_page_count_minimum` | `TestTier2BoundaryQuality` | Uses `pypdf` to assert `len(reader.pages) >= 15`. | Template survey (`TPI_IA_2025-TEMPLATE.pdf` has 22 pages) |
| **T2.2** | `test_t2_2_pdf_dimensions_a4` | `TestTier2BoundaryQuality` | Audits mediabox across all pages against A4 format (`595.28 x 841.89 pt` with `± 6 pt` tolerance). | ISO 216 / Chromium Print-to-PDF |
| **T2.3** | `test_t2_3_pdf_text_extraction_and_encoding` | `TestTier2BoundaryQuality` | Extracts text; asserts length > 5,000 chars, 0 replacement characters (`\ufffd`), and valid Spanish diacritics. | Font encoding standards |
| **T2.4** | `test_t2_4_image_assets_and_figure_integrity` | `TestTier2BoundaryQuality` | Scans all image links in Markdown/HTML and asserts referenced local files exist on disk with size > 0. | Markdown / HTML specifications |
| **T2.5** | `test_t2_5_build_pdf_execution` | `TestTier2BoundaryQuality` | Executes `python build_pdf.py` as a subprocess; asserts return code is `0` and output PDF is generated. | Toolchain survey |
| **T3.1** | `test_t3_1_ground_truth_baseline_metrics` | `TestTier3QuantitativeIntegrity` | Asserts exact presence of Baseline metrics in report: Box F1 `0.6464`, Mask F1 `0.6132`, QA `0.6053`, Kaggle `0.6615`. | `tpi-ia-2026p-21.ipynb` Cells 66-70 |
| **T3.2** | `test_t3_2_ground_truth_v3_improved_metrics` | `TestTier3QuantitativeIntegrity` | Asserts presence of V3 metrics in report: Box F1 `0.6722`, Mask F1 `0.6351`, QA `0.7895`, Kaggle `0.6800`. | `tpi-ia-2026p-21.ipynb` Cells 81-111 |
| **T3.3** | `test_t3_3_negative_hypotheses_documented` | `TestTier3QuantitativeIntegrity` | Asserts documentation of refuted hypotheses: `pad_fix` (delta=0), `OWLv2 Large` (rejected), `SAM2 multimask` (rejected). | `tpi-ia-2026p-21.ipynb` Sec. 8, 10, 11 |
| **T3.4** | `test_t3_4_theoretical_terms_grounding` | `TestTier3QuantitativeIntegrity` | Asserts report articulates deep learning theory: convolución, receptive field, transfer learning, harmonic mean, desbalance. | `IA-Resumen-Completo.pdf` |
| **T3.5** | `test_t3_5_non_technical_clarity_and_jargon_free` | `TestTier3QuantitativeIntegrity` | Asserts `documento_explicativo_no_tecnico.md` contains >= 1200 words and zero heavy mathematical formulas (`\mathcal{L}`, `\sum`, `\int`). | `ORIGINAL_REQUEST.md` R2 |
| **T4.1** | `test_t4_1_deliverable_metadata_consistency` | `TestTier4RealWorldAcceptance` | Cross-audits that "Grupo 21", "Inteligencia Artificial", and "UTN" appear consistently across all 3 text deliverables. | Course administration |
| **T4.2** | `test_t4_2_student_authors_and_professors_referenced` | `TestTier4RealWorldAcceptance` | Cross-audits that all 5 student authors (Ocampo, Pecchio, Lopez Quinteros, Chaile, Perez) are acknowledged. | Notebook Cell 1 metadata |

---

## 4. How to Execute the Test Suite

### Option 1: Standalone CLI Runner (Recommended)
Executes all 4 tiers and prints formatted visual diagnostics and a pass/fail summary:
```powershell
python test_e2e_deliverables.py
```
**Exit Code Semantics**:
- `0`: All 16 tests passed. All deliverables satisfy 100% of acceptance criteria.
- `1`: One or more tests failed. Diagnostics will display exact missing sections, broken links, or mismatched metrics.

### Option 2: Standard Python Unittest Runner
```powershell
python -m unittest test_e2e_deliverables.py -v
```

---

## 5. Triage and Diagnostic Guide for Milestone Workers

When developing or updating deliverables, consult this triage table to resolve test failures:

### Failure in Tier 1 (`TestTier1DeliverablesCoverage`)
- **`test_t1_1_primary_deliverables_exist`**: One or more required files do not exist at the workspace root. Ensure `informe_tecnico_tpi.pdf`, `informe_tecnico_tpi.html`, `informe_tecnico_tpi.md`, `build_pdf.py`, `documento_explicativo_no_tecnico.md`, and `guia_defensa_oral_tpi.md` are placed directly in the workspace root.
- **`test_t1_2_technical_report_six_mandatory_sections`**: Markdown headings in `informe_tecnico_tpi.md` do not match the required section naming. Use clear headers like `# 1. Portada`, `# 2. Análisis del dataset (EDA)`, `# 3. Metodología`, `# 4. Resultados`, `# 5. Discusión y análisis de errores`, `# 6. Conclusiones y trabajo futuro`.
- **`test_t1_3_non_technical_document_pipeline_stages`**: Ensure `documento_explicativo_no_tecnico.md` explicitly addresses all 5 stages: Percepción, Segmentación, Representación, Razonamiento, and Interacción.
- **`test_t1_4_oral_defense_guide_structure`**: Ensure `guia_defensa_oral_tpi.md` includes the 10-minute presentation strategy and the questions/answers bank.

### Failure in Tier 2 (`TestTier2BoundaryQuality`)
- **`test_t2_1_pdf_page_count_minimum`**: The compiled PDF has fewer than 15 pages. Add full technical details, diagrams, tables, and discussions from the notebook analysis.
- **`test_t2_2_pdf_dimensions_a4`**: In `build_pdf.py` or CSS `@page`, ensure page dimensions are set to A4 (`size: A4;` or `210mm x 297mm`). Avoid custom page sizes.
- **`test_t2_3_pdf_text_extraction_and_encoding`**: PDF must contain selectable text (not an image-only scan) and valid UTF-8 encoding without broken character codes (`\ufffd`).
- **`test_t2_4_image_assets_and_figure_integrity`**: Markdown or HTML refers to an image path that does not exist. Verify relative image paths or embed assets.
- **`test_t2_5_build_pdf_execution`**: `python build_pdf.py` failed or crashed. Run `python build_pdf.py` manually in PowerShell and check stderr output.

### Failure in Tier 3 (`TestTier3QuantitativeIntegrity`)
- **`test_t3_1_ground_truth_baseline_metrics`**: Make sure the report explicitly contains: Box F1 `0.6464`, Mask F1 `0.6132`, QA `0.6053`, and Kaggle `0.6615`.
- **`test_t3_2_ground_truth_v3_improved_metrics`**: Make sure the report explicitly contains: Box F1 `0.6722`, Mask F1 `0.6351`, QA `0.7895`, and Kaggle `0.6800`.
- **`test_t3_3_negative_hypotheses_documented`**: Ensure Section 3/4 documents why `pad_fix` yielded delta `0.0000`, why `OWLv2 Large` was rejected, and why `SAM2 multimask` was discarded in favor of single-mask mode.
- **`test_t3_4_theoretical_terms_grounding`**: Ground each pipeline stage in deep learning concepts: `convolución`, `campo receptivo`, `transfer learning`, `media armónica`, and `desbalance de clases`.
- **`test_t3_5_non_technical_clarity_and_jargon_free`**: Remove LaTeX equations (`\mathcal{L}`, `\sum`, etc.) from `documento_explicativo_no_tecnico.md`. Use plain intuitive descriptions instead.

### Failure in Tier 4 (`TestTier4RealWorldAcceptance`)
- **`test_t4_1_deliverable_metadata_consistency`**: Ensure all documents mention "Grupo 21", "Inteligencia Artificial", and "UTN".
- **`test_t4_2_student_authors_and_professors_referenced`**: Ensure the 5 group members (Ocampo, Pecchio, Lopez Quinteros, Chaile, Perez) are listed in the authors section.
