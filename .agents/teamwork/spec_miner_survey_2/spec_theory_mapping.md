# Mapeo Integral de Especificaciones, Rúbrica Académica y Fundamentos Teóricos
**Trabajo Práctico Integrador — Primavera 2026: Comprensión Visual de Escenas**  
**Cátedra de Inteligencia Artificial — Universidad Tecnológica Nacional (UTN)**  
*Documento de Investigación y Minería de Especificaciones Técnicas y Teóricas*

---

## 1. Resumen Ejecutivo y Alcance del Relevamiento

El presente documento constituye el marco de referencia formal que articula:
1. Las directivas académicas, requerimientos técnicos y rúbrica de evaluación establecidos en `TPI Primavera 2026 - Comprensión visual de escenas.pdf`.
2. Las pautas de formato, diseño editorial y estructura tipográfica extraídas de `TPI_IA_2025-TEMPLATE.pdf`.
3. El sustento epistemológico y teórico de Deep Learning, Computer Vision y Machine Learning derivado de `IA-Resumen-Completo.pdf` y la literatura canónica de la disciplina.
4. El framework de justificación metodológica ("por qué hicimos lo que hicimos y por qué funciona") para defender cada decisión de diseño algorítmico implementada en `tpi-ia-2026p-21.ipynb`.

---

## 2. Requerimientos Académicos y Rúbrica de Evaluación (TPI Primavera 2026)

### 2.1. Definición del Problema y Progresión Conceptual
El objetivo del Trabajo Práctico Integrador es construir un sistema de **comprensión visual de escenas** capaz de transformar una imagen bidimensional en una representación estructurada auditable, describirla formalmente y responder preguntas deterministas y semánticas sobre su contenido.

La cátedra impone una progresión conceptual estricta de 5 estadios:
$$\text{Percepción} \longrightarrow \text{Segmentación} \longrightarrow \text{Representación} \longrightarrow \text{Razonamiento} \longrightarrow \text{Interacción}$$

- **Percepción:** Localización de objetos mediante detección *open-vocabulary* (OWLv2 / YOLO-World / Grounding DINO).
- **Segmentación:** Segmentación de instancias mediante *prompts* geométricos (bounding boxes) con SAM2 (Segment Anything Model 2).
- **Representación:** Construcción determinista de un grafo/objeto estructurado en formato JSON (`SceneJSON`), serializando propiedades geométricas, atributos de apariencia (color) y relaciones topológicas espaciales.
- **Razonamiento:** Motor de inferencia sobre el JSON predicho para resolver preguntas cerradas (conteo, existencia, posición, tamaño, relaciones espaciales).
- **Interacción:** Módulo de lenguaje natural mediante un LLM liviano ejecutable en Kaggle para interpretar consultas abiertas, traducir intenciones a consultas estructuradas intermedias y verbalizar descripciones factuales.

> **Antipatrón Prohibido por la Cátedra:**  
> Queda terminantemente prohibido resolver el trabajo enviando directamente la imagen a un modelo multimodal de visión-lenguaje (VLM de caja negra de propósito general como GPT-4V o Gemini). La representación intermedia (`SceneJSON`) es el núcleo del trabajo y debe ser observable, auditable, verificable y consultable de manera independiente.

---

### 2.2. Dataset y Política de Anotación LVIS (Evaluación Federada)
El dataset oficial está basado en un subconjunto de LVIS / COCO:
- **Conjunto de Desarrollo:** 120 imágenes anotadas con 120 categorías evaluables. Se utiliza para el Análisis Exploratorio de Datos (EDA), experimentación, calibración de umbrales y validación cruzada local.
  - De estas 120 imágenes, 20 poseen consignas fijas asociadas para el benchmark de preguntas (VQA) y descripción.
- **Conjunto de Test (Competencia):** 60 imágenes no anotadas públicamente para conformar el *Leaderboard* de Kaggle.
- **Entregable de Predicciones (`submission.csv`):** Exactamente 80 filas:
  - 60 filas para las imágenes del test de la competencia (solo percepción visual y estructura).
  - 20 filas para las imágenes de desarrollo del benchmark (incluyendo `questions` y `questions_llm`).

#### Mecánica de la Evaluación Federada LVIS
A diferencia de COCO clásico (donde todas las imágenes están exhaustivamente anotadas para las 80 clases), LVIS utiliza un vocabulario de gran tamaño bajo el supuesto de que **la ausencia de una anotación no implica la ausencia del objeto**. Se definen 4 estados mutuamente excluyentes por categoría e imagen:
1. **Categoría Positiva:** Presenta una o más instancias anotadas en el *Ground Truth*. Omitir un objeto de esta categoría computa como **Falso Negativo (FN)**.
2. **Categoría Verificada Ausente (`neg_category_ids`):** Un revisor humano inspeccionó la imagen y confirmó que la categoría no existe. Predecir un objeto de esta categoría computa formalmente como **Falso Positivo (FP)**.
3. **Categoría Positiva No Exhaustiva (`not_exhaustive_category_ids`):** La categoría está presente y tiene algunas anotaciones, pero existen instancias adicionales sin delimitar. Predecir una instancia no anotada se **ignora en el cálculo** (no se penaliza como FP).
4. **Categoría No Verificada:** No tiene instancias anotadas ni figura en la lista de negativas verificadas. Al no haber certeza sobre su presencia/ausencia, cualquier predicción de esta categoría se excluye del cómputo de falsos positivos.

$$\text{Recall} = \frac{TP}{\text{Instancias Anotadas Positivas}}$$
$$\text{Precisión} = \frac{TP}{TP + FP_{\text{verificados}}}$$

> **Requisito Metodológico:** Toda métrica de precisión debe informarse junto con su **cobertura de evaluación** (proporción de predicciones sujetas a verificación frente al total generado).

---

### 2.3. Rúbrica de Calificación y Criterios de Aprobación
Los criterios de evaluación son acumulativos. Cada nivel exige el cumplimiento total de los requisitos de los niveles precedentes.

