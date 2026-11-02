# TRABAJO PRÁCTICO INTEGRADOR: COMPRENSIÓN VISUAL DE ESCENAS
## Cátedra de Inteligencia Artificial — Primavera 2026
**Universidad Tecnológica Nacional (UTN) — Facultad Regional Córdoba**  
**Curso:** 5K2 | **Grupo N° 21**

---

### Integrantes (Grupo 21)
- **Chaile, Emmanuel Ricardo** — Legajo: 89767
- **López Quinteros, Manuel** — Legajo: 99026
- **Ocampo, Gabriel** — Legajo: 93368
- **Pecchio, Valentina** — Legajo: 94416
- **Perez, Alvaro** — Legajo: 97986

### Cuerpo Docente
- **Ing. García, Mario Alejandro**
- **Ing. Guzman, Analía**
- **Ing. Gramatica, Martin**

---

## 📌 Resumen del Proyecto

Este repositorio contiene la entrega final del **Trabajo Práctico Integrador de Inteligencia Artificial (Primavera 2026)**.  
El sistema implementa una arquitectura **neuro-simbólica modular de cinco estadios** para la comprensión visual de escenas en imágenes del mundo real, rechazando modelos de visión-lenguaje (VLMs) de caja negra opacos y garantizando un 100% de interpretabilidad y auditoría:

1. **Percepción Visual Open-Vocabulary:** Detección de objetos con `OWLv2 Base (ViT-B/16)` combinada con inferencia multiescala por mosaicos $2 \times 2$ con 25% de solapamiento (aumento efectivo de resolución de $1,75\times$).
2. **Segmentación de Instancias:** Segmentación geométrica a nivel de píxel con `SAM2 (Segment Anything Model 2 Small Hiera)` guiado por bounding boxes como prompts espaciales.
3. **Representación Estructurada (`SceneJSON`):** Grafo de escena computable con centroides discretizados en una cuadrícula topológica $3 \times 3$, paleta estandarizada de 11 colores, predicados espaciales direccionales y compresión RLE en orden Fortran (*column-major*).
4. **Razonamiento y Consulta (VQA):** Motor en tres capas desacopladas con intérprete semántico (`Qwen2.5-1.5B-Instruct`), motor determinista factual con política de ausencia derivada (`not_detected`) y filtro algorítmico de fidelidad verbal.
5. **Auditoría y Trazabilidad:** Módulo `PipelineTracer` con validación estricta bajo el estándar `Draft7 JSON Schema`.

---

## 📂 Estructura de Entregables Principales

- 📄 [`INFORME_TPI_IA_2026P_21.md`](INFORME_TPI_IA_2026P_21.md): **Informe Técnico Oficial Final** del Grupo 21, estructurado en las 9 secciones académicas, con análisis del EDA, justificación metodológica del pipeline, barridos de hiperparámetros, resultados, análisis de errores cualitativo y figuras integradas.
- 📓 [`tpi-ia-2026p-21.ipynb`](tpi-ia-2026p-21.ipynb): **Notebook de desarrollo y evaluación final**, con las 72 celdas ejecutadas de punta a punta, sin errores y con reproducibilidad garantizada (`seed = 42`).
- 📊 [`submission.csv`](submission.csv): **Archivo oficial de predicciones** para el conjunto de prueba de Kaggle (80 imágenes con SceneJSON serializado), obteniendo un puntaje oficial en el Leaderboard ciego de **`0,6926`**.
- 🎯 [`guia_defensa_oral_tpi.md`](guia_defensa_oral_tpi.md): **Guía Táctica Maestra para la Defensa Oral**, con cronograma estricto de 10 minutos asignado por integrante, tabla resumen de métricas, banco de 25 preguntas técnicas con respuestas fundamentadas en código y teoría, y protocolo para preguntas trampa.
- 📘 [`documento_explicativo_no_tecnico.md`](documento_explicativo_no_tecnico.md): **Documento conceptual accesible**, que explica intuitivamente el funcionamiento del sistema mediante analogías visuales (*El Detective, El Escultor, El Cartógrafo, El Verificador y El Inspector*), sin jerga matemática densa.

---

## 📊 Métricas y Resultados Consolidados

| Dimensión / Métrica | Línea Base (V1) | Tuned Thresholds (V2) | V3 Multiescala (Final) | $\Delta$ Total | Estado / Impacto |
|---|:---:|:---:|:---:|:---:|---|
| **Score Oficial Kaggle (Test)** | 0,6615 | 0,6763 | **0,6926** | **+0,0311** | **Máximo score alcanzado** |
| **F1-Score de Cajas (LVIS)** | 0,6464 | 0,6520 | **0,6722** | **+0,0258** | Supera holgadamente el 0,50 de Promoción |
| **Precisión de Cajas** | 0,6591 | 0,7060 | **0,7159** | $+0,0568$ | Supresión masiva de falsos positivos |
| **Recall de Cajas** | 0,6341 | 0,6030 | **0,6335** | $-0,0006$ | Preservado pese a umbral más estricto |
| **Cobertura de Cajas** | 0,3959 | 0,4012 | **0,4249** | $+0,0290$ | Mayor fracción de predicciones evaluables |
| **F1-Score de Máscaras (SAM2)** | 0,6132 | 0,6200 | **0,6351** | **+0,0219** | Alta fidelidad a nivel de píxel |
| **Consistencia `SceneJSON`** | 1,0000 | 1,0000 | **1,0000** | $0,0000$ | 100% conforme a Draft-07 JSON Schema |
| **VQA Exactitud Determinista** | 0,6053 | 0,6053 | **0,7895** | **+0,1842** | 30/38 preguntas cerradas correctas |
| **VQA Exactitud Modo LLM** | 0,4211 | 0,4211 | **0,5789** | **+0,1578** | 22/38 preguntas cerradas correctas |
| **VQA Descripciones Válidas** | 0,0% | 0,0% | **100,0%** | $+100,0\%$ | 20/20 consignas generadas con éxito |
| **Filtro de Fidelidad LLM** | 30,0% | 30,0% | **71,4%** | $+41,4\%$ | Fallback determinista en el resto |
| **Score de Percepción** | 0,4730 | 0,4787 | **0,4912** | $+0,0182$ | $0,40 F1_{box} + 0,35 F1_{mask}$ |
| **Latencia Media Total** | 1,26 s/img | 1,26 s/img | **2,87 s/img** | $+1,61\text{ s}$ | 3,8 min para las 80 imágenes de test |

---

## 🛠️ Tecnologías y Modelos Empleados

- **Detección Open-Vocabulary:** `google/owlv2-base-patch16-ensemble` (Hugging Face Transformers / PyTorch)
- **Segmentación Guiada por Cajas:** `Meta SAM 2 (sam2_hiera_small.pt)`
- **Modelo de Lenguaje para VQA:** `Qwen/Qwen2.5-1.5B-Instruct`
- **Evaluación y Esquema:** `pycocotools`, `jsonschema`, `torchvision`
- **Dataset:** LVIS / COCO (120 imágenes de desarrollo, 1.790 instancias, 120 categorías)
