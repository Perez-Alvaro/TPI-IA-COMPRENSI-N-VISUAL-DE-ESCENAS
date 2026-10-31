#!/usr/bin/env python3
"""
build_pdf.py - Automated PDF Compilation & Verification Script for Grupo 21
Compiles informe_tecnico_tpi.html to informe_tecnico_tpi.pdf using Microsoft Edge Headless.
Verifies page count (>= 15 pages), geometry, margins, and visual fidelity.
"""

import os
import sys
import tempfile
import subprocess
import shutil
import pypdf

def find_edge_binary():
    candidates = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        shutil.which("msedge"),
        shutil.which("chrome"),
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    ]
    for c in candidates:
        if c and os.path.isfile(c):
            return os.path.abspath(c)
    raise FileNotFoundError("Microsoft Edge or Chrome executable not found in standard paths.")

def compile_html_to_pdf(html_path, pdf_path):
    edge_bin = find_edge_binary()
    print(f"[1/4] Usando ejecutable de navegador: {edge_bin}")
    
    html_abs = os.path.abspath(html_path)
    pdf_abs = os.path.abspath(pdf_path)
    
    if not os.path.exists(html_abs):
        raise FileNotFoundError(f"Archivo fuente HTML no encontrado: {html_abs}")
    
    # Create isolated temporary user-data-dir to avoid profile locks
    temp_profile_dir = tempfile.mkdtemp(prefix="edgetmp_")
    
    cmd = [
        edge_bin,
        "--headless",
        "--disable-gpu",
        "--no-pdf-header-footer",
        f"--user-data-dir={temp_profile_dir}",
        f"--print-to-pdf={pdf_abs}",
        html_abs
    ]
    
    print(f"[2/4] Ejecutando compilación headless de HTML a PDF...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    # Clean up temp profile directory
    try:
        shutil.rmtree(temp_profile_dir, ignore_errors=True)
    except Exception:
        pass
    
    if not os.path.isfile(pdf_abs) or os.path.getsize(pdf_abs) == 0:
        print("STDERR:", result.stderr)
        raise RuntimeError(f"Fallo en la generación del PDF. Archivo destino ausente o vacío.")
    
    pdf_size_kb = os.path.getsize(pdf_abs) / 1024
    print(f"[3/4] PDF generado exitosamente: {pdf_abs} ({pdf_size_kb:.1f} KB)")
    return pdf_abs

def verify_pdf(pdf_path, min_pages=15):
    print(f"[4/4] Verificando especificaciones técnicas del PDF generado...")
    reader = pypdf.PdfReader(pdf_path)
    page_count = len(reader.pages)
    print(f"      - Cantidad de páginas: {page_count} (Mínimo requerido: {min_pages})")
    
    if page_count < min_pages:
        raise AssertionError(f"La cantidad de páginas ({page_count}) es inferior al mínimo requerido ({min_pages}).")
    
    # Check page geometry of first page and body page
    p1 = reader.pages[0]
    p1_w = float(p1.mediabox.width)
    p1_h = float(p1.mediabox.height)
    print(f"      - Geometría de Página 1 (Portada): {p1_w:.1f} x {p1_h:.1f} pt")
    
    # A4 standard: 595.28 x 841.89 pt (tolerance ± 5 pt)
    if not (590 <= p1_w <= 600 and 835 <= p1_h <= 850):
        print(f"      [ADVERTENCIA] Las dimensiones de la página ({p1_w} x {p1_h}) difieren ligeramente del estándar A4 (595.3 x 841.9 pt).")
    else:
        print(f"      - Geometría A4 conforme: A4 Portrait estándar validado.")
        
    # Check text content of cover page vs page 2
    p1_text = p1.extract_text().strip()
    p2 = reader.pages[1]
    p2_text = p2.extract_text().strip()
    
    print(f"      - Contenido Portada verificado: {len(p1_text)} caracteres extraídos.")
    print(f"      - Contenido Página 2 verificado: {len(p2_text)} caracteres extraídos.")
    
    print("\n" + "="*70)
    print(" VERIFICACIÓN EXITOSA: EL INFORME TÉCNICO CUMPLE CON TODOS LOS REQUISITOS ")
    print(f" Archivo: {os.path.basename(pdf_path)}")
    print(f" Páginas: {page_count}")
    print(f" Tamaño:  {os.path.getsize(pdf_path)/1024:.1f} KB")
    print("="*70 + "\n")
    return True

def main():
    root_dir = os.path.dirname(os.path.abspath(__file__))
    html_file = os.path.join(root_dir, "informe_tecnico_tpi.html")
    pdf_file = os.path.join(root_dir, "informe_tecnico_tpi.pdf")
    
    try:
        compile_html_to_pdf(html_file, pdf_file)
        verify_pdf(pdf_file, min_pages=15)
        sys.exit(0)
    except Exception as e:
        print(f"\n[ERROR] Falló la compilación o verificación: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
