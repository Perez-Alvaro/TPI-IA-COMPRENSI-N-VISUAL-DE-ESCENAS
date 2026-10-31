# Project: TPI Comprensión Visual de Escenas (Primavera 2026 - Grupo 21)

## Architecture
The system delivers three coordinated publication-grade artifacts documenting the neuro-symbolic visual scene understanding pipeline developed in `tpi-ia-2026p-21.ipynb`:
1. **Technical Report (`informe_tecnico_tpi.pdf`, `.html`, `.md`)**: Structured academic report strictly following the 6 sections and visual geometry of `TPI_IA_2025-TEMPLATE.pdf`, with deep theoretical justification from `IA-Resumen-Completo.pdf`.
2. **Non-Technical Explanation (`documento_explicativo_no_tecnico.md`)**: Accessible, conceptual, intuitive narrative explaining the entire visual pipeline, decisions, and business value without advanced mathematical jargon.
3. **Oral Defense Preparation Guide (`guia_defensa_oral_tpi.md`)**: Comprehensive Q&A bank anticipating technical, algorithmic, and theoretical defense questions with rigorous mathematical and empirical answers.
4. **E2E Verification & Auditing Suite (`TEST_INFRA.md`, `test_e2e_deliverables.py`)**: Opaque-box test suite validating structure, content completeness, formatting compliance, and technical accuracy.

## Feature Inventory
| # | Feature | Description | Milestone | Source |
|---|---------|-------------|-----------|--------|
| F1 | Cover Page & Institutional Branding | UTN FRC logo, Cátedra IA, Grupo 21, teachers, students, delivery date | M1 | Template & Guidelines |
| F2 | Dataset Analysis & EDA Documentation | 120 dev images, 1.790 annotations, small object skew (71%), LVIS federated annotations, VQA distribution | M1 | Notebook Cells 4–19 |
| F3 | Pipeline Architecture & Methodology | 5-stage pipeline: Perception (OWLv2), Segmentation (SAM2), Representation (SceneJSON 3x3), Reasoning (Decoupled VQA), Auditing (PipelineTracer) | M1 | Notebook Cells 20–80 |
| F4 | Theoretical Deep Learning Justification | "Why we did each step and why it works" grounded in IA-Resumen-Completo (convolutions, pooling, transfer learning, activations, loss, optimizers, F1 harmonic mean) | M1 | IA-Resumen-Completo & Guidelines |
| F5 | Iterative Improvements & Hypotheses | Detailed analysis of V1 -> V2 -> V3 (grid search conf/nms, multiscale tiling 2x2 with 25% overlap, size-adaptive thresholding, VQA prompt expansion, semantic normalization, retry loop, absence policy, and refuting pad_fix, OWLv2 Large, SAM2 multimask) | M1 | Notebook Cells 81–114 |
| F6 | Quantitative Results & Comparison Tables | Baseline vs V2 vs V3 metrics (Box F1 0.6464 -> 0.6722, Mask F1 0.6132 -> 0.6351, QA 0.6053 -> 0.7895, Kaggle 0.6615 -> 0.6763 -> 0.6800, latency breakdown) | M1 | Notebook Cells 66–111 |
| F7 | Error Analysis & Edge Cases | Specific analysis of false positives/negatives, confusing classes (traffic light vs streetlight, textured surfaces, statues), small object limits, spatial relation challenges | M1 | Notebook Cells 105–109 |
| F8 | Conclusions & Future Work | Synthesis of engineering lessons, neuro-symbolic advantages, computational bottlenecks, future research paths | M1 | Notebook Cells 112–115 |
| F9 | Template Visual & Typographic Layout | Exact reproduction of TPI_IA_2025-TEMPLATE.pdf: A4, 1 col, 25.4 mm (72 pt) margins, Arial (26/20/13/11 pt), Courier New (11 pt), right page number starting p.2 | M1 | Template PDF Inspection |
| F10 | PDF Compilation & Structured Source | Automated generation via Edge Headless with --no-pdf-header-footer to produce pristine publication-quality PDF | M1 | Toolchain Survey |
| F11 | Non-Technical Explanatory Document | Self-contained, accessible, conceptual markdown document explaining the pipeline in plain language | M2 | Original Request R2 |
| F12 | Oral Defense Q&A Preparation Guide | Exhaustive guide with 10-minute presentation strategy and Q&A covering technical trade-offs, hyperparameters, and theory | M3 | Original Request R3 |
| F13 | E2E Verification & Test Infrastructure | Verification harness asserting section presence, layout geometry, theoretical coverage, and metric accuracy | E2E Track | Original Request Acceptance Criteria |

