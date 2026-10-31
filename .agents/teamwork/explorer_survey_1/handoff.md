# Handoff Report — explorer_survey_1

**Agent:** `explorer_survey_1`  
**Mission:** Exhaustive technical analysis of the development notebook `tpi-ia-2026p-21.ipynb`.  
**Target Recipient:** Orchestrator (`e6000da0-6c1a-42bc-ba41-ede0dc95ba86`) / Subsequent reporting & authoring agents.  
**Delivered Artifacts:**
- Primary Report: `c:\Users\perez\OneDrive\Documents\Ing.Sist-NUBE\IA\TPI IA 2026\.agents\teamwork\explorer_survey_1\notebook_analysis.md`
- Raw Extracted Content: `c:\Users\perez\OneDrive\Documents\Ing.Sist-NUBE\IA\TPI IA 2026\.agents\teamwork\explorer_survey_1\extracted_notebook_data.txt`

---

## 1. Observation

### 1.1. Context and Environment
- **Workspace:** `c:\Users\perez\OneDrive\Documents\Ing.Sist-NUBE\IA\TPI IA 2026`
- **Notebook File:** `tpi-ia-2026p-21.ipynb` (115 cells: 53,288 characters of Markdown, 174,521 characters of Code, 302 KB total text dump).
- **Course & Group:** UTN Cátedra de Inteligencia Artificial (Primavera 2026), Curso 5k2, Grupo 21:
  - Ocampo, Gabriel (93368)
  - Pecchio, Valentina (94416)
  - Lopez Quinteros, Manuel (99026)
  - Chaile, Emmanuel Ricardo (89767)
  - Perez, Alvaro (97986)

### 1.2. Key Code and Output Evidence Directly Extracted
1. **Dataset & EDA (Cells 4–19):**
   - Development set: 120 images, 1.790 annotations across 120 categories (COCO/LVIS format). Mean objects per image: 14,92.
   - Scale distribution: Mean relative area = 0,0375, median = 0,0061. 71,06% of objects are `small` (<0,01 area ratio), 24,02% are `medium` (0,01–0,10), and 4,92% are `large` ($\ge 0,10$).
   - LVIS Federated Metadata: 74 of 120 images declare negative categories (118 declarations, 0,98/image); 47 declare non-exhaustive categories.
   - Benchmark VQA: 60 questions on 20 images (`questions_dev.jsonl`: 20 description, 10 count, 10 existence, 10 relation, 5 position, 5 size).
2. **Baseline Model V1 (Cells 20–80):**
   - Detector: `google/owlv2-base-patch16-ensemble` (ViT-B/16, $960 \times 960$ square input, prompt `"a photo of a {cat}"`, `CONFIDENCE_THRESHOLD = 0.15`, class-wise `NMS_THRESHOLD = 0.30`).
   - Segmenter: SAM2 `sam2_hiera_small` (`sam2_hiera_s.yaml`, checkpoint `sam2_hiera_small.pt`, single mask mode `multimask_output = False`).
   - Representation: `SceneJSON` with 3x3 centroid grid, size categories, 11-color palette, spatial relations (`left_of`, `right_of`, `above`, `below`, `overlaps`), RLE Fortran compression.
   - Auditing: `PipelineTracer` logging stages (`load_image`, `detection`, `segmentation`, `scene_json`, `validation`), JSON Schema validation via `jsonschema.Draft7Validator`, consistency check `check_scene_consistency`.
   - Baseline Metrics: Box F1 = 0,6464 (P = 0,6591, R = 0,6341, Coverage = 0,3959), Mask F1 = 0,6132 (IoU mean with correct box = 0,785), Scene Consistency = 100% (120/120 images), QA Deterministic = 0,6053, QA LLM = 0,4211, Proxy Score = 0,6745. Kaggle Test Score V1 = 0,6615.
3. **Iterative Experiments & Improvements (Cells 81–114):**
   - *Negative pad_fix (Cell 73):* Exact delta 0,0000; transformers library already handles padding post-processing.
   - *Grid search Conf/NMS (Cell 82):* Best Conf = 0,17, NMS = 0,35. Perception score: 0,4730 -> 0,4787. Kaggle Test Score V2 = 0,6763.
   - *Detector scaling H1 (Cell 92):* OWLv2 Large rejected (Box F1 0,626 vs 0,651, Mask F1 0,586 vs 0,620, 4,7x slower: 11,45 s vs 2,44 s).
   - *Multiscale Tiling H2 (Cell 92):* OWLv2 Base + 2x2 tiles with 25% overlap confirmed (Box F1: 0,651 -> 0,664, Mask F1: 0,620 -> 0,627). Optimum: `conf = 0.23`, `nms = 0.30`, `tile_delta = 0.0`. Small-object recall preserved (0,569 vs 0,575) while precision surged.
   - *Area-adaptive threshold (Cell 99):* `conf_large = 0.15` for area $\ge 0.05$ boosted Box F1 to 0,6722 and Mask F1 to 0,6351 (perception score 0,4912).
   - *SAM2 Mask Selection (Cell 95):* Single mask (0,627 Mask F1) beat best_score (0,590) and box_iou (0,608).
   - *VQA Engine & LLM Enhancements (Cells 100–104):*
     - Qwen2.5-1.5B few-shot prompt expansion resolved 20/20 descriptions (0% -> 100%).
     - Semantic normalization via OWLv2 text embeddings (cos sim $\ge 0.85$, margin 0.02) resolved keyboard, fridge, cell phone.
     - Self-correction / Retry with feedback (`interpret_with_retry`) boosted existence agreement to 90%.
     - Derived absence policy (`not_detected`) boosted deterministic QA accuracy to 0,7895 (+18,4%) and LLM QA accuracy to 0,5526 (+13,2%).
     - Proxy score reached 0,7083 (+0,0338). Final Kaggle Test Score V3 = 0,6800.