| Nivel | Requisitos Técnicos Obligatorios | Umbrales Cuantitativos |
|---|---|---|
| **Condiciones de Validez (Obligatorias)** | - Notebook 100% reproducible en Kaggle con salidas persistidas.<br>- Cero fuga de datos (*data leakage*): inferencia ciega sin consultar anotaciones del dataset.<br>- Reporte técnico en Markdown consistente con la implementación.<br>- Defensa oral individual satisfactoria de todos los integrantes. | Fuga de datos o manipulación = Desaprobación directa. |
| **Aprobado** | - EDA riguroso que motive decisiones posteriores.<br>- Pipeline visual completa (Detección Open-Vocab + SAM2 + SceneJSON válido).<br>- Soporte determinista en `questions` para existencia y conteo.<br>- Trazabilidad básica de ejecución, tiempos y estados.<br>- Evaluación con métricas justificadas y análisis de casos correctos y fallidos. | **$F_1$ Detección $\ge 0,40$** (con $\text{IoU} \ge 0,50$ y política LVIS). |
| **Promoción** | - Todo lo de Aprobado.<br>- Atributos y relaciones espaciales útiles consultables en JSON.<br>- Inclusión válida de `questions_llm` con LLM liviano en Kaggle generando JSON intermedio.<br>- Resolución de preguntas de ubicación, comparación, atributos y relaciones.<br>- Manejo explícito de preguntas ambiguas, no soportadas o sin información suficiente.<br>- `PipelineTracer` integral para trazabilidad de parámetros, artefactos y propagación de errores.<br>- Mejora comprobada mediante experimentación controlada vs línea base. | **$F_1$ Detección $\ge 0,50$** (con $\text{IoU} \ge 0,50$ y política LVIS). |
| **Sobresaliente** | - Todo lo de Promoción.<br>- Extensión no trivial del sistema (ej. percepción multiescala guiada, ensamble híbrido o filtrado topológico avanzado).<br>- Hipótesis de diseño formalmente enunciada y contrastada empíricamente.<br>- Evaluación cuantitativa de la ganancia marginal obtenida.<br>- Análisis crítico de costo computacional vs latencia vs mejora métrica. | Superación estadísticamente significativa de la línea base con balance de recursos. |

#### Composición del `PipelineScore` en Leaderboard
$$\text{PipelineScore} = 0,40 \cdot F_{1,\text{cajas}} + 0,35 \cdot F_{1,\text{máscaras}} + 0,15 \cdot \text{Consistencia}_{\text{SceneJSON}} + 0,10 \cdot \text{Score}_{\text{QA}}$$

---

### 2.4. Estructura Mandatoria del Informe Técnico (6 Secciones)
El informe debe desarrollarse respetando rigurosamente las 6 secciones normativas y el diseño tipográfico de la plantilla institucional:
1. **Portada:** Datos institucionales (UTN - FRBA / FRC, Cátedra Inteligencia Artificial, Curso 5K3A), Título del Trabajo, Docentes a cargo, Grupo N°, Integrantes con nombre y legajo, Fecha de entrega.
2. **Análisis del Dataset (EDA):** Caracterización de la densidad de instancias, distribución semántica de clases (desbalance y cola larga), análisis geométrico de escala (small/medium/large), análisis de la política LVIS (negativos y no exhaustivos), y caracterización del benchmark de preguntas.
3. **Metodología:** Detalle paso a paso del pipeline de inferencia (`OpenVocabDetector` $\to$ `SAM2Segmenter` $\to$ `build_scene_json` $\to$ `PipelineTracer` $\to$ `QAEngine`), justificación técnica y teórica de cada decisión ("por qué se hizo y por qué funciona"), y detalle de las mejoras introducidas respecto a la línea base.
4. **Resultados:** Presentación tabular y gráfica de métricas de detección ($P, R, F_1$), segmentación (IoU, $F_1$ de máscaras), fidelidad del SceneJSON y rendimiento del módulo VQA por categoría de pregunta.
5. **Discusión y Análisis de Errores:** Examen cualitativo y cuantitativo de fallas: falsos positivos por ambigüedad semántica, falsos negativos en objetos pequeños/ocultos, propagación de errores entre detección y segmentación, y análisis de consultas ambiguas/no soportadas.
6. **Conclusiones y Trabajo Futuro:** Síntesis crítica de los hallazgos empíricos, lecciones aprendidas sobre arquitecturas neuro-simbólicas, trade-offs de ingeniería y líneas de investigación futura.

---

### 2.5. Lineamientos para la Defensa Oral
- Duración estricta: Máximo 10 minutos de presentación, seguidos de ronda de preguntas individuales por parte de los docentes evaluadores.
- Requisito de suficiencia: Cada integrante debe dominar la totalidad del sistema, responder con rigor matemático y conceptual, y ser capaz de justificar cualquier línea de código o decisión de hiperparámetros.
- Verificación en vivo: La cátedra se reserva el derecho de someter imágenes inéditas a la pipeline en vivo para verificar la independencia de las anotaciones y la reproducibilidad técnica.

---

## 3. Fundamentos Teóricos Detallados (`IA-Resumen-Completo.pdf` y Deep Learning)

### 3.1. Operaciones Convolucionales y Jerarquías Espaciales

#### Convolución Discreta 2D y Compartición de Pesos
La convolución en visión artificial representa una transformación espacial local donde un kernel o máscara $M \in \mathbb{R}^{m \times n}$ se desplaza sobre una región $W$ de la imagen de entrada:
$$\text{conv}(W, M) = \sum_{i=1}^m \sum_{j=1}^n W_{ij} \cdot M_{ij} + b$$

- **Compartición de parámetros (*weight sharing*):** A diferencia de una capa densamente conectada donde cada conexión tiene un peso único, el kernel convolucional reutiliza los mismos coeficientes en todas las posiciones espaciales de la imagen. Esto aporta:
  1. Reducción exponencial del número de parámetros libres, mitigando el sobreajuste.
  2. **Equivarianza a traslaciones:** Si un patrón visual se desplaza en la imagen de entrada, su mapa de activación resultante se desplaza en igual magnitud.
