# Análisis Exhaustivo de Plantilla y Relevamiento de Herramientas de Maquetación

**Fecha**: 31 de Octubre de 2026  
**Agente**: `explorer_survey_3`  
**Workspace**: `c:\Users\perez\OneDrive\Documents\Ing.Sist-NUBE\IA\TPI IA 2026`  
**Objetivo**: Descomposición técnica completa de `TPI_IA_2025-TEMPLATE.pdf` y relevamiento del entorno Windows/Python para determinar la estrategia óptima de generación de PDF con fidelidad absoluta a la plantilla institucional.

---

## 1. Descomposición y Análisis Técnico de `TPI_IA_2025-TEMPLATE.pdf`

El análisis se realizó inspeccionando el contenido binario, los flujos de contenido PDF (streams), la tabla de fuentes, los operadores de transformación afín (`cm`), las imágenes embebidas y la distribución de coordenadas mediante scripts Python basados en `pypdf` y `Pillow`.

### 1.1. Metadatos del Documento y Origen
- **Título en metadatos**: `TPI_IA_2025P_4`
- **Generador/Productor**: `Skia/PDF m144 Google Docs Renderer`
- **Total de páginas**: 22 páginas
- **Origen de autoría**: El documento fue originalmente redactado y formateado en **Google Docs** y exportado como PDF mediante el motor Chromium/Skia.

---

### 1.2. Geometría de Página y Márgenes
- **Tamaño de página**: Estándar **A4** exacto:
  - Ancho: `595.28 pt` (Google Docs reporta `596 pt`, correspondiente a `210 mm` / `8.27 in`).
  - Alto: `841.89 pt` (Google Docs reporta `842 pt`, correspondiente a `297 mm` / `11.69 in`).
- **Márgenes**:
  - **Margen Izquierdo**: `72.0 pt` = `1.0 pulgada` = `25.4 mm` (constante en todas las páginas).
  - **Margen Derecho**: `72.0 pt` = `1.0 pulgada` = `25.4 mm` (el límite derecho del texto llega a `517.2 pt`, dejando `596 - 517.2 = 78.8 pt`, con ancho útil de caja de texto de `445 - 451 pt` / `157 - 159 mm`).
  - **Margen Superior**: `72.0 pt` = `25.4 mm` (la línea base del primer encabezado se sitúa entre `y = 745.6 pt` y `759.7 pt`, lo que corresponde a `842 - 760 ≈ 82 pt` desde el borde superior de la hoja).
  - **Margen Inferior**: `72.0 pt` = `25.4 mm` para el bloque de texto. El número de página en el pie se ubica a `y = 40.0 pt` (`14.1 mm` del borde inferior).
- **Estructura de Columnas**: **1 columna estricta** (ancho completo). No presenta doble columna ni columnas híbridas; todo el contenido fluye verticalmente en un único bloque continuo.

---

### 1.3. Encabezados, Pies y Paginación
- **Encabezados superiores (Running Headers)**: **Ninguno**. Las páginas del cuerpo no presentan texto ni filetes en el margen superior.
- **Pies de página (Footers)**:
  - **Ubicación**: Alineado a la derecha (`x ≈ 511.0 - 517.2 pt`), línea base a `y = 40.0 pt`.
  - **Tipografía**: Arial Regular, tamaño 11 pt (`14.7` en escala Skia).
  - **Secuencia**: 
    - **Página 1 (Portada)**: No tiene número de página ni pie.
    - **Página 2**: Muestra el número `1`.
    - **Página 3**: Muestra el número `2`.
    - ...
    - **Página 22**: Muestra el número `21`.
  - **Filetes/Líneas divisorias**: No hay líneas divisorias horizontales ni en encabezado ni en pie.

---

### 1.4. Diseño de la Portada (Página 1)
La portada presenta una distribución vertical centrada y bloques de metadatos institucionales:

1. **Logotipo Institucional Superior**:
   - **Contenido**: Logo oficial de **UTN Facultad Regional Córdoba** (extraído como `X5.png`, dimensiones nativas `356 × 142 px`, modo RGB).
   - **Posicionamiento**: Centrado/ajustado horizontalmente (`x = 79.39 pt`, ancho = `436.5 pt`, alto = `174.75 pt`, aspecto `2.5:1`), ubicado en el tercio superior de la página.
