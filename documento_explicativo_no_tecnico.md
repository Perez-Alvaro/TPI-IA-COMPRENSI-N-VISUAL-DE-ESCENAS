# Más Allá de la Caja Negra: Cómo una Inteligencia Artificial Aprende a Ver, Entender y Razonar el Mundo Visual

**Documento Explicativo y Conceptual para Audiencias Generales y Evaluadores**  
*Trabajo Práctico Integrador: Comprensión Visual de Escenas — Inteligencia Artificial (Primavera 2026)*  
*Universidad Tecnológica Nacional — Facultad Regional Córdoba — Grupo 21*

---

> ### 💡 Resumen Ejecutivo en 60 Segundos
> La mayoría de los sistemas modernos de Inteligencia Artificial que "miran" imágenes operan como **cajas negras**: reciben una fotografía, procesan millones de cálculos matemáticos ocultos y arrojan una respuesta en texto. Aunque a menudo suenan convincentes, estos modelos sufren de un defecto crítico: **alucinan**. Se equivocan al contar cosas sencillas, confunden la izquierda con la derecha y no pueden explicar el porqué de sus afirmaciones.
> 
> En este proyecto rompimos con ese paradigma. Diseñamos una arquitectura **Neuro-Simbólica** que une lo mejor de dos mundos:
> 1. **La Red Neuronal (El Ojo Artístico):** Reconoce formas, colores y siluetas en el caos visual del mundo real.
> 2. **La Lógica Simbólica (El Cerebro Racional):** Traduce lo que ve en un mapa estructurado y verificable, donde las matemáticas y las reglas espaciales son exactas, deterministas y 100% auditables.
> 
> A lo largo de este documento explicamos cómo construimos este sistema, las metáforas que guiaron su diseño, los descubrimientos que nos llevaron a la cima de la competencia de Kaggle y por qué este enfoque es el futuro de la IA confiable en la industria.

---

```
========================================================================================================
                      MAPA CONCEPTUAL DEL SISTEMA NEURO-SIMBÓLICO
========================================================================================================

    [ FOTOGRAFÍA BRUTA ]
             │
             ▼
    ┌─────────────────────────┐
    │  ETAPA 1: EL DETECTIVE  │  Localiza cualquier objeto en la escena mediante
    │  (OWLv2 Open-Vocabulary)│  lenguaje natural, sin listas rígidas preconcebidas.
    └───────────┬─────────────┘
                │   (Marcos de ubicación preliminares)
                ▼
    ┌─────────────────────────┐
    │  ETAPA 2: EL ESCULTOR   │  Recorta con precisión milimétrica la silueta exacta
    │      (Meta SAM2)        │  de cada objeto, separándolo átomo por átomo del fondo.
    └───────────┬─────────────┘
                │   (Máscaras pixel-exactas)
                ▼
    ┌─────────────────────────┐
    │ ETAPA 3: EL CARTÓGRAFO  │  Organiza el espacio en una cuadrícula topológica 3x3,
    │      (SceneJSON)        │  extrae colores dominantes y computa relaciones espaciales.
    └───────────┬─────────────┘
                │   (Plano arquitectónico digital transparente)
                ▼
    ┌─────────────────────────┐
    │  ETAPA 4: EL VERIFICADOR│  Resuelve preguntas de conteo, existencia y ubicación
    │  (Razonamiento Híbrido) │  mediante matemáticas exactas, anulando alucinaciones.
    └───────────┬─────────────┘
                │   (Respuestas certeras con evidencia)
                ▼
    ┌─────────────────────────┐
    │  ETAPA 5: EL INSPECTOR  │  Valida que cada dato cumpla el estándar de calidad
    │   (Control y Auditoría) │  y registra la "caja negra" de tiempos y decisiones.
    └─────────────────────────┘
========================================================================================================
```

---

## 1. Introducción y El Desafío Visual: ¿Qué Significa Realmente "Comprender" una Imagen?

### El Abismo entre Mirar Píxeles y Entender la Realidad
Para una persona, mirar una fotografía es un acto instantáneo y natural. Si vemos una foto de una cocina familiar, nuestro cerebro identifica de inmediato la mesa de madera en el centro, los platos servidos, el perro sentado a la izquierda y la taza de café humeante cerca del borde. Comprendemos intuitivamente la profundidad, las relaciones entre los objetos e incluso el contexto de la situación.

Para una computadora, en cambio, **una imagen no es más que una planilla de cálculo gigante**. Es una matriz de millones de números que representan la intensidad de luz roja, verde y azul de cada punto diminuto (píxel). No hay etiquetas, no hay objetos, no hay espacio: solo números que cambian según la iluminación y la sombra.

```
La ilusión visual:
Lo que ve un ser humano:              Lo que ve una computadora:
┌───────────────────────────┐         ┌───────────────────────────┐
│        [ GATITO ]         │         │ [142, 85, 23] [145, 87, 24]│
│         dormido           │  ───►   │ [140, 83, 21] [210, 190, 15]│
│      sobre la mesa        │         │ [12,  14, 18] [95,  102, 88]│
└───────────────────────────┘         └───────────────────────────┘
   Significado semántico                    Matriz numérica cruda
```

### La Trampa de la Clasificación Simple
Durante la última década, los avances en visión por computadora se popularizaron a través de modelos de **clasificación de imágenes**. Si le mostramos una foto a uno de estos sistemas, nos dice con un 98% de seguridad: *"Es un perro"*.

