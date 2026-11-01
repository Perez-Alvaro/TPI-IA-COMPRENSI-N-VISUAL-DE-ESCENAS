# Guía Táctica Maestra para la Defensa Oral del TPI: Comprensión Visual de Escenas
**Trabajo Práctico Integrador — Primavera 2026**  
**Cátedra de Inteligencia Artificial — Universidad Tecnológica Nacional (UTN)**  
**Facultad Regional Córdoba / Facultad Regional Buenos Aires**  
**Curso:** 5k2 | **Grupo:** 21  

---

### Nómina Oficial del Equipo (Grupo 21)
- **Ocampo, Gabriel** — Legajo: 93368
- **Pecchio, Valentina** — Legajo: 94416
- **Lopez Quinteros, Manuel** — Legajo: 99026
- **Chaile, Emmanuel Ricardo** — Legajo: 89767
- **Perez, Alvaro** — Legajo: 97986

---

## 1. Estrategia Táctica de Defensa y Cronograma Estricto de 10 Minutos

El tribunal docente evaluará con cronómetro en mano: el tiempo máximo de exposición es de **exactamente 10 minutos**, seguido de una ronda de preguntas individuales y eventual testeo en vivo con imágenes no vistas. Exceder los 10 minutos conlleva penalización directa en la rúbrica de síntesis técnica.

### 1.1. Desglose Minuto a Minuto con Mensajes Clave

```
+--------------------------------------------------------------------------------------------------+
| CRONOGRAMA MAESTRO DE DEFENSA (10 MINUTOS ESTRICTOS)                                             |
+--------+---------------+-------------------------------------+-----------------------------------+
| MINUTO | BLOQUE        | ORADOR RESPONSABLE                  | MENSAJE FUERZA / OBJETIVO         |
+--------+---------------+-------------------------------------+-----------------------------------+
| 00-02  | Contexto,     | Gabriel Ocampo                      | Demostrar dominio del problema:   |
|        | Problema y    | (Legajo 93368)                      | 71% de objetos pequeños (<1% área)|
|        | EDA           |                                     | y política federada LVIS.         |
+--------+---------------+-------------------------------------+-----------------------------------+
| 02-05  | Arquitectura  | Valentina Pecchio (Leg. 94416)      | Defender la pipeline modular      |
|        | de Pipeline y | Manuel Lopez Quinteros (Leg. 99026) | neuro-simbólica (OWLv2 + SAM2 +   |
|        | Metodología   |                                     | SceneJSON 3x3) vs VLMs opacos.    |
+--------+---------------+-------------------------------------+-----------------------------------+
| 05-08  | Experimentos, | Emmanuel Ricardo Chaile             | Presentar el salto métrico V1->V3 |
|        | Mosaicos y    | (Legajo 89767)                      | (F1 Box 0.6722, Kaggle 0.6800) y  |
|        | Resultados    |                                     | refutación de hipótesis fallidas. |
+--------+---------------+-------------------------------------+-----------------------------------+
| 08-10  | VQA, Análisis | Alvaro Perez                        | Explicar desacoplamiento VQA,     |
|        | de Errores y  | (Legajo 97986)                      | casos borde (semáforos/estatuas)  |
|        | Conclusiones  |                                     | y cerrar con rigor de ingeniería. |
+--------+---------------+-------------------------------------+-----------------------------------+
```

---

### 1.2. Matriz de Roles y Asignación de Ponencias

#### Miembro 1: Gabriel Ocampo (Legajo 93368) — Apertura, Problema y EDA (Minutos 0:00 - 2:00)
- **Objetivo:** Captar inmediatamente la atención del tribunal, plantear los objetivos de la cátedra y justificar por qué las particularidades del dataset condicionaron toda la ingeniería posterior.
- **Puntos clave de intervención:**
  1. *Planteo formal:* Construcción de un pipeline modular auditable para transformar imágenes RGB en un grafo de escena computable (`SceneJSON`) y responder consultas visuales (VQA) deterministas y mediante LLM.
  2. *Hallazgo crítico del EDA:* El dataset de desarrollo (120 imágenes, 1.790 instancias, 120 categorías) presenta un **desbalance geométrico extremo**: el **71,06% son objetos pequeños (`small`, 1.272 instancias)** con área relativa $< 1\%$ de la escena (mediana: $0,61\%$), el **24,02% son objetos medianos (`medium`, 430 instancias)** entre 1% y 10%, y el **4,92% son objetos grandes (`large`, 88 instancias)** con $\ge 10\%$ del área total.
  3. *Complejidad visual:* Promedio de 14,92 objetos/imagen con picos que superan los 40 y 60 objetos en escenas hacinadas.
  4. *La trampa de LVIS:* Explicar por qué LVIS requiere una **política de evaluación federada**: al no haber anotación exhaustiva, predecir una clase no verificada no se penaliza como Falso Positivo para no castigar al modelo por descubrir instancias omitidas por los anotadores humanos.
- **Frase de transición:** *"Para resolver este desafío perceptivo sin caer en cajas negras multimodales, Valentina y Manuel explicarán la arquitectura modular de 5 estadios que implementamos."*

#### Miembro 2: Valentina Pecchio (Legajo 94416) — Percepción y Segmentación (Minutos 2:00 - 3:30)
- **Objetivo:** Explicar con precisión técnica cómo opera la etapa visual profunda y por qué se seleccionaron los modelos fundacionales adoptados.
- **Puntos clave de intervención:**
  1. *Percepción Open-Vocabulary (OWLv2 ViT-B/16):* Empleamos `google/owlv2-base-patch16-ensemble` ($960 \times 960$ px). Opera mediante proyección multimodal contrastiva (estilo CLIP) alineando los parches visuales con consultas de texto `"a photo of a {category}"` para las 120 clases sin reentrenamiento supervisado.
  2. *Segmentación Guiada por Prompts (SAM2):* Usamos Meta SAM2 (`sam2_hiera_small.pt`). Las bounding boxes de OWLv2 actúan como prompts espaciales. La extracción de características visuales se computa una única vez por imagen (`set_image`), decodificando las máscaras binarias de cada instancia en milisegundos.
  3. *Modo de máscara:* Demostrar por qué operamos con `multimask_output = False` (retornando la hipótesis de mayor score), evitando la sobre-segmentación de partes en objetos pequeños.
- **Frase de transición:** *"Una vez que obtenemos cajas y máscaras pixel-perfect, Manuel detallará cómo serializamos esta geometría en un grafo interpretable."*

#### Miembro 3: Manuel Lopez Quinteros (Legajo 99026) — Representación Estructurada y Trazabilidad (Minutos 3:30 - 5:00)
- **Objetivo:** Demostrar el cumplimiento de la consigna central de la cátedra: la representación intermedia simbólica observable y su validación formal.
- **Puntos clave de intervención:**
  1. *Esquema `SceneJSON`:* Estructura formal serializada que incluye metadatos de imagen, lista de objetos tipificados y grafo de relaciones topológicas.
  2. *Cuantización espacial 3x3:* Cálculo del centroide de masa $(\bar{x}, \bar{y})$ a partir de la máscara binaria proyectado a una cuadrícula ortogonal de 9 sectores (`top_left` a `bottom_right`). Si la máscara es anómala, fallback seguro al centro geométrico del bounding box.
  3. *Compresión RLE Fortran-order:* Serialización de máscaras mediante Run-Length Encoding en orden de columnas (`order="F"`), cumpliendo con la especificación de COCO/LVIS y reduciendo el consumo de memoria en un 95% respecto a tensores binarios densos.
  4. *Relaciones Topológicas Deterministas:* Evaluación de pares de objetos mediante predicados booleanos (`left_of`, `right_of`, `above`, `below`, `overlaps`, `inside`) con margen de tolerancia del 5%.
  5. *Módulo de Auditoría (`PipelineTracer`):* Context manager que cronometra cada fase, registra fallas sin abortar el lote y valida sintaxis mediante `jsonschema.Draft7Validator` (100% de consistencia lograda en las 120 imágenes).
- **Frase de transición:** *"Con este pipeline base funcional, Emmanuel presentará cómo optimizamos los hiperparámetros y qué experimentos científicos confirmaron nuestra solución final."*

#### Miembro 4: Emmanuel Ricardo Chaile (Legajo 89767) — Experimentación, Mosaicos y Resultados (Minutos 5:00 - 8:00)
- **Objetivo:** Exponer la progresión empírica de resultados (V1 $\to$ V2 $\to$ V3), la justificación física de los mosaicos y la refutación honesta de hipótesis nulas.
- **Puntos clave de intervención:**
  1. *Salto de la Línea Base (V1):* Confianza 0,15, NMS 0,30 $\implies$ $F1_{box} = 0,6464$, $F1_{mask} = 0,6132$, Score Kaggle = **0,6615**.
  2. *Optimización Bidimensional (V2):* Barrido sistemático de umbrales en 120 imágenes. Se identificó el óptimo en `conf = 0.17`, `nms = 0.35`, elevando el score de Kaggle a **0,6763**.
  3. *La Gran Innovación V3 — Mosaicos Multiescala $2 \times 2$ con 25% de Overlap:* Para rescatar el 71% de objetos pequeños invisibles a la grilla de parches de $16 \times 16$ px de ViT, subdividimos la imagen en 4 ventanas de $\approx 366 \times 275$ px, reescaladas cada una a $960 \times 960$ px. Esto introduce un **zoom digital óptico efectivo de $1,75\times$**.
  4. *Filtrado de mosaicos:* Descarte de cajas a $<4\text{ px}$ de bordes internos (objetos truncados) y de cajas con área $>10\%$ del total (delegadas a la imagen global), seguido de NMS global unificado.
  5. *Umbrales adaptativos:* Umbral permisivo de 0,15 para objetos grandes ($\ge 5\%$ del área) y 0,23 para el resto.
  6. *Resultados Ganadores V3:* $F1_{box} = \mathbf{0,6722}$, $F1_{mask} = \mathbf{0,6351}$, **Kaggle Oficial = 0,6800**.
  7. *Experimentos Negativos Clave:*
     - `pad_fix`: $\Delta = 0,0000$ (Hugging Face ya compensaba el padding internamente).
     - OWLv2 Large: Rechazado; $F1_{box}$ cayó a $0,626$ por proliferación de falsos positivos y latencia $4,7\times$ mayor ($11,45\text{ s}$ vs $2,44\text{ s}$).
     - SAM2 Multimask: Rechazado; $F1_{mask}$ cayó a $0,590$ por fragmentación de objetos pequeños.
- **Frase de transición:** *"Para completar el sistema, Alvaro explicará la arquitectura neuro-simbólica del módulo VQA, el análisis de errores y las conclusiones finales."*

