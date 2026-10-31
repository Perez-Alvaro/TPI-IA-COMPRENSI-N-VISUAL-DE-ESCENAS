# Informe Técnico Exhaustivo del Notebook de Desarrollo
**Archivo analizado:** `tpi-ia-2026p-21.ipynb`  
**Proyecto:** Trabajo Práctico Integrador: Comprensión Visual de Escenas  
**Cátedra:** Inteligencia Artificial — Universidad Tecnológica Nacional (Primavera 2026)  
**Curso:** 5k2 | **Grupo:** 21  
**Integrantes:**
- Ocampo, Gabriel — Legajo 93368
- Pecchio, Valentina — Legajo 94416
- Lopez Quinteros, Manuel — Legajo 99026
- Chaile, Emmanuel Ricardo — Legajo 89767
- Perez, Alvaro — Legajo 97986

---

## 1. Dataset y Análisis Exploratorio de Datos (EDA)

### 1.1. Estructura y Partición del Conjunto de Datos
- **Fuente y entorno:** Dataset alojado en la competencia de Kaggle `tpi-ia-2026-primavera-comprension-visual-de-escenas`.
- **Conjunto de Desarrollo (`development`):**
  - **Total de imágenes:** 120 imágenes en formato JPEG/PNG (almacenadas en `development/images/`).
  - **Total de anotaciones:** 1.790 instancias anotadas (`annotations.json` estructurado bajo formato COCO/LVIS).
  - **Vocabulario evaluable:** 120 categorías semánticas cerradas extraídas de LVIS/COCO.
- **Conjunto de Evaluación / Test (`test_images.csv`):**
  - 60 imágenes de prueba independientes sin anotaciones públicas provistas.
- **Formato final de entrega (`sample_submission.csv`):**
  - 80 filas en total: 20 imágenes del benchmark de desarrollo (con campos `questions` y `questions_llm`) + 60 imágenes de test.

### 1.2. Estadísticas de Distribución y Complejidad Visual
- **Densidad de objetos por imagen:**
  - **Promedio:** 14,92 objetos por imagen.
  - **Distribución:** Fuertemente sesgada a la derecha. La gran mayoría de las imágenes concentra entre 5 y 15 instancias.
  - **Casos extremos:** Escenas de alta complejidad visual y hacinamiento que superan los 40 y alcanzan hasta 60 objetos anotados, provocando severas oclusiones.
- **Composición de categorías (Top Frecuentes):**
  - El Top 15 está integrado por objetos de interior y mobiliario: `book`, `car`, `chair`, `box`, `bottle`, `cup`, `table`, entre otros.
  - No existe un monopolio de una única clase; hay una amplia diversidad intra-escena que valida la necesidad de un modelo de vocabulario abierto (*Open-Vocabulary*).
- **Distribución de Escala y Tamaño Relativo ($Área_{caja} / Área_{imagen}$):**
  - **Promedio:** 0,0375 (3,75% de la superficie de la imagen).
  - **Mediana:** 0,0061 (¡el 50% de las instancias ocupa menos del 0,61% del total de la escena!).
  - **Cuantiles de clasificación adoptados para el grafo de escena:**
    - `small` (pequeño): Área relativa $< 0,01$ ($< 1\%$). Representa el **71,06%** de todas las anotaciones (1.272 de 1.790 instancias).
    - `medium` (mediano): $0,01 \le \text{Área relativa} < 0,10$ ($1\% \le \text{área} < 10\%$). Representa el **24,02%** de las instancias (430 objetos).
    - `large` (grande): Área relativa $\ge 0,10$ ($\ge 10\%$). Representa el **4,92%** de las instancias (88 objetos).
  - **Conclusión técnica:** El desafío central de percepción visual radica en los objetos de escala reducida (*small*), altamente vulnerables al umbral de confianza, al submuestreo de parches y a la pérdida de detalle geométrico.