Sin embargo, clasificar una imagen completa es como escuchar a un loro repetir una palabra cuando ve una mancha de color:
- **No sabe cuántos perros hay:** Podría haber uno solo o una manada de diez; la respuesta seguirá siendo *"perro"*.
- **No sabe dónde están:** No tiene idea de si el perro está en el centro, en una esquina o asomándose detrás de un sillón.
- **No sabe qué más hay:** Ignora por completo que al lado del perro hay un gato, una pelota roja y una ventana abierta.
- **No distingue el objeto del fondo:** No puede separar la silueta del perro del pasto sobre el que está parado.

### El Verdadero Reto: La Comprensión Holística de Escenas
Para que una máquina realmente **comprenda** una escena visual, debe ser capaz de resolver cuatro interrogantes simultáneos:

1. **¿Qué cosas hay y dónde se ubican?** (*Detección multiobjeto*): Marcar con precisión la zona aproximada de cada entidad presente en la escena.
2. **¿Cuál es la forma exacta de cada cosa?** (*Segmentación de instancias*): Pintar píxel por píxel el contorno del objeto, separándolo con bisturí del fondo y de otros objetos que lo toquen.
3. **¿Cómo se organiza el espacio?** (*Cartografía y topología*): Entender qué objeto está a la izquierda de cuál, qué está encima de qué, quién contiene a quién y cuál es el tamaño relativo de las cosas.
4. **¿Cómo podemos razonar sobre la escena?** (*Preguntas y respuestas visuales - VQA*): Responder preguntas en lenguaje natural (como *"¿Cuántas sillas rodean a la mesa?"* o *"¿Hay una botella roja a la derecha del monitor?"*) sin inventar datos y con certeza absoluta.

### El Desafío del Mundo Real: Un Universo de Objetos Diminutos
En el mundo real las escenas no son fotos de estudio prolijas. En nuestro conjunto de datos de estudio (compuesto por 120 imágenes de desarrollo con un total de **1.790 anotaciones** de referencia y un promedio de casi 15 objetos por fotografía, con picos de más de 40 objetos hacinados):
- **Objetos pequeños (`small`):** El **71,06% de las instancias (1.272 objetos)** son diminutos y ocupan menos del 1% del área total de la imagen (como una taza al fondo de un salón, un picaporte, una llave o una fruta lejana).
- **Objetos medianos (`medium`):** El **24,02% de las instancias (430 objetos)** tienen un tamaño moderado, ocupando entre el 1% y el 10% de la escena visual.
- **Objetos grandes (`large`):** Apenas el **4,92% de las instancias (88 objetos)** superan el 10% del área de la imagen (muebles principales, vehículos en primer plano o personas completas).
- **Oclusiones severas:** Los objetos se tapan parcialmente entre sí. Un libro tapa parte de una mesa; una persona sostiene un teléfono ocultando la mitad de su superficie.
- **Ambigüedad y texturas:** ¿Es esa luminaria urbana un semáforo o una farola? ¿Es ese adorno de piedra un perro real o una estatua decorativa?

Enfrentar este nivel de complejidad requería una estrategia de diseño radicalmente superior a las soluciones convencionales.

---

## 2. La Elección Estratégica: ¿Por qué una Arquitectura Neuro-Simbólica y no una "Caja Negra"?

### El Canto de Sirenas de los Modelos Gigantes (VLMs)
En la actualidad existe una fuerte tendencia comercial hacia los denominados **Modelos de Visión-Lenguaje Multimodales (VLMs)** de gran escala (como GPT-4V, Claude o Gemini). La promesa parece mágica: uno le entrega la imagen cruda al modelo gigante y le pide directamente: *"Dime todo lo que ves y responde mis preguntas"*.

Sin embargo, en entornos industriales, médicos y de ingeniería crítica, esta solución de **caja negra** presenta fallas estructurales inaceptables:

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    EL PROBLEMA DE LA CAJA NEGRA                         │
│                                                                         │
│   [ FOTO CRUDA ] ──► [ MODELO GIGANTE VLM ] ──► "Veo 4 botellas azules"│
│                      (Malla opaca de miles                               │
│                       de millones de pesos)   ¿Son realmente 4?         │
│                                               ¿Dónde están?             │
│                                               ¿Por qué dice azul?       │
│                                               ¿Podemos confiar? NO.     │
└─────────────────────────────────────────────────────────────────────────┘
```

1. **Alucinaciones Aritméticas:** Los modelos de lenguaje están entrenados para predecir qué palabra suena bonita después de otra, no para hacer matemáticas. Si hay 7 cajas en una estantería, un modelo gigante puede decir que hay 5, 8 o 10 con la misma seguridad imperturbable.
2. **Ceguera Espacial:** Tienen grandes dificultades para calcular con rigor si un objeto está a la izquierda, a la derecha o detrás de otro en un plano tridimensional proyectado a 2D.
3. **Opacidad e Inaudibilidad:** Si el sistema comete un error grave (por ejemplo, en un vehículo autónomo que no frena ante un peatón o un robot quirúrgico que confunde una vena con un tejido conectivo), es imposible abrir el modelo para entender qué cálculo falló.
4. **Inestabilidad:** Si cambiamos una palabra en la pregunta (*"¿Cuántas botellas hay?"* versus *"Dime el número de botellas que ves"*), el modelo puede dar dos respuestas numéricas contradictorias.

### La Solución Inteligente: El Paradigma Neuro-Simbólico
Para resolver este dilema, la cátedra estableció un lineamiento metodológico firme: **prohibido usar modelos de caja negra directa**. En su lugar, construimos un sistema **Neuro-Simbólico**.

¿Qué significa esto? Significa orquestar un matrimonio armonioso entre dos corrientes históricas de la Inteligencia Artificial:

| Dimensión | Enfoque Neuronal (El Ojo Artístico) | Enfoque Simbólico (El Cerebro Racional) |
|---|---|---|
| **Especialidad** | Percibir lo caótico, continuo y visual (luces, texturas, formas, píxeles). | Razonar sobre lo discreto, exacto y lógico (números, relaciones, reglas). |
| **Fortaleza** | Reconoce un gato aunque esté de espaldas, con sombra o tapado por una sábana. | Si hay 3 gatos, suma 1 + 1 + 1 y el resultado es matemáticamente 3, sin margen de error. |
| **Debilidad** | Puede alucinar, no garantiza exactitud matemática ni consistencia espacial. | Incapaz de procesar directamente una foto de píxeles sin que alguien se la traduzca antes. |
| **Nuestro Rol** | Detectar objetos y recortar sus siluetas en la imagen cruda. | Construir el plano, contar, comprobar distancias y auditar respuestas. |

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                    NUESTRA ARQUITECTURA NEURO-SIMBÓLICA                      │
│                                                                              │
│   [ IMAGEN ] ──► [ RED NEURONAL ] ──► [ SceneJSON ] ──► [ MOTOR LÓGICO ]    │
│                     (Ojo Experto)        (El Plano         (Cerebro Exacto)  │
│                                         Transparente)                        │
│                                                                 │            │
│                                                                 ▼            │
│                                                      [ RESPUESTA CERTERA ]   │
│                                                      (Conteo exacto,         │
│                                                       evidencia visual y     │
│                                                       auditoría total)       │
└──────────────────────────────────────────────────────────────────────────────┘
```