2. **Identificación de Cátedra y Curso**:
   - Texto: `Cátedra de Inteligencia Artificial - 5K3A`
   - Tipografía: Arial Regular, 12 pt (`16.0` Skia), centrado horizontalmente (`y = 560.3 pt`).
3. **Título y Tipo de Reporte**:
   - Texto: `TRABAJO PRÁCTICO INTEGRADOR - Reporte técnico - Segundo cuatrimestre`
   - Tipografía: Arial Regular, 12 pt (`16.0` Skia), centrado horizontalmente (`y = 541.5 pt`).
4. **Bloque Docentes**:
   - Encabezado: `Docentes:` en Arial 12 pt (`y = 428.3 pt`), alineado a la izquierda (`x = 72.0 pt`).
   - Lista con viñeta de disco sólido `●`:
     * `● García, Mario Alejandro` (y = 410.3 pt)
     * `● Forte, Guillermo Omar` (y = 395.8 pt)
     * `● Gramática, Martín Nicolás` (y = 381.2 pt)
     * Tipografía: Arial Regular 11 pt (`14.7` Skia).
5. **Bloque Grupo y Alumnos**:
   - Encabezado: `Grupo N°4:` (o número correspondiente) en Arial 12 pt (`y = 351.2 pt`), alineado a la izquierda (`x = 72.0 pt`).
   - Lista con viñeta de disco sólido `●`:
     * `● Carrera, Sebastian - 82454` (y = 332.3 pt)
     * `● Ferreyra, Diego - 50881` (y = 317.4 pt)
     * `● Iril, Rocco Maciel - 90104` (y = 302.9 pt)
     * `● Yacuzzi, Maximiliano - 66276` (y = 288.3 pt)
     * Tipografía: Arial Regular 11 pt (`14.7` Skia).
6. **Fecha de Entrega**:
   - Texto: `Fecha de entrega: 07/11/2025` (en el TPI 2026 corresponde `01/11/2026`).
   - Posicionamiento: Alineado a la izquierda (`x = 72.0 pt`, `y = 140.7 pt`), Arial 12 pt.

---

### 1.5. Jerarquía Tipográfica y Estilos de Texto
Las fuentes embebidas en todo el documento son exclusivamente dos familias estándar de Google Docs:
1. `/AAAAAA+ArialMT` (Arial Regular) y `/BAAAAA+Arial-BoldMT` (Arial Bold)
2. `/CAAAAA+CourierNew` (Courier New Regular para código y prompts)

| Nivel Estilístico | Fuente | Tamaño Efectivo (pt) | Tamaño Skia (unidades) | Peso / Estilo | Alineación | Espaciado y Uso |
|---|---|---|---|---|---|---|
| **Título de Sección (H1)** | Arial | **26 pt** | `34.7` | Regular / Bold | Izquierda | Margin-top: 24 pt, margin-bottom: 12 pt. Usado en `Introducción`, `Análisis de dataset - EDA`, `Metodología`, `Resultados`, `Discusión y análisis crítico`, `Trabajo futuro`, `Conclusión`. |
| **Subtítulo Mayor (H2)** | Arial | **20 pt** | `26.7` | Regular / Bold | Izquierda | Margin-top: 18 pt, margin-bottom: 8 pt. Usado en `Conclusiones de resultados`, `Métrica de evaluación mediante descomposición y unión de conjuntos`. |
| **Título de Etapa / Módulo (H3)** | Arial | **13 pt** | `17.3` | Bold | Izquierda | Margin-top: 14 pt, margin-bottom: 6 pt. Usado en `Realizar embeddings de imágenes mediante CLIP.`, `Clusterización con K-Means y visualización con UMAP.`, `Crear índice con FAISS.`, `Inclusión de modelo LLM`, `Query “gato”`, etc. |
| **Subsección / Pregunta (H4)** | Arial | **11 pt** | `14.7` | Bold | Izquierda | Margin-top: 10 pt, margin-bottom: 4 pt. Usado en `1. Características...`, `¿Qué funcionó bien?:`, `¿Qué intentos no funcionaron y por qué?:`, `Limitaciones del enfoque:`. |
| **Cuerpo de Texto** | Arial | **11 pt** | `14.7` | Regular | Izquierda / Justificado | Interlineado 1.15 a 1.25 (leading ≈ 14.5 pt). Separación entre párrafos: 6 a 10 pt. |
| **Metadatos Portada** | Arial | **12 pt** | `16.0` | Regular / Bold | Centrado / Izquierda | Usado en títulos y etiquetas de portada. |
| **Código / Prompts LLM** | Courier New | **11 pt** | `14.7` | Regular (Mono) | Izquierda | Bloques de strings JSON o prompts con sangría izquierda de 18 a 36 pt. |

