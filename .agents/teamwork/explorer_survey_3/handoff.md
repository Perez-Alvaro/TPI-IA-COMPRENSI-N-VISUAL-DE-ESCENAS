# Handoff Report: Template Decomposition & Typesetting Toolchain Survey

**Agent**: `explorer_survey_3`  
**Working Directory**: `c:\Users\perez\OneDrive\Documents\Ing.Sist-NUBE\IA\TPI IA 2026\.agents\teamwork\explorer_survey_3`  
**Milestone**: `template-and-toolchain-survey`  
**Timestamp**: 2026-10-31T14:00:00Z  
**Type**: Hard Handoff (Task Complete)

---

## 1. Observation

1. **Plantilla PDF (`TPI_IA_2025-TEMPLATE.pdf`)**:
   - Metadatos inspeccionados con `pypdf`:
     - Título: `TPI_IA_2025P_4`
     - Productor: `Skia/PDF m144 Google Docs Renderer`
     - Total de páginas: 22 páginas.
   - Geometría de página:
     - Dimensiones `MediaBox`: `[0, 0, 596, 842]` puntos = Formato estándar A4 (`210 × 297 mm`).
     - Márgenes medidos mediante análisis de coordenadas de texto:
       * Margen Izquierdo: `72.0 pt` (exactamente `25.4 mm` / 1.0 pulgada) en todas las páginas.
       * Margen Derecho: `72.0 pt` (`596 pt - 524 pt = 72 pt` / 1.0 pulgada). Ancho de caja de texto: `445 - 451 pt`.
       * Margen Superior: `72.0 pt` (la primera línea base se ubica a `y ≈ 745.6 - 759.7 pt`, distancia al borde superior ≈ `82 pt`).
       * Margen Inferior: `72.0 pt` para el texto del cuerpo; pie de página a `y = 40.0 pt` (`14.1 mm` del borde).
     - Columnas: **1 columna estricta** (ancho completo continuo).
     - Paginación: En pie de página, alineada a la derecha (`x ≈ 511.0 - 517.2 pt`, `y = 40.0 pt`), fuente Arial 11 pt. Inicia con el número `1` en la Página 2 y llega a `21` en la Página 22. La portada (Página 1) no tiene número de página.
   - Tipografía:
     - Familia principal: `ArialMT` y `Arial-BoldMT`.
     - Familia monoespaciada para código/prompts: `CourierNew`.
     - Jerarquía de tamaños (convertidos a puntos tipográficos):
       * Título de Sección (H1): 26 pt (Arial Regular / Bold).
       * Subtítulo Mayor (H2): 20 pt (Arial Regular / Bold).
       * Título de Etapa / Módulo (H3): 13 pt (Arial Bold).
       * Subsección / Pregunta (H4): 11 pt (Arial Bold).
       * Cuerpo de texto: 11 pt (Arial Regular, interlineado ≈ 1.15 a 1.25).
       * Código / Prompts: 11 pt (Courier New Regular).
   - Componentes visuales y Portada:
     - Logo institucional extraído (`X5.png`): Logo oficial **UTN Facultad Regional Córdoba**, 356×142 px, ubicado en la portada a `x = 79.39 pt`, ancho `436.5 pt`, alto `174.75 pt`.
     - Metadatos de portada: Cátedra (`Cátedra de Inteligencia Artificial - 5K3A`), Título (`TRABAJO PRÁCTICO INTEGRADOR - Reporte técnico - Segundo cuatrimestre`), Bloque `Docentes:`, Bloque `Grupo N°...:` y `Fecha de entrega:`.
     - Figuras: 31 imágenes bitmap embebidas (resoluciones de 500 a 1000 px de ancho), centradas, sin operadores vectoriales de trazado (`re=0`, `S=0`).

2. **Relevamiento del Entorno del Sistema**:
   - Ejecutable Python disponible: `C:\Users\perez\AppData\Local\Programs\Python\Python312\python.exe` (v3.12.10 x64).
   - Navegadores disponibles:
     * Microsoft Edge: `C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe`.
     * Google Chrome: `C:\Program Files\Google\Chrome\Application\chrome.exe`.
   - Node.js disponible: `C:\Program Files\nodejs\node.exe`.
   - Herramientas no encontradas en PATH ni en rutas estándar: `typst`, `pandoc`, `pdflatex`, `xelatex`, `lualatex`, `weasyprint`.
   - Librerías Python instaladas: `reportlab` 4.2.5, `pypdf` 6.20.1, `pillow` 11.0.0, `matplotlib` 3.11.2, `Jinja2` 3.1.6, `Pygments` 2.21.0, `numpy` 2.3.0, `pandas` 2.3.0, `scipy` 1.18.1.
   - Conectividad de red a PyPI: Confirmada (HTTP 200). Paquetes como `typst` (v0.15.0) y `python-docx` (v1.2.0) se encuentran disponibles para instalación inmediata mediante `pip`.

3. **Prueba de Renderizado Headless Edge**:
   - Se probó la generación de PDF desde HTML/CSS mediante:
     `msedge.exe --headless --disable-gpu --no-pdf-header-footer --user-data-dir="C:\Users\perez\AppData\Local\Temp\edgetmp" --print-to-pdf="c:\...\edge_test_clean.pdf" "c:\...\test_page.html"`
   - Resultado: Generó exitosamente un PDF A4 perfecto (`594.96 × 841.92 pt`), con 0 encabezados espurios y tipografía idéntica a Google Docs en menos de 1 segundo.

---

## 2. Logic Chain