### El Escudo de la Transparencia: El `SceneJSON`
En el corazón de nuestra arquitectura reside un artefacto clave: el **SceneJSON** (el "Plano de la Escena").
En lugar de permitir que la IA hable directamente sobre la foto, obligamos a las redes neuronales a traducir primero todo lo que ven a un formato estructurado, ordenado y legible tanto por humanos como por computadoras.

Cada objeto en el plano cuenta con:
- **Identificador unívoco:** Objeto #1, Objeto #2, etc.
- **Categoría:** Qué cosa es (ej. `chair`, `bottle`, `table`).
- **Nivel de Confianza:** Un valor porcentual que indica cuán seguro está el detector.
- **Silueta Geométrica:** La máscara exacta de píxeles codificada de forma compacta.
- **Posición en el Tablero:** En qué sector de una cuadrícula de 3×3 se encuentra.
- **Tamaño Relativo:** Si es pequeño, mediano o grande en relación con la habitación.
- **Color Dominante:** Su tono cromático predominante según una paleta estandarizada.
- **Grafo de Conexiones:** Su relación de vecindad con los demás objetos (*"está a la izquierda de la mesa"*, *"está encima del mantel"*).

Gracias a este plano intermedio, **las alucinaciones quedan erradicadas**. Si se le pregunta al sistema cuántas botellas hay, el sistema no adivina: abre el archivo, cuenta las filas que dicen "botella" y entrega el número con un 100% de reproducibilidad matemática.

---

## 3. El Viaje a Través de las 5 Etapas del Pipeline (Explicado con Metáforas)

Para comprender cómo funciona el sistema completo, imaginemos una fábrica de precisión donde trabajan cinco especialistas en cadena. Cada uno recibe el trabajo del anterior, le añade valor técnico y se lo entrega al siguiente con total rigurosidad.

```
+----------------------------------------------------------------------------------------------------+
|                                    LA CADENA DE MONTAJE VISUAL                                     |
+--------------------------+--------------------------+----------------------------------------------+
| Etapa / Especialista     | Nombre Técnico           | Misión Central                               |
+--------------------------+--------------------------+----------------------------------------------+
| 1. El Detective          | OWLv2 Open-Vocabulary    | Encontrar cualquier objeto en la imagen      |
| 2. El Escultor           | Meta SAM2                | Recortar la silueta exacta a nivel píxel     |
| 3. El Cartógrafo         | SceneJSON Topológico     | Construir el plano espacial y de relaciones  |
| 4. El Juez Verificador   | QAEngine Híbrido + LLM   | Responder preguntas con rigor matemático     |
| 5. El Inspector de Firma | Schema Validator + Trace | Auditar la calidad y asegurar trazabilidad   |
+--------------------------+--------------------------+----------------------------------------------+
```

---

### Etapa 1: El Detective de Vocabulario Abierto (Localización Visual)

```
        Fotografía Cruda                        Marcos de Búsqueda
    ┌───────────────────────┐               ┌───────────────────────┐
    │       /\_/\   [Taza]  │   OWLv2       │   ┌───────┐   ┌─────┐ │
    │      ( o.o )          │  ───────►     │   │ Gato  │   │Taza │ │
    │       > ^ <   [Plato] │               │   └───────┘   └─────┘ │
    └───────────────────────┘               └───────────────────────┘
```

#### La Metáfora
Imagine un detective clásico de policía al que solo le enseñaron 10 fotos de criminales conocidos. Si entra a un banco y ve a un delincuente nuevo o a un cómplice disfrazado, no sabrá qué hacer porque no está en su lista fija de 10 personas.

Ahora imagine a un **Detective Moderno de Vocabulario Abierto**: no memoriza fotos fijas, sino que sabe leer cualquier descripción escrita en lenguaje natural. Si le decimos *"Busca una mochila azul desgastada"*, *"Busca un extintor de incendios"* o *"Busca una lámpara de pie"*, el detective sabe perfectamente qué rasgos visuales corresponden a esos conceptos, sin importar si los vio ayer o hace un año.