### 1.3. Política de Anotación Federada de LVIS
Debido al amplio vocabulario de LVIS, las imágenes no poseen verificación exhaustiva de todas las 120 clases:
- **Imágenes con categorías negativas verificadas (`neg_category_ids`):** 74 de 120 imágenes.
- **Total acumulado de declaraciones negativas:** 118 declaraciones (promedio de 0,98 clases negativas por imagen).
- **Total de declaraciones no exhaustivas (`not_exhaustive_category_ids`):** 47 declaraciones.
- **Reglas de evaluación federada LVIS implementadas:**
  1. *Categoría positiva:* Tiene instancias anotadas en Ground Truth (GT). Predicciones no emparejadas con IoU $\ge 0,5$ son Falsos Positivos (FP), y anotaciones sin predicción son Falsos Negativos (FN).
  2. *Categoría negativa verificada:* Toda predicción de esa categoría es castigada directamente como FP.
  3. *Categoría no exhaustiva:* Las instancias GT se emparejan normalmente, pero las predicciones sobrantes sin pareja son **ignoradas** (no suman FP).
  4. *Categoría no verificada:* La predicción se marca como **ignorada** (ni TP ni FP), garantizando que no se penalice al modelo por descubrir objetos reales omitidos por el anotador humano.
  5. *Métrica de Cobertura:* Fracción de predicciones evaluables:
     $$\text{Cobertura} = \frac{TP + FP}{TP + FP + \text{Ignoradas}}$$

### 1.4. Benchmark de Preguntas Visuales (VQA)
El conjunto de preguntas de desarrollo (`tpi_2026_qa_public/questions_dev.jsonl`) cuenta con:
- **Total:** 60 consignas distribuidas en 20 imágenes únicas (exactamente 3 preguntas por imagen).
- **Tipos de operaciones (`type`):**
  - `description`: 20 consignas (1 por imagen; requiere texto libre factual).
  - `count`: 10 preguntas (requiere número entero).
  - `existence`: 10 preguntas (requiere booleano `"yes"` / `"no"`).
  - `relation`: 10 preguntas (requiere booleano `"yes"` / `"no"` evaluando predicados espaciales).
  - `position`: 5 preguntas (requiere celda de grilla 3×3, ej. `"top_left"`, `"center"`).
  - `size`: 5 preguntas (requiere clase ordinal `"small"`, `"medium"`, `"large"`).
- **Formatos de respuesta (`answer_format`):**
  - `free_text`: 20
  - `boolean`: 20
  - `integer`: 10
  - `position_3x3`: 5
  - `size_class`: 5

---

## 2. Pipeline de Preprocesamiento y Extracción Multiescala

### 2.1. Inferencia Base del Detector Open-Vocabulary
- **Modelo:** `google/owlv2-base-patch16-ensemble` (Vision Transformer ViT-B/16 con parches de 16×16 píxeles).
- **Formulación de consultas de texto:**
  $$\text{Query}_i = \text{"a photo of a } \{cat_i\}\text{"} \quad \forall cat_i \in \text{Vocabulario (120 clases)}$$
- **Geometría de entrada y reescalado:**
  - El preprocesador de Hugging Face redimensiona y añade padding a la imagen para convertirla en un cuadrado de $960 \times 960$ px.
  - Como las imágenes del dataset rondan dimensiones de $640 \times 480$ px, la relación de aspecto original se compensa en el post-procesamiento mapeando las coordenadas al lado mayor (`side = max(W, H)`).
- **Supresión de No Máximos (NMS):**
  - Se ejecuta `torchvision.ops.batched_nms` de forma independiente por categoría semántica.
  - Permite la coexistencia de cajas jerárquicamente superpuestas entre diferentes clases (ej. una persona que contiene una camisa y una mochila).

### 2.2. Pipeline Multiescala por Mosaicos (Extensión V3)
Para superar la ceguera del detector ante instancias menores al 1% de la imagen, se implementó una estrategia de inferencia en pirámide multirresolución espacial:
1. **Generación de mosaicos ($2 \times 2$ con solapamiento):**
   - Se divide la imagen en una cuadrícula de $2 \times 2$ ventanas con solape del $25\%$ (`overlap = 0.25`).
   - Dimensiones de cada mosaico:
     $$tw = \left\lceil \frac{W}{2 - (2 - 1) \cdot 0.25} \right\rceil = \left\lceil \frac{W}{1.75} \right\rceil, \quad th = \left\lceil \frac{H}{1.75} \right\rceil$$
     Para una imagen típica de $640 \times 480$, cada ventana mide $366 \times 275$ px.
   - Cada mosaico es reescalado a la resolución nativa de $960 \times 960$, aplicando un aumento lineal efectivo de $\approx 1.75\times$ de zoom digital.