#### Miembro 5: Alvaro Perez (Legajo 97986) — Razonamiento VQA, Errores y Conclusiones (Minutos 8:00 - 10:00)
- **Objetivo:** Mostrar cómo el LLM razona sin alucinar, analizar los casos de falla cualitativos y cerrar la defensa con solidez técnica.
- **Puntos clave de intervención:**
  1. *Arquitectura VQA de Tres Capas Desacopladas:*
     - *Capa 1 (Intérprete):* `Qwen2.5-1.5B-Instruct` traduce lenguaje natural a un JSON intermedio formal (`QUERY_SPEC`). Implementamos un bucle de reintento (`interpret_with_retry`) con sugerencias semánticas mediante similitud coseno de embeddings OWLv2, logrando 100% de interpretación en descripciones y 90% en existencia.
     - *Capa 2 (Motor Determinista):* Ejecución directa sobre `SceneJSON`. Aplica la **política de ausencia derivada (`not_detected`)** para responder explícitamente `"no"` o `0` con nota de auditoría en lugar de colapsar con `insufficient_information`. Exactitud determinista saltó de **0,6053 a 0,7895 (+18,4%)**.
     - *Capa 3 (Verbalizador y Filtro de Fidelidad):* Si el LLM altera números o entidades del motor, el filtro `is_faithful` revierte inmediatamente a la plantilla determinista rígida (84,9% de verbalizaciones aprobadas).
  2. *Análisis de Errores Reales:*
     - Confusión simétrica entre `traffic light` (26 FP) y `streetlight` (21 FP) por similitud estructural urbana.
     - Detección de textura sin contexto de materialidad en `tpi_0085.jpg` (estatua de perro clasificada como animal vivo y relieve en piedra clasificado como elefante).
     - Falsos negativos severos en objetos alargados (`strap`: 17,4% recall) y ocluidos (`book`: 19,6% recall).
  3. *Cierre Conclusivo:* Demostramos que la arquitectura modular neuro-simbólica supera a los modelos monolíticos opacos, entregando un sistema verificable, con cero fugas de datos y un desempeño superior validado en el Leaderboard oficial.
- **Frase final de cierre:** *"Quedamos a disposición de los profesores para la sesión de preguntas técnicas y demostración en vivo."*

---

### 1.3. Protocolo de Transición y Cues Verbales

Para proyectar máxima sincronización de equipo, los integrantes deben utilizar transiciones verbales directas y concisas. Nunca dudar de quién tiene la palabra.

| Transición | Orador Saliente | Orador Entrante | Frase Conectora Mandatoria |
|---|---|---|---|
| **T1 (Min 2:00)** | Gabriel Ocampo | Valentina Pecchio | *"Valentina nos detallará cómo el modelo de percepción extrae las primitivas visuales de estas escenas complejas."* |
| **T2 (Min 3:30)** | Valentina Pecchio | Manuel Lopez Quinteros | *"Manuel explicará cómo convertimos estas máscaras y cajas en la representación simbólica estructurada exigida."* |
| **T3 (Min 5:00)** | Manuel Lopez Quinteros | Emmanuel Chaile | *"Emmanuel presentará la progresión experimental que llevamos a cabo y cómo los mosaicos multiescala elevaron nuestra métrica."* |
| **T4 (Min 8:00)** | Emmanuel Chaile | Alvaro Perez | *"Alvaro finalizará con la arquitectura desacoplada del razonamiento VQA, los patrones de error y nuestras conclusiones."* |

---

### 1.4. Protocolo de Contingencia ("Safety Fallback")

Si un docente interrumpe con una pregunta durante los 10 minutos de exposición:
1. **El orador que tiene la palabra en ese instante toma el control de la respuesta.** No mirarse entre compañeros esperando quién habla.
2. Si la pregunta corresponde a la especialidad temática de otro miembro, el orador responde en una frase y cede cortésmente la palabra: *"Es un punto clave de la etapa de segmentación; Valentina puede precisar la matemática del decoder de SAM2"*.
3. **Control del tiempo:** Si la interrupción docente consume más de 60 segundos, el equipo no debe acelerar atropelladamente el contenido restante; debe saltar directo a los resultados cuantitativos y conclusiones, manteniendo la calma.

---

### 1.5. Master Elevator Pitch (< 60 Segundos)

> *"Nuestro proyecto resuelve la comprensión visual de escenas complejas bajo una arquitectura neuro-simbólica modular de cinco estadios que desacopla la percepción profunda del razonamiento lógico, eliminando el sesgo de 'caja negra' de los VLMs end-to-end.  
> Ante un dataset donde el 71% de los objetos son diminutos —ocupando menos del 1% de la escena— combinamos la detección de vocabulario abierto de OWLv2 con la segmentación guiada por prompts de SAM2, estructurando la geometría en un grafo `SceneJSON` con compresión RLE y discretización espacial 3x3.  
> Mediante una innovación de mosaicos multiescala 2x2 con 25% de solape que otorga un aumento óptico de 1.75x, junto a un módulo VQA con autocorrección semántica y motor determinista infalible, elevamos el F1 de detección de 0.6464 a 0.6722, la exactitud de preguntas de 60.5% a 78.95%, y alcanzamos un score oficial de 0.6800 en el Leaderboard de Kaggle, todo con 100% de consistencia de esquema y trazabilidad auditable."*

---

### 1.6. Key Metrics Cheat-Sheet (Tabla Resumen de Bolsillo)

Llevar estos números memorizados al examen:

| Dimensión / Métrica | Versión V1 (Línea Base) | Versión V2 (Tuning Umbrales) | Versión V3 (Multiescala + VQA Fina) | $\Delta$ Total (V3 vs V1) | Meta de Cátedra |
|---|---|---|---|---|---|
| **Box F1-Score** | 0,6464 | 0,6520 | **0,6722** | $+0,0258$ | $\ge 0,50$ (Promoción) |
| **Box Precision** | 0,6591 | 0,7060 | **0,7159** | $+0,0568$ | — |
| **Box Recall** | 0,6341 | 0,6030 | **0,6335** | $-0,0006$ | — |
| **Mask F1-Score** | 0,6132 | 0,6200 | **0,6351** | $+0,0219$ | — |
| **Mask Precision** | 0,6270 | — | **0,6840** | $+0,0570$ | — |
| **Mask Recall** | 0,6000 | — | **0,5793** | $-0,0207$ | — |
| **Consistencia SceneJSON** | 1,0000 (100%) | 1,0000 (100%) | **1,0000 (100%)** | $0,0000$ | 100% obligatorio |
| **VQA Exactitud Determinista** | 0,6053 (23/38) | 0,6053 (23/38) | **0,7895 (30/38)** | $+0,1842$ (+18,4%) | — |
| **VQA Exactitud LLM** | 0,4211 (16/38) | 0,4211 (16/38) | **0,5526 (21/38)** | $+0,1315$ (+13,2%) | — |
| **PipelineScore Local** | 0,6745 | 0,6810 | **0,7083** | $+0,0338$ | — |
| **Score Oficial Kaggle (Test)** | **0,6615** | **0,6763** | **0,6800** | $\mathbf{+0,0185}$ | Top Benchmark |
| **Latencia Total End-to-End** | $\approx 1,25\text{ s/img}$ | $\approx 1,25\text{ s/img}$ | **$3,25\text{ s/img}$** | $+2,00\text{ s}$ ($2,6\times$) | Operable en GPU T4 |
| **Desglose Latencia V3** | OWLv2: 2,44s (75%) \| SAM2: 0,43s (13%) \| SceneJSON: 0,28s (9%) \| Valid: 0,09s (3%) | — | — |

#### Resumen Estadístico del Dataset (EDA Cheat-Sheet de Bolsillo):
- **Total de Instancias Ground Truth:** **1.790 anotaciones** distribuidas en 120 imágenes de desarrollo (media: 14,92 obj/imagen).
- **Objetos Pequeños (`small`, área $< 1\%$):** **71,06% (1.272 instancias)** — Mediana de área relativa: 0,61% (cuello de botella de resolución).
- **Objetos Medianos (`medium`, área $1\% - 10\%$):** **24,02% (430 instancias)** — Recall sostenido en 0,765.
- **Objetos Grandes (`large`, área $\ge 10\%$):** **4,92% (88 instancias)** — Salvaguarda adaptativa con `conf_large = 0.15`.
- **Anotación Federada LVIS:** 118 declaraciones de ausencia (`neg_category_ids`) en 74 imágenes y 47 declaraciones no exhaustivas.

---

## 2. Banco Exhaustivo de Preguntas y Respuestas Técnicas (Q&A Bank)

Organizado en 7 bloques temáticos rigurosos con formulación matemática y referencias al código del notebook `tpi-ia-2026p-21.ipynb` y al apunte `IA-Resumen-Completo.pdf`.

---

### Bloque A: Planteo del Problema y Política de Evaluación Federada de LVIS

#### Pregunta A.1: "¿Por qué fue necesario adoptar la política de evaluación federada de LVIS en lugar del cálculo convencional de mAP de COCO?"
- **Respuesta Técnica Fundamentada:**  
  "En el benchmark de COCO clásico (80 clases), se asume una hipótesis de mundo cerrado con **anotación exhaustiva**: todo objeto visible de esas 80 clases ha sido anotado. Bajo esa premisa, cualquier detección generada por el modelo que no coincida con una anotación de ground truth es, por definición, un Falso Positivo ($FP$).  
  Sin embargo, nuestro proyecto opera sobre un vocabulario de 120 categorías de LVIS en un dataset de mundo abierto. Anotar exhaustivamente 120 clases (muchas de ellas raras o de escala diminuta) en cada imagen es humanamente inviable. Por diseño del protocolo LVIS, **la ausencia de una anotación no implica la ausencia física del objeto en la imagen**.  
  Si aplicáramos el mAP estándar de COCO, un detector de vocabulario abierto potente como OWLv2 detectaría correctamente objetos legítimos (como un tenedor o una botella en el fondo) que el anotador humano simplemente pasó por alto, y el evaluador lo penalizaría injustamente sumando un Falso Positivo. La política federada resuelve esto particionando las categorías por imagen en cuatro estados: positivas anotadas, negativas verificadas por un revisor (`neg_category_ids`), positivas no exhaustivas (`not_exhaustive_category_ids`), y categorías no verificadas."

#### Pregunta A.2: "¿Cómo opera matemáticamente la penalización de predicciones y qué tratamiento reciben las categorías negativas y no exhaustivas?"
- **Respuesta Técnica Fundamentada:**  
  "La formulación matemática de LVIS establece reglas disyuntivas para clasificar cada predicción $p_i$ generada por el detector:
  1. **Categoría Positiva:** Existe en el conjunto de ground truth de la imagen ($c \in GT$). Si la predicción $p_i$ tiene una intersección sobre unión $\text{IoU} \ge 0,50$ con una instancia no asignada, computa como **Verdadero Positivo ($TP$)**. Las predicciones restantes de esa clase sin emparejamiento computan como **Falsos Positivos ($FP$)**, y las anotaciones GT no detectadas computan como **Falsos Negativos ($FN$)**.
  2. **Categoría Negativa Verificada ($c \in \text{neg\_category\_ids}$):** Un revisor humano inspeccionó la escena y certificó que dicha clase no existe. Por lo tanto, **cualquier predicción de esa categoría computa directamente como Falso Positivo ($FP$)**, castigando las alucinaciones del modelo. En nuestro dataset hay 118 declaraciones negativas en 74 imágenes.
  3. **Categoría No Exhaustiva ($c \in \text{not\_exhaustive\_category\_ids}$):** Se sabe que existen más instancias de las anotadas. Si la predicción coincide con un GT ($\text{IoU} \ge 0,50$), es $TP$; pero si no empareja, **se marca como Ignorada** (no suma $FP$). Hay 47 declaraciones de este tipo en el dataset.
  4. **Categoría No Verificada:** No está anotada ni fue verificada como ausente. Cualquier predicción se marca como **Ignorada** (ni $TP$ ni $FP$).
  
  Por ende, el Recall evalúa la exhaustividad sobre el GT verificado, mientras que la Precisión se calcula estrictamente sobre el subconjunto de predicciones evaluables:
  $$\text{Recall} = \frac{TP}{TP + FN}, \qquad \text{Precisión} = \frac{TP}{TP + FP_{\text{verificados}}}"$$