## Milestones
| # | Name | Scope | Dependencies | Status |
|---|------|-------|-------------|--------|
| E2E | E2E Testing Track | Design and establish opaque-box test suite (`TEST_INFRA.md`, `test_e2e_deliverables.py`) and publish `TEST_READY.md` | none | DONE |
| M1 | Technical Report Generation & Typesetting | Complete 6-section academic report: canonical Markdown (`informe_tecnico_tpi.md`), structured HTML/CSS source (`informe_tecnico_tpi.html`), compilation script (`build_pdf.py`), and publication PDF (`informe_tecnico_tpi.pdf`) | none | DONE |
| M2 | Non-Technical Conceptual Markdown | Comprehensive non-technical explanatory guide (`documento_explicativo_no_tecnico.md`) | none | DONE |
| M3 | Oral Defense Preparation Guide | Rigorous defense preparation Q&A document (`guia_defensa_oral_tpi.md`) | none | DONE |
| M4 | Final Integration, E2E Pass & Audit | Execute full E2E verification test suite (100% pass) and independent Forensic Audit (`teamwork_auditor`) | M1, M2, M3, E2E | DONE |

## Interface Contracts
### M1 Technical Report ↔ E2E Verification
- Primary artifact: `informe_tecnico_tpi.pdf` (valid PDF, 20 pages >=15 minimum, A4 format 595.0x841.9 pt, no edge header/footer artifacts, cover page with logo).
- Canonical Markdown: `informe_tecnico_tpi.md` (contains all 6 mandatory sections).
- Structured source: `informe_tecnico_tpi.html` and compilation script `build_pdf.py` (verified exit code 0).

### M2 Non-Technical Guide ↔ E2E Verification
- File: `documento_explicativo_no_tecnico.md` (591 lines, 50.6 KB).
- Content: Explains the entire pipeline conceptually, no heavy mathematical jargon, covers all 5 stages, decisions, and results.

### M3 Defense Guide ↔ E2E Verification
- File: `guia_defensa_oral_tpi.md` (537 lines, 67.9 KB).
- Content: Comprehensive Q&A bank (25 technical questions across 7 blocks), 10-minute oral defense structure, technical justifications, mathematical proofs of F1 and LVIS policies, trade-off explanations.

## Code Layout
- `.agents/teamwork/`: Metadata, coordination plans, and agent progress (never source code).
- Workspace Root:
  - `informe_tecnico_tpi.pdf`: Final publication-quality technical report (20 pages, 1.8 MB).
  - `informe_tecnico_tpi.html`: Structured HTML/CSS typesetting source.
  - `informe_tecnico_tpi.md`: Canonical Markdown technical report.
  - `build_pdf.py`: Automated build script compiling HTML to PDF via Edge Headless.
  - `documento_explicativo_no_tecnico.md`: Non-technical conceptual explanation.
  - `guia_defensa_oral_tpi.md`: Oral defense Q&A preparation guide.
  - `test_e2e_deliverables.py`: Independent E2E test verification harness (16 test cases).
  - `TEST_INFRA.md`: E2E test suite documentation.
  - `TEST_READY.md`: Signal indicating E2E test harness readiness.
  - `report_assets/`: 11 high-resolution charts and institutional logo.