2. **Filtrado geométrico en mosaicos:**
   - *Descarte por borde interno:* Si una caja detectada en un mosaico toca un límite interior a menos de 4 píxeles (`edge_px = 4`), se descarta por considerarse un objeto truncado por el corte de la ventana.
   - *Descarte por área excesiva:* Cajas cuya área relativa supere el $10\%$ del área total de la imagen (`tile_max_area = 0.10`) se eliminan, delegando su detección a la pasada de imagen completa.
3. **Fusión y unificación:**
   - Las coordenadas de los mosaicos se trasladan a coordenadas globales $(x + x_0, y + y_0)$.
   - Se aplica NMS por clase sobre la unión de la imagen completa y los mosaicos.

---

## 3. Modelo Base (Línea Base — Versión V1)

### 3.1. Arquitectura de Componentes
1. **Percepción (Detección Open-Vocabulary):**
   - Arquitectura: `google/owlv2-base-patch16-ensemble` (ViT-B/16, resolución $960 \times 960$).
   - Configuración: `CONFIDENCE_THRESHOLD = 0.15`, `NMS_THRESHOLD = 0.30`.
   - Justificación del umbral bajo: Minimizar falsos negativos en el 71% de objetos pequeños identificados en el EDA.
2. **Segmentación de Instancias:**
   - Arquitectura: `Segment Anything Model 2 (SAM2)` utilizando el checkpoint `sam2_hiera_small.pt` y configuración `sam2_hiera_s.yaml`.
   - Mecanismo de prompt: Las bounding boxes de OWLv2 alimentan directamente a SAM2 como prompts espaciales.
   - Eficiencia: La extracción de características visuales (`predictor.set_image`) se ejecuta una única vez por imagen; las máscaras se generan iterativamente sobre dicho embedding.
   - Modo de salida: `multimask_output = False` (retorna exclusivamente la máscara con mayor score).
3. **Representación Estructurada (`SceneJSON`):**
   - *Centroides y Discretización Espacial:* Centroide de masa $(\bar{x}, \bar{y})$ calculado a partir de la máscara binaria. Se mapea a una grilla de $3 \times 3$ celdas (`top_left`, `top_center`, `top_right`, `middle_left`, `center`, `middle_right`, `bottom_left`, `bottom_center`, `bottom_right`). Fallback al centro de la caja delimitadora ante máscaras nulas.
   - *Escala Ordinal:* `small` ($< 1\%$), `medium` ($1\% \le \text{área} < 10\%$), `large` ($\ge 10\%$).
   - *Color Dominante:* Mediana de los píxeles de la máscara proyectada sobre una paleta estándar de 11 colores (`PALETTE`).
   - *Relaciones Espaciales:* Grafo de relaciones que evalúa pares de objetos mediante predicados oficiales (`left_of`, `right_of`, `above`, `below`, `overlaps`) con un margen del $5\%$ y umbral de solapamiento del $5\%$.
   - *Compresión:* Máscaras binarias codificadas en Run-Length Encoding (RLE) en orden Fortran (`order="F"`), formato compatible con COCO.
4. **Módulo de Trazabilidad (`PipelineTracer`):**
   - Context manager `@contextmanager` para cada etapa (`load_image`, `detection`, `segmentation`, `scene_json`, `validation`).
   - Captura excepciones con traceback acotado a 3 niveles sin interrumpir la ejecución del lote.
   - Registro de metadatos de entorno (`run_config.json`: versiones, hardware GPU, semillas).
   - Validación sintáctica mediante `jsonschema.Draft7Validator` contra `scene_schema.json` y consistencia lógica mediante `check_scene_consistency`.