#### Pregunta A.3: "Si su precisión de cajas es de 0,7159 pero la cobertura de evaluación es del 39,59%, ¿qué significa exactamente esta cobertura y por qué no invalida el resultado?"
- **Respuesta Técnica Fundamentada:**  
  "La cobertura de evaluación de LVIS cuantifica la fracción de predicciones generadas por el modelo que caen en categorías auditables (positivas o negativas verificadas):
  $$\text{Cobertura} = \frac{TP + FP_{\text{verificados}}}{TP + FP_{\text{verificados}} + \text{Predicciones Ignoradas}} = \frac{1.135 + 587}{1.135 + 587 + 2.628} = 0,3959$$
  Esto significa que de las $4.350$ cajas generadas en el barrido de 120 clases, $2.628$ cajas corresponden a categorías 'no verificadas' en esas imágenes específicas.  
  No invalida el resultado en absoluto; de hecho, es la norma estándar documentada en el paper original de LVIS (Gupta et al., CVPR 2019). OWLv2 evalúa las 120 consultas de texto en paralelo sobre cada imagen. Muchas de esas clases pueden estar físicamente presentes en el fondo sin estar anotadas. Evaluar precisión únicamente sobre las $1.722$ predicciones verificables garantiza rigor estadístico sin inflar ni castigar artificialmente al modelo. Además, el balance final queda garantizado por el $F_1$-Score armónico de **0,6722**, el cual combina precisión y recall de manera estricta."

---

### Bloque B: Decisiones Arquitectónicas y Trade-offs del Pipeline

#### Pregunta B.1: "¿Por qué utilizaron la combinación desacoplada OWLv2 + SAM2 en lugar de un detector entrenado de extremo a extremo como Mask R-CNN o YOLOv8-Seg?"
- **Respuesta Técnica Fundamentada:**  
  "Los modelos tradicionales como Mask R-CNN o YOLOv8 son detectores de **vocabulario cerrado**: su cabeza de clasificación final es una capa lineal fija que mapea a un número estático de clases preentrenadas (habitualmente 80 de COCO). Adaptarlos al vocabulario de 120 clases de LVIS hubiera requerido reentrenar o ajustar finamente la red con un conjunto de datos masivo con máscaras píxel a píxel, lo cual generaría severo sobreajuste dado el tamaño acotado del conjunto de desarrollo (120 imágenes) y la escasez de muestras en la cola larga.  
  Adoptar un enfoque modular fundacional desacoplado ofrece ventajas insuperables:
  1. **OWLv2 (`google/owlv2-base-patch16-ensemble`)** aprovecha un espacio multimodal preentrenado contrastivamente (ViT-B/16 con alineación CLIP-like). Permite consultar dinámicamente cualquier vocabulario en lenguaje natural en tiempo de inferencia sin requerir una sola época de backpropagation ni modificar los pesos de la red.
  2. **SAM2 (`sam2_hiera_small.pt`)** fue entrenado sobre SA-1B (más de mil millones de máscaras). Su decodificador espacial recibe la caja delimitadora de OWLv2 como prompt geométrico y genera la máscara de segmentación con precisión a nivel de píxel.
  
  Separar la detección de la segmentación desacopla la optimización: podemos ajustar los umbrales de detección sin degradar la fidelidad del contorno de las máscaras."

#### Pregunta B.2: "¿Por qué la cátedra prohibió explícitamente el uso de VLMs 'end-to-end' (como GPT-4V o LLaVA) y qué garantías técnicas ofrece la representación intermedia neuro-simbólica?"
- **Respuesta Técnica Fundamentada:**  
  "La cátedra prohibió los VLMs directos porque actúan como 'cajas negras' no auditables que sufren de **alucinación perceptual y espacial**:
  1. *Falta de interpretabilidad:* Si un VLM responde que hay '4 sillas', es imposible determinar si vio 4 sillas reales, si alucinó basándose en el contexto del texto, o si contó la misma silla dos veces.
  2. *Incapacidad geométrica estricta:* Los modelos autorregresivos de visión-lenguaje son notoriously malos prediciendo coordenadas numéricas continuas y máscaras binarias precisas.
  
  Nuestra arquitectura **neuro-simbólica** resuelve esto mediante un contrato formal de representación intermedia (`SceneJSON`):
  - La red neuronal profunda (OWLv2 + SAM2) se encarga exclusivamente de la **percepción continua** (extracción de características, localización y segmentación).
  - La información visual se 'cristaliza' en un grafo simbólico determinista con identificadores unívocos, categorías discretas, centroides discretizados en 3x3 y máscaras RLE.
  - El razonamiento (conteo, existencia, relaciones espaciales) es ejecutado por un motor algorítmico determinista. Si el sistema dice que hay '4 sillas', el JSON lista exactamente los `object_id: [1, 5, 8, 12]` con sus máscaras auditables. Garantiza **cero alucinación factual** y reproducibilidad matemática absoluta."

#### Pregunta B.3: "¿Cuáles son los trade-offs críticos de latencia vs precisión entre la Línea Base (V1) y la versión multiescala (V3)?"
- **Respuesta Técnica Fundamentada:**  
  "El análisis de costo computacional documentado en la Sección 13 del notebook revela los siguientes compromisos de ingeniería:
  - **Línea Base (V1):** Realiza una única pasada inferencial de OWLv2 a resolución $960 \times 960$. Latencia media: **1,25 segundos por imagen** (Detección: 0,82s, SAM2: 0,32s, SceneJSON: 0,11s).
  - **Pipeline V3 (Multiescala):** Ejecuta 5 pasadas inferenciales de OWLv2 (1 imagen global + 4 mosaicos de alta resolución). Latencia media: **3,25 segundos por imagen** (un factor de $2,6\times$).
    - Detección multiescala: $2,44\text{ s}$ ($75,08\%$ del tiempo total).
    - Segmentación SAM2: $0,43\text{ s}$ ($13,23\%$).
    - Construcción SceneJSON: $0,28\text{ s}$ ($8,62\%$).
    - Validación sintáctica: $0,09\text{ s}$ ($2,77\%$).
  
  *Justificación del trade-off:* Para un sistema de comprensión de escenas offline (como la evaluación de 80 imágenes en Kaggle), pasar de 1,25s a 3,25s por imagen es un costo plenamente asumible en una GPU Nvidia T4 (el procesamiento del batch completo insume menos de 5 minutos, muy por debajo del límite de 9 horas de Kaggle). A cambio de esa latencia adicional, el $F_1$ de cajas se elevó de 0,6464 a 0,6722 y el score de Kaggle saltó de 0,6615 a 0,6800. La inversión computacional estuvo directamente correlacionada con la ganancia en exactitud."

---

### Bloque C: Hiperparámetros, Barridos y Refutación de Hipótesis Negativas

#### Pregunta C.1: "¿Cómo se realizó el barrido bidimensional de hiperparámetros y qué criterio matemático guio la elección de los umbrales óptimos?"
- **Respuesta Técnica Fundamentada:**  
  "En la Sección 8 del notebook implementamos un barrido en grilla (*Grid Search*) bidimensional sobre las 120 imágenes del conjunto de desarrollo:
  - Rango de confianza evaluado: $\tau_{\text{conf}} \in [0,12; 0,50]$ con paso de $0,01$.
  - Rango de IoU para Non-Maximum Suppression: $\tau_{\text{NMS}} \in [0,25; 0,50]$ con paso de $0,05$.
  - Función objetivo optimizada (Score de Percepción de la Cátedra):
    $$S_{\text{perc}} = 0,40 \cdot F_{1,\text{box}}(\tau_{\text{conf}}, \tau_{\text{NMS}}) + 0,35 \cdot F_{1,\text{mask}}(\tau_{\text{conf}}, \tau_{\text{NMS}})$$
  
  En la Línea Base V1 teníamos $(\tau_{\text{conf}}=0,15, \tau_{\text{NMS}}=0,30)$ con $S_{\text{perc}} = 0,4730$.  
  El barrido identificó un óptimo local sin mosaicos en $(\tau_{\text{conf}}=0,17, \tau_{\text{NMS}}=0,35)$ con $S_{\text{perc}} = 0,4787$ ($+0,0057$). Esta configuración constituyó la entrega V2 y produjo un salto inmediato en el Leaderboard de Kaggle de 0,6615 a 0,6763.  
  Posteriormente, al incorporar los mosaicos multiescala en V3, la mayor densidad de propuestas exigió subir el umbral de confianza a $\tau_{\text{conf}} = 0,23$ y mantener $\tau_{\text{NMS}} = 0,30$. Este umbral más estricto eliminó masivamente falsos positivos en el fondo sin degradar el recall, ya que los objetos pequeños compensaron su score gracias al zoom digital de los mosaicos."

#### Pregunta C.2: "¿Por qué el experimento de corrección de padding (`pad_fix`) arrojó una mejora matemática exactamente de 0,0000 ($\Delta = 0,0000$)?"
- **Respuesta Técnica Fundamentada:**  
  "En la Sección 7 del notebook formulamos la hipótesis de que, al convertir las imágenes no cuadradas ($640 \times 480$) en tensores cuadrados ($960 \times 960$) con padding para OWLv2, las coordenadas relativas predichas por la red sufrían una distorsión anisótropa si se desnormalizaban asumiendo el ancho y alto originales de forma independiente. Implementamos una rutina manual `pad_fix` para compensar el padding en el lado menor (`side = max(W, H)`).  
  Al reevaluar el pipeline completo sobre las 120 imágenes, **la diferencia en todas las métricas de cajas, máscaras y VQA fue idénticamente 0,0000**.  
  *Causa técnica descubierta:* Al auditar el código fuente del procesador de Hugging Face (`Owlv2Processor.post_process_object_detection`), verificamos que la biblioteca ya aplica internamente la inversión geométrica exacta del padding y redimensionamiento cuando se le suministra el argumento `target_sizes`. Nuestra función externa estaba compensando una distorsión que el framework ya corregía de manera transparente. Siguiendo el principio de parsimonia y optimización de código, desactivamos esa rutina redundante."