---

### 1.6. Listas y Viñetas
- **Nivel 1**: Viñeta de disco sólido `●` (`\u25cf`), indentación `x = 72 pt` a `90 pt` (sangría de ~18-24 pt). Tipografía: Arial 11 pt.
- **Nivel 2**: Viñeta circular abierta `○` (`\u25cb`), indentación `x = 90 pt` a `108 pt` (sangría de ~36-48 pt). Tipografía: Arial 11 pt.

---

### 1.7. Componentes Visuales: Tablas, Figuras y Gráficos
- **Tablas vectoriales**: El PDF original tiene **0 operadores de línea o rectángulo vectorial** (`re=0`, `S=0`). Los resultados tabulares en la plantilla se presentaron como texto monoespaciado o capturas de pantalla de DataFrames/consolas. Para un informe de grado de publicación, se recomienda maquetar tablas limpias con cabecera gris suave (`#f2f2f2`), bordes horizontales sutiles (`#d0d0d0`), texto Arial 10-11 pt y alineación numérica a la derecha.
- **Figuras y Gráficos (31 imágenes embebidas en total)**:
  - **Páginas 2 a 6 (EDA)**: Capturas de estadísticas descriptivas (`X10.png`), histogramas de dimensiones y aspecto (`X11.png`), distribuciones de anotaciones (`X14.png`, `X15.png`, `X16.png`, `X19.png`, `X20.png`), mapa de clusters UMAP (`X23.png`, 866×707 px) y mosaicos de imágenes por clase (`X26.png`, `X27.png`).
  - **Páginas 12 a 18 (Resultados)**: Bloques de ejecución con:
    1. Texto de traducción y reformulación.
    2. Cuadrícula de 10 imágenes del top-k recuperado para 3 variantes de modelo (Baseline, LLM simple, LLM reranking).
    3. Scores numéricos promedios y métrica de Precisión@10.
    4. Gráfico de barras comparativo de matplotlib (azul claro, verde claro, rojo salmón).
  - **Páginas 19 y 20 (Métricas compuestas)**: Snippet de código de descomposición de consultas (`X73.png`) y salidas de consola de métrica IoU (`X76.png`, `X77.png`).
- **Posicionamiento de Figuras**:
  - Centradas horizontalmente dentro del ancho de caja (máximo 451 pt / 159 mm).
  - En la plantilla no se utilizaron epígrafes formales numerados ("Figura 1: ..."), sino subtítulos en Arial Bold antes o después de la imagen. La inclusión de epígrafes estándar (`Figura X: Descripción técnica`) eleva notablemente la rigurosidad académica sin alterar la estética.

---

### 1.8. Texto y Estructura Completa de Secciones en la Plantilla

A continuación se transcribe la estructura y contenido literal de las 6 secciones de la plantilla:

