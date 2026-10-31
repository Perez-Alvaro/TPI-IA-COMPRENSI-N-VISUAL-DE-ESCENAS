# FORENSIC AUDIT REPORT — TPI IA 2026 DELIVERABLES

**Work Product**: All project deliverables (`informe_tecnico_tpi.pdf`, `informe_tecnico_tpi.html`, `informe_tecnico_tpi.md`, `documento_explicativo_no_tecnico.md`, `guia_defensa_oral_tpi.md`, `build_pdf.py`, `test_e2e_deliverables.py`, `report_assets/`)  
**Auditor**: `auditor_1` (Forensic Integrity Auditor)  
**Profile**: General Project / Academic Engineering Report  
**Integrity Mode**: Development (per `ORIGINAL_REQUEST.md`, Line 7)  
**Verdict**: **CLEAN**

---

## 1. Observation

Direct empirical observations made across the workspace (`c:\Users\perez\OneDrive\Documents\Ing.Sist-NUBE\IA\TPI IA 2026`):

### 1.1 Deliverable Files Existence, Sizes, and Headings
All deliverables exist at workspace root, non-empty, and with substantial academic depth:
- `informe_tecnico_tpi.pdf`: 1,870,705 bytes, 20 pages, A4 standard dimensions (`594.96 x 841.92 pt`).
- `informe_tecnico_tpi.html`: 51,138 bytes, 984 lines, 7,153 words.
- `informe_tecnico_tpi.md`: 53,680 bytes, 520 lines, 7,461 words (9 H1, 18 H2, 25 H3 headings covering all 6 mandatory sections).
- `documento_explicativo_no_tecnico.md`: 50,650 bytes, 590 lines, 5,428 words (1 H1, 7 H2, 18 H3 headings; 0 heavy LaTeX math formulas; 5 pipeline stages fully covered).
- `guia_defensa_oral_tpi.md`: 67,968 bytes, 536 lines, 9,760 words (1 H1, 4 H2, 18 H3 headings; 10-minute presentation breakdown for all 5 team members with exact minute-by-minute scripts; comprehensive Q&A bank).
- `build_pdf.py`: 4,443 bytes, 120 lines (operational build script invoking Microsoft Edge / Chrome headless).
- `test_e2e_deliverables.py`: 24,194 bytes, 558 lines (16 comprehensive unit tests across 4 tiers).
- `report_assets/`: 11 image assets totaling 1.62 MB, all valid PNGs with standard headers (e.g., `fig_pipeline_architecture.png` at 2952x1320 px, `fig5_lvis_tuning_curve.png` at 2220x1170 px).

### 1.2 PDF Compilation and Engine Metadata
Execution of `python build_pdf.py`:
```
[1/4] Usando ejecutable de navegador: C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe
[2/4] Ejecutando compilación headless de HTML a PDF...
[3/4] PDF generado exitosamente: C:\Users\perez\OneDrive\Documents\Ing.Sist-NUBE\IA\TPI IA 2026\informe_tecnico_tpi.pdf (1826.9 KB)
[4/4] Verificando especificaciones técnicas del PDF generado...
      - Cantidad de páginas: 20 (Mínimo requerido: 15)
      - Geometría de Página 1 (Portada): 595.0 x 841.9 pt
      - Geometría A4 conforme: A4 Portrait estándar validado.
      - Contenido Portada verificado: 812 caracteres extraídos.
      - Contenido Página 2 verificado: 2157 caracteres extraídos.
Exit code: 0
```
Inspection of `informe_tecnico_tpi.pdf` via `pypdf`:
- Creator: `Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/156.0.0.0 Safari/537.36 Edg/156.0.0.0`
- Producer: `Skia/PDF m156`
- CreationDate: `D:20261031141701+00'00'`
- Total extracted text: >25,000 characters; Spanish diacritics present (`áéíóúñ`); zero `\ufffd` replacement characters.