4. **Computational Latency (Cell 111):**
   - Stage times: Load image = 0,01 s, Validation = 0,09 s, SceneJSON = 0,28 s, Segmentation = 0,43 s, Detection = 2,44 s (75% of total time due to 5 OWLv2 passes).
   - End-to-end average latency: 1,25 s/image (Baseline) -> 3,25 s/image (V3).

---

## 2. Logic Chain

1. **Premise 1 (EDA):** The dataset is severely skewed towards small objects (median relative area 0,0061, 71% small). Setting high confidence thresholds prematurely causes catastrophic false negatives in baseline OWLv2 (recall in small is only 0,575 vs 0,852 in large).
2. **Premise 2 (Evaluation Policy):** Because LVIS uses federated annotations with explicit negative categories and unverified categories, naive COCO metrics would heavily penalize valid open-vocabulary predictions. An exact federated LVIS matcher (`lvis_match`) is required to avoid misleading optimization.
3. **Premise 3 (Perception Bottleneck):** Hyperparameter tuning alone (Section 8) reached an asymptotic ceiling (+0,0057 perception score) because standard OWLv2 at 960x960 cannot resolve sub-patch features. Scaling model capacity to OWLv2 Large failed because parameters increased without resolving spatial detail and inference slowed 4,7x.
4. **Premise 4 (Multiscale Resolution):** Tiling the image into 2x2 crops with 25% overlap provided an effective $1.75\times$ zoom. This allowed raising the confidence threshold from 0,15 to 0,23 to eliminate 162 false positives while preserving small object recall (0,569 vs 0,575).
5. **Premise 5 (VQA Decoupling):** LLMs are prone to hallucination when asked to perform numerical counts or spatial reasoning directly. Decoupling the VQA pipeline into (1) LLM/Regex Query Interpreter, (2) Deterministic Graph Engine, and (3) Verbalizer with an algorithmic fidelity check eliminated hallucinations and boosted deterministic accuracy to 78,95%.

---

## 3. Caveats

1. **Parameter Tuning Set:** All hyperparameter sweeps (confidence, NMS, multiscale, absence policy) were selected on the 120 development images; generalization is validated primarily by the blind test score on Kaggle (V1: 0,6615 -> V2: 0,6763 -> V3: 0,6800).
2. **Derived Absence vs Ground Truth:** The `not_detected` policy marks absence with confidence 0,5 and an explicit note. In open-vocabulary vision, non-detection is not verified visual absence.
3. **LLM Spatial Relation Limitation:** Qwen2.5-1.5B struggled with directional orientation in Spanish relations (only 30% interpretation agreement on relations), requiring regex fallback for robust deterministic evaluation.
4. **Spanish Vocabulary Hallucination in Free-Text Descriptions:** The fidelity filter tests English vocabulary names in `« »`; when Qwen writes in natural Spanish, secondary descriptive elements (e.g. "baño principal") occasionally bypass the English filter.

---

## 4. Conclusion

The technical development in `tpi-ia-2026p-21.ipynb` represents a rigorously designed, reproducible, and verifiable visual scene understanding system:
- **Baseline established:** OWLv2 Base + SAM2 Small + SceneJSON achieves Box F1 0,6464, Mask F1 0,6132, QA 0,6053, Kaggle 0,6615.
- **Negative hypotheses documented:** `pad_fix` (0,0000 delta), OWLv2 Large (worse F1 and 4,7x latency), and SAM2 multimask selection (degraded small object mask IoU) were rigorously tested and rejected.
- **Winning improvements proven:**
  1. Multiscale 2x2 overlapping tiling + confidence threshold 0,23.
  2. Size-adaptive thresholding (`conf_large = 0.15`).
  3. 3-layer decoupled VQA architecture with self-correcting retry loop and derived absence policy.
- **Final performance:** Box F1 0,6722 (+0,0258), Mask F1 0,6351 (+0,0219), QA Deterministic 0,7895 (+0,1842), Kaggle Test Score 0,6800 (+0,0185).

---

## 5. Verification Method

To independently verify all findings and figures:
1. **Inspect Raw Extracted Data:**
   - File: `.agents/teamwork/explorer_survey_1/extracted_notebook_data.txt`
   - Check Cell 6 (EDA counts), Cell 12 (Relative areas), Cell 66 (Baseline Box metrics), Cell 69 (Baseline Mask metrics), Cell 71 (Baseline QA metrics), Cell 92 (Multiscale comparison table), Cell 99 (Final V3 metrics), Cell 110 (Final comparison table), Cell 111 (Latency breakdown).
2. **Inspect Comprehensive Technical Analysis:**
   - File: `.agents/teamwork/explorer_survey_1/notebook_analysis.md`
   - Cross-reference all 11 cataloged figures and their corresponding notebook cell output plots.
3. **Independent Python Inspection Command:**
   ```powershell
   python -c "import json; nb=json.load(open('tpi-ia-2026p-21.ipynb', encoding='utf-8')); print('Total cells:', len(nb['cells']))"
   ```
4. **Invalidation Conditions:**
   - If any reported metric (e.g. Box F1 0,6464, V3 Box F1 0,6722, Kaggle V1 0,6615, V3 0,6800) does not match the cell execution stream text in `tpi-ia-2026p-21.ipynb`.
