# BRIEFING — 2026-10-31T13:54:00Z

## Mission
Perform an exhaustive technical analysis of the development notebook `tpi-ia-2026p-21.ipynb` covering Dataset & EDA, Preprocessing/Augmentation, Baseline Model, Iterative Improvements, Error Analysis, and Notebook Outputs/Assets.

## 🔒 My Identity
- Archetype: explorer
- Roles: investigation, synthesis
- Working directory: c:\Users\perez\OneDrive\Documents\Ing.Sist-NUBE\IA\TPI IA 2026\.agents\teamwork\explorer_survey_1
- Original parent: e6000da0-6c1a-42bc-ba41-ede0dc95ba86
- Milestone: Notebook Technical Analysis

## 🔒 Key Constraints
- Read-only investigation — do NOT implement
- Strictly observe file boundaries (only write inside `.agents/teamwork/explorer_survey_1/`)
- Extract verbatim configurations, parameters, and metrics from notebook `tpi-ia-2026p-21.ipynb`

## Current Parent
- Conversation ID: e6000da0-6c1a-42bc-ba41-ede0dc95ba86
- Updated: not yet

## Investigation State
- **Explored paths**: `ORIGINAL_REQUEST.md`, `tpi-ia-2026p-21.ipynb` (all 115 cells, code, markdown, outputs, figures).
- **Key findings**:
  - Dataset: 120 dev images, 1.790 instances, 120 classes. Skewed heavily to small objects (median area ratio 0,0061, 71% small). LVIS federated annotations: 74 imgs with negative categories, 47 non-exhaustive.
  - Baseline (V1): OWLv2 Base (conf 0,15, NMS 0,30) + SAM2 Small (single mask) + SceneJSON (3x3 grid, 11-color palette, spatial relations, RLE) + PipelineTracer. Metrics: Box F1 0,6464, Mask F1 0,6132, Consistency 100%, QA Det 0,6053, QA LLM 0,4211, Kaggle V1 0,6615.
  - V2: Grid search tuning (conf 0,17, NMS 0,35) -> Kaggle V2 0,6763.
  - V3: Multiscale 2x2 overlapping tiling (zoom 1,75x) + conf 0,23 / NMS 0,30 + size-adaptive threshold (conf_large 0,15) + SAM2 single mode confirmed + 3-layer VQA with self-correcting retry, semantic normalization (OWLv2 text embeddings), and derived absence policy (`not_detected`). Metrics: Box F1 0,6722, Mask F1 0,6351, Consistency 100%, QA Det 0,7895, QA LLM 0,5526, Proxy 0,7083, Kaggle V3 0,6800.
  - Negative experiments documented: `pad_fix` (0,0000 delta), OWLv2 Large (rejected, 4,7x slower), SAM2 multimask selection (rejected).
  - Catalog of 11 figures with detailed descriptions.
- **Unexplored areas**: None regarding `tpi-ia-2026p-21.ipynb`.

## Key Decisions Made
- Extracted and dumped full raw notebook data to `extracted_notebook_data.txt` for lossless reproducibility.
- Synthesized an exhaustive 8-section technical report in `notebook_analysis.md`.
- Prepared structured 5-component handoff in `handoff.md`.

## Artifact Index
- `.agents/teamwork/explorer_survey_1/DISPATCH.md` — Inbound instructions
- `.agents/teamwork/explorer_survey_1/BRIEFING.md` — Situational awareness working memory
- `.agents/teamwork/explorer_survey_1/progress.md` — Liveness heartbeat
- `.agents/teamwork/explorer_survey_1/extracted_notebook_data.txt` — Full raw cell & output dump
- `.agents/teamwork/explorer_survey_1/notebook_analysis.md` — Comprehensive technical survey report
- `.agents/teamwork/explorer_survey_1/handoff.md` — Structured 5-component handoff report
