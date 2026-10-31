# Empirical Challenge & Quantitative Verification Report

**Author**: EMPIRICAL CHALLENGER (Role: critic, specialist)  
**Workspace**: `c:\Users\perez\OneDrive\Documents\Ing.Sist-NUBE\IA\TPI IA 2026`  
**Working Directory**: `.agents/teamwork/challenger_1`  
**Verdict**: `APPROVE`

---

## 1. Observation

Direct empirical observations obtained from executing verification harnesses and inspecting the execution stream of `tpi-ia-2026p-21.ipynb` against the three primary deliverables (`informe_tecnico_tpi.md`, `documento_explicativo_no_tecnico.md`, `guia_defensa_oral_tpi.md`):

### 1.1. Execution Stream Ground Truth in `tpi-ia-2026p-21.ipynb`
- **Cell 110 Output (Final Dev Comparison Baseline vs. V3)**:
  ```text
                 baseline (S7)      V3   delta
  box_f1                0.6464  0.6722  0.0258
  box_precision         0.6591  0.7159  0.0568
  box_recall            0.6341  0.6335 -0.0006
  coverage              0.3959  0.4249  0.0290
  mask_f1               0.6132  0.6351  0.0219
  consistency           1.0000  1.0000  0.0000
  qa_acc_det            0.6053  0.7895  0.1842
  qa_acc_llm            0.4211  0.5526  0.1315
  proxy_score           0.6745  0.7083  0.0338
  ```
- **Cell 111 Source & Execution (Latency Breakdown)**:
  ```python
  etapas = ['Carga de Imagen', 'Validación', 'SceneJSON', 'Segmentación', 'Detección']
  tiempos_v3 = [0.01, 0.09, 0.28, 0.43, 2.44] # Medias obtenidas en las ejecuciones
  ```
  Sum total latency: $0.01 + 0.09 + 0.28 + 0.43 + 2.44 = 3.25\text{ s}$.
- **Cell 83 Source & Markdown Output (Kaggle Leaderboard Progression)**:
  ```markdown
  | Versión | Configuración | Score en Kaggle |
  |---|---|---|
  | V1 | Línea base: OWLv2 base, conf 0,15, NMS 0,30 | 0,6615 |
  | V2 | Umbrales de la sección 8: conf 0,17, NMS 0,35 | 0,6763 |
  | V3 (final) | Mosaicos + conf 0,23 / NMS 0,30 + mejoras de QA (secciones 10–12) | 0,6800 |
  ```
- **Cell 6 & Cell 66 Outputs (Dataset & Object Scale Distribution)**:
  - Cell 6: Total imágenes dev = 120, Total categorías = 120, Total instancias anotadas = 1790.
  - Cell 66: Recall por tamaño del objeto:
    - `small`: 1272 instancias (Recall: 0.575) $\rightarrow \frac{1272}{1790} = 71.061\% \approx 71.06\%$.
    - `medium`: 430 instancias (Recall: 0.765) $\rightarrow \frac{430}{1790} = 24.022\% \approx 24.02\%$.
    - `large`: 88 instancias (Recall: 0.852) $\rightarrow \frac{88}{1790} = 4.916\% \approx 4.92\%$.
- **Negative Hypotheses Ground Truth in Notebook**:
  - `pad_fix`: Cell 74 note states `"Esta celda de arriba fue comentada porque dio diferencia 0"`. Cell 77 states: `"reescalar las cajas al lado mayor de la imagen dio métricas idénticas a la línea base, porque la versión de transformers usada ya compensa el relleno de OWLv2 en el post-procesamiento"`.
  - `OWLv2 Large`: Cell 89 states: `"DETECTORS = {'base': detector} # OWLv2 large descartado: score 0,4650 vs 0,4852 y 4,7x más lento"`. Cell 92 confirms Large had Box F1 0.626 vs 0.651 Base, Mask F1 0.586 vs 0.620 Base, and 11.45 s/img vs 2.44 s/img (4.7x slower).
  - `SAM2 Multimask`: Cell 95 documents `single` (Mask F1 0.627, IoU 0.789) vs `best_score` (0.590) vs `box_iou` (0.608). Verdict: `"Hipótesis rechazada. Elegir entre las 3 máscaras de SAM2 empeoró el resultado..."`.

### 1.2. Deliverable Citations Observed
- `informe_tecnico_tpi.md`:
  - Lines 53, 358: Baseline Box F1 = 0.6464, V3 Box F1 = 0.6722 (Delta: +0.0258).
  - Lines 53, 362: Baseline Mask F1 = 0.6132, V3 Mask F1 = 0.6351 (Delta: +0.0219).
  - Lines 53, 365, 393: Baseline QA Det = 0.6053, V3 QA Det = 0.7895 (Delta: +0.1842, +30.4%).
  - Lines 53, 368: Kaggle Blind Test Scores: V1 = 0.6615, V2 = 0.6763, V3 = 0.6800.
  - Lines 64, 100: 120 dev images, 1.790 annotations, 71.06% small (1.272 / 1.790). Figure 3 legend explicitly displays Small 71.06%, Medium 24.02%, Large 4.92%.
  - Table 2 (Lines 403-411): OWLv2 detection = 2.440 s (75.08%), SAM2 segmentation = 0.430 s (13.23%), SceneJSON = 0.280 s (8.62%), Validation = 0.090 s (2.77%), Load image = 0.010 s (0.31%), Total = 3.250 s (100.00%).
  - Section 5.1 (Lines 425-443): Full theoretical and empirical breakdown of `pad_fix` ($\Delta = 0.0000$), OWLv2 Large failure ($4.7\times$ slower, Box F1 0.6260), and SAM2 multimask rejection.