- **Inspiración Biológica y Arquitectura Jerárquica:** El resumen de la cátedra resalta el modelo biológico de Hubel & Wiesel (1960s) sobre la corteza visual primaria (V1) y el Neocognitron de Fukushima (1980):
  - **Células Simples (Capas S):** Tienen campos receptivos pequeños y sintonizados a orientaciones específicas; detectan bordes, gradientes de color y texturas primitivas mediante operaciones convolucionales locales.
  - **Células Complejas (Capas C):** Integran las respuestas de múltiples células simples adyacentes para lograr invariancia a pequeñas traslaciones y cambios de escala (precursor directo del *pooling*).
  - **Jerarquía profunda:** Las capas iniciales capturan micro-características locales; las capas intermedias componen motivos, esquinas y texturas complejas; las capas superiores abstraen representaciones semánticas globales de partes de objetos e instancias completas.

#### Parámetros de Diseño Espacial: Padding, Stride y Campo Receptivo
- **Padding:** Adición de valores (habitualmente ceros, *zero-padding*) en los márgenes de la matriz de entrada.
  - *Valid padding:* No añade píxeles; la dimensión espacial disminuye tras cada convolución ($O = I - K + 1$).
  - *Same padding:* Añade $\lfloor K/2 \rfloor$ píxeles por lado, preservando la dimensión espacial ($O = I$). Evita la pérdida prematura de información geométrica en los bordes de la imagen.
- **Stride (Paso):** Distancia de desplazamiento del kernel sobre la matriz de entrada. Un stride $S > 1$ reduce la resolución del mapa de características a una tasa de $1/S$, realizando un submuestreo espacial integrado.
- **Campo Receptivo (*Receptive Field - RF*):** La región del espacio de entrada original que incide sobre la activación de una neurona particular en una capa profunda. El RF crece linealmente con el tamaño de los kernels y multiplicativamente con el factor de stride acumulado:
$$RF_l = RF_{l-1} + (K_l - 1) \cdot \prod_{i=1}^{l-1} S_i$$
Para detectar objetos de gran tamaño o capturar el contexto semántico de una escena, la arquitectura debe garantizar un campo receptivo lo suficientemente amplio como para cubrir el objeto completo.

---

### 3.2. Funciones de Activación y sus Propiedades Matemáticas

#### Necesidad de la No Linealidad
Cualquier composición de transformaciones afines lineales es idénticamente reducible a una única transformación lineal:
$$W_2 \cdot (W_1 \cdot x + b_1) + b_2 = (W_2 W_1) \cdot x + (W_2 b_1 + b_2) = W' \cdot x + b'$$
Por ende, una red neuronal multicapa sin funciones de activación no lineales es matemáticamente incapaz de separar datos que no sean linealmente separables (ej. el problema de la XOR documentado en las páginas 39-41 del resumen).

| Función | Definición Matemática | Rango de Salida | Derivada | Propiedades y Justificación de Uso |
|---|---|---|---|---|
| **Sigmoide** | $\sigma(z) = \frac{1}{1 + e^{-z}}$ | $(0, 1)$ | $\sigma(z)(1 - \sigma(z))$ | Transforma valores reales en probabilidades continuas. Sufre del problema de **desvanecimiento de gradiente** (*vanishing gradient*) para $|z| > 4$, ya que $\sigma'(z) \le 0,25$. |
| **Tanh** | $\tanh(z) = \frac{e^z - e^{-z}}{e^z + e^{-z}}$ | $(-1, 1)$ | $1 - \tanh^2(z)$ | Centrada en cero, acelerando la convergencia frente a la sigmoide, pero aún saturable en valores extremos. |
| **ReLU** | $f(z) = \max(0, z)$ | $[0, +\infty)$ | $f'(z) = \begin{cases} 1 & z > 0 \\ 0 & z < 0 \end{cases}$ | Resuelve el desvanecimiento de gradiente en la región positiva; derivada unitaria constante; cómputo extremadamente eficiente; induce representaciones dispersas (*sparsity*). Riesgo de *Dying ReLU* si los gradientes llevan los pesos a la región $z < 0$. |
| **Leaky ReLU** | $f(z) = \max(\alpha z, z), \alpha \approx 0,01$ | $(-\infty, +\infty)$ | $f'(z) = \begin{cases} 1 & z > 0 \\ \alpha & z < 0 \end{cases}$ | Previene neuronas muertas manteniendo un gradiente residual pequeño en la región negativa. |
| **Softmax** | $\sigma(z)_i = \frac{e^{z_i}}{\sum_{j=1}^C e^{z_j}}$ | $(0, 1), \sum_i \sigma(z)_i = 1$ | $\frac{\partial \sigma_i}{\partial z_j} = \sigma_i (\delta_{ij} - \sigma_j)$ | Generalización multiclase que normaliza logits en una distribución de probabilidad categórica mutuamente excluyente. |

---

### 3.3. Mecanismos de Submuestreo: Pooling vs Global Average Pooling vs Flatten

- **Max Pooling:** Selecciona la activación máxima dentro de una ventana espacial local (típicamente $2 \times 2$ con stride 2).
  - *Función teórica:* Extrae la característica más prominente (ej. bordes o puntos angulosos) y confiere **invariancia local a traslaciones** y perturbaciones menores.
- **Average Pooling:** Calcula el promedio aritmético de las activaciones en la ventana. Preserva información contextual suave y fondos homogéneos, pero atenúa características de contraste extremo.
- **Flatten vs Global Average Pooling (GAP):**
  - *Flatten:* Aplana un tensor 3D de características de dimensiones $H \times W \times C$ en un vector unidimensional de longitud $H \cdot W \cdot C$. Al conectarse a una capa densa ($D$ neuronas), genera $(H \cdot W \cdot C) \times D$ parámetros. Esto produce una explosión de parámetros, vulnerabilidad severa al sobreajuste y la destrucción abrupta de la coherencia espacial.
  - *Global Average Pooling (GAP):* Colapsa cada mapa de características espacial $H \times W$ calculando la media de sus activaciones, produciendo un vector de longitud $C$. Posee **cero parámetros entrenables**, actúa como un regularizador estructural forzando a que cada canal se especialice en un concepto semántico global, y desacopla la arquitectura de un tamaño de imagen fijo.

---

### 3.4. Funciones de Pérdida (Loss Functions) y Optimización