#### Cómo Opera en Nuestro Sistema
En nuestro pipeline, este rol lo cumple el modelo **OWLv2** (*Open-World Localization* de Google):
- **Alineación Texto-Imagen:** El modelo proyecta simultáneamente el texto que buscamos (por ejemplo, las 120 categorías que evalúa el dataset) y las partes de la imagen a un mismo "lenguaje universal" de representaciones matemáticas.
- **Sin Categorías Cerradas:** Si la imagen tiene objetos exóticos o combinaciones complejas, el detector los encuentra comparando la similitud entre la idea escrita y el patrón visual.
- **El Dilema del Filtro de Confianza:** El detective le asigna a cada sospechoso un puntaje de seguridad entre 0 y 1. Si ponemos un umbral muy alto (ej. 0,50), el detective solo señalará lo obvio y pasará por alto el 71% de los objetos pequeños. Si ponemos un umbral demasiado permisivo (ej. 0,05), verá fantasmas en las sombras de las paredes. Tras rigurosos análisis empíricos, fijamos su umbral en **0,15 - 0,23**, logrando el equilibrio óptimo entre no perder objetos y no inventar falsas alarmas.

---

### Etapa 2: El Escultor de Alta Precisión (Segmentación a Nivel Píxel)

```
       Marco Rectangular Ruidoso                   Silueta Quirúrgica Píxel a Píxel
       ┌────────────────────────┐                    ┌────────────────────────┐
       │ Mesa... ░░░░░░░░░░░░░░ │                    │        ░░░░░░░░        │
       │ Fondo.. ░░░ [GATO] ░░░ │     Meta SAM2      │       ░░░░░░░░░░       │
       │ Pared.. ░░░░░░░░░░░░░░ │    ───────────►    │        ░░░░░░░░        │
       └────────────────────────┘                    └────────────────────────┘
```

#### La Metáfora
El Detective hizo un trabajo formidable al marcar la zona donde está el gato, pero su herramienta es tosca: dibujó un **rectángulo envolvente** (*bounding box*). Ese rectángulo encierra al gato, pero también atrapa un pedazo de la alfombra sobre la que duerme, la pata de la silla contigua y la pared del fondo. Si intentamos calcular el color del gato analizando todo ese marco, el color de la alfombra distorsionará la medición.

Entra en acción **El Escultor de Alta Precisión**. El escultor toma el marco del detective como una pista de dónde mirar y, utilizando un bisturí microscópico, recorta exactamente los píxeles que pertenecen al cuerpo del felino, descartando cada mota de polvo del fondo.

#### Cómo Opera en Nuestro Sistema
Este papel lo ejecuta **SAM2** (*Segment Anything Model 2* de Meta):
- **Modelos Fundacionales al Servicio del Detalle:** Entrenado con más de mil millones de máscaras visuales, SAM2 conoce las fronteras naturales de prácticamente cualquier objeto material del mundo real.
- **Inferencia Instantánea por Capas:** Primero procesa la imagen para entender su estructura volumétrica una sola vez. Luego, cada vez que el detective le pasa un rectángulo, genera la silueta binaria en una fracción de segundo (0,43 segundos para todos los objetos de la foto).
- **Compresión Inteligente (RLE):** Guardar una silueta de un millón de píxeles punto por punto ocuparía demasiado espacio de memoria. El escultor empaqueta la máscara en un formato compacto llamado *Run-Length Encoding* (RLE): en lugar de escribir `0, 0, 0, 0, 1, 1, 1`, escribe `4 ceros seguidos de 3 unos`, reduciendo el peso del archivo en más de un 95% sin perder un solo píxel de resolución.

---

### Etapa 3: El Cartógrafo Espacial (Estructuración del SceneJSON)

```
        Siluetas Desparramadas                       El Tablero Cartográfico 3x3
    ┌──────────────────────────────┐              ┌────────────┬────────────┬────────────┐
    │  (Objeto A)                  │              │  TOP_LEFT  │ TOP_CENTER │ TOP_RIGHT  │
    │                              │              │  [Obj A]   │            │            │
    │             (Objeto B)       │  ────────►   ├────────────┼────────────┼────────────┤
    │                              │              │ MID_LEFT   │   CENTER   │ MID_RIGHT  │
    │    (Objeto C)                │              │            │  [Obj B]   │            │
    └──────────────────────────────┘              ├────────────┼────────────┼────────────┤
                                                  │ BOT_LEFT   │ BOT_CENTER │ BOT_RIGHT  │
                                                  │  [Obj C]   │            │            │
                                                  └────────────┴────────────┴────────────┘
```

#### La Metáfora
Tener un montón de siluetas recortadas en una mesa sigue sin ser suficiente. Si usted es el director de logística de un almacén o el comandante de una misión de rescate, necesita un **mapa unificado**.

El **Cartógrafo Espacial** toma las siluetas, calcula su centro de gravedad exacto y dibuja una cuadrícula formal sobre la escena, como si colocara un tablero de ajedrez gigante sobre la imagen.

#### Cómo Opera en Nuestro Sistema
El cartógrafo ejecuta tres operaciones sistemáticas para estructurar el plano digital `SceneJSON`, completando toda la organización espacial y de atributos en apenas **0,28 segundos** (0.28s) por fotografía:
1. **La Cuadrícula 3×3:** Divide la imagen en 9 regiones normalizadas:
   - Fila Superior: `arriba a la izquierda` (`top_left`), `arriba al centro` (`top_center`), `arriba a la derecha` (`top_right`).
   - Fila Central: `medio a la izquierda` (`middle_left`), `centro absoluto` (`center`), `medio a la derecha` (`middle_right`).
   - Fila Inferior: `abajo a la izquierda` (`bottom_left`), `abajo al centro` (`bottom_center`), `abajo a la derecha` (`bottom_right`).