#### Pregunta C.3: "¿Por qué falló la Hipótesis H1 al escalar a OWLv2 Large (peor F1 y 4,7x mayor latencia)?"
- **Respuesta Técnica Fundamentada:**  
  "En la Sección 9 evaluamos el detector escalado `google/owlv2-large-patch14-ensemble` (resolución $1008 \times 1008$, parches de 14 px) bajo la hipótesis clásica de que un modelo con mayor capacidad paramétrica mejoraría la percepción.  
  Los resultados empíricos forzaron el **rechazo inmediato de la hipótesis**:
  - OWLv2 Base (ViT-B/16): $F1_{box} = 0,651$, $F1_{mask} = 0,620$, Latencia = **2,44 s/img**.
  - OWLv2 Large (ViT-L/14): $F1_{box} = 0,626$ ($-0,025$), $F1_{mask} = 0,586$ ($-0,034$), Latencia = **11,45 s/img** ($4,7\times$ más lento).
  
  *Explicación teórica:* El espacio de representación semántica de OWLv2 Large es mucho más denso y propenso a activar similitudes marginales cuando se le inyectan simultáneamente 120 consultas textuales en imágenes de interiores. El modelo generó una **explosión masiva de falsos positivos** en clases visualmente ambiguas (ej. confundiendo sombras y molduras con objetos reales), deteriorando severamente la precisión. Además, un incremento de 4,7 veces en tiempo de cómputo volvía inviable el pipeline en hardware estándar de Kaggle."

#### Pregunta C.4: "¿Por qué el modo `single-mask` de SAM2 superó consistentemente al modo `multimask` (`best_score` y `box_iou`)?"
- **Respuesta Técnica Fundamentada:**  
  "SAM2 incorpora un decodificador de máscaras diseñado para resolver la ambigüedad inherente de los prompts puntuales: cuando se le entrega un punto, el objeto puede ser una parte, el subcomponente o la totalidad del cuerpo; por ende, `multimask_output = True` genera 3 hipótesis jerárquicas de máscara con sus correspondientes scores de calidad predichos.  
  En la Sección 11 contrastamos tres estrategias de selección de máscara alimentadas por las cajas de OWLv2:
  1. Modo `single` (`multimask=False`): $F1_{mask} = \mathbf{0,627}$, IoU medio = $\mathbf{0,789}$, IoU en objetos pequeños = $\mathbf{0,753}$.
  2. Modo `best_score` (seleccionar la hipótesis con mayor IoU predicho por SAM2): $F1_{mask} = 0,590$, IoU medio = $0,746$.
  3. Modo `box_iou` (seleccionar la máscara cuya caja envolvente tenga mayor IoU con el prompt de OWLv2): $F1_{mask} = 0,608$, IoU medio = $0,759$.
  
  *Causa física de la degradación:* Cuando el prompt es una **bounding box acotada** (y no un punto ambiguo), la frontera geométrica exterior del objeto ya está delimitada por la caja. En el 71% de objetos pequeños del dataset, el estimador interno de calidad de SAM2 suele asignar mayor puntuación a subpartes internas de alto contraste (sobre-segmentación) o a regiones que incorporan fondo ruidoso. El modo `single` está optimizado para colapsar en la máscara integral que llena el prompt cuadrangular, demostrando ser el más robusto empíricamente."

---

### Bloque D: Multiescala por Mosaicos (Tiling) y Teoría de Visión Artificial

#### Pregunta D.1: "Explique la formulación matemática de los mosaicos 2x2 con 25% de solapamiento y demuestre cómo produce un boost efectivo de ~1,75x en resolución espacial."
- **Respuesta Técnica Fundamentada:**  
  "Sea una imagen de dimensiones $W \times H$. Si dividimos el dominio en $N_x = 2$ particiones horizontales y $N_y = 2$ verticales, permitiendo una fracción de solapamiento $\phi = 0,25$ ($25\%$), el ancho $tw$ y alto $th$ de cada ventana de mosaico se deduce de la cobertura total:
  $$W = N_x \cdot tw - (N_x - 1) \cdot \phi \cdot tw = tw \cdot [2 - (1) \cdot 0,25] = tw \cdot 1,75$$
  Despejando las dimensiones de cada mosaico:
  $$tw = \left\lceil \frac{W}{1,75} \right\rceil, \qquad th = \left\lceil \frac{H}{1,75} \right\rceil$$
  Para una imagen estándar del dataset de $640 \times 480$ píxeles:
  $$tw = \left\lceil \frac{640}{1,75} \right\rceil = 366\text{ px}, \qquad th = \left\lceil \frac{480}{1,75} \right\rceil = 275\text{ px}$$
  
  Cuando ese recorte de $366 \times 275$ px se introduce al preprocesador de OWLv2, la red lo interpola y escala a su tamaño nativo de inferencia de $960 \times 960$ px.  
  El factor de magnificación lineal efectivo sobre la imagen original viene dado por la relación de escalas:
  $$\text{Zoom Lineal} = \frac{W}{tw} = \frac{640}{366} \approx 1,75\times$$
  En términos de densidad superficial de muestreo de información, el incremento de resolución en área equivale a $(1,75)^2 \approx 3,06\times$. Esto significa que un objeto diminuto que en la imagen completa ocupaba una mancha de $8 \times 8$ píxeles, dentro del mosaico pasa a representarse con $14 \times 14$ píxeles, cruzando el umbral de discriminación del Vision Transformer."

#### Pregunta D.2: "¿Por qué la arquitectura Vision Transformer (ViT-B/16) presenta un límite intrínseco de resolución para objetos pequeños con parches de 16x16 píxeles?"
- **Respuesta Técnica Fundamentada:**  
  "En un Vision Transformer estándar como el ViT-B/16 de OWLv2, la imagen de entrada de $960 \times 960$ px se discretiza en una cuadrícula fija de parches no solapados de $16 \times 16$ píxeles:
  $$N_{\text{tokens}} = \left(\frac{960}{16}\right) \times \left(\frac{960}{16}\right) = 60 \times 60 = 3.600\text{ tokens espaciales}$$
  Cada parche de $16 \times 16$ píxeles se proyecta linealmente a un único vector de embedding mediante una convolución 2D con kernel $16 \times 16$ y stride 16.  
  *El cuello de botella físico:* Si un objeto pequeño en la imagen original mide $10 \times 10$ píxeles, al reescalarse a la imagen global de $960 \times 960$ ocupará aproximadamente $15 \times 15$ píxeles. Esto significa que **el objeto entero cae dentro de un único parche de token visual**.  
  Dentro de un token individual, la auto-atención del Transformer no puede resolver relaciones espaciales internas ni bordes; toda la señal del objeto se promedia con los píxeles de fondo que comparten ese parche. Como consecuencia, el embedding visual pierde las altas frecuencias espaciales y colapsa la similitud coseno con el texto de la clase.  
  Al aplicar el mosaico multiescala con zoom $1,75\times$, ese mismo objeto pasa a abarcar entre 3 y 4 parches contiguos, permitiendo que el mecanismo de atención capture contornos discriminantes y recupere la detección."

#### Pregunta D.3: "¿Cómo opera el filtrado geométrico de recortes (descarte por borde interno y límite de área máxima) y su unificación mediante NMS?"
- **Respuesta Técnica Fundamentada:**  
  "Procesar ventanas independientes introduce dos patologías geométricas que resolvimos algorítmicamente en la Sección 10.1:
  1. **Filtrado por Borde Interno (`edge_px = 4`):** Cuando una ventana corta arbitrariamente la escena, un objeto grande o mediano puede quedar seccionado por la mitad. El detector en el mosaico detectaría la mitad visible y predeciría una caja falsa incompleta. Si cualquier coordenada de la caja predicha se encuentra a menos de 4 píxeles del límite interior del recorte (los bordes que no coinciden con el perímetro de la imagen global), la detección se descarta formalmente:
     $$\text{si } x_{\min} \le 4 \text{ o } y_{\min} \le 4 \text{ o } x_{\max} \ge (tw - 4) \text{ o } y_{\max} \ge (th - 4) \implies \text{Descartar}$$
  2. **Filtrado por Área Máxima (`tile_max_area = 0.10`):** Los mosaicos fueron diseñados exclusivamente para rescatar objetos pequeños. Si en un mosaico se detecta un objeto cuya área calculada supera el 10% del área total de la imagen completa, se suprime, delegando su detección a la pasada de imagen global donde se tiene el contexto semántico completo.
  
  *Unificación global:* Las cajas supervivientes se proyectan al sistema de coordenadas de la imagen completa sumando el desplazamiento del cuadrante $(x + x_0, y + y_0)$. Finalmente, concatenamos las predicciones de la imagen global con las de los 4 mosaicos y ejecutamos un **NMS por clase batched** (`torchvision.ops.batched_nms`) con $\tau_{\text{NMS}} = 0,30$. Las detecciones de mosaicos y de escala global se fusionan armónicamente eliminando duplicados."

---

### Bloque E: Representación de Escena y Desacoplamiento del Razonamiento VQA

#### Pregunta E.1: "¿Cuál es la estructura formal del esquema `SceneJSON` y por qué es obligatorio utilizar compresión RLE en orden Fortran (column-major)?"
- **Respuesta Técnica Fundamentada:**  
  "El objeto `SceneJSON` responde a la especificación formal validada contra `scene_schema.json` mediante `jsonschema.Draft7Validator`. Posee tres componentes jerárquicos:
  1. `image`: Metadatos contextuales (`image_id`, dimensiones de imagen $W, H$).
  2. `objects`: Lista de instancias detectadas, donde cada entrada contiene:
     - `object_id`: Entero secuencial unívoco.
     - `category`: Nombre de la clase validada dentro de las 120 categorías.
     - `confidence`: Probabilidad empírica calibrada $[0, 1]$.
     - `bbox`: Coordenadas normalizadas $[x_{\min}, y_{\min}, w, h]$ en $[0, 1]$.
     - `centroid_3x3`: Categoría discreta de posición en la grilla topológica.
     - `relative_size`: Categoría ordinal de escala (`small`, `medium`, `large`).
     - `dominant_color`: Etiqueta cromática proyectada sobre paleta de 11 colores.
     - `segmentation`: Diccionario con la máscara codificada en RLE (`counts` y `size`).
  3. `relations`: Lista de tripletas relacionales $\langle \text{obj}_i, \text{predicado}, \text{obj}_j \rangle$.
  
  *Justificación del orden Fortran (`order="F"`):*  
  En Python/NumPy, los arreglos se almacenan por defecto en memoria siguiendo el orden de filas o Row-Major (orden 'C'). Sin embargo, las especificaciones canónicas de evaluación de segmentación de COCO y LVIS (implementadas en `pycocotools.mask.encode`) exigen estrictamente el almacenamiento en **orden de columnas o Column-Major (orden Fortran 'F')**.  
  Si se serializa una máscara binaria en orden 'C', el algoritmo RLE agrupa las secuencias de ceros y unos leyendo horizontalmente; al decodificarlo en `pycocotools`, la librería lo interpreta verticalmente, lo que produce una **transposición geométrica de la máscara** ($x \leftrightarrow y$). Esto destruiría por completo la métrica de IoU frente al ground truth. Garantizar `np.asfortranarray(mask.astype(np.uint8))` en `mask_to_rle` fue mandatorio para alcanzar 100% de consistencia de schema."