#### Entropía Cruzada Categórica (CCE) vs Sparse CCE
Para una tarea de clasificación multiclase sobre $C$ categorías:
$$\mathcal{L}_{\text{CCE}} = - \sum_{c=1}^C y_c \log(\hat{y}_c)$$
Donde $y$ es el vector objetivo codificado en *one-hot* y $\hat{y}$ son las probabilidades predichas por Softmax. Minimizar la entropía cruzada equivale a minimizar la **divergencia de Kullback-Leibler (KL)** entre la distribución real y la estimada por la red:
$$D_{\text{KL}}(P \parallel Q) = \sum_x P(x) \log\left(\frac{P(x)}{Q(x)}\right)$$
- **Sparse Categorical Cross-Entropy:** Si la etiqueta verdadera es un escalar entero $k \in \{1, \dots, C\}$:
$$\mathcal{L}_{\text{SCCE}} = - \log(\hat{y}_k)$$
Ambas formulaciones son idénticas en valor de pérdida y gradiente, pero Sparse CCE optimiza radicalmente la memoria y el cómputo al prescindir de la alocación de matrices dispersas *one-hot*.

#### Pérdidas en Detección de Objetos
La detección combina clasificación multiclase y regresión espacial continua:
$$\mathcal{L}_{\text{det}} = \mathcal{L}_{\text{cls}}(\hat{p}, p) + \lambda \mathcal{L}_{\text{box}}(\hat{b}, b)$$
- $\mathcal{L}_{\text{cls}}$: Focal Loss o Cross-Entropy binaria ponderada para manejar el desbalance extremo entre fondo y objetos.
- $\mathcal{L}_{\text{box}}$: Pérdida GIoU (Generalized IoU) o DIoU / CIoU combinada con Smooth $L_1$, penalizando la discordancia de área, solapamiento y aspecto geométrico.

#### Algoritmos de Optimización y Learning Rate
El entrenamiento de redes neuronales se formula como un problema de optimización no convexo sobre la superficie de error:
- **Descenso de Gradiente Estocástico (SGD):** Actualiza pesos con mini-batches: $w_{t+1} = w_t - \alpha \nabla \mathcal{L}(w_t)$.
- **SGD con Momentum:** Introduce inercia física para amortiguar oscilaciones en direcciones de alta curvatura y acelerar a través de planicies:
$$v_t = \gamma v_{t-1} + \alpha \nabla \mathcal{L}(w_t), \quad w_{t+1} = w_t - v_t$$
- **Adam (Adaptive Moment Estimation):** Combina el momentum (primer momento $m_t$) con la escala adaptativa del gradiente al cuadrado (segundo momento no centrado $v_t$), aplicando corrección de sesgo:
$$\hat{m}_t = \frac{m_t}{1 - \beta_1^t}, \quad \hat{v}_t = \frac{v_t}{1 - \beta_2^t}, \quad w_{t+1} = w_t - \frac{\alpha}{\sqrt{\hat{v}_t} + \epsilon} \hat{m}_t$$
- **Programación de la Tasa de Aprendizaje (*Learning Rate Scheduling*):** Estrategias como *Cosine Annealing* o *ReduceLROnPlateau* previenen la divergencia en fases iniciales y permiten un ajuste fino dentro de mínimos locales estrechos.

---

### 3.5. Técnicas de Regularización y Prevención del Sobreajuste

El sobreajuste (*overfitting*) se manifiesta cuando un modelo con alta capacidad paramétrica memoriza el ruido estadístico del conjunto de entrenamiento perdiendo capacidad de generalización sobre datos no observados:

1. **Regularización $L_2$ (Ridge / Weight Decay):**
$$\mathcal{L}_{\text{total}} = \mathcal{L}_0 + \frac{\lambda}{2} \sum_{i} w_i^2$$
Su gradiente $-\lambda w_i$ encoge continuamente los pesos hacia cero sin anularlos estrictamente, acotando la constante de Lipschitz de la función neuronal y forzando fronteras de decisión suaves.
2. **Regularización $L_1$ (Lasso):**
$$\mathcal{L}_{\text{total}} = \mathcal{L}_0 + \lambda \sum_{i} |w_i|$$
Genera una penalización constante independiente de la magnitud del peso, forzando coeficientes irrelevantes exactamente a cero (esparcidad y selección implícita de variables).
3. **Dropout:** Durante el paso de entrenamiento hacia adelante, desactiva aleatoriamente neuronas con probabilidad $p$ (comúnmente 0,2 a 0,5):
$$\tilde{y} = \frac{1}{1-p} \cdot (y \odot m), \quad m_i \sim \text{Bernoulli}(1-p)$$
Evita la co-adaptación perjudicial de neuronas (donde una neurona compensa los errores de otra) y aproxima un ensamble exponencial de $2^N$ subredes compartiendo parámetros.
4. **Batch Normalization (BN):** Normaliza las activaciones de un mini-batch a media cero y varianza unitaria, escalándolas y desplazándolas mediante parámetros aprendibles $\gamma$ y $\beta$:
$$\hat{x}_i = \frac{x_i - \mu_B}{\sqrt{\sigma_B^2 + \epsilon}}, \quad y_i = \gamma \hat{x}_i + \beta$$
Estabiliza la distribución de entradas a capas profundas (mitigando el cambio covariable interno), alisa la topología de la superficie de pérdida y permite tasas de aprendizaje sustancialmente mayores.
5. **Data Augmentation:** Incrementa la variabilidad del conjunto de entrenamiento mediante transformaciones afines sintéticas (rotaciones, recortes, escalado, volteo horizontal, perturbaciones fotométricas de color), forzando al modelo a aprender representaciones invariantes a transformaciones no semánticas.

---

### 3.6. Transfer Learning y Modelos Fundacionales en Visión

#### Transferencia Inductiva y Reutilización de Características
El aprendizaje por transferencia (*Transfer Learning*) aprovecha el conocimiento adquirido en una tarea fuente con abundancia masiva de datos $(\mathcal{D}_S, \mathcal{T}_S)$ (ej. preentrenamiento sobre ImageNet-21k, SA-1B o pares imagen-texto web) para resolver una tarea objetivo $(\mathcal{D}_T, \mathcal{T}_T)$ con datos acotados.
- **Jerarquía de representaciones reutilizables:**
  - *Capas tempranas:* Codifican primitivas visuales universales (bordes, contrastes locales, texturas). Son idénticamente útiles en cualquier dominio de visión por computadora.
  - *Capas intermedias y profundas:* Codifican geometrías compuestas y partes semánticas.