2. **La Brújula de Relaciones Topológicas:** Compara cada par de objetos y dictamina con precisión milimétrica si están relacionados en el espacio:
   - *"El objeto A está a la izquierda de B (`left_of`)"* (si su margen horizontal dista más de un 5%).
   - *"El objeto B está encima de C (`above`)"*.
   - *"El objeto D está contenido dentro de E (`inside`)"* (si el área de solapamiento supera el 85%, por ejemplo una corbata sobre una camisa).
3. **El Escáner de Color Dominante:** Analiza los píxeles reales de la silueta (descartando el fondo) y los clasifica dentro de una paleta oficial de 11 colores estandarizados (`black`, `blue`, `brown`, `gray`, `green`, `orange`, `pink`, `purple`, `red`, `white`, `yellow`), evitando confusiones cromáticas subjetivas.

---

### Etapa 4: El Juez Verificador de Hechos (Razonamiento Libre de Alucinaciones)

```
        PREGUNTA DEL USUARIO:
        "¿Cuántas botellas rojas hay en el centro de la mesa?"
                                  │
                                  ▼
                ┌───────────────────────────────────┐
                │ CAPA 1: EL TRADUCTOR NEURONAL     │
                │ Convierte lenguaje natural a      │
                │ una orden de búsqueda precisa.    │
                └─────────────────┬─────────────────┘
                                  │  Filtro: {clase: "botella", color: "red", zona: "center"}
                                  ▼
                ┌───────────────────────────────────┐
                │ CAPA 2: EL MOTOR FACTUAL (CÓDIGO) │
                │ Consulta el SceneJSON con lógica  │
                │ matemática pura (Cero Alucinación)│
                └─────────────────┬─────────────────┘
                                  │  Resultado exacto: 2 unidades (Evidencia: [Obj_3, Obj_7])
                                  ▼
                ┌───────────────────────────────────┐
                │ CAPA 3: EL VERBALIZADOR Y FILTRO  │
                │ Redacta la respuesta y audita que │
                │ no se cambie ningún número.       │
                └─────────────────┬─────────────────┘
                                  │
                                  ▼
        RESPUESTA VERIFICADA:
        "Hay exactamente 2 botellas rojas en el centro de la escena."
```

#### La Metáfora
Imagine un juicio oral. Si dejamos que un testigo elocuente pero fantasioso (un modelo de lenguaje generativo) hable libremente sobre lo que vio en la noche del crimen, adornará la historia con detalles inventados, cambiará las horas y dirá que vio a tres sospechosos cuando solo había uno.

Por eso, el tribunal cuenta con un **Juez Estricto**:
- El testigo solo tiene permitido traducir la pregunta del público en un pedido formal al archivo de actas.
- El secretario del juzgado abre el libro de actas (el plano del Cartógrafo) y cuenta los registros con lápiz y papel.
- Si el testigo intenta leer la sentencia y altera un solo dato numérico, el juez le quita la palabra de inmediato y lee la sentencia oficial directamente del libro de actas.

#### Cómo Opera en Nuestro Sistema
Diseñamos un módulo de razonamiento en 3 capas blindadas:
1. **El Traductor Semántico (LLM Qwen 2.5):** Un modelo de lenguaje ligero que lee la pregunta humana (ej. *"¿Hay algún vehículo a la izquierda del ciclista?"*) y la traduce a una fórmula estructurada sin inventar respuestas. Si comete un error en el formato, un mecanismo de autocorrección le devuelve el error para que lo arregle de inmediato.
2. **El Motor Determinista Factual:** Toma la fórmula y consulta el `SceneJSON`. La suma de objetos la hace un contador matemático en Python. **La probabilidad de equivocarse en el conteo de los objetos registrados es cero.**
3. **El Filtro de Fidelidad Algorítmico:** Si el modelo de lenguaje redacta una respuesta final para que suene amigable pero cambia un número o una posición, nuestro sistema rechaza su texto y emite la respuesta formal estructurada de forma automática.

---

### Etapa 5: El Inspector de Calidad y la Caja Negra de Trazabilidad

```
       SceneJSON Recién Creado                    Auditoría y Certificación
    ┌──────────────────────────────┐              ┌──────────────────────────────┐
    │  {                           │              │  [✓] Estructura Schema 100%  │
    │    "objects": [...],         │  ────────►   │  [✓] Consistencia Lógica     │
    │    "relations": [...]        │              │  [✓] Trazabilidad Registrada │
    │  }                           │              │  [✓] Cero Fuga de Datos      │
    └──────────────────────────────┘              └──────────────────────────────┘
```

#### La Metáfora
En la industria aeronáutica o en las líneas de fabricación de automóviles de lujo, ningún producto sale a la calle sin pasar por la estación del **Inspector de Calidad**, y ningún avión vuela sin una **Caja Negra de Trazabilidad** que registre segundo a segundo cada decisión de vuelo.

Si una puerta no cierra con una tolerancia inferior a un milímetro, el vehículo vuelve al taller. Si ocurre un incidente en vuelo, la caja negra permite recrear con absoluta certeza qué interruptor se tocó y por qué.

#### Cómo Opera en Nuestro Sistema
1. **El Inspector de Esquema (`Schema Validator`):** Cada plano generado es examinado automáticamente contra una norma internacional estricta (`Draft-07 JSON Schema`). Si un objeto carece de etiqueta, si una coordenada se desborda de la foto o si una relación espacial es absurda (ej. que un objeto esté a la izquierda y a la derecha de sí mismo), el archivo es rechazado y corregido al instante. El sistema alcanzó un **100% de consistencia perfecta en todas las imágenes evaluadas**.
2. **La Caja Negra (`PipelineTracer`):** Un supervisor digital monitorea el consumo de memoria, el tiempo en milisegundos que consumió cada modelo, los parámetros empleados y los identificadores de hardware. Si ocurre una excepción inesperada (por ejemplo, una imagen corrupta o falta de memoria en la placa de video), el sistema captura el incidente con elegancia, realiza una acción de respaldo y continúa trabajando sin colapsar el lote.