#### Pregunta E.2: "¿Cómo opera la cuantización espacial del centroide en la grilla 3x3 y cómo se calculan las relaciones espaciales entre objetos?"
- **Respuesta Técnica Fundamentada:**  
  "La discretización del plano continuo en la grilla de $3 \times 3$ celdas se ejecuta sobre el centroide de masa $(\bar{x}, \bar{y})$ calculado a partir de los momentos espaciales de la máscara binaria $M(x, y)$:
  $$\bar{x} = \frac{\sum_{x, y} x \cdot M(x, y)}{\sum_{x, y} M(x, y)}, \qquad \bar{y} = \frac{\sum_{x, y} y \cdot M(x, y)}{\sum_{x, y} M(x, y)}$$
  Las coordenadas normalizadas se mapean a los 9 sectores dividiendo el espacio en tercios ortogonales con clamping estricto en $[0, 1]$:
  $$\text{Sector Horizontal} = \begin{cases} \text{left} & \bar{x} < 1/3 \\ \text{center} & 1/3 \le \bar{x} < 2/3 \\ \text{right} & \bar{x} \ge 2/3 \end{cases}, \qquad \text{Sector Vertical} = \begin{cases} \text{top} & \bar{y} < 1/3 \\ \text{middle} & 1/3 \le \bar{y} < 2/3 \\ \text{bottom} & \bar{y} \ge 2/3 \end{cases}$$
  La concatenación genera las 9 regiones canónicas (`top_left`, `top_center`, `top_right`, `middle_left`, `center`, `middle_right`, `bottom_left`, `bottom_center`, `bottom_right`).  
  
  Para las **relaciones espaciales**, evaluamos pares de objetos $(A, B)$ mediante predicados topológicos deterministas utilizando un margen de holgura $\delta = 0,05$ ($5\%$):
  - `left_of`: $x_{\max}(A) < x_{\min}(B) + \delta$ y solapamiento vertical $\text{IoU}_y(A, B) > 0,10$.
  - `right_of`: $x_{\min}(A) > x_{\max}(B) - \delta$ y solapamiento vertical $\text{IoU}_y(A, B) > 0,10$.
  - `above`: $y_{\max}(A) < y_{\min}(B) + \delta$ y solapamiento horizontal $\text{IoU}_x(A, B) > 0,10$.
  - `below`: $y_{\min}(A) > y_{\max}(B) - \delta$ y solapamiento horizontal $\text{IoU}_x(A, B) > 0,10$.
  - `overlaps`: Intersección de cajas $\frac{\text{Área}(A \cap B)}{\min(\text{Área}(A), \text{Área}(B))} \ge 0,05$.  
  Esto transforma relaciones geométricas continuas en aserciones proposicionales discretas indiscutibles."

#### Pregunta E.3: "¿Cómo funciona el módulo VQA neuro-simbólico desacoplado en tres capas y cómo previene las alucinaciones lingüísticas?"
- **Respuesta Técnica Fundamentada:**  
  "El módulo VQA opera bajo una estricta arquitectura desacoplada de tres capas:
  1. **Capa 1: Intérprete de Lenguaje Natural (`Qwen2.5-1.5B-Instruct`):**  
     El modelo de lenguaje pequeño solo recibe la pregunta en lenguaje natural. Su única función es actuar como un parser semántico guiado por un system prompt altamente restrictivo (`INTERP_SYSTEM_V3`), emitiendo un objeto JSON formal estructurado (`QUERY_SPEC`) con los campos: `intent` (`existence`, `count`, `position`, `size`, `relation`, `description`), `target_class`, `ref_class` y `spatial_predicate`. **El LLM no tiene acceso a la imagen ni a los datos de la escena**, anulando cualquier posibilidad de que invente respuestas fácticas.
  2. **Capa 2: Motor Determinista Factual (`QAEngine`):**  
     Recibe el `QUERY_SPEC` y ejecuta una consulta lógica sobre el `SceneJSON` de la imagen mediante código Python puro.
     - Si la intención es `count`, cuenta las instancias filtradas por la categoría requerida.
     - Si es `existence`, verifica si el conteo es $>0$.
     - Si es `position`, extrae el `centroid_3x3` del objeto correspondiente.
     - La respuesta es matemáticamente infalible y genera una traza de auditoría con la lista de `evidence: [object_ids]`.
  3. **Capa 3: Verbalizador y Filtro de Fidelidad (`is_faithful`):**  
     Para responder en lenguaje natural fluido, un generador produce la oración final. Sin embargo, un filtro algorítmico determinista (`is_faithful`) analiza por expresiones regulares si los números, categorías o cuadrantes citados en el texto del LLM coinciden estrictamente con los devueltos por el motor determinista. Si el LLM comete una inconsistencia, el sistema aborta automáticamente y emite la respuesta generada por una plantilla fija predefinida. Esta arquitectura garantizó un **100% de evidencia auditada** y elevó la exactitud de VQA a **0,7895**."

#### Pregunta E.4: "¿En qué consiste el bucle de autocorrección con reintento (`interpret_with_retry`) y la política de ausencia derivada (`not_detected`)?"
- **Respuesta Técnica Fundamentada:**  
  "Representan las dos mejoras clave introducidas en la versión V3 para resolver fallas sistémicas observadas en la línea base:
  1. **Autocorrección con Reintento (`interpret_with_retry`):**  
     En V1, si el LLM emitía un JSON mal formateado o nombraba una categoría inexistente en el vocabulario oficial de 120 clases (ej. interpretaba 'luminaria' en lugar de 'streetlight'), la consulta colapsaba en error. En V3 implementamos un mecanismo iterativo: si el validador sintáctico falla, se extrae el término problemático, se computa la **similitud coseno entre su embedding textual y los embeddings de las 120 clases de OWLv2**, y se le suministran al LLM los 5 candidatos válidos más cercanos en un segundo prompt de rescate. Gracias a esto, la tasa de interpretación de preguntas de existencia subió del 80% al 90%, y las descripciones alcanzaron el **100% de éxito**.
  2. **Política de Ausencia Derivada (`not_detected`):**  
     En V1, cuando el usuario preguntaba por un objeto ausente de la imagen (ej. '¿Hay un bote?'), el motor determinista devolvía `insufficient_information` porque la clase no estaba en la imagen ni en las negativas verificadas de LVIS. En una evaluación de QA humana, esto se computaba como error. En V3 establecimos formalmente que si no hay detecciones en el SceneJSON para esa categoría en preguntas de existencia, conteo o relación, el motor deriva una respuesta explícita: responde `'no'` o `'0'`, asignando una confianza derivada de $0,5$ y dejando un registro de auditoría en los metadatos indicando que la ausencia no está formalmente certificada por ground truth. Esto desbloqueó de inmediato un incremento masivo de exactitud en el benchmark."

---

### Bloque F: Análisis de Errores y Casos Borde Cualitativos

#### Pregunta F.1: "¿Cuáles fueron las principales fuentes de Falsos Positivos observadas en el notebook y qué casos cualitativos concretos analizaron?"
- **Respuesta Técnica Fundamentada:**  
  "En el conjunto de desarrollo se detectaron 587 Falsos Positivos en la línea base, reducidos a 425 en V3. El análisis detallado de la Sección 12.6 reveló que **581 de esos 587 casos corresponden a categorías positivas presentes en la escena sin emparejar con el GT**, mientras que solo 6 casos correspondieron a clases formalmente negativas de LVIS.  
  Las principales causas sistemáticas fueron:
  1. *Confusión semántica y co-ocurrencia urbana:* `traffic light` acumuló 26 FP y `streetlight` 21 FP. Ambos objetos son luminarias metálicas situadas en la parte superior de postes urbanos. En tomas lejanas, el detector activó ambas consultas con scores similares para la misma entidad física.
  2. *Ambigüedad de formas geométricas repetitivas:* `ski` registró 19 FP, provocados por pasamanos, barandas de balcones y rejas metálicas horizontales que el modelo clasificó como esquíes.
  3. *Ruido de fondo en micro-objetos:* Clases como `sock` (16 FP), `knob` (16 FP) y `wall socket` (13 FP) proliferaron en paredes con interruptores y texturas complejas.
  
  *Caso cualitativo destacado:* En la imagen `tpi_0085.jpg` (analizada en las Figuras 5 y 8), el detector demostró 'ceguera de materialidad': identificó un perro con confianza 0,1945 sobre lo que en realidad era una **estatua de piedra ornamental**, y predijo un elefante con confianza 0,4086 sobre un **bajo relieve tallado en una pared de roca**. OWLv2 detecta patrones texturales locales alineados al concepto semántico pero no modela si la entidad tiene vida orgánica o si es una escultura inanimada."

#### Pregunta F.2: "¿Cuáles fueron los patrones dominantes de Falsos Negativos y por qué ciertas clases tuvieron un recall extremadamente bajo?"
- **Respuesta Técnica Fundamentada:**  
  "El análisis de los 655 Falsos Negativos documentó una correlación directa entre el tamaño relativo del objeto y la tasa de omisión:
  - Objetos grandes (`large`): Recall = **0,852** (85,2%).
  - Objetos medianos (`medium`): Recall = **0,765** (76,5%).
  - Objetos pequeños (`small`): Recall = **0,575** (57,5%).
  
  Al analizar las categorías con peor recall (con $\ge 5$ instancias), encontramos tres patrones físicos:
  1. *Estructuras filiformes delgadas:* `strap` (correas de bolsos y mochilas) tuvo un recall de apenas **0,174** (17,4% en 23 instancias). Las correas carecen de un parche interior homogéneo de $16 \times 16$ px; su trazo es absorbido por la convolución del parche contra el fondo.
  2. *Oclusión densa y apilamiento:* `book` registró un recall de **0,196** (19,6% en 46 instancias). En bibliotecas y estanterías hacinadas, los libros no aparecen como rectángulos frontales sino como lomos estrechos contiguos; el detector fusiona los libros adyacentes o los descarta por NMS.
  3. *Escala microscópica:* `doorknob` (pomo de puerta) obtuvo recall de **0,200** y `earring` (aro/pendiente) **0,333**, ocupando menos del 0,1% del área de la imagen."

#### Pregunta F.3: "¿Qué dificultades se presentaron en las preguntas espaciales y cómo afectó la ambigüedad lingüística del español?"
- **Respuesta Técnica Fundamentada:**  
  "El módulo VQA en modo LLM enfrentó dos obstáculos en consultas espaciales:
  1. *Ambigüedad deíctica (punto de vista del observador vs objeto):* Consultas como '¿Está la taza a la izquierda del plato?' dependen de si se asume la perspectiva de la cámara o la orientación intrínseca de una persona en la mesa. Nuestro motor determinista resuelve esto formalmente estableciendo como convención el **sistema de coordenadas de la pantalla 2D** ($x=0$ a la izquierda, $x=1$ a la derecha).
  2. *Traducción semántica del español:* El modelo `Qwen2.5-1.5B` procesa preguntas en español, pero el vocabulario de LVIS y los predicados del `QUERY_SPEC` están estrictamente en inglés. En ocasiones el LLM tradujo 'al lado de' como predicados simétricos no contemplados. En V3 incorporamos en el prompt del sistema la tabla canónica de traducción de predicados espaciales, eliminando el 100% de los errores de sintaxis en consultas relacionales."

---

### Bloque G: Fundamentos Matemáticos y Teóricos (`IA-Resumen-Completo.pdf`)