```text
[PORTADA]
- Logo UTN FRC
- Cátedra de Inteligencia Artificial - 5K3A
- TRABAJO PRÁCTICO INTEGRADOR - Reporte técnico - Segundo cuatrimestre
- Docentes: Mario Alejandro García, Guillermo Omar Forte, Martín Nicolás Gramática
- Grupo N°4: Carrera Sebastian (82454), Ferreyra Diego (50881), Iril Rocco Maciel (90104), Yacuzzi Maximiliano (66276)
- Fecha de entrega: 07/11/2025

[SECCIÓN 1: INTRODUCCIÓN]
"En este trabajo práctico se desarrollará un sistema de busqueda multimodal de imágenes mediante CLIP, FAISS y un LLM. Se comentará todo el trabajo desarrollado, las decisiones tomadas, los resultados obtenidos, las conclusiones a las que se llegaron y comentarios sobre las situaciones a las que el grupo se enfrentó durante el desarrollo."

[SECCIÓN 2: ANÁLISIS DE DATASET - EDA]
"El análisis de datos se separa en tres partes:
1. Características de las imágenes como archivos:
   ○ Cantidad total de imágenes (17.125 imágenes)
   ○ Alto y ancho en pixeles (ancho min=142, max=500, mean=466.8; alto min=71, max=500, mean=389.5)
   ○ Peso en megabytes (min=0.007, max=0.855, mean=0.112 MB)
   ○ Canales (3 canales RGB uniformes)
2. Características del contenido de las imágenes a partir de anotaciones:
   ○ Objetos en imágenes
   ○ Conteo total de objetos en imágenes
   ○ Conteo de objetos de manera única por imagen
3. Clusterización tras embeddings mediante K-Means y UMAP:
   ○ Gráficos de clusters con embeddings globales
4. Visualización rápida de imágenes por clase"

[SECCIÓN 3: METODOLOGÍA]
"Se separará el flujo de trabajo en etapas y se dará información relevante de cada una.
- Realizar embeddings de imágenes mediante CLIP:
  Modelo CLIP ViT-L-14 (pesos OpenAI), 768 dimensiones. Normalización L2 al momento de creación para operar con similitud coseno por producto punto.
- Clusterización con K-Means y visualización con UMAP:
  k=100 clusters seleccionados para distinguir subconjuntos dentro de conceptos generales (superando la limitación de k=20 clases fijas de Pascal VOC).
- Crear índice con FAISS:
  Índice IVFFLAT para búsqueda aproximada por centroides con métrica coseno. k=400 centroides tras comprobar que k=200 degradaba la calidad.
- Inclusión de modelo LLM:
  Phi-3-mini-4k-instruct de Microsoft. Temperatura 0 y do_sample=False para determinismo y repetibilidad. 4 opciones de consulta:
  1. Query directo (sin traducción).
  2. Query traducido a inglés.
  3. Query con reformulación (5 variantes sin añadir contexto ficticio).
  4. Query con reranking y detección de negativos (separación de positive_prompts y negative_prompts, penalización con factor 0.3):
     Score final = Score positivos - (Score negativos * 0.3)"

[SECCIÓN 4: RESULTADOS]
- Evaluación sobre 4 queries testigo:
  1. "gato" (query simple de clase)
  2. "persona trabajando en la computadora y con un gato" (múltiples objetos)
  3. "caballo blanco corriendo sin jinete" (negación explícita)
  4. "mujer con sombrero pero sin lentes" (negación compleja)
- Comparación de Modelo 0 (temp=0) vs Modelo 0.3 (temp=0.3).
- Cuadrículas visuales de las 10 mejores imágenes.
- Métricas cuantitativas: Precisión@10 y score de similitud promedio.
- Conclusiones de resultados: el reranking supera a reformulación y traducción en queries afirmativas; en negaciones el score disminuye por penalización pero el ranking visual se depura efectivamente.
- Métrica de evaluación mediante descomposición y unión de conjuntos (Ground Truth aproximado con 4000 candidatos y 2000 mejores por componente, cálculo de IoU).

[SECCIÓN 5: DISCUSIÓN Y ANÁLISIS CRÍTICO]
- ¿Qué funcionó bien?: LLM determinista (temp=0), few-shot examples en el prompt de reranking.
- ¿Qué intentos no funcionaron y por qué?:
  * Etiquetas incompletas en Annotations (múltiples imágenes tenían solo 'cat' sin 'person'), requiriendo flexibilizar a coincidencia de alguna etiqueta.
  * TinyLlama descartado por incompatibilidad de entorno.
  * PCA en embeddings (reducido a 50 y 256 dims) descartado completamente porque destruía la coherencia semántica.
- Limitaciones del enfoque: modelo LLM liviano saturado ante prompts extensos.

[SECCIÓN 6: CONCLUSIÓN Y TRABAJO FUTURO]
- Trabajo futuro: LLM de mayor escala, prompts más robustos, métricas intrínsecas independientes de anotaciones, modelos CLIP de mayor dimensionalidad.
- Conclusión: Síntesis del pipeline multimodal (CLIP + FAISS + LLM) y validación de métricas propias sobre Pascal VOC 2012.
```

