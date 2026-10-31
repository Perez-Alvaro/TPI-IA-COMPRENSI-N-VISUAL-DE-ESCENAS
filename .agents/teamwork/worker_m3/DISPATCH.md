## 2026-10-31T14:03:31Z
You are an implementation worker operating in workspace:
c:\Users\perez\OneDrive\Documents\Ing.Sist-NUBE\IA\TPI IA 2026
Your dedicated working directory is:
c:\Users\perez\OneDrive\Documents\Ing.Sist-NUBE\IA\TPI IA 2026\.agents\teamwork\worker_m3

MANDATORY FIRST STEP:
Read the authoritative user request at:
c:\Users\perez\OneDrive\Documents\Ing.Sist-NUBE\IA\TPI IA 2026\.agents\teamwork\ORIGINAL_REQUEST.md

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

EXCLUSIVE FILE WRITE OWNERSHIP:
You own and write exclusively to:
1. c:\Users\perez\OneDrive\Documents\Ing.Sist-NUBE\IA\TPI IA 2026\guia_defensa_oral_tpi.md
And your own working directory files in `.agents\teamwork\worker_m3\`.
DO NOT modify any other implementation files or other agent directories.

INPUT INFORMATION TO READ:
- c:\Users\perez\OneDrive\Documents\Ing.Sist-NUBE\IA\TPI IA 2026\.agents\teamwork\orchestrator_1\PROJECT.md
- c:\Users\perez\OneDrive\Documents\Ing.Sist-NUBE\IA\TPI IA 2026\.agents\teamwork\explorer_survey_1\notebook_analysis.md (115 cells analyzed, all experimental data, error cases)
- c:\Users\perez\OneDrive\Documents\Ing.Sist-NUBE\IA\TPI IA 2026\.agents\teamwork\spec_miner_survey_2\spec_theory_mapping.md (theory of vision, metrics, LVIS policy, grading rubric, 5 key oral defense questions)

YOUR MISSION (Milestone 3 — Oral Defense Preparation Guide):
Author `guia_defensa_oral_tpi.md` at workspace root.
This guide is the master tactical playbook for Grupo 21 (Ocampo, Pecchio, Lopez Quinteros, Chaile, Perez) to ace the 10-minute oral defense and Q&A session:
1. Tactical Defense Strategy:
   - 10-minute strict time breakdown (Minute 0-2 Context & Problem, Minute 2-5 Architecture & Methodology, Minute 5-8 Experiments & Winning Results, Minute 8-10 Error Analysis & Conclusions).
   - Role distribution and speaking order across all 5 team members.
   - Master elevator pitch and key metrics cheat-sheet (Box F1 0.6722, Mask F1 0.6351, QA 0.7895, Kaggle 0.6800).
2. Deep-Dive Q&A Bank (At least 20 detailed questions divided into 7 thematic blocks):
   - Block A: Problem Statement & LVIS Federated Evaluation Policy (Why federated evaluation is necessary, why standard COCO mAP penalizes open-vocabulary predictions, how negative and non-exhaustive categories are handled).
   - Block B: Architectural Choices & Trade-offs (Why OWLv2 ViT-B/16 + SAM2 Hiera Small instead of YOLOv8, Mask R-CNN, or end-to-end VLMs; why neuro-symbolic intermediate representation is mandatory per assignment rules; latency vs accuracy trade-offs).
   - Block C: Hyperparameters & Negative Hypotheses (Detailed explanation of confidence and NMS sweeps; why pad_fix yielded exactly 0.0000 delta; why OWLv2 Large failed with worse F1 and 4.7x latency; why SAM2 single-mask mode outperformed multimask).
   - Block D: Multiscale Tiling & Computer Vision Theory (Mathematical explanation of 2x2 tiling with 25% overlap, effective 1.75x resolution boost, ViT 16x16 patch resolution limits, spatial feature maps, and why this solved the small-object detection bottleneck).
   - Block E: Scene Representation & VQA Decoupling (SceneJSON schema, 3x3 centroid grid quantization, Fortran-order RLE compression, Qwen2.5-1.5B prompt expansion, semantic embedding normalization with cosine similarity, self-correcting retry loop, and the derived absence policy).
   - Block F: Error Analysis & Edge Cases (Concrete failure modes from notebook: traffic lights vs streetlights, complex textures, stone statues, small-object limits, spatial ambiguity in Spanish).
   - Block G: Mathematical & Theoretical Foundations from `IA-Resumen-Completo.pdf` (Why harmonic mean for F1 score, mathematical formulation of precision-recall curves, ROC/AUC, Cross-Entropy vs Focal Loss, Adam optimizer mechanics, weight decay and regularization).
3. "Trap" Questions & Defense Traps:
   - Common pitfalls during defense, what NOT to say, and how to pivot back to solid empirical data and theoretical principles.

Ensure the document is structured, comprehensive, and includes exact formulas and technical rigor.