#### Pregunta G.1: "Demuestre matemáticamente por qué el F1-Score emplea la media armónica y demuestre su ventaja frente a la media aritmética o geométrica en detección de objetos."
- **Respuesta Técnica Fundamentada:**  
  "Sean Precisión $P = \frac{TP}{TP + FP}$ y Recall $R = \frac{TP}{TP + FN}$.  
  La media armónica de dos números reales positivos $P$ y $R$ se define formalmente como el inverso de la media aritmética de sus inversos:
  $$F_1 = \mathcal{H}(P, R) = \frac{2}{\frac{1}{P} + \frac{1}{R}} = \frac{2}{\frac{R + P}{P \cdot R}} = 2 \cdot \frac{P \cdot R}{P + R}$$
  Sustituyendo $P$ y $R$ por sus definiciones algebraicas:
  $$F_1 = \frac{2 \cdot \left(\frac{TP}{TP + FP}\right) \cdot \left(\frac{TP}{TP + FN}\right)}{\frac{TP}{TP + FP} + \frac{TP}{TP + FN}} = \frac{2 \cdot \frac{TP^2}{(TP + FP)(TP + FN)}}{\frac{TP(TP + FN) + TP(TP + FP)}{(TP + FP)(TP + FN)}} = \frac{2 \cdot TP^2}{TP(2 \cdot TP + FP + FN)} = \frac{2 \cdot TP}{2 \cdot TP + FP + FN}$$
  
  *Demostración de la ventaja frente a la media aritmética:*  
  Supóngase un detector ingenuo patológico que, para maximizar el recall, emite miles de cajas por imagen prediciendo todas las clases posibles en todo píxel. Dicho modelo obtendrá un recall perfecto $R = 1,0$, pero su precisión colapsará debido a una marea de falsos positivos, por ejemplo $P = 0,05$.
  - Si calculáramos la **media aritmética**:
    $$\mathcal{A}(P, R) = \frac{P + R}{2} = \frac{0,05 + 1,0}{2} = 0,525$$
    El modelo obtendría un 52,5% de rendimiento, superando falsamente el umbral de aprobación de 0,50 de la cátedra con un sistema totalmente inútil en producción.
  - Al calcular la **media armónica**:
    $$F_1 = 2 \cdot \frac{0,05 \cdot 1,0}{0,05 + 1,0} = \frac{0,10}{1,05} \approx 0,0952 \quad (9,5\%)$$
    
  Matemáticamente, la media armónica satisface la propiedad de dominancia asintótica: $\lim_{P \to 0} \mathcal{H}(P, R) = 0$ para cualquier $R > 0$. La media armónica se encuentra fuertemente dominada por el menor de los dos términos, forzando al detector a optimizar simultáneamente la exactitud y la exhaustividad."

#### Pregunta G.2: "¿Cómo se formulan formalmente las curvas Precisión-Recall y ROC/AUC y cómo se interpreta el espacio de operación de un clasificador?"
- **Respuesta Técnica Fundamentada:**  
  "En un detector probabilístico, cada predicción tiene asignado un score de confianza $s \in [0, 1]$. Al variar un umbral de decisión continuo $\tau \in [0, 1]$, se obtienen distintos puntos operativos:
  1. **Curva ROC (Receiver Operating Characteristic):**  
     Grafica la Tasa de Verdaderos Positivos ($\text{TPR} = \text{Recall} = \frac{TP}{TP+FN}$) en el eje de ordenadas frente a la Tasa de Falsos Positivos ($\text{FPR} = \frac{FP}{FP+TN} = 1 - \text{Especificidad}$) en el eje de abscisas a medida que $\tau$ desciende de 1 a 0.  
     El **Área Bajo la Curva ROC (AUC-ROC)** se formula integralmente como:
     $$\text{AUC} = \int_{0}^1 \text{TPR}(\tau) \, d(\text{FPR}(\tau)) = P(s(x^+) > s(x^-))$$
     Representa la probabilidad estadística de que una instancia positiva elegida al azar reciba un score de confianza mayor que una instancia negativa elegida al azar.
  2. **Curva Precisión-Recall (PR):**  
     Grafica la Precisión $P(\tau)$ frente al Recall $R(\tau)$. En detección de objetos y datasets fuertemente desbalanceados (donde la clase 'fondo' supera en millones de veces a los objetos, haciendo que los Verdaderos Negativos $TN$ sean incalculables e irrelevantes), la curva ROC resulta engañosa porque un número astronómico de $TN$ mantiene el $\text{FPR}$ artificialmente cerca de cero.  
     La curva PR es estrictamente informativa: para calcular el **Average Precision (AP)** se utiliza la curva interpolada monótonamente decreciente:
     $$\rho_{\text{interp}}(r) = \max_{\tilde{r} \ge r} P(\tilde{r}), \qquad \text{AP} = \int_0^1 \rho_{\text{interp}}(r) \, dr$$
     El punto de tangencia con las curvas de nivel hiperbólicas de $F_1$ constante ($P \cdot R / (P+R) = k$) define el **umbral óptimo de operación**, el cual determinamos empíricamente en $\tau = 0,17$ para V2 y $\tau = 0,23$ para V3."

#### Pregunta G.3: "Compare matemáticamente la función de pérdida Entropía Cruzada Categórica con la Focal Loss y explique su rol frente al desbalance extremo en detección."
- **Respuesta Técnica Fundamentada:**  
  "En clasificación binaria multietiqueta (o detección densa), la Entropía Cruzada convencional sobre una probabilidad estimada $p_t \in [0, 1]$ se define como:
  $$\mathcal{L}_{\text{CE}}(p_t) = -\log(p_t), \qquad \text{donde } p_t = \begin{cases} p & \text{si } y = 1 \\ 1 - p & \text{si } y = 0 \end{cases}$$
  En una imagen típica, se evalúan miles de posiciones espaciales de las cuales más del 99% corresponden a 'fondo fácil' (*easy negatives*), para las cuales $p_t \ge 0,9$. Aunque la pérdida de cada ejemplo fácil sea pequeña ($-\log(0,9) \approx 0,10$), la suma acumulada de miles de ejemplos fáciles domina totalmente el gradiente durante el backpropagation, ahogando la señal de las pocas instancias positivas reales.
  
  Para neutralizar este fenómeno, Lin et al. (ICCV 2017) introdujeron la **Focal Loss**, incorporando un factor modulador dinámico $(1 - p_t)^\gamma$ con parámetro de enfoque $\gamma \ge 0$ y balanceador $\alpha_t$:
  $$\mathcal{L}_{\text{FL}}(p_t) = -\alpha_t (1 - p_t)^\gamma \log(p_t)$$
  - Si un ejemplo es un negativo fácil ($p_t \to 1$), el factor modulador $(1 - p_t)^\gamma \to 0$, suprimiendo su contribución al gradiente a una tasa exponencial. Por ejemplo, con $\gamma = 2$, un negativo con $p_t = 0,99$ reduce su pérdida en un factor de $(1 - 0,99)^2 = 0,0001$ ($10.000$ veces menos peso).
  - Si una instancia es difícil o mal clasificada ($p_t \le 0,5$), $(1 - p_t)^\gamma \approx 1$, preservando la magnitud total del gradiente.
  
  Modelos fundacionales como OWLv2 y SAM2 incorporan variantes de Focal Loss y BCE balanceada durante su preentrenamiento para estabilizar el aprendizaje de regiones visuales dispersas."

#### Pregunta G.4: "Explique el funcionamiento físico y matemático del optimizador Adam (momentos de primer y segundo orden con corrección de sesgo) frente a SGD con Momentum."
- **Respuesta Técnica Fundamentada:**  
  "El Descenso de Gradiente Estocástico con Momentum emula una partícula con masa moviéndose sobre la superficie de pérdida, utilizando un acumulador de velocidad $v_t$ para amortiguar oscilaciones en direcciones de alta curvatura:
  $$v_t = \gamma v_{t-1} + \alpha g_t, \qquad \theta_{t+1} = \theta_t - v_t$$
  Sin embargo, SGD aplica la misma tasa de aprendizaje escalar $\alpha$ a todos los parámetros de la red, independientemente de la frecuencia de activación de cada peso.
  
  El algoritmo **Adam (Adaptive Moment Estimation)**, ampliamente documentado en el capítulo de optimización de `IA-Resumen-Completo.pdf`, mantiene estimaciones exponenciales móviles del vector gradiente (primer momento, media) y del gradiente al cuadrado (segundo momento no centrado, varianza no centrada):
  $$m_t = \beta_1 m_{t-1} + (1 - \beta_1) g_t \quad (\text{Dirección de movimiento con inercia})$$
  $$v_t = \beta_2 v_{t-1} + (1 - \beta_2) g_t^2 \quad (\text{Escala adaptativa de magnitud por parámetro})$$
  donde típicamente $\beta_1 = 0,9$ y $\beta_2 = 0,999$.
  
  *Corrección de sesgo (Bias Correction):*  
  Dado que los acumuladores se inicializan en cero ($m_0 = 0, v_0 = 0$), en los primeros pasos temporales $t$ las medias móviles se encuentran severamente sesgadas hacia el origen. Adam corrige este artefacto dividiendo por $(1 - \beta^t)$:
  $$\hat{m}_t = \frac{m_t}{1 - \beta_1^t}, \qquad \hat{v}_t = \frac{v_t}{1 - \beta_2^t}$$
  A medida que $t \to \infty$, $\beta^t \to 0$ y el factor de corrección tiende suavemente a 1.
  
  *Regla de actualización final:*
  $$\theta_{t+1} = \theta_t - \frac{\alpha}{\sqrt{\hat{v}_t} + \epsilon} \hat{m}_t$$
  Físicamente, cada parámetro recibe un paso de aprendizaje adaptativo individual: los pesos con gradientes infrecuentes o pequeños reciben pasos proporcionalmente mayores, mientras que los pesos con oscilaciones violentas se amortiguan, permitiendo una convergencia rápida y estable en modelos complejos basados en Transformers."

#### Pregunta G.5: "Explique el mecanismo analítico de regularización por Weight Decay (L2) frente a Lasso (L1) y su impacto en las fronteras de decisión."
- **Respuesta Técnica Fundamentada:**  
  "En aprendizaje profundo, el sobreajuste ocurre cuando una red con millones de grados de libertad ajusta pesos desmesuradamente grandes para interpolar el ruido del dataset de entrenamiento, provocando que la función aprendida presente derivadas espaciales extremas (fronteras de decisión convolutas y frágiles).
  
  1. **Regularización $L_2$ (Weight Decay / Ridge):**  
     Añade a la función de pérdida empírica $\mathcal{L}_0$ una penalización cuadrática sobre la norma euclidiana del tensor de pesos:
     $$\mathcal{L}_{\text{total}} = \mathcal{L}_0(\theta) + \frac{\lambda}{2} \|\theta\|_2^2 = \mathcal{L}_0(\theta) + \frac{\lambda}{2} \sum_i w_i^2$$
     Al derivar respecto a un peso $w_i$:
     $$\frac{\partial \mathcal{L}_{\text{total}}}{\partial w_i} = \frac{\partial \mathcal{L}_0}{\partial w_i} + \lambda w_i$$
     La actualización por gradiente queda:
     $$w_{t+1} = w_t - \alpha \left(\frac{\partial \mathcal{L}_0}{\partial w_t} + \lambda w_t\right) = w_t (1 - \alpha \lambda) - \alpha \frac{\partial \mathcal{L}_0}{\partial w_t}$$
     El factor $(1 - \alpha \lambda) < 1$ encoge multiplicativamente el peso en cada iteración antes de aplicar el gradiente. Esto acota la **constante de Lipschitz** de la red neuronal, forzando funciones continuas y suaves que generalizan con robustez ante perturbaciones de entrada.
  
  2. **Regularización $L_1$ (Lasso):**  
     Añade la norma del valor absoluto:
     $$\mathcal{L}_{\text{total}} = \mathcal{L}_0(\theta) + \lambda \sum_i |w_i|, \qquad \frac{\partial \mathcal{L}_{\text{total}}}{\partial w_i} = \frac{\partial \mathcal{L}_0}{\partial w_i} + \lambda \cdot \text{sign}(w_i)$$
     A diferencia de $L_2$ (cuya fuerza de contracción disminuye cuando el peso se acerca a cero), $L_1$ ejerce una fuerza de arrastre constante $\lambda$ sin importar cuán pequeño sea el peso. Esto empuja numéricamente coeficientes irrelevantes exactamente a cero, induciendo **esparcidad (*sparsity*)** y actuando como un mecanismo implícito de selección de características."