### 1.3 Empirical Claims vs Notebook Ground Truth
Inspection of `tpi-ia-2026p-21.ipynb` cell outputs:
- **Baseline (V1)**:
  - Cell 66: `Detección (cajas): {'TP': 1135, 'FP': 587, 'FN': 655, 'ignored': 2628, 'precision': 0.6591, 'recall': 0.6341, 'f1': 0.6464, 'coverage': 0.3959}`
  - Cell 69: `Segmentación (máscaras): {'TP': 1074, 'FP': 639, 'FN': 716, 'ignored': 2637, 'precision': 0.627, 'recall': 0.6, 'f1': 0.6132, 'coverage': 0.3938}`
  - Cell 72: `qa_acc_det: 0.6053`
  - Cell 83: `| V1 | Línea base: OWLv2 base, conf 0,15, NMS 0,30 | 0,6615 |`
- **V2 Optimization**:
  - Cell 83: `| V2 | Umbrales de la sección 8: conf 0,17, NMS 0,35 | 0,6763 |`
- **V3 Final Solution**:
  - Cell 83 & 113: `| V3 (final) | Mosaicos + conf 0,23 / NMS 0,30 + mejoras de QA | 0,6800 |`
  - Cell 110:
    ```
                   baseline (S7)      V3   delta
    box_f1                0.6464  0.6722  0.0258
    box_precision         0.6591  0.7159  0.0568
    box_recall            0.6341  0.6335 -0.0006
    mask_f1               0.6132  0.6351  0.0219
    qa_acc_det            0.6053  0.7895  0.1842
    proxy_score           0.6745  0.7083  0.0338
    ```
  - Cell 111 & 112: `tiempos_v3 = [0.01, 0.09, 0.28, 0.43, 2.44]`; latencia total aumentó de $1.25\text{ s}$ a $3.25\text{ s}$.
- **Negative Hypotheses**:
  - `pad_fix`: Cell 73 & 83 confirm zero gain ($\Delta = 0.0000$).
  - `owlv2-large`: Cell 85 & 113 confirm rejection (latency $4.7\times$ higher: $11.45\text{ s}$ vs $2.44\text{ s}$; drop in Box F1 to $0.626$).
  - `SAM2 multimask`: Cell 95 & 96 confirm rejection (selection mode: `single` retained, multimask degraded mask F1 due to part-level over-segmentation).

### 1.4 Theoretical Grounding vs `IA-Resumen-Completo.pdf`
- Page 23 of `IA-Resumen-Completo.pdf` explicitly defines F1-Score as the harmonic mean:
  *"La puntuación F1 es la media armónica de la precisión y recall... ¿Por qué la media armónica? Dado que la media armónica de una lista de números se inclina fuertemente hacia últimos elementos de la lista, tiende... a agravar el impacto de los pequeños. La medida F1 castiga más los valores extremos."*
- `informe_tecnico_tpi.md` (lines 339-346) and `informe_tecnico_tpi.html` explicitly ground their metric analysis in this exact harmonic mean formulation, alongside convolutional hierarchy ($RF_l = RF_{l-1} + (K_l - 1) \prod S_i$), inductive zero-shot transfer learning, and LVIS federated annotation evaluation.

### 1.5 Academic Compliance on Vision-Language Prohibitions
- Inspection of `tpi-ia-2026p-21.ipynb` Cells 50-60 and `TPI Primavera 2026 - Comprensión visual de escenas.pdf` Pages 5-9 confirms:
  1. The vision pipeline uses `google/owlv2-base-patch16-ensemble` (box detection) and `sam2_hiera_small.pt` (mask segmentation).
  2. The output of perception is converted into an explicit, auditable scene graph serialized as `SceneJSON` (with 3x3 quantized spatial positions, RLE column-major masks, dominant colors, and bounding boxes).
  3. No end-to-end vision-language model (e.g. GPT-4V, LLaVA, Gemini Vision) ever receives raw image pixels to answer questions.
  4. The LLM (`Qwen/Qwen2.5-1.5B-Instruct` in Cell 54) operates exclusively on the textual question string to parse it into an intermediate query specification JSON (`QUERY_SPEC`).
  5. The deterministic query engine (`find_objects`) executes the structured query strictly over `SceneJSON` objects to compute the answer and isolate evidence IDs.
  6. The LLM only verbalizes the deterministic result, protected by a fidelity verification filter (`is_faithful`).

### 1.6 E2E Deliverables Test Execution
Execution of `python test_e2e_deliverables.py`:
```
----------------------------------------------------------------------
Ran 16 tests in 7.117s

OK
================================================================================
  AUDIT SUMMARY
================================================================================
  Total Executed : 16
  Passed         : 16 (100.0%)
  Failures       : 0
  Errors         : 0
--------------------------------------------------------------------------------
  STATUS: ALL CHECKS PASSED (100% COMPLIANT) - ACCEPTANCE CONFIRMED
================================================================================
Exit code: 0
```