---

## 4. Innovaciones de Ingeniería: Lo que Funcionó, las Sorpresas y los Experimentos Fallidos

En la ciencia de datos aplicada, los mayores aprendizajes no provienen de seguir recetas teóricas, sino del choque entre las hipótesis iniciales y la evidencia empírica. A continuación, revelamos las cuatro batallas de ingeniería más trascendentes del proyecto:

---

### Innovación 1: "La Lupa Digital" (Mosaicos Multiescala)

```
        Visión Convencional                           Estrategia con Lupa Multiescala
        (Un solo vistazo global)                      (Vistazo global + 4 Cuadrantes de Alta Definición)
    ┌──────────────────────────────┐              ┌──────────────┬──────────────┐
    │                              │              │  Cuadrante 1 │  Cuadrante 2 │
    │     [Objeto minúsculo]       │              │  (Zoom 1.75x)│  (Zoom 1.75x)│
    │     (Borron de 4 píxeles)    │  ────────►   ├──────────────┼──────────────┤
    │                              │              │  Cuadrante 3 │  Cuadrante 4 │
    │                              │              │  (Zoom 1.75x)│  (Zoom 1.75x)│
    └──────────────────────────────┘              └──────────────┴──────────────┘
```

#### El Problema
El análisis exploratorio inicial nos reveló un dato contundente: **el 71,06% de todos los objetos de la escena ocupan menos del 1% del tamaño de la imagen**.
Cuando un detector de visión artificial procesa una fotografía de alta resolución, se ve obligado a reducirla para que quepa en la memoria de la tarjeta gráfica. Al encoger la imagen, una botella lejana o un pájaro en el horizonte se convierten en un manchón borroso de 4 o 5 píxeles. El detector simplemente no puede verlos.

#### La Solución de Ingeniería
Implementamos una estrategia inspirada en la forma en que un humano busca una joya perdida en una alfombra: primero mira la habitación entera y luego se arrodilla con una **lupa virtual**.
- Dividimos la fotografía en **4 cuadrantes (mosaicos de 2×2)** que se solapan entre sí en un 25% para no partir ningún objeto a la mitad.
- Cada cuadrante es ampliado digitalmente a la resolución nativa máxima del detector, logrando un **aumento óptico efectivo de 1,75×**.
- Un filtro inteligente descarta los objetos que tocan el borde del recorte (evitando registrar objetos cortados) y aquellos demasiado grandes (que corresponden a la vista general).
- Finalmente, unificamos todas las observaciones en un único mapa coherente.

#### El Impacto
Esta técnica permitió rescatar decenas de objetos pequeños que antes eran invisibles, logrando mantener el nivel de detección en objetos diminutos incluso cuando elevamos la exigencia de confianza para erradicar falsos positivos.

---

### Sorpresa 2: Por Qué "Más Grande No Siempre es Mejor" (OWLv2 Base vs. Large)

```
========================================================================================================
                          LA BATALLA DE LOS MODELOS: BASE VS. LARGE
========================================================================================================
 Modelo Evaluado       Tamaño en Memoria   Tiempo por Imagen   F1-Score Cajas   Veredicto
--------------------------------------------------------------------------------------------------------
 OWLv2 Base            ~150M Parámetros    2,44 segundos       0,6510           GANADOR (Ágil y preciso)
 OWLv2 Large           ~430M Parámetros    11,45 segundos      0,6260           PERDEDOR (Lento y confuso)
--------------------------------------------------------------------------------------------------------
 Diferencia            4x Más Pesado       4,7x Más Lento      -0,0250 (Peor)   HIPÓTESIS RECHAZADA
========================================================================================================
```

#### La Hipótesis Intuitiva
En el mundo de la inteligencia artificial abunda el dogma del escalado: *"Si un modelo mediano es bueno, el modelo gigante será invencible"*. Confiando en esta premisa, decidimos reemplazar nuestro detector base (`OWLv2 Base`) por su hermano mayor (`OWLv2 Large`), un coloso con el cuádruple de parámetros y mayor resolución de procesamiento.

#### El Choque con la Realidad
Al someter ambos modelos al banco de pruebas oficial, los resultados fueron una sorpresa mayúscula:
1. **Velocidad destruida:** El modelo Large tardó **11,45 segundos por imagen** frente a los **2,44 segundos** del Base (casi 5 veces más lento). Procesar nuestro lote de trabajo se volvía inviable.
2. **Pérdida de puntería:** Lejos de mejorar, la precisión general **empeoró**. El modelo Large, al poseer tanta capacidad matemática libre, comenzó a sobreinterpretar texturas del fondo y generó una avalancha de falsas alarmas (falsos positivos) ante un vocabulario diverso de 120 clases.

#### La Lección Estratégica
En ingeniería de sistemas, **la fuerza bruta no reemplaza a la sintonía fina**. Un modelo mediano, ágil y perfectamente calibrado en sus umbrales supera con holgura a un gigante pesado, torpe y costoso de operar.

---

### Innovación 3: El Arte de Reconocer la Ignorancia (La Política de Ausencia Derivada)

```
        PREGUNTA: "¿Hay un oso polar en el living?"
        
        Comportamiento Común de la IA:
        [ Error: No tengo información ]   ó   [ "Sí, detrás del sillón" (Alucinación) ]
        
        Nuestra Política de Ausencia Derivada:
        ┌────────────────────────────────────────────────────────────────────────┐
        │ Respuesta Certera: "NO" (Conteo: 0)                                   │
        │ Nota de Transparencia Epistémica:                                      │
        │ "El objeto no fue detectado en el plano visual disponible.             │
        │ Confianza derivada: 50% (No se certifica ausencia absoluta de fondo)." │
        └────────────────────────────────────────────────────────────────────────┘
```