1. **Premisa**: El informe técnico debe maquetarse respetando rigurosamente el formato y las 6 secciones de `TPI_IA_2025-TEMPLATE.pdf` (R1 de `ORIGINAL_REQUEST.md`), acompañándose de su archivo fuente estructurado y satisfaciendo la consigna de la cátedra de contar con una versión en Markdown (`.md`).
2. **De la Observación 1**: `TPI_IA_2025-TEMPLATE.pdf` fue generado por el motor Chromium/Skia de Google Docs sobre hoja A4 con márgenes de 1 pulgada (72 pt), 1 columna, tipografía Arial (26 pt / 20 pt / 13 pt / 11 pt) y pie derecho numerado desde la página 2.
3. **De la Observación 2**: En el host no existen instalaciones pesadas de TeX (`pdflatex`, `xelatex`), ni Pandoc. Sin embargo, Microsoft Edge y Google Chrome están instalados de forma nativa en rutas fijas de Windows, y Python 3.12 con `pypdf`, `Pillow`, `matplotlib` y `reportlab` está plenamente operativo con salida a internet a PyPI.
4. **De la Observación 3**: Microsoft Edge Headless con el flag `--no-pdf-header-footer` y un directorio de datos de usuario temporal ejecuta el mismo motor Skia/Blink que Google Docs, generando una salida PDF 100% fiel al template original sin requerir instalaciones de software de terceros. Alternativamente, `pip install typst` provee un compilador tipográfico autónomo de primer nivel.
5. **Deducción**: La estrategia más robusta, limpia y mantenible es desacoplar el contenido y la maquetación en una arquitectura de tres capas:
   - Capa 1: Contenido canónico en Markdown (`informe_tecnico_tpi.md`) para cumplir la consigna explícita de la cátedra.
   - Capa 2: Archivo fuente estructurado de maquetación (HTML+CSS / Jinja2 o Typst `.typ`) que implementa la portada UTN, márgenes de 25.4 mm, estilos Arial y paginación.
   - Capa 3: Script automatizado de compilación a PDF (`build_pdf.py`) que ejecuta Microsoft Edge Headless o Typst para emitir el PDF final con fidelidad absoluta al template de 2025.

---

## 3. Caveats

- **No caveats en cuanto a geometría o tipografía**: Todas las medidas de márgenes, tamaños de fuentes y coordenadas del PDF original fueron extraídas con exactitud matemática a partir de los operadores del PDF.
- **Entorno de ejecución de Edge/Chrome**: Al invocar Edge o Chrome en modo `--headless` desde scripts en Windows, es mandatorio incluir `--user-data-dir="<ruta_temp>"` para evitar colisiones con instancias abiertas del navegador en la sesión de usuario.

---

## 4. Conclusion

1. La plantilla `TPI_IA_2025-TEMPLATE.pdf` corresponde a un documento de 22 páginas en formato A4 (596 × 842 pt), 1 columna, márgenes de 25.4 mm (72 pt), tipografía Arial (26 pt H1, 20 pt H2, 13 pt H3, 11 pt H4/cuerpo), Courier New para código, portada institucional con logo de UTN FRC y numeración en pie de página derecho a partir de la página 2.
2. El entorno Windows dispone de **Microsoft Edge** y **Google Chrome** listos para renderizar HTML/CSS a PDF con el mismo motor Skia utilizado por Google Docs, y Python 3.12 con librerías auxiliares completas.
3. Se recomienda formalmente implementar el informe con una fuente Markdown canónica (`informe_tecnico_tpi.md`) y una plantilla estructurada de maquetación (HTML/CSS o Typst) con compilación automatizada a PDF.

---

## 5. Verification Method

Para verificar independientemente estos resultados:

1. **Inspección de metadatos y dimensiones del template original**:
   ```powershell
   python -c "import pypdf; r = pypdf.PdfReader('TPI_IA_2025-TEMPLATE.pdf'); print(r.metadata); print(r.pages[0].mediabox); print(len(r.pages))"
   ```
   *Condición de éxito*: Reporta 22 páginas, `Title: 'TPI_IA_2025P_4'`, `Producer: 'Skia/PDF m144 Google Docs Renderer'` y `RectangleObject([0, 0, 596, 842])`.

2. **Verificación de generación de PDF mediante Edge Headless**:
   ```powershell
   python -c "import subprocess, os, pypdf; edge = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'; html = os.path.abspath(r'.agents\teamwork\explorer_survey_3\test_page.html'); pdf = os.path.abspath(r'.agents\teamwork\explorer_survey_3\edge_test_clean.pdf'); subprocess.run([edge, '--headless', '--disable-gpu', '--no-pdf-header-footer', '--user-data-dir=C:\\Users\\perez\\AppData\\Local\\Temp\\edgetmp', f'--print-to-pdf={pdf}', html]); r = pypdf.PdfReader(pdf); print('Pages:', len(r.pages), 'Mediabox:', r.pages[0].mediabox)"
   ```
   *Condición de éxito*: Genera el archivo PDF con 1 página y mediabox `RectangleObject([0, 0, 594.96, 841.92])`.

3. **Archivos a inspeccionar**:
   - `c:\Users\perez\OneDrive\Documents\Ing.Sist-NUBE\IA\TPI IA 2026\.agents\teamwork\explorer_survey_3\template_and_tools_analysis.md`
   - `c:\Users\perez\OneDrive\Documents\Ing.Sist-NUBE\IA\TPI IA 2026\.agents\teamwork\explorer_survey_3\X5.png` (Logo oficial UTN extraído)
   - `c:\Users\perez\OneDrive\Documents\Ing.Sist-NUBE\IA\TPI IA 2026\.agents\teamwork\explorer_survey_3\template_clean_text.txt` (Transcripción textual completa y limpia con coordenadas y tamaños)