### 3.2. Métricas Cuantitativas de la Línea Base (Desarrollo)
| Métrica | Valor Línea Base (V1) | Detalle / Conteo |
|---|---|---|
| **Box Precision** | 0,6591 | TP: 1.135, FP: 587 |
| **Box Recall** | 0,6341 | FN: 655, Ignoradas: 2.628 |
| **Box F1-Score** | 0,6464 | Supera el umbral de aprobación de 0,50 |
| **Box Coverage** | 0,3959 | Evaluabilidad federada LVIS |
| **Mask Precision** | 0,6270 | TP: 1.074, FP: 639 |
| **Mask Recall** | 0,6000 | FN: 716, Ignoradas: 2.637 |
| **Mask F1-Score** | 0,6132 | Pérdida de 61 TP de cajas al pasar a máscaras |
| **Mask Coverage** | 0,3938 | Cobertura en evaluación de segmentación |
| **Consistencia SceneJSON** | 1,0000 (100%) | 120/120 imágenes sin errores de schema ni consistencia |
| **Exactitud QA Determinista** | 0,6053 | Evaluado en 38 preguntas válidas con GT |
| **Exactitud QA LLM** | 0,4211 | Evaluado en 38 preguntas válidas con GT |
| **Pipeline Proxy Score** | 0,6745 | $0.40 \cdot F1_{box} + 0.35 \cdot F1_{mask} + 0.15 \cdot Cons + 0.10 \cdot QA_{mean}$ |
| **Score Oficial Kaggle (Test)** | **0,6615** | Evaluación en el conjunto ciego de test (60 imgs) |

---

## 4. Mejoras Iterativas y Experimentación Controlada

### 4.1. Experimento Negativo: Corrección de Padding (`pad_fix`)
- **Hipótesis:** Al reescalar las cajas generadas por OWLv2 al lado mayor (`max(W, H)`), se corregiría la distorsión introducida por el padding cuadrado.
- **Resultado:** **Diferencia exactamente cero ($\Delta = 0,0000$)** en todas las métricas de cajas, máscaras y QA.
- **Causa identificada:** La versión de la biblioteca `transformers` de Hugging Face ya compensa internamente el padding en `post_process_object_detection`.
- **Decisión:** La celda se comentó en el notebook para evitar duplicar el tiempo de ejecución.

### 4.2. Optimización Bidimensional de Hiperparámetros (Sección 8)
- **Metodología:** Barrido bidimensional (Grid Search) sobre las 120 imágenes de desarrollo evaluando candidatos de confianza (`BASE_CONF_FOR_TUNING = 0.12` a `0.50` con paso `0.01`) y NMS (`0.25`, `0.30`, `0.35`, `0.40`, `0.45`, `0.50`).
- **Métrica de selección:** Score de Percepción $= 0,40 \cdot F1_{box} + 0,35 \cdot F1_{mask}$.
- **Resultado:**
  - Configuración base (Conf 0,15, NMS 0,30): Score = **0,4730** ($F1_{box} = 0,6464, F1_{mask} = 0,6132$).
  - Configuración óptima (Conf 0,17, NMS 0,35): Score = **0,4787** ($\Delta = +0,0057$).
- **Impacto en Kaggle (Entrega V2):**
  - **Score Kaggle subió de 0,6615 a 0,6763 ($\Delta = +0,0148$).**
- **Diagnóstico:** El ajuste de umbrales modula el balance precisión/recall pero no es capaz de recuperar instancias que el modelo no detecta en su resolución base.

### 4.3. Escalado del Detector: OWLv2 Base vs. Large (Hipótesis H1)
- **Hipótesis:** `google/owlv2-large-patch14-ensemble` (resolución $1008 \times 1008$, parches de 14 px) mejorará la detección respecto a ViT-B/16.
- **Resultado empírico:** **HIPÓTESIS RECHAZADA.**
  - OWLv2 Base: $F1_{box} = 0,651$, $F1_{mask} = 0,620$, Score = **0,4771**, Latencia = **2,44 s/img**.
  - OWLv2 Large: $F1_{box} = 0,626$, $F1_{mask} = 0,586$, Score = **0,4555**, Latencia = **11,45 s/img** ($4,7\times$ más lento).