- `documento_explicativo_no_tecnico.md`:
  - Lines 98, 372: Documents 120 images, 1.790 annotations, 71.06% small instances.
  - Documents OWLv2 detection 2.44 s, SAM2 0.43 s, total 3.25 s.
  - Documents Kaggle scores V1 0.6615, V2 0.6763, V3 0.6800.
  - Section 8: Explains failures of OWLv2 Large and other negative experiments conceptually.
- `guia_defensa_oral_tpi.md`:
  - Lines 56, 385-393: Documents 120 images, 1.790 annotations, 71.06% small, recall by scale (large 0.852, medium 0.765, small 0.575), and worst category recalls (`strap` 0.174, `book` 0.196, `doorknob` 0.200).
  - Lines 252-273: Detailed technical justification for OWLv2 Large rejection ($4.7\times$ latency penalty, 0.626 F1) and SAM2 multimask failure ($0.627$ vs $0.590$).
  - Documents all latencies (OWLv2 2.44 s, SAM2 0.43 s, SceneJSON 0.28 s, total 3.25 s).
  - Documents Box F1 (0.6464 $\rightarrow$ 0.6722), Mask F1 (0.6132 $\rightarrow$ 0.6351), QA Deterministic (0.6053 $\rightarrow$ 0.7895), Kaggle (0.6615 $\rightarrow$ 0.6763 $\rightarrow$ 0.6800).

### 1.3. Test Suite Executions
- `python test_e2e_deliverables.py`:
  - Ran 16 test cases covering Tier 1 to Tier 4.
  - Exit code: 0. 16/16 passed (100%).
- `python test_empirical_challenger.py` (Independent Challenge Suite):
  - Ran 8 comprehensive test cases across all quantitative dimensions.
  - Exit code: 0. 8/8 passed (100%).
- `python build_pdf.py`:
  - Exit code: 0. Generated 20-page A4 PDF (`informe_tecnico_tpi.pdf`, 1826.9 KB).

---

## 2. Logic Chain

1. **Direct Traceability to Execution Stream**:
   Every numerical claim in the deliverables was traced to its point of origin in `tpi-ia-2026p-21.ipynb`.
   - Box F1 (0.6464 and 0.6722) originated from cells 66, 99, and 110.
   - Mask F1 (0.6132 and 0.6351) originated from cells 69, 99, and 110.
   - QA Deterministic Accuracy (0.6053 and 0.7895) originated from cells 72 and 110.
   - Blind Test Kaggle Scores (0.6615, 0.6763, 0.6800) originated from cells 83 and 113.
   - Size distribution ($1272 / 1790 = 71.06\%$, $430 / 1790 = 24.02\%$, $88 / 1790 = 4.92\%$) originated from cell 6 and cell 66.
   - Latencies ($2.44\text{ s} + 0.43\text{ s} + 0.28\text{ s} + 0.09\text{ s} + 0.01\text{ s} = 3.25\text{ s}$) originated from cell 111.
   - Negative experiments (`pad_fix` $\Delta = 0$, OWLv2 Large $4.7\times$ slowdown & 0.626 F1, SAM2 single vs multimask) originated from cells 74/77, 89/92, and 95.

2. **Differentiating Intermediate vs. Final V3 Scores**:
   An initial adversarial check was performed on the presence of Box F1 = 0.6641 and Mask F1 = 0.6273 (observed in cell 98 and cell 113).
   The logic chain reveals that cell 98 executed the initial multiscale pipeline, whereas cell 99 (Section 12.1b) introduced the post-processing large-area filter (`conf_large = 0.15`), elevating the score to Box F1 = 0.6722 and Mask F1 = 0.6351 (as recorded in the final comparison table in cell 110).
   The technical report correctly presents the final post-processed V3 metrics (0.6722 and 0.6351) in Table 1 and Executive Summary, while transparently documenting the raw multiscale performance (0.6641 and 0.6273) in the ablation progression. This is accurate and consistent with the notebook execution.

3. **Absence of Numerical Contradictions or Rogue Numbers**:
   Regex scans across all three documents confirmed that no rogue or distorted Kaggle scores (e.g. claiming scores above 0.6800 or below 0.6615 for evaluated configurations) exist.
   Decimal representations in Spanish texts (`0,6800`, `2,44 s`) and English formats (`0.6800`, `2.44 s`) reflect the exact same mathematical values.

---

## 3. Caveats

- **No Caveats**. All 7 quantitative verification items specified in the mission prompt were empirically reproduced, programmatically tested, and confirmed against the notebook cells.

---

## 4. Conclusion

All quantitative claims, empirical metrics, dataset distributions, execution latencies, and negative hypotheses documented across `informe_tecnico_tpi.md`, `documento_explicativo_no_tecnico.md`, and `guia_defensa_oral_tpi.md` faithfully match the ground-truth execution outputs in `tpi-ia-2026p-21.ipynb`.

Zero factual discrepancies, rounding errors, or numerical contradictions exist.

**FINAL VERDICT**: `APPROVE`

---

## 5. Verification Method

To independently reproduce and verify this assessment:

1. **Run the Independent Empirical Challenger Suite**:
   ```bash
   python test_empirical_challenger.py
   ```
   *Expected result*: Ran 8 tests, 0 failures, 0 errors, OK.

2. **Run the Automated E2E Deliverables Test Suite**:
   ```bash
   python test_e2e_deliverables.py
   ```
   *Expected result*: Ran 16 tests, 0 failures, 0 errors, OK (100% compliant).

3. **Verify Clean PDF Compilation**:
   ```bash
   python build_pdf.py
   ```
   *Expected result*: Exit code 0, generates `informe_tecnico_tpi.pdf` (20 pages, A4 geometry).