- **Estrategias de Adaptación:**
  - *Feature Extraction (Freezing):* Se congelan los pesos del *backbone* preentrenado y se entrena únicamente una cabeza de clasificación lineal o MLP sobre los embeddings extraídos. Ideal cuando el dataset objetivo es pequeño y el dominio visual es similar.
  - *Fine-Tuning (Ajuste Fino):* Se descongelan las capas profundas del *backbone* y se actualizan con una tasa de aprendizaje reducida ($\alpha_{\text{backbone}} \approx 0,1 \cdot \alpha_{\text{head}}$), adaptando las características semánticas a las particularidades del dominio objetivo sin destruir las primitivas preaprendidas (*catastrophic forgetting*).

#### Fundamentos de Modelos Empleados en el TPI
1. **OWLv2 (Open-Vocabulary Object Detector):**
   - Basado en arquitectura Vision Transformer (ViT).
   - Proyecta los parches de imagen y las consultas textuales abiertas a un espacio de embedding multimodal compartido alineado mediante entrenamiento contrastivo (estilo CLIP).
   - Permite consultar cualquier categoría léxica en tiempo de inferencia calculando la similitud coseno entre el embedding del parche visual y la proyección textual de la clase, sin requerir reentrenamiento del modelo.
2. **SAM2 (Segment Anything Model 2):**
   - Modelo fundacional de segmentación basado en transformadores espaciales con memoria temporal y mecanismos de atención cruzada (*promptable mask decoder*).
   - Entrenado con más de mil millones de máscaras (dataset SA-1B).
   - Recibe prompts geométricos externos (cajas delimitadoras predichas por OWLv2) y decodifica la máscara binaria exacta de la instancia con fidelidad a nivel píxel, superando las limitaciones de rectángulos envolventes ruidosos.

---

### 3.7. Métricas de Evaluación y Análisis Estadístico de Rendimiento

#### Matriz de Confusión y Derivaciones
| | Condición Real Positiva | Condición Real Negativa |
|---|---|---|
| **Predicción Positiva** | Verdadero Positivo ($TP$) | Falso Positivo ($FP$) |
| **Predicción Negativa** | Falso Negativo ($FN$) | Verdadero Negativo ($TN$) |

$$\text{Accuracy} = \frac{TP + TN}{TP + TN + FP + FN} \quad (\text{Sesgada ante clases desbalanceadas})$$
$$\text{Recall / Sensibilidad} = \frac{TP}{TP + FN} \quad (\text{Capacidad de detectar la clase})$$
$$\text{Precisión} = \frac{TP}{TP + FP} \quad (\text{Confiabilidad de la detección positiva})$$
$$\text{Especificidad} = \frac{TN}{TN + FP} \quad (\text{Capacidad de discriminar casos negativos})$$

#### $F_1$-Score y la Media Armónica
El $F_1$-score representa la media armónica entre precisión y recall:
$$F_1 = 2 \cdot \frac{\text{Precisión} \cdot \text{Recall}}{\text{Precisión} + \text{Recall}} = \frac{2 \cdot TP}{2 \cdot TP + FP + FN}$$
- *Justificación matemática:* A diferencia de la media aritmética $\frac{P+R}{2}$, la media armónica castiga severamente los valores extremos. Si un modelo predice infinitas cajas logrando $\text{Recall}=1,0$ pero $\text{Precisión}=0,05$, la media aritmética daría $0,525$ (aparentemente aceptable), mientras que la media armónica da $F_1 = 0,095$, reflejando fielmente la degradación del sistema.

#### Agregación Multiclase: Macro vs Weighted vs Micro $F_1$
- **Micro $F_1$:** Acumula globalmente los $TP, FP, FN$ sumando todas las clases. Es numéricamente idéntico a la precisión global, dominado por las clases mayoritarias.
- **Macro $F_1$:** Promedio aritmético simple de los $F_1$ individuales de cada clase:
$$\text{Macro } F_1 = \frac{1}{C} \sum_{c=1}^C F_{1,c}$$
Asigna el mismo peso a una clase rara con 2 muestras que a una clase frecuente con 1000 muestras. Es la métrica estándar para detectar colapso de rendimiento en la cola larga.
- **Weighted $F_1$:** Pondera el $F_1$ de cada clase por su soporte relativo ($N_c / N_{\text{total}}$), mitigando la penalización por clases minoritarias.

#### Curva ROC, Espacio de Operación y AUC
- La curva ROC (*Receiver Operating Characteristic*) grafica el $\text{True Positive Rate}$ ($\text{TPR} = \text{Recall}$) en función del $\text{False Positive Rate}$ ($\text{FPR} = 1 - \text{Especificidad}$) a medida que se varía el umbral de decisión $\tau \in [0, 1]$.
- El **AUC (Área Bajo la Curva)** cuantifica la probabilidad de que el clasificador asigne una puntuación mayor a una instancia positiva elegida al azar que a una negativa elegida al azar:
  - $\text{AUC} = 1,0$: Clasificador perfecto con separación absoluta.
  - $\text{AUC} = 0,5$: Comportamiento equivalente al azar aleatorio (línea diagonal).
  - $\text{AUC} < 0,5$: Inversión de etiquetas o falla estructural del clasificador.

#### Métrica de Solapamiento Espacial: Intersection over Union (IoU)
$$\text{IoU}(A, B) = \frac{\text{Área}(A \cap B)}{\text{Área}(A \cup B)}$$
En la competencia oficial, un objeto detectado se valida como Verdadero Positivo si y solo si su categoría coincide con la anotación de ground truth y el $\text{IoU} \ge 0,50$.

---

## 4. Matriz de Descubrimiento de Características y Casos Borde