- **Conclusión:** OWLv2 Large incrementó falsos positivos en el vocabulario de 120 clases sin ganar sensibilidad en objetos pequeños, aumentando inaceptablemente el cómputo.

### 4.4. Extensión Multiescala con Mosaicos $2 \times 2$ (Hipótesis H2)
- **Hipótesis:** La inferencia por mosaicos $2 \times 2$ con $25\%$ de solape recuperará objetos pequeños.
- **Resultado:** **CONFIRMADA PARCIALMENTE.**
  - OWLv2 Base sin mosaicos: $F1_{box} = 0,651$, $F1_{mask} = 0,620$, Score = **0,4771**.
  - OWLv2 Base con mosaicos $2 \times 2$: $F1_{box} = \mathbf{0,6641}$, $F1_{mask} = \mathbf{0,6273}$, Score = $\mathbf{0,4852}$ ($\Delta = +0,0081$).
  - Umbral óptimo resultante: `conf = 0.23`, `nms = 0.30`, `tile_delta = 0.0`.
  - El recall en objetos pequeños se mantuvo intacto ($0,569$ vs $0,575$) a pesar de incrementar el umbral de 0,15 a 0,23, eliminando masivamente falsos positivos.

### 4.5. Umbrales Adaptativos por Tamaño y Filtrado entre Clases (Sección 12.1b)
- **Ajuste:** Umbral diferencial para objetos grandes (`conf_large = 0.15` para áreas relativas $\ge 0.05$) y umbral general de `conf = 0.23` para el resto.
- **Resultado:**
  - $F1_{box}$ se elevó a **0,6722** ($P = 0,7159, R = 0,6335$).
  - $F1_{mask}$ se elevó a **0,6351** ($P = 0,6840, R = 0,5793$).
  - Score de percepción alcanzó **0,4912**.

### 4.6. Selección de Máscaras en SAM2 (Sección 11)
- **Hipótesis:** Evaluar las 3 hipótesis de máscara devueltas por SAM2 (`multimask_output = True`) y seleccionar la de mayor score o la de mayor IoU con la caja aumentará el $F1_{mask}$.
- **Resultado:** **HIPÓTESIS RECHAZADA.**
  - Modo `single` (`multimask=False`): $F1_{mask} = \mathbf{0,627}$, IoU medio = $\mathbf{0,789}$, IoU small = $\mathbf{0,753}$.
  - Modo `best_score`: $F1_{mask} = 0,590$, IoU medio = $0,746$, IoU small = $0,692$.
  - Modo `box_iou`: $F1_{mask} = 0,608$, IoU medio = $0,759$, IoU small = $0,724$.
- **Causa:** En objetos pequeños, las máscaras alternativas de SAM2 aíslan subpartes o incorporan fondo indeseado. Se ratificó el modo `single`.
- **Prueba de SAM 2.1:** Los pesos de `sam2.1_hiera_small.pt` rindieron Score = 0,4911 vs 0,4912; se conservó SAM2 original.

### 4.7. Arquitectura y Mejoras del Módulo VQA (Sección 12.2 - 12.5)
- **Arquitectura de Tres Capas:**
  1. *Capa 1: Intérprete de Consultas:*
     - Modo Determinista: Reglas fijas y extracción de relaciones mediante regex (`RELATION_PATTERNS`).
     - Modo LLM: `Qwen/Qwen2.5-1.5B-Instruct` guiado por prompt restrictivo (`INTERP_SYSTEM_V3`) que traduce preguntas en lenguaje natural a la especificación formal `QUERY_SPEC`.
     - *Autocorrección con reintento (`interpret_with_retry`):* Si la validación sintáctica falla, se devuelve el error al LLM junto a los 5 candidatos semánticos más cercanos (usando embeddings de texto de OWLv2). La interpretación correcta de existencia subió del $80\%$ al $90\%$, y la de descripciones alcanzó el $100\%$.
  2. *Capa 2: Motor Determinista Factual:*
     - Ejecución directa sobre el grafo `SceneJSON`.
     - Manejo de ambigüedad (`ambiguous`) si múltiples instancias difieren en atributos.
     - *Política de ausencia derivada (`not_detected`):* Si no hay detecciones para una clase en existencia, conteo o relación, el sistema responde explícitamente `"no"` o `0` con confianza derivada $0,5$ y nota de auditoría indicando que la ausencia no está verificada en la imagen, en lugar de abortar con `insufficient_information`.
     - Umbral del motor calibrado a `min_conf = 0.23`.
  3. *Capa 3: Verbalizador y Filtro de Fidelidad:*
     - Verbalizador determinista rígido (`verbalize_v3`) vs. Verbalizador con LLM (`verbalize_llm`).
     - *Filtro de fidelidad algorítmico (`is_faithful`):* Comprueba por expresiones regulares que los números y zonas exactas devueltas por el motor figuren en la respuesta del LLM. Si el LLM altera la verdad matemática, se produce un fallback automático hacia la plantilla rígida.