#### El Problema
La mayoría de los sistemas de preguntas y respuestas visuales caen en dos extremos viciosos cuando se les pregunta por un objeto que no está en la foto:
- O inventan una respuesta afirmativa para complacer al usuario (alucinación).
- O se bloquean y devuelven un mensaje de error técnico del tipo *"información insuficiente"*, frustrando al usuario.

#### Nuestra Solución
Implementamos una **política de ausencia derivada formal**. Si el usuario pregunta por la existencia de una guitarra en una oficina y nuestro cartógrafo no tiene ninguna guitarra registrada:
1. El sistema responde con claridad: **"No hay ninguna"** (o conteo = 0).
2. Pero añade una **nota de auditoría epistémica**: declara que la ausencia se deriva de que el detector no la observó, reconociendo con humildad que el objeto podría estar fuera de campo o fuertemente tapado.

Esta simple innovación incrementó la precisión de respuesta a preguntas de existencia del **80% al 90%** y redujo las quejas del sistema por falta de información a niveles mínimos.

---

### Experimento Fallido: El "Arreglo Fantasma" de la Distorsión Cuadrada

#### La Hipótesis
Las fotografías de las cámaras suelen ser rectangulares (por ejemplo, 640×480 píxeles), pero los modelos de visión suelen exigir imágenes cuadradas (como 960×960 píxeles). Para convertir un rectángulo en cuadrado sin estirar la imagen, se le agregan bandas negras o grises a los costados (*padding*).
Supusimos que este relleno estaba descalibrando las coordenadas que devolvía el detector, por lo que escribimos un algoritmo matemático meticuloso para desarmar el relleno y corregir las cajas.

#### El Resultado Empírico
Al ejecutar las pruebas comparativas con y sin nuestro parche, **la diferencia en todas las métricas fue exactamente cero ($\Delta = 0,0000$)**.
Al investigar en profundidad el código fuente de la biblioteca de Hugging Face, descubrimos que la función oficial ya realizaba esa compensación internamente de forma silenciosa.

#### La Lección
**Verificar antes de asumir**. Gracias a que medimos con rigor científico antes de incorporar el cambio, evitamos introducir complejidad innecesaria en el código y comentamos la función para no gastar tiempo de cómputo en vano.

---

## 5. Los Números en Términos Humanos y el Impacto en el Mundo Real

### La Escalada Hacia la Cima Competitiva
A lo largo de semanas de desarrollo iterativo, medimos el rendimiento del sistema en cada transformación. El siguiente cuadro ilustra cómo cada decisión de ingeniería se tradujo en mejoras directas y tangibles:

```
========================================================================================================
                          PROGRESIÓN HISTÓRICA DEL RENDIMIENTO
========================================================================================================
 Indicador de Éxito            Versión 1           Versión 2           Versión 3 (Final)   Ganancia
                               (Línea Base)        (Calibración Fina)  (Multiescala + VQA) Neta Total
--------------------------------------------------------------------------------------------------------
 Puntería en Cajas (Box F1)    0,6464              0,6520              0,6722              +2,58 puntos
 Calidad de Siluetas (Mask F1) 0,6132              0,6200              0,6351              +2,19 puntos
 Exactitud en Preguntas (QA)   60,53%              60,53%              78,95%              +18,42% ¡SALTO!
 Comprensión de Descripciones  0,00%               0,00%               100,0%              +100% PERFECTO
 Puntuación en Kaggle (Test)   0,6615              0,6763              0,6926              +0,0311 ¡RÉCORD!
--------------------------------------------------------------------------------------------------------
 Tiempo por Foto (Latencia)    1,26 segundos       1,26 segundos       2,87 segundos       Compromiso justo
========================================================================================================
```

```
Evolución de la Exactitud en Preguntas y Respuestas (VQA):
100% ───────────────────────────────────────────────────────────── 100% (Descripciones V3)
 80% ────────────────────────────────────────────── 78.95% (QA Determinista V3)
 60% ─── 60.53% (Línea Base V1) ── 60.53% (V2)
 40%
 20%
  0% ─── 0.00% (Descripciones V1)
```

#### ¿Qué Significan Estos Números en la Práctica?
- **El Salto de Preguntas (+18,4%):** En la versión inicial, el sistema acertaba apenas 6 de cada 10 preguntas sobre la escena y fallaba rotundamente al intentar describir la imagen. En la versión final, responde con certeza casi 8 de cada 10 preguntas y logra una **comprensión perfecta (100%)** al interpretar pedidos de descripción en lenguaje natural (20 de 20 consignas validadas).
- **Puntuación en Kaggle de 0,6926:** Este puntaje oficial alcanzado en el conjunto de prueba (`submission.csv`, 80 imágenes) sitúa al sistema en el escalón más alto de la competencia académica, demostrando que la solución no solo funciona en el laboratorio, sino que generaliza con solidez sobre imágenes desconocidas que el modelo jamás había visto.
- **El Costo Asumido (2,87 segundos):** Procesar cada imagen en apenas 2,87 segundos permite resolver el conjunto completo de 80 imágenes de prueba en menos de 4 minutos sobre una GPU estándar, garantizando una respuesta ágil mientras se erradican los errores visuales y las alucinaciones.

---

### ¿Para Qué Sirve Todo Esto? Aplicaciones en el Mundo Real