### Features Discovered
| # | Categoría | Feature | Descripción | Inputs | Outputs | Manejo de Errores | Descubierto Vía |
|---|---|---|---|---|---|---|---|
| F1 | Percepción | Detección Open-Vocabulary (`OpenVocabDetector`) | Detección de objetos sin conjunto cerrado de clases usando alineación texto-imagen. | Imagen RGB, lista de clases léxicas, `conf_thr`, `nms_thr`. | Lista de dicts con `bbox`, `label`, `score`. | Retorna lista vacía si ninguna clase supera el umbral de confianza. | Notebook Sec. 2 & PDF Pág. 5 |
| F2 | Segmentación | Segmentación Guiada por Prompts (`SAM2Segmenter`) | Extracción de máscaras binarias de alta resolución a partir de bounding boxes. | Imagen RGB, lista de bounding boxes. | Tensor de máscaras booleanas $[N, H, W]$ y scores de máscara. | Captura excepciones CUDA OOM y realiza fallback a caja envolvente completa. | Notebook Sec. 3 & PDF Pág. 5 |
| F3 | Representación | Compresión RLE Column-Major (`mask_to_rle`) | Serialización compacta de máscaras binarias en formato RLE no comprimido. | Máscara booleana 2D numpy $[H, W]$. | Diccionario `{'size': [H, W], 'counts': [...]}` con orden Fortran. | Comprobación de orden column-major obligatoria para validar contra el schema. | Notebook Sec. 4 & PDF Pág. 5 |
| F4 | Representación | Cuantización Espacial 3x3 (`get_grid_position`) | Asignación discreta del centroide a una de las 9 regiones topológicas oficiales. | Centroide normalizado $(cx, cy) \in [0, 1]^2$. | String de región (`top_left`...`bottom_right`). | Clamping numérico estricto en $[0, 1]$ para evitar índices fuera de rango. | Notebook Sec. 4 & PDF Pág. 6 |
| F5 | Representación | Clasificación de Tamaño Relativo (`get_relative_size`) | Discretización del área normalizada del objeto en categorías de escala. | Área normalizada del objeto respecto a $H \times W$. | Categoría discreta: `'small'`, `'medium'`, `'large'`. | Umbrales normativos fijos ($\le 0,05 \to$ small, $\le 0,25 \to$ medium, $> 0,25 \to$ large). | Notebook Sec. 4 & PDF Pág. 7 |
| F6 | Representación | Grafo de Relaciones Topológicas (`spatial_relations`) | Cálculo determinista de predicados espaciales entre pares de instancias (`left_of`, `above`, `inside`). | Lista de cajas y máscaras de la escena, margen y umbrales de solapamiento. | Lista de tuplas/relaciones estructuradas. | Filtra relaciones redundantes o simétricas inconsistentes. | Notebook Sec. 4 & PDF Pág. 6 |
| F7 | Auditoría | Trazabilidad de Pipeline (`PipelineTracer`) | Registro estructurado y auditable de tiempos de ejecución, parámetros y artefactos. | Context manager de ejecución por imagen y módulo. | Diccionario estructurado serializado en logs/JSON con trazas completas. | Captura `sys.exc_info()`, traceback completo y marca estado `ERROR`. | Notebook Sec. 5 & PDF Pág. 6 |
| F8 | Razonamiento | Motor VQA Determinista (`QAEngine.deterministic`) | Resolución de consultas estructuradas (conteo, existencia, posición, tamaño, relaciones) directamente sobre SceneJSON. | Objeto SceneJSON, `operation_type`, `target_class`, `ref_class`. | Diccionario con `answer`, `normalized_answer`, `evidence`, `confidence`. | Retorna `unsupported` o `insufficient_information` ante atributos inexistentes. | Notebook Sec. 6 & PDF Pág. 7 |
| F9 | Interacción | Interpretación Neuro-Simbólica LLM (`QAEngine.llm`) | Traducción de texto libre en lenguaje natural a consulta estructurada intermedia en JSON mediante LLM. | String de pregunta abierta, prompt estructurado del sistema. | JSON intermedio estructurado (`intent`, `filters`, `target`). | Captura de formato inválido mediante regex, reintento con prompt de rescate o fallback seguro. | Notebook Sec. 6 & PDF Pág. 7 |
| F10 | Optimización | Percepción Multiescala y Tiling | Procesamiento de recortes en alta resolución para rescatar objetos pequeños/lejanos. | Imagen original dividida en cuadrantes solapados. | Detecciones agregadas fusionadas con NMS multiescala. | Supresión estricta de duplicados mediante NMS entre escalas con umbral adaptativo. | Notebook Sec. 10 & PDF Pág. 9 |
| F11 | Segmentación | Selección de Máscara Óptima SAM2 | Selección de la máscara de mayor consistencia entre las 3 opciones multimáscara. | Salidas multiescala de SAM2 y caja predictora. | Máscara singular refinada de máxima compatibilidad geométrica. | Descarta máscaras con IoU de caja anormalmente bajo ($< 0,3$). | Notebook Sec. 11 & PDF Pág. 9 |

---