---

## 5. Análisis Exhaustivo de Errores

### 5.1. Patrones de Falsos Positivos
- En la línea base se observaron 587 FP:
  - **581 casos corresponden a categorías positivas presentes en la imagen sin emparejamiento:** Se trata de detecciones duplicadas o desplazadas en zonas de alta densidad.
  - **Solo 6 casos corresponden a categorías explícitamente negativas de LVIS.**
- **Top categorías con mayores Falsos Positivos:**
  - `traffic light` (26) y `streetlight` (21): Confusión semántica y visual mutua ante postes de alumbrado y luminarias urbanas.
  - `ski` (19): Líneas rectas y barrotes metálicos confundidos con esquíes.
  - `sock` (16) y `knob` (16): Objetos pequeños en fondos ruidosos.
  - `baseball bat` (15) y `wall socket` (13).
- **Ejemplos cualitativos específicos analizados:**
  - En la imagen de prueba `tpi_0085.jpg`, una estatua de piedra en el fondo fue detectada como `dog` (confianza 0,1945), y un relieve tallado en una pared fue clasificado como `elephant` (confianza 0,4086). El detector se guía por texturas visuales locales sin modelar el contexto de materialidad.

### 5.2. Patrones de Falsos Negativos (Omisiones de Detección)
- En la línea base se registraron 655 FN.
- **Sensibilidad según escala del objeto:**
  - `large`: Recall de **0,852** (85,2%).
  - `medium`: Recall de **0,765** (76,5%).
  - `small`: Recall de tan solo **0,575** (57,5%).
- **Categorías con peor Recall (en clases con $\ge 5$ instancias):**
  - `strap` (correa): Recall **0,174** (23 instancias). Objetos finos y alargados.
  - `book` (libro): Recall **0,196** (46 instancias). Lomos y libros apilados ocluidos.
  - `doorknob` (pomo): Recall **0,200** (10 instancias). Objetos diminutos.
  - `curtain` (cortina): Recall **0,241** (29 instancias).
  - `taillight` (luz trasera): Recall **0,278** (18 instancias).
  - `streetlight` (luminaria): Recall **0,333** (9 instancias).
  - `earring` (aro/pendiente): Recall **0,333** (9 instancias).
  - `clock` (reloj): Recall **0,333** (6 instancias).
- **Impacto de la V3:** Los mosaicos lograron mantener el recall en objetos pequeños en $0,569$ mitigando el aumento del umbral de confianza a $0,23$, lo que redujo los FP de 587 a 425 en desarrollo.

### 5.3. Análisis de Errores en el Módulo VQA
- **Línea base (38 preguntas evaluables):**
  - Determinista: 23 aciertos, 15 errores (Exactitud = 0,605). Causa dominante: 9 casos de `insufficient_information`, 4 errores de detección y 1 de ambigüedad.
  - LLM: 16 aciertos, 22 errores (Exactitud = 0,421). Causas: 12 `insufficient_information`, 5 `unsupported` (el LLM no supo interpretar la consigna de descripción), 3 errores de detección y 1 de interpretación.
  - Solo el 30,0% de las verbalizaciones del LLM pasaban el filtro de fidelidad.