---

## 2. Logic Chain

1. **Absence of Cheating / Hardcoded Shortcuts**:
   - `test_e2e_deliverables.py` performs real assertions on filesystem artifacts, extracts text from the PDF via binary parsing (`pypdf`), runs a headless browser compilation subprocess (`build_pdf.py`), and validates mathematical regex patterns.
   - The test assertions and report metrics correspond 1-to-1 with actual computation logs and execution tables in `tpi-ia-2026p-21.ipynb`. No hardcoded bypasses or facade return values exist.
2. **Absence of Facade Implementations**:
   - Deliverable artifacts are comprehensive, publication-grade documents (HTML: 7,153 words; MD report: 7,461 words; Non-technical: 5,428 words; Oral defense guide: 9,760 words).
   - `build_pdf.py` contains authentic logic executing Microsoft Edge Headless CLI, producing a 20-page A4 PDF matching the institutional template.
3. **Absence of Fabricated Verification Outputs**:
   - No pre-populated `.log` or fake attestation files were found in the workspace.
   - All tests and compilations were executed dynamically by the auditor with verified exit code 0.
4. **Authenticity of Scientific Claims**:
   - Every single reported metric (Baseline Box F1 0.6464, Mask F1 0.6132, QA 0.6053, Kaggle 0.6615; V2 Kaggle 0.6763; V3 Box F1 0.6722, Mask F1 0.6351, QA 0.7895, Kaggle 0.6800; latencies 1.25s -> 3.25s) is verified directly in notebook execution cells 66, 69, 72, 83, 99, 110, 111, 112, and 113.
   - Negative results (`pad_fix` $\Delta = 0.0000$, OWLv2 Large rejection, SAM2 multimask rejection) are documented honestly with full ablation evidence.
5. **Academic Compliance**:
   - The strict prohibition against end-to-end black-box vision-language models was fully honored.
   - The intermediate representation (`SceneJSON`) serves as the sole, auditable bridge between perception and reasoning, with deterministic execution enforcing truthfulness and auditability.

---

## 3. Caveats

- In `tpi-ia-2026p-21.ipynb`, heavy training and grid-sweep cells (e.g. Cells 82 and 84) were executed during the experimental phase in Kaggle (producing the serialized run traces in `/kaggle/working/runs`), and the delivery version of the notebook is structured to run the winning V3 pipeline (`submission.csv`). The historical outputs and logs remain stored and verified in the notebook cells.
- No other caveats.

---

## 4. Conclusion

The deliverables submitted for the TPI IA 2026 (Comprensión Visual de Escenas — Grupo 21) exhibit exemplary technical depth, complete authenticity, and zero integrity violations. All requirements from `ORIGINAL_REQUEST.md` and the cátedra guidelines are fully satisfied.

**Final Verdict**: **CLEAN**

---

## 5. Verification Method

To independently reproduce the forensic verification:

1. **Verify E2E Deliverables Test Suite**:
   ```powershell
   python test_e2e_deliverables.py
   ```
   *Expected outcome*: 16/16 tests pass with exit code 0.
2. **Verify PDF Compilation**:
   ```powershell
   python build_pdf.py
   ```
   *Expected outcome*: Compiles `informe_tecnico_tpi.html` into `informe_tecnico_tpi.pdf` (20 pages, A4 standard) with exit code 0.
3. **Verify Empirical Claims in Development Notebook**:
   ```powershell
   python .agents/teamwork/auditor_1/audit_inspect_nb.py
   ```
   *Expected outcome*: Displays exact matching strings for Box F1, Mask F1, QA accuracy, Kaggle leaderboard scores, and negative hypotheses across cells 66, 69, 72, 83, 99, 110, 111, and 113.
4. **Verify Theoretical Grounding in Reference Guide**:
   ```powershell
   python .agents/teamwork/auditor_1/audit_theory.py
   ```
   *Expected outcome*: Confirms exact alignment with `IA-Resumen-Completo.pdf` page 23 for harmonic mean in F1-score and CNN receptive field equations.