### Edge Cases
| # | Feature | Escenario de Entrada / Condición Borde | Comportamiento Observado / Mitigación Implementada |
|---|---|---|---|
| E1 | `OpenVocabDetector` | Imagen con fondo homogéneo sin objetos presentes o umbral de confianza muy alto ($conf > 0,8$). | El detector devuelve una lista vacía de detecciones. `build_scene_json` construye un `SceneJSON` válido con lista de objetos vacía (`objects: []`), evitando errores en módulos posteriores. |
| E2 | `OpenVocabDetector` | Escenas densas con múltiples instancias superpuestas de la misma clase (ej. rebaño, cubiertos). | OWLv2 produce múltiples cajas redundantes que se anidan. Si el umbral NMS es muy permisivo ($> 0,6$), se saturan falsos positivos; si es muy bajo ($< 0,2$), se suprimen instancias reales contiguas. Se ajustó a $NMS=0,45$. |
| E3 | `SAM2Segmenter` | Bounding box degenerada o extremadamente pequeña ($w < 3\text{ px}$ o $h < 3\text{ px}$). | SAM2 puede fallar al interpolar el grid de embeddings o predecir una máscara vacía (todos ceros). La pipeline valida el área de la máscara predicha; si es nula, se genera una máscara rectangular de fallback igual a la bounding box. |
| E4 | `mask_to_rle` | Máscara completamente vacía (todos false) o completamente llena (todos true). | En una máscara de ceros, la función genera `counts: [H * W]`. En una de unos, genera `counts: [0, H * W]`. Cumple formalmente con la especificación RLE sin desbordar memoria. |
| E5 | `get_grid_position` | Centroide ubicado exactamente en las fronteras de división ($x = 1/3$ o $x = 2/3$). | Comparaciones con menor estricto e igualdad acotada evitan que un centroide pertenezca a dos celdas o caiga fuera del array tridimensional $3 \times 3$. |
| E6 | `spatial_relations` | Dos objetos con cajas mutuamente inclusivas (ej. una persona vistiendo una campera). | La función calcula la tasa de solapamiento direccional. Si $\text{Área}(A \cap B) / \text{Área}(A) > 0,85$, clasifica la relación como `inside` o `contains` en lugar de una relación direccional `left_of`/`above`. |
| E7 | `QAEngine` (Conteo) | Pregunta por la cantidad de objetos de una categoría inexistente en el JSON. | La consulta determinista filtra los objetos por la etiqueta solicitada. Al obtener 0 instancias, retorna formalmente `answer: 0`, `normalized_answer: 0` y `evidence: []` con confianza $1,0$. |
| E8 | `QAEngine` (Semántica) | Pregunta sobre propiedades físicas no modeladas en el JSON (ej. "¿De qué material es la mesa?"). | El motor detecta que el atributo consultado no forma parte del esquema formal de propiedades, devolviendo `normalized_answer: "unsupported"`, cumpliendo estrictamente con la consigna de la cátedra de no inventar respuestas. |
| E9 | `QAEngine` (LLM) | El modelo LLM alucina texto conversacional ("¡Claro! Aquí está el JSON...") antes del bloque de código. | Un parser robusto con expresiones regulares aísla el bloque `{...}` interno más exterior y valida su conformidad sintáctica con `json.loads`. Si la decodificación falla, dispara un prompt estructurado de rescate en una segunda pasada. |
| E10 | `LVIS Evaluation` | Predicción de un objeto perteneciente a una categoría clasificada como "no verificada" en la imagen. | El evaluador LVIS excluye formalmente la predicción del cómputo de falsos positivos en lugar de penalizarla, preservando la métrica de precisión y registrando la reducción en la cobertura de evaluación. |

---

## 5. Framework de Justificación Teórica ("Por qué hicimos cada cosa y por qué funciona")

Este framework responde de manera explícita a la consigna central de la cátedra: **"Justificar técnicamente con la teoría el motivo de cada elección algorítmica y de diseño, demostrando por qué hicimos cada cosa y por qué funciona"**.

```
========================================================================================================
ETAPA DEL PIPELINE        DECISIÓN TÉCNICA IMPLEMENTADA           SUSTENTO TEÓRICO / CÁTEDRA
========================================================================================================
Arquitectura Global       Descomposición modular:                Rechaza el sesgo de caja negra
                          Percepción -> Segmentación ->           de los VLMs directos. Garantiza
                          Representación -> Razonamiento          interpretabilidad, audibilidad y
                          -> Interacción neuro-simbólica.         cero alucinación factual.
--------------------------------------------------------------------------------------------------------
Exploración de Datos      Caracterización de escala,             Alineación con la teoría de
(EDA)                     densidad y desbalance en cola          distribución de patrones de la cátedra.
                          larga del vocabulario LVIS.             Motiva la necesidad de percepción
                                                                  multiescala para objetos pequeños.
--------------------------------------------------------------------------------------------------------
Módulo de Percepción      Adopción de detector Open-Vocabulary    Reutilización de representaciones en
                          basado en ViT (OWLv2) con               espacio multimodal preentrenado (CLIP).
                          alineación texto-imagen.                Permite transfer learning inductivo
                                                                  sin entrenamiento supervisado previo.
--------------------------------------------------------------------------------------------------------
Calibración de            Búsqueda en grilla (grid search)        Optimización empírica de la frontera de
Detección                 de umbrales de confianza (0,15) y       decisión sobre la curva ROC/PR.
                          Non-Maximum Suppression (0,45).         Maximiza el F1 armónico penalizando
                                                                  falsos positivos y duplicados espaciales.
--------------------------------------------------------------------------------------------------------
Extensión Perceptiva      Tiling multiescala de parches           Preservación de frecuencias espaciales
(Mejora V3)               para imágenes densas y objetos          altas. Mitiga la pérdida de resolución
                          pequeños (small).                       por patch embedding (16x16) en ViT.
--------------------------------------------------------------------------------------------------------
Módulo de                 Uso de Segment Anything Model 2         Transferencia de conocimiento fundacional
Segmentación              (SAM2) guiado por prompts de cajas      (1B máscaras). Sustituye máscaras
                          predichas por OWLv2.                    paramétricas por segmentación a nivel píxel.
--------------------------------------------------------------------------------------------------------
Refinamiento de           Selección multimáscara basada           Control de ambigüedad jerárquica
Máscaras                  en consistencia de IoU y filtrado       (todo vs parte) intrínseca en SAM2.
                          de geometrías degeneradas.              Evita sub/sobre-segmentación de instancias.
--------------------------------------------------------------------------------------------------------
Representación            Serialización en RLE column-major       Compresión sin pérdida que respeta
Estructurada              (Fortran order) cumpliendo con          la localidad espacial. Minimiza el costo
                          `scene_schema.json`.                    de almacenamiento frente a matrices densas.
--------------------------------------------------------------------------------------------------------
Geometría y               Discretización del plano continuo en    Abstracción simbólica: transforma
Topología                 grilla 3x3 y relaciones direccionales   coordenadas continuas en predicados
                          (`left_of`, `above`, `inside`).         lógicos deterministas para razonamiento.
--------------------------------------------------------------------------------------------------------
Trazabilidad y            Implementación de `PipelineTracer`      Principios de ingeniería y reproducibilidad:
Auditoría                 con logging de estados, latencias y     permite aislar cascadas de error
                          propagación de errores.                 entre etapas sucesivas del pipeline.
--------------------------------------------------------------------------------------------------------
Razonamiento              Consultas algorítmicas deterministas    Determinismo computacional: exactitud
Determinista              directamente sobre el SceneJSON         100% libre de alucinación aritmética
                          para existencia, conteo y relaciones.   en conteos y comparaciones espaciales.
--------------------------------------------------------------------------------------------------------
Módulo de Lenguaje        Arquitectura neuro-simbólica:           Aprovecha la competencia lingüística
(Promoción)               LLM liviano como parser semántico       del LLM para desambiguar lenguaje natural
                          a JSON intermedio ejecutable.           delegando la ejecución factual al código.
--------------------------------------------------------------------------------------------------------
Gestión de                Respuesta explícita `unsupported`       Manejo riguroso de incertidumbre epistémica:
Incertidumbre             ante atributos o clases inexistentes    es preferible una abstención justificada
                          sin inventar información.               a una alucinación convincente.
========================================================================================================
```