#### Pregunta G.6: "Explique la operación de Convolución 2D discreta, el concepto de Campo Receptivo (Receptive Field) y cómo se estructuran las jerarquías visuales en visión computacional."
- **Respuesta Técnica Fundamentada:**  
  "En visión por computadora y redes neuronales convolucionales (CNNs), la convolución 2D discreta aplica un kernel o filtro parametrizado $W \in \mathbb{R}^{m \times n}$ sobre un mapa de características de entrada $M$:
  $$\text{Conv}(W, M)_{ij} = (W * M)_{ij} = \sum_{u=1}^m \sum_{v=1}^n W_{uv} \cdot M_{i+u-1, j+v-1}$$
  Esta operación introduce dos propiedades inductivas fundamentales: **compartición de pesos** (*weight sharing*) e **invarianza local por traslación**.  
  
  *Campo Receptivo (Receptive Field):*  
  El campo receptivo de una neurona en la capa $l$ es la región espacial de la imagen de entrada original que influye en su activación. Crece inductivamente capa tras capa en función del tamaño del kernel $K_l$ y el stride acumulado:
  $$RF_l = RF_{l-1} + (K_l - 1) \cdot \prod_{i=1}^{l-1} S_i$$
  - **Jerarquía Biológica (Hubel y Wiesel / Neocognitron de Fukushima):** En las capas iniciales, los campos receptivos son diminutos (ej. $3 \times 3$ o $5 \times 5$ px), emulando las *células simples* de la corteza visual primaria que detectan gradientes de borde, líneas orientadas y texturas elementales.
  - A medida que se profundiza en la red mediante convoluciones sucesivas y submuestreo, el campo receptivo se expande hasta abarcar la escena completa, emulando las *células complejas* que reconocen partes de objetos y conceptos semánticos abstractos.
  - *Contraste con Vision Transformers (OWLv2):* A diferencia de las CNNs donde el campo receptivo crece gradualmente, el mecanismo de auto-atención multi-cabeza (MHSA) de ViT conecta todos los parches espaciales entre sí desde la primera capa, otorgando un **campo receptivo global inmediato**, pero exigiendo preentrenamiento masivo al carecer del sesgo inductivo de localidad espacial."

#### Pregunta G.7: "Compare los distintos tipos de Pooling (Max, Average y Global Pooling) y explique su rol en la reducción dimensional y la invarianza espacial."
- **Respuesta Técnica Fundamentada:**  
  "El submuestreo o *pooling* reduce progresivamente la resolución espacial de los mapas de características intermedias $(H \times W \to \frac{H}{s} \times \frac{W}{s})$, reduciendo drásticamente la carga computacional y el número de parámetros de las capas densas subsecuentes, mitigando el sobreajuste.
  
  1. **Max Pooling:**  
     Extrae el valor máximo dentro de una ventana local $p \times p$:
     $$y_{ij} = \max_{u, v \in [1, p]} x_{i \cdot s + u, j \cdot s + v}$$
     *Propiedad:* Preserva las activaciones de mayor intensidad (características más prominentes como bordes nítidos, esquinas y contrastes fuertes). Aporta **invarianza local ante pequeñas traslaciones y deformaciones**: si un rasgo se desplaza uno o dos píxeles dentro de la ventana, la activación máxima de salida permanece inalterada.
  
  2. **Average Pooling:**  
     Calcula la media aritmética de los elementos de la ventana:
     $$y_{ij} = \frac{1}{p^2} \sum_{u=1}^p \sum_{v=1}^p x_{i \cdot s + u, j \cdot s + v}$$
     *Propiedad:* Suaviza la respuesta espacial reteniendo información estadística del contexto y texturas homogéneas, pero atenúa características de bordes abruptos.
  
  3. **Global Average / Max Pooling (GAP / GMP):**  
     Colapsa la totalidad de la dimensión espacial $H \times W$ a un único escalar por canal ($1 \times 1 \times C$):
     $$\text{GAP}_c = \frac{1}{H \cdot W} \sum_{i=1}^H \sum_{j=1}^W x_{ijc}$$
     Introducido en arquitecturas modernas (Network in Network, ResNet) para reemplazar las capas completamente conectadas (FC) finales, eliminando millones de parámetros y volviendo a la red totalmente independiente del tamaño de resolución de entrada."

#### Pregunta G.8: "¿Qué es el Problema de Desvanecimiento del Gradiente (Vanishing Gradient), por qué ocurre con funciones sigmoideas y cómo lo resuelven ReLU y las Conexiones Residuales (ResNet / Hiera en SAM2)?"
- **Respuesta Técnica Fundamentada:**  
  "Durante el entrenamiento mediante retropropagación (*backpropagation*), el gradiente de la función de pérdida $\mathcal{L}$ respecto a los pesos de una capa inicial $w_1$ se calcula aplicando recursivamente la regla de la cadena:
  $$\frac{\partial \mathcal{L}}{\partial w_1} = \frac{\partial \mathcal{L}}{\partial a_L} \cdot \prod_{l=2}^L \left( \frac{\partial a_l}{\partial z_l} \cdot \frac{\partial z_l}{\partial a_{l-1}} \right) \cdot \frac{\partial z_1}{\partial w_1}$$
  donde $\frac{\partial a_l}{\partial z_l} = \sigma'(z_l)$ es la derivada de la función de activación.
  
  *Causa del Desvanecimiento:*  
  En funciones saturantes clásicas como la sigmoide $\sigma(z) = \frac{1}{1 + e^{-z}}$, su derivada alcanza un valor máximo de apenas $\sigma'(0) = 0,25$ y decae asintóticamente a cero para $|z| > 4$. Al multiplicar decenas de términos acotados por $0,25$, el gradiente decrece exponencialmente ($0,25^L \to 0$), congelando el aprendizaje de las capas tempranas.
  
  *Soluciones Teóricas Canónicas:*
  1. **Funciones No Saturantes (ReLU / Leaky ReLU):**  
     $$\text{ReLU}(z) = \max(0, z), \qquad \text{ReLU}'(z) = \begin{cases} 1 & z > 0 \\ 0 & z \le 0 \end{cases}$$
     Para activaciones positivas, la derivada es exactamente $1$, permitiendo que el gradiente fluya sin atenuarse a través de capas profundas.
  2. **Conexiones Residuales (*Skip Connections* / He et al., ResNet 2015):**  
     En lugar de forzar a las capas intermedias a aprender un mapeo directo $H(x)$, un bloque residual aprende una función residual $F(x) = H(x) - x$, reformulando la salida como:
     $$y = F(x, \{W_i\}) + x$$
     Al calcular el gradiente respecto a la entrada:
     $$\frac{\partial \mathcal{L}}{\partial x} = \frac{\partial \mathcal{L}}{\partial y} \cdot \left( \frac{\partial F}{\partial x} + \mathbf{1} \right)$$
     El término aditivo $+1$ actúa como una **superautopista para el gradiente**: incluso si el gradiente a través de las capas parametrizadas $\frac{\partial F}{\partial x}$ tiende a cero, el gradiente directo $\frac{\partial \mathcal{L}}{\partial y} \cdot 1$ fluye intacto hacia las capas iniciales sin desvanecerse.  
     *Aplicación en el TPI:* La arquitectura *Hiera-Small* empleada en SAM2 (`sam2_hiera_small.pt`) es un Vision Transformer jerárquico que integra estos principios residuales multiescala, permitiendo entrenar decodificadores de máscaras ultraprofundos con alta fidelidad a nivel de píxel."

#### Pregunta G.9: "Compare rigurosamente el paradigma de detección YOLO (One-Stage) frente a los Vision Transformers Multimodales (OWLv2 Open-Vocabulary)."
- **Respuesta Técnica Fundamentada:**  
  "El desarrollo de detectores modernos de objetos presenta dos grandes filosofías de ingeniería:
  
  1. **Paradigma YOLO (You Only Look Once / Redmon et al., 2015):**  
     - *Mecánica:* Divide la imagen en una cuadrícula fija de $S \times S$ celdas. Si el centro de un objeto cae en una celda, esa celda es responsable de predecir $B$ bounding boxes, sus coordenadas $[x, y, w, h]$, un factor de objetidad (*objectness*) y las probabilidades condicionales de clase $P(C_i | \text{Obj})$ para un conjunto cerrado de $K$ clases predefinidas.
     - *Optimización:* Evalúa todo en una **única pasada hacia adelante** (*one-stage*), optimizando una función de pérdida multi-tarea combinada (error cuadrático en coordenadas + entropía cruzada en clases). Emplea Non-Maximum Suppression (NMS) para suprimir cajas duplicadas.
     - *Fortaleza / Limitación:* Extremadamente veloz (adecuado para tiempo real a 60+ FPS), pero restringido a un vocabulario estático cerrado y con dificultad histórica para detectar objetos pequeños hacinados en la misma celda de la grilla.
  
  2. **Paradigma Vision Transformer Multimodal Open-Vocabulary (OWLv2 / Minderer et al., 2022):**  
     - *Mecánica:* No posee una cabeza de clasificación fija ni predice sobre clases discretas cerradas. Descompone la imagen en parches espaciales proyectados como tokens visuales procesados por capas de auto-atención global (ViT-B/16).
     - *Alineación Multimodal:* Un codificador de texto procesa consultas arbitrarias en lenguaje natural (ej. *'a photo of a {category}'* para 120 clases). Las predicciones de caja y clase se obtienen calculando la similitud coseno escalada entre los embeddings visuales de parches y los embeddings textuales en un espacio latente conjunto preentrenado contrastivamente (estilo CLIP).
     - *Fortaleza / Limitación:* Vocabulario ilimitado y capacidad de transferencia de disparo cero (*zero-shot*), resolviendo problemas con cola larga (LVIS) sin requerir reentrenamiento supervisado, a costa de mayor latencia computacional (2,44s por imagen frente a los ~20ms de YOLO)."