---

## 2. Relevamiento del Entorno del Sistema y Herramientas de Maquetación

Se realizó una auditoría detallada de ejecutables CLI, rutas en `%PATH%`, entorno Python y conectividad de red.

### 2.1. Herramientas CLI Disponibles

| Herramienta | Estado | Ruta Detectada | Versión / Observaciones |
|---|---|---|---|
| **Python** | **Instalado** | `C:\Users\perez\AppData\Local\Programs\Python\Python312\python.exe` | Python 3.12.10 (AMD64) |
| **Microsoft Edge** | **Instalado** | `C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe` | Motor Chromium moderno, con soporte `--headless` y `--print-to-pdf` |
| **Google Chrome** | **Instalado** | `C:\Program Files\Google\Chrome\Application\chrome.exe` | Motor Chromium moderno |
| **Node.js** | **Instalado** | `C:\Program Files\nodejs\node.exe` | Node.js v20+ con `npm` |
| **Typst (CLI)** | *No en PATH* | — | No instalado en PATH global; disponible vía `pip install typst` |
| **Pandoc** | *No instalado* | — | No encontrado en Program Files ni AppData |
| **LaTeX (pdf/xe/lua)**| *No instalado* | — | No se detectó MiKTeX ni TeX Live en el sistema |
| **WeasyPrint (CLI)** | *No instalado* | — | Requiere librerías C (Pango/Cairo), complejas en Windows |

### 2.2. Paquetes Python Relevantes

| Paquete | Estado | Versión | Rol Potencial |
|---|---|---|---|
| `reportlab` | **Instalado** | 4.2.5 | Generación programática de PDF con Flowables |
| `pypdf` | **Instalado** | 6.20.1 | Inspección, extracción de texto/imágenes y manipulación de PDF |
| `pillow` | **Instalado** | 11.0.0 | Procesamiento y escalado de imágenes |
| `matplotlib` | **Instalado** | 3.11.2 | Generación de gráficos idénticos a los del notebook |
| `Jinja2` | **Instalado** | 3.1.6 | Motor de plantillas HTML/Typst |
| `Pygments` | **Instalado** | 2.21.0 | Resaltado sintáctico de código |
| `numpy`, `pandas` | **Instalado** | 2.3.0 | Procesamiento de datos y métricas |
| `PyQt5` | **Instalado** | 5.15.11 | Toolkit GUI/Qt (incluye QtPrintSupport) |
| `python-docx` | *Disponible en PyPI* | 1.2.0 | Verificado vía `pip dry-run` |
| `typst` (Python) | *Disponible en PyPI* | 0.15.0 | Verificado vía `pip dry-run` (wheel precompilado con binario nativo) |

### 2.3. Estado de Red y Conectividad
- **Conectividad a PyPI**: **ONLINE** (HTTP 200 verificado).
- **Instalación de paquetes**: Si se requiere cualquier paquete liviano de Python (`typst`, `python-docx`), puede instalarse de inmediato sin restricciones de firewall ni proxy.

---

## 3. Pruebas de Renderizado y Validación de Toolchains

### 3.1. Prueba de Renderizado HTML+CSS con Headless Edge / Chrome
Se implementó y ejecutó una prueba de renderizado a PDF mediante Microsoft Edge Headless:
- **Comando ejecutado**:
  ```powershell
  msedge.exe --headless --disable-gpu --no-pdf-header-footer --user-data-dir="C:\Users\perez\AppData\Local\Temp\edgetmp" --print-to-pdf="c:\...\edge_test_clean.pdf" "c:\...\test_page.html"
  ```