---

## 6. Guía de Preparación para la Defensa Oral (Preguntas Clave y Argumentación)

### Pregunta 1: "¿Por qué no utilizaron un modelo de lenguaje-visión de gran escala (VLM) como GPT-4V o LLaVA para resolver todo el problema de forma end-to-end?"
*Respuesta Técnica Fundamentada:*  
"El enunciado de la cátedra prohíbe explícitamente el uso de VLMs end-to-end porque buscamos evitar el comportamiento de 'caja negra'. Los VLMs directos sufren de alucinaciones espaciales severas (son propensos a fallar en conteos precisos y en la localización exacta de coordenadas de bounding boxes) y no ofrecen una representación intermedia observable. Al estructurar el pipeline en etapas modulares (*Percepción $\to$ Segmentación $\to$ Representación $\to$ Razonamiento*), desacoplamos la percepción visual del razonamiento simbólico. Esto garantiza que la información visual quede cristalizada en un `SceneJSON` determinista, auditable y formalmente verificable, donde cada respuesta a una pregunta cuenta con identificadores unívocos de evidencia empírica en la imagen."

### Pregunta 2: "¿Cómo opera matemáticamente la política de evaluación federada de LVIS y por qué una alta precisión no garantiza por sí sola un buen modelo?"
*Respuesta Técnica Fundamentada:*  
"Bajo la política federada de LVIS, un dataset con vocabulario amplio no puede ser anotado exhaustivamente en todas sus imágenes. Por ello, solo se computan Falsos Positivos sobre aquellas categorías explícitamente verificadas como ausentes (`neg_category_ids`). Si un detector predice una clase que no está anotada ni figura como negativa verificada (categoría no verificada), esa predicción se ignora para no penalizar injustamente al modelo. Por lo tanto, si un modelo tiene un umbral de confianza muy alto o un vocabulario sesgado hacia clases no verificadas, su precisión matemática puede ser artificialmente alta simplemente porque el denominador de evaluación carece de cobertura. Es mandatorio reportar la métrica de precisión en conjunto con la **cobertura de evaluación** y apoyarse en el $F_1$-score con $\text{IoU} \ge 0,50$."

### Pregunta 3: "¿Por qué el $F_1$-score utiliza la media armónica en lugar de la media aritmética?"
*Respuesta Técnica Fundamentada:*  
"La media aritmética pondera linealmente precisión y recall, lo que permite compensar un valor pésimo en una métrica con un valor alto en la otra. Por ejemplo, un modelo trivial que predice cientos de cajas por imagen obtendría un $\text{Recall} \approx 1,0$ pero una $\text{Precisión} \approx 0,05$; su media aritmética sería $0,525$, enmascarando el colapso del sistema. La media armónica $F_1 = 2 \cdot \frac{P \cdot R}{P + R}$ se aproxima asintóticamente al menor de los dos valores, castigando drásticamente el desequilibrio entre falsos positivos y falsos negativos. Solo se obtienen valores altos de $F_1$ cuando el detector es simultáneamente confiable (alta precisión) y exhaustivo (alto recall)."

### Pregunta 4: "¿Cuál es la función matemática del Non-Maximum Suppression (NMS) y cómo influye el umbral elegido?"
*Respuesta Técnica Fundamentada:*  
"Los detectores convolucionales y de transformadores evalúan múltiples ventanas o parches superpuestos, generando típicamente decenas de predicciones redundantes para un único objeto físico. El algoritmo NMS ordena las predicciones descendentemente por su puntaje de confianza; selecciona la caja de mayor confianza y suprime todas las demás cajas candidatas de la misma clase cuya intersección sobre unión ($\text{IoU}$) supere un umbral prefijado $\tau_{\text{NMS}}$. Si fijamos un umbral muy estricto ($\tau_{\text{NMS}} < 0,3$), el algoritmo corre el riesgo de suprimir instancias reales legítimas que se encuentran parcialmente ocluidas o muy próximas entre sí (ej. personas caminando en grupo). Si el umbral es muy permisivo ($\tau_{\text{NMS}} > 0,6$), subsisten cajas duplicadas para la misma instancia, disparando los falsos positivos y arruinando el conteo en el módulo de razonamiento."

### Pregunta 5: "¿Cómo interactúa el LLM en el modo de promoción y qué garantías existen contra las alucinaciones?"
*Respuesta Técnica Fundamentada:*  
"El LLM liviano actúa exclusivamente como un parser semántico y traductor neuro-simbólico, no como un motor de inferencia factual directo. El modelo recibe únicamente el texto de la consulta en lenguaje natural y tiene prohibido el acceso a la imagen. Su tarea se restringe a emitir un JSON intermedio formal que encapsula la intención de la consulta, la categoría objetivo, la categoría de referencia y el predicado espacial o de conteo. Este JSON intermedio es validado sintácticamente por nuestro código y ejecutado de manera 100% determinista por el motor algorítmico sobre el `SceneJSON`. De esta forma, el conteo matemático, la comprobación de relaciones espaciales y el filtrado son ejecutados por código determinista infalible, eliminando cualquier posibilidad de que el LLM invente datos o sufra alucinaciones aritméticas."

---

## 7. Registro de Trazabilidad y Verificación
- Archivo de especificación base: `TPI Primavera 2026 - Comprensión visual de escenas.pdf` (11 páginas analizadas exhaustivamente).
- Archivo de teoría de referencia: `IA-Resumen-Completo.pdf` (110 páginas analizadas y cotejadas en Unidades 1, 2, redes neuronales, CNNs, métricas y optimización).
- Cuaderno de código de referencia: `tpi-ia-2026p-21.ipynb` (115 celdas inspeccionadas, validando la coherencia entre código, hiperparámetros y marco teórico).
- Plantilla de estilo y formato: `TPI_IA_2025-TEMPLATE.pdf` (22 páginas relevadas para asegurar maquetado fiel y secciones normativas).