La arquitectura neuro-simbólica que desarrollamos no es un mero ejercicio académico; es la base operativa de tecnologías críticas que transformarán diversas industrias en los próximos años:

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                    APLICACIONES INDUSTRIALES DE ALTO IMPACTO                            │
└─────────────────────────────────────────────────────────────────────────────────────────┘

  🚗 VEHÍCULOS AUTÓNOMOS Y SEGURIDAD VIAL
  Un vehículo no puede permitirse "alucinar" un obstáculo ni confundir una sombra con un
  peatón. Nuestro sistema cartografía la calle en regiones estrictas, sabe con exactitud
  dónde está la bicicleta a la izquierda y certifica matemáticamente si el carril está libre.

  🏭 INSPECCIÓN Y CONTROL DE CALIDAD EN FÁBRICAS
  En una línea de ensamblaje de motores o placas electrónicas, una cámara con nuestra
  "lupa multiescala" localiza tornillos diminutos (menores al 1% de la imagen), cuenta las
  piezas colocadas sin errar una sola unidad y audita que cada cable esté en su posición.

  🤖 ROBÓTICA COLABORATIVA Y LOGÍSTICA
  Un brazo robótico en un almacén inteligente necesita algo más que saber qué paquete agarrar:
  necesita saber su silueta milimétrica para orientar su pinza mecánica y conocer sus
  relaciones espaciales para no derribar las cajas linderas.

  🏥 ASISTENCIA MÉDICA Y TRAZABILIDAD QUIRÚRGICA
  En un quirófano, un sistema que asiste al equipo médico debe contabilizar gasas y pinzas
  con certeza absoluta antes de cerrar una intervención. El enfoque neuro-simbólico no
  "cree" que están todas: verifica formalmente que cada elemento esté presente y en su sitio.
```

---

## 6. Glosario de Analogías Intuitivas

Para que cualquier persona —desde un estudiante que recién comienza hasta un directivo de empresa— pueda comunicarse fluidamente con los ingenieros del proyecto, compilamos este diccionario de traducciones intuitivas:

```
========================================================================================================
                          DICCIONARIO DE TRADUCCIÓN TÉCNICA - INTUITIVA
========================================================================================================
 Término Técnico        La Metáfora Cotidiana       ¿Qué Hace en Realidad?
--------------------------------------------------------------------------------------------------------
 Bounding Box           El marco de fotos           Un rectángulo provisional con coordenadas (X, Y)
                        preliminar                  que indica dónde está el objeto aproximadamente.

 Máscara de             El recorte con tijera       La silueta coloreada píxel por píxel que separa
 Segmentación           de precisión quirúrgica     el cuerpo del objeto del fondo y de sus vecinos.

 Open-Vocabulary        El detective con internet   Un modelo que busca cualquier cosa escrita en
 (Vocabulario Abierto)  y sin lista fija            lenguaje natural, sin estar atado a clases fijas.

 SceneJSON              El plano catastral          Un archivo de texto ordenado que guarda todos los
                        del agrimensor              objetos, posiciones, colores y relaciones de la foto.

 Neuro-Simbólico        El matrimonio entre el ojo  La unión entre una red neuronal que percibe formas
                        artístico y la calculadora  y un motor lógico que cuenta y razona sin fallar.

 Non-Maximum            El árbitro que expulsa a    Un filtro matemático que elimina rectángulos
 Suppression (NMS)      los mirones duplicados      repetidos que compiten por el mismo objeto físico.

 Intersection over      La prueba de coincidencia   Una fórmula que mide qué porcentaje de la silueta
 Union (IoU)            de dos calcomanías          detectada encaja exactamente sobre la silueta real.

 F1-Score               El promedio exigente que    Una nota de examen que promedia aciertos y faltas,
                        no perdona a los tramposos  castigando duro a los modelos que inventan de más.

 Tiling Multiescala     La lupa del inspector       Dividir la imagen en 4 partes ampliadas para
 (Mosaicos)             de joyas                    descubrir objetos minúsculos sin perder resolución.

 Alucinación Visual     El cuento del loro          Cuando una IA generativa inventa objetos o
                        charlatán                   cantidades que no existen en la imagen para salir del paso.

 Política de Ausencia   El testimonio honesto       Responder con seguridad "no está" reconociendo que
 Derivada               del testigo prudente        no fue visto, en lugar de bloquearse o mentir.

 PipelineTracer         La caja negra indestructible  Un sistema de registro que anota cada segundo,
                        de un avión comercial       parámetro y fallo para que el trabajo sea auditable.
========================================================================================================
```

---

## 7. Conclusión y Mirada al Futuro

El proyecto desarrollado para el TPI de Inteligencia Artificial Primavera 2026 demuestra que **el verdadero progreso de la visión artificial no consiste en construir modelos cada vez más gigantescos y oscuros, sino en diseñar arquitecturas inteligentes que sepan coordinar la intuición visual con la verdad lógica**.

Al combinar la versatilidad de los detectores de vocabulario abierto, la fineza milimétrica de los modelos de segmentación fundacional, la cartografía topológica estructurada y el razonamiento determinista libre de alucinaciones, logramos un sistema que no solo compite con éxito en los rankings cuantitativos, sino que ofrece aquello que la sociedad y la industria le exigen a la tecnología del mañana: **confianza, explicabilidad y rigor científico.**

---
*Documento explicativo conceptual elaborado por el Grupo 21 — Cátedra de Inteligencia Artificial — UTN FRC (Primavera 2026)*  
*Docentes evaluadores: Ing. García, Mario Alejandro | Ing. Guzman, Analía | Ing. Gramatica, Martin*  
*Informe técnico oficial: `INFORME_TPI_IA_2026P_21.md` | Inferencia y submission: `submission.csv` (Score: 0,6926) | Código: `tpi-ia-2026p-21.ipynb`.*