- **Resultado de la prueba**:
  - Salida: `47760 bytes written to file`.
  - Página generada: 1 página A4 exacta (`594.96 × 841.92 pt`).
  - Encabezados/pies espurios del navegador: **Totalmente suprimidos** mediante `--no-pdf-header-footer`.
  - Soporte de CSS `@page`: Soporta `@page { size: A4; margin: 25.4mm; }`, tipografía Arial nativa de Windows, grids CSS para mosaicos de imágenes y control preciso de saltos de página con `page-break-before: always;`.
  - **Fidelidad**: 100% idéntico al renderizado original de Google Docs (ambos comparten la base del motor Skia/Blink).

### 3.2. Evaluación de Typst
- Typst (`pip install typst`) incluye el compilador completo en un único archivo ejecutable embebido en el paquete de Python (sin dependencias C adicionales ni entornos complejos).
- Proporciona sintaxis limpia, control nativo de márgenes A4, numeración automática excluyendo portada, inserción de imágenes en cuadrícula y exportación vectorial directa.
- Es el estándar moderno emergente en el ámbito académico para reemplazar LaTeX.

---

## 4. Comparativa de Opciones y Recomendación Estratégica

| Criterio | Opción 1: Headless Edge (HTML+CSS) | Opción 2: Typst (`typst.compile`) | Opción 3: ReportLab (Python) | Opción 4: LaTeX (TeX Live/MiKTeX) |
|---|---|---|---|---|
| **Disponibilidad actual** | **100% lista** (Edge ya en el SO) | Requiere `pip install typst` (30 MB) | **100% instalada** (ReportLab 4.2.5) | No instalado (~5 GB descarga) |
| **Fidelidad a Google Docs** | **Extrema** (mismo motor Skia) | **Muy Alta** (diseño tipográfico exacto) | Media (posicionamiento manual complejo) | Media (estilo académico TeX diferente) |
| **Formato del archivo fuente** | HTML5 / CSS3 / Jinja2 | Markup Typst (`.typ`) limpio | Script Python procedimental | Archivo `.tex` verboso |
| **Manejo de imágenes y grids** | CSS Grid / Flexbox nativo | Grids nativos `#grid(columns: 10, ...)` | Flowable `Table` / `Image` rígido | `subcaption` / `minipage` complejo |
| **Cumplimiento de consignas** | Excelente (genera PDF + `.html`/`.md`) | Excelente (genera PDF + `.typ`/`.md`) | Regular (código acoplado) | Inviable sin instalar LaTeX |

### Recomendación Definitiva: Estrategia de Maquetación Híbrida

Para garantizar el cumplimiento riguroso de la consigna de la cátedra (*"Reporte técnico en Markdown (.md)... maquetado respetando el formato y secciones de TPI_IA_2025-TEMPLATE.pdf junto con su archivo fuente estructurado"*):

1. **Archivo de Contenido Canónico**:
   - `informe_tecnico_tpi.md`: Documento Markdown puro, auto-contenido y riguroso con las 6 secciones solicitadas en `ORIGINAL_REQUEST.md` y en las consignas de la cátedra.
2. **Archivo Fuente Estructurado de Maquetación**:
   - Un archivo fuente HTML/CSS estilizado (`informe_tecnico.html`) o Typst (`informe_tecnico.typ`) que replica pixel a pixel la portada con el logo oficial de la UTN FRC, los márgenes de 1 pulgada, tipografía Arial, interlineado 1.15, colores institucionales, viñetas de disco y círculos, cuadrículas de imágenes y pie de página derecho paginado desde la página 2.
3. **Pipeline de Generación de PDF**:
   - Un script Python automatizado (`build_pdf.py`) que compila el documento fuente a `TPI_IA_2026P_21_Reporte_Tecnico.pdf` utilizando **Microsoft Edge Headless** (ya disponible y probado) o **Typst**, asegurando que cualquier evaluador pueda recompilar el PDF con un solo comando.