#### Pregunta G.10: "Enmarque el sistema desarrollado dentro de la Teoría de Agentes Inteligentes (Russell & Norvig / Unidad 1): Describa el marco REAS/PEAS, caracterice las propiedades del entorno y justifique por qué es un Agente Reactivo Basado en Modelos."
- **Respuesta Técnica Fundamentada:**  
  "De acuerdo con los fundamentos canónicos de la Unidad 1 de la materia (`IA-Resumen-Completo.pdf` y Russell & Norvig):
  
  1. **Marco REAS (PEAS en inglés):**
     - **Rendimiento (Performance):** Métrica combinada de calidad oficial de la cátedra:
       $$\text{PipelineScore} = 0,40 \cdot F_{1,\text{box}} + 0,35 \cdot F_{1,\text{mask}} + 0,15 \cdot \text{Consistencia} + 0,10 \cdot \text{Exactitud}_{\text{QA}}$$
     - **Entorno (Environment):** Fotografías bidimensionales RGB del dataset de desarrollo y prueba en Kaggle con alta complejidad visual, oclusiones y anotación federada LVIS.
     - **Actuadores (Actuators):** Generación y serialización del archivo estructurado `SceneJSON` (con máscaras RLE y relaciones topológicas), exportación del `submission.csv` y emisión de respuestas textuales auditables.
     - **Sensores (Sensors):** Matriz de píxeles capturada del archivo de imagen (canales RGB) y el flujo de texto de las preguntas de usuario en lenguaje natural.
  
  2. **Propiedades del Entorno de Trabajo:**
     - **Parcialmente Observable:** El agente no posee información total del estado físico del mundo debido a oclusiones mutuas entre objetos, sombras, objetos fuera de encuadre y anotaciones federadas incompletas.
     - **Determinista en Razonamiento / Estocástico en Percepción:** La inferencia neuronal de punto flotante opera en modo determinista estricto fijando semillas (`seed = 42`, `temperature = 0.0`), y la ejecución simbólica de consultas sobre el grafo JSON es 100% determinista.
     - **Episódico:** Cada imagen constituye un episodio atómico e independiente. La percepción o respuesta en la imagen $t$ no afecta el estado interno ni condiciona la inferencia en la imagen $t+1$.
     - **Estático:** La escena visual no muta ni evoluciona en el tiempo mientras los algoritmos de detección, segmentación y VQA están deliberando.
     - **Híbrido Continuo/Discreto:** Continuo en la fase perceptiva (coordenadas numéricas de cajas flotantes en $[0, 1]$, probabilidades de confianza y tensores de píxeles) y discreto en la representación simbólica (grilla topológica $3 \times 3$, conteos enteros y clases semánticas).
  
  3. **Tipología de Agente: Agente Reactivo Basado en Modelos:**  
     Un *agente reactivo simple* con mapeo directo entrada $\to$ salida (como un VLM end-to-end opaco) colapsa ante oclusiones y falta de observabilidad. Nuestro sistema es formalmente un **Agente Basado en Modelos**:
     - Mantiene un **estado interno explícito del mundo físico**: el grafo estructurado `SceneJSON`.
     - Este estado interno modela 'cómo está el mundo ahora' (qué objetos existen, cuáles son sus contornos exactos, en qué región de la grilla 3x3 yacen y cómo se relacionan espacialmente).
     - Desacoplar la percepción continua de la actualización del modelo interno garantiza que el subsistema de razonamiento consulte hechos cristalizados, impidiendo alucinaciones y permitiendo auditar matemáticamente cada respuesta."

---

## 3. Preguntas Trampa ("Trap Questions"), Antipatrones de Defensa y Protocolos de Respuesta

Los profesores suelen formular preguntas con premisas falsas o provocaciones técnicas para evaluar si el grupo comprende verdaderamente los fundamentos o si memorizó respuestas sin criterio.

---

### Matriz de Preguntas Trampa

| # | Pregunta Trampa del Evaluador | Trampa Oculta / Premisa Falsa | Antipatrón: Lo que NUNCA se debe decir | Respuesta Ganadora (The Pivot Strategy) |
|---|---|---|---|---|
| **T.1** | *"¿Por qué no hicieron fine-tuning completo de OWLv2 y SAM2 sobre las 120 imágenes para mejorar la precisión?"* | El docente quiere inducir al error de sugerir entrenamiento supervisado sobre un dataset minúsculo. | *"No nos dio el tiempo"* o *"Kaggle no tenía suficiente GPU"*. | **Pivotar a Overfitting y Data Efficiency:** Explicar que 120 imágenes para 120 clases representan apenas 1 imagen por clase en promedio. Reentrenar 150M de parámetros provocaría sobreajuste catastrófico (*catastrophic forgetting*). El mérito residió en formular un pipeline de zero-shot inference fundacional sin tocar pesos. |
| **T.2** | *"Si su detector tiene 0,71 de precisión de cajas, ¿por qué no subieron el umbral de confianza a 0,80 para tener 0,95 de precisión?"* | Ignorar el compromiso precisión-recall y la media armónica. | *"Sí, podríamos haberlo subido para que no tenga falsos positivos"*. | **Pivotar a la Dinámica del F1:** Mostrar que elevar la confianza a 0,80 destruye el recall (cayendo de 0,63 a menos de 0,15), colapsando el F1 armónico a $<0,25$. El objetivo del TPI es optimizar el balance armónico evaluable. |
| **T.3** | *"En VQA, ¿por qué usan un LLM si el motor determinista es más exacto (0,78 vs 0,55)?"* | La premisa busca que descarten el módulo LLM del nivel de Promoción. | *"El LLM anda peor, lo pusimos porque lo pedía la consigna"*. | **Pivotar a la Separación Neuro-Simbólica:** Explicar que el LLM no es un motor de respuestas, sino una interfaz de lenguaje natural. Los humanos no preguntan en JSON formal; el LLM dota al sistema de flexibilidad conversacional, mientras que el motor determinista garantiza la veracidad factual. |
| **T.4** | *"¿Por qué no usaron una cuadrícula de 10x10 en lugar de 3x3 para la posición de los centroides?"* | Presión hacia hiper-resolución innecesaria que introduce fragilidad. | *"Podríamos haber hecho 10x10 para que sea más preciso"*. | **Pivotar a la Rúbrica y Robustez Semántica:** La rúbrica fija formalmente la grilla de 9 celdas (`top_left` a `bottom_right`). Además, una grilla de 10x10 volvería al sistema hipersensible al ruido del centroide en objetos en movimiento o bordes deformados. |
| **T.5** | *"¿Cómo saben que el pipeline no tiene fuga de datos (data leakage) del conjunto de test?"* | Cuestionar la integridad del score de 0,6800 en Kaggle. | *"El código lo corrió Kaggle directamente"*. | **Pivotar a la Arquitectura Ciegan:** El script de inferencia procesa el CSV de test de manera ciega: no lee ninguna etiqueta de ground truth (las cuales son privadas de la cátedra), y las máscaras y cajas se deducen puramente de los píxeles de las imágenes en tiempo de ejecución. |
| **T.6** | *"¿Por qué el F1 de máscaras (0,6351) es menor que el de cajas (0,6722)?"* | Intentar que admitan un error de segmentación. | *"SAM2 anduvo más o menos bien"*. | **Pivotar a la Propagación de Errores y Geometría:** El cálculo de IoU sobre máscaras binarias es geométricamente mucho más estricto que sobre cajas rectangulares envolventes. Cualquier divergencia a nivel de píxel en bordes delgados castiga la intersección, perdiéndose 61 TP de cajas al traducirlas a máscaras. |
| **T.7** | *"Si los mosaicos 2x2 mejoraron el resultado, ¿por qué no hicieron 4x4 u 8x8 con 16 recortes?"* | Empujar hacia una extrapolación absurda sin considerar latencia ni contexto. | *"Habría sido mejor pero no tuvimos tiempo de probarlo"*. | **Pivotar a Rendimiento Decreciente y Latencia:** 4x4 mosaicos implicaría 17 pasadas inferenciales por imagen ($\approx 12\text{ segundos}$ por imagen), incrementando masivamente los falsos positivos en objetos truncados y destruyendo el contexto global necesario para reconocer categorías complejas. |
| **T.8** | *"El LLM a veces no responde y dice 'unsupported', ¿eso no es una falla de su sistema?"* | Confundir abstención justificada con fallo de software. | *"Es una limitación del modelo chico Qwen"*. | **Pivotar a la Rúbrica de Promoción:** La consigna exige explícitamente responder `unsupported` o `insufficient_information` ante atributos inexistentes. Abstenerse de inventar respuestas no es una falla; es una garantía de seguridad contra alucinaciones. |

---

### Protocolo General para Desactivar Trampas (The Pivot Framework)

Cuando el tribunal plantee una objeción incisiva:
1. **Validar y reconocer la premisa:** *"Es una excelente observación, profesor..."* (Demuestra madurez, jamás ponerse a la defensiva).
2. **Identificar la restricción o fundamento teórico:** *"...sin embargo, en este dominio rige el principio de [desbalance de clases / compromiso sesgo-varianza / política LVIS / consigna de interpretabilidad]"*.
3. **Presentar la evidencia empírica cuantitativa:** *"Cuando ensayamos esa alternativa en el notebook [Citar Celda / Experimento], observamos que la métrica cayó en [X] puntos debido a [Falsos Positivos / Latencia / Fragmentación]"*.
4. **Conclusión firme:** *"Por lo tanto, la configuración adoptada representa el compromiso óptimo demostrable entre capacidad expresiva y rigor matemático."*

---

## 4. Hoja de Ruta Práctica para el Día de la Defensa (Checklist de Preparación)

### 4.1. Checklist Pre-Defensa (24 Horas Antes)
- [ ] **Notebook en Kaggle:** Versión pública y ejecutable de `tpi-ia-2026p-21.ipynb` con todas las celdas corridas y las salidas visualizadas (gráficos y tablas visibles sin necesidad de re-ejecución).
- [ ] **Submission Persistida:** Archivo `submission.csv` (80 filas válidas) verificado localmente con script de consistencia de columnas y valores.
- [ ] **Informe Técnico Impreso y Digital:** Tener a mano `informe_tecnico_tpi.pdf` para abrirlo de inmediato ante cualquier consulta de figuras o fórmulas.
- [ ] **Entorno de Demostración Local / Kaggle:** Sesión de Kaggle con GPU T4 pre-asignada por si la cátedra solicita inferencia en vivo sobre una imagen inédita.
- [ ] **Sincronización de Equipo:** Ensayo cronometrado de los 10 minutos con el software de presentación.

### 4.2. Protocolo de Ejecución Durante la Presentación
1. **Cronómetro a la vista:** Gabriel Ocampo inicia un cronómetro en el celular apoyado sobre la mesa al comenzar a hablar.
2. **Voz firme y contacto visual:** No leer diapositivas ni textos largos; utilizar las diapositivas como apoyo gráfico exclusivo (Figuras 1 a 11 del informe).
3. **Dominio transversal:** Aunque cada integrante tenga asignado un bloque, cualquiera debe estar preparado para responder repreguntas teóricas de la Sección 2.
4. **Espíritu de cuerpo:** Apoyar a los compañeros; si un integrante titubea en un número exacto, otro miembro puede intervenir constructivamente: *"Exactamente, alcanzamos 0,6722 en Box F1"*.

---
*Fin de la Guía Táctica Maestra para la Defensa Oral — Grupo 21 (UTN Primavera 2026)*