- **Pipeline V3 Final:**
  - Determinista: 30 aciertos, 8 errores (**Exactitud = 0,7895**, $+18,4\%$). Errores restantes: 3 instancias omitidas por el detector, 2 falsos positivos, 1 categoría negativa, 1 información insuficiente y 1 ambigüedad.
  - LLM: 21 aciertos, 17 errores (**Exactitud = 0,5526**, $+13,2\%$). Errores restantes: 6 fallas de interpretación en relaciones espaciales complejas, 6 casos `unsupported`, 2 omisiones de detección, 2 insuficiencia y 1 categoría negativa.
  - Las 20 consignas de descripción pasaron de un 0% a un **100% de éxito en interpretación**.
  - **Fidelidad:** El 100% de las evidencias apunta a objetos válidos del JSON, 100% de reproducibilidad, y 84,9% de verbalizaciones del LLM aprobadas sin recurrir a la plantilla determinista.

---

## 6. Progresión Integral de Resultados y Rendimiento Computacional

### 6.1. Cuadro Comparativo Global de Entregas
| Métrica | V1 (Línea Base) | V2 (Tuning Umbrales) | V3 (Multiescala + VQA Fina) | $\Delta$ Total (V3 vs V1) |
|---|---|---|---|---|
| **Box F1-Score** | 0,6464 | 0,6520 | **0,6722** | $+0,0258$ |
| **Box Precision** | 0,6591 | 0,7060 | **0,7159** | $+0,0568$ |
| **Box Recall** | 0,6341 | 0,6030 | **0,6335** | $-0,0006$ |
| **Mask F1-Score** | 0,6132 | 0,6200 | **0,6351** | $+0,0219$ |
| **Consistencia SceneJSON** | 1,0000 | 1,0000 | **1,0000** | $0,0000$ |
| **QA Determinista** | 0,6053 | 0,6053 | **0,7895** | $+0,1842$ |
| **QA LLM** | 0,4211 | 0,4211 | **0,5526** | $+0,1315$ |
| **Proxy Score Local** | 0,6745 | 0,6810 | **0,7083** | $+0,0338$ |
| **Score Kaggle (Test)** | **0,6615** | **0,6763** | **0,6800** | $\mathbf{+0,0185}$ |

### 6.2. Análisis de Latencias y Costo de Cómputo por Etapa (V3)
- **Desglose de tiempo de ejecución promedio por imagen (V3):**
  - **Carga de Imagen (`load_image`):** $0,01\text{ s}$ ($0,31\%$).
  - **Detección Multiescala (`detection`):** **$2,44\text{ s}$ ($75,08\%$)** — Cuello de botella principal debido a las 5 pasadas inferenciales de OWLv2 (1 completa + 4 mosaicos).
  - **Segmentación SAM2 (`segmentation`):** $0,43\text{ s}$ ($13,23\%$).
  - **Construcción SceneJSON (`scene_json`):** $0,28\text{ s}$ ($8,62\%$).
  - **Validación de Schema (`validation`):** $0,09\text{ s}$ ($2,77\%$).
- **Latencia total end-to-end:**
  - Línea Base (1 pasada OWLv2): $\approx 1,25\text{ s/imagen}$.
  - Pipeline V3 (5 pasadas OWLv2): $\approx 3,25\text{ s/imagen}$ ($2,6\times$ de incremento).
- **Evaluación de viabilidad:** Un incremento a 3,25 segundos por imagen es plenamente asumible para sistemas de inspección visual offline y procesamiento batch de 80 imágenes, justificando el aumento en robustez geométrica y precisión.

---

## 7. Catálogo de Figuras y Activos Gráficos del Notebook

Los siguientes gráficos fueron generados y almacenados durante la ejecución del notebook y constituyen la evidencia visual obligatoria para la maquetación del informe técnico:

1. **Figura 1 (EDA - Densidad):** `Distribución de la cantidad de objetos por imagen (Dataset de Desarrollo)`. Histograma con 15 bins que evidencia el sesgo derecho y picos extremos de más de 40 objetos (Celda 6).
2. **Figura 2 (EDA - Semántica):** `Top 15 de Categorías más frecuentes en el Dataset de Desarrollo`. Gráfico de barras horizontales mostrando el predominio de objetos de interior (`book`, `car`, `chair`, `box`) (Celda 9).
3. **Figura 3 (EDA - Escala):** `Distribución del Tamaño Relativo de los Objetos (Área Caja / Área Imagen)`. Histograma demostrando la concentración del 71% de instancias en el rango $< 1\%$ de área relativa (Celda 12).
4. **Figura 4 (EDA - VQA):** `Distribución de los Tipos de Preguntas en el Benchmark de Desarrollo`. Gráfico de barras con la distribución de operaciones (`description`: 20, `count`: 10, `existence`: 10, `relation`: 10, `position`: 5, `size`: 5) (Celda 18).
5. **Figura 5 (Percepción Base):** `Detección OWLv2 | Imagen: tpi_0085.jpg | Conf: 0.15 | NMS: 0.30`. Imagen cualitativa con bounding boxes y etiquetas de confianza que demuestra detección exhaustiva (33 instancias) e ilusiones visuales (perro de piedra y elefante en relieve) (Celda 23).
6. **Figura 6 (Segmentación Base):** `Validación SAM2: Imagen Original vs. Máscara de Instancia`. Comparativa visual lado a lado validando la máscara sobre `motorcycle` (Celda 28).
7. **Figura 7 (Curvas LVIS):** `Detección: Barrido de umbral y Cobertura de Evaluación (LVIS)`. Gráfico de curvas mostrando la relación inversa entre Precisión (65,9% a 95,8%) y Recall (63,4% a 13,9%), el máximo de F1 en 0,15-0,20 y la dinámica de cobertura (Celda 67).
8. **Figura 8 (Análisis Cualitativo de Errores):** `Inspección de Casos Extremos con Código de Colores`. Visualización de la imagen con más falsos negativos y menos falsos negativos (Verde: GT detectado, Amarillo: FN omitido, Rojo: FP verificable) (Celda 76).
9. **Figura 9 (Sensibilidad por Escala):** `Sensibilidad (Recall) según el tamaño del objeto: Línea Base vs. V3`. Gráfico de barras agrupadas comparando el recall en *small* (0,575 vs 0,569), *medium* (0,765 vs 0,765) y *large* (0,852 vs 0,693) (Celda 93).
10. **Figura 10 (Rendimiento VQA):** `Exactitud del módulo VQA por Tipo de Pregunta y Modo`. Gráfico de barras agrupadas comparando Motor Determinista vs. Intérprete LLM en Conteo, Existencia, Posición, Relaciones y Tamaño (Celda 106).
11. **Figura 11 (Latencias y Costo Computacional):** `Tiempo de ejecución por etapa en el pipeline V3` y `Comparativa de costo total Pipeline Línea Base vs. V3`. Panel doble con desglose porcentual por etapa y salto de latencia de 1,25 s a 3,25 s (Celda 111).

---

## 8. Declaración de Modelos, Dependencias y Recursos

| Componente | Identificador / Repositorio | Licencia | Propósito en el Pipeline |
|---|---|---|---|
| **Detector Base** | `google/owlv2-base-patch16-ensemble` | Apache 2.0 | Detección open-vocabulary base y en mosaicos |
| **Detector Escalado** | `google/owlv2-large-patch14-ensemble` | Apache 2.0 | Experimento H1 de escalado (descartado por costo/rendimiento) |
| **Segmentador** | Meta SAM2 (`sam2_hiera_small.pt`) | Apache 2.0 | Segmentación guiada por bounding boxes |
| **Modelo de Lenguaje** | `Qwen/Qwen2.5-1.5B-Instruct` | Apache 2.0 | Traductor de consultas a JSON formal, verbalizador y descriptor |
| **Librerías Core** | `PyTorch`, `torchvision`, `transformers` | Open Source | Cómputo tensorial e inferencia de modelos neuronales |
| **Herramientas de Soporte** | `pycocotools`, `jsonschema` | BSD / MIT | Evaluación federada LVIS y validación de esquemas Draft-07 |
