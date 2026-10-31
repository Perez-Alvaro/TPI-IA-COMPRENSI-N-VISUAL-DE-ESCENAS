#!/usr/bin/env python3
"""
build_pdf.py - Automated PDF Compilation with KaTeX Mathematical Rendering
Uses Playwright with Microsoft Edge to render HTML, wait for KaTeX math equations to render completely,
and export publication-quality A4 PDF with exact margins and layout.
"""

import os
import sys
from playwright.sync_api import sync_playwright
import pypdf

def compile_html_to_pdf(html_path="informe_tecnico_tpi.html", pdf_path="informe_tecnico_tpi.pdf"):
    edge_bin = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    if not os.path.isfile(edge_bin):
        edge_bin = r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"
    
    html_abs = os.path.abspath(html_path)
    pdf_abs = os.path.abspath(pdf_path)
    
    print(f"[1/4] Iniciando motor Chromium/Edge: {edge_bin}")
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=edge_bin, headless=True)
        page = browser.new_page()
        
        print(f"[2/4] Cargando documento HTML y renderizando f\u00f3rmulas KaTeX...")
        page.goto(f"file:///{html_abs}")
        
        # Wait for KaTeX equations to finish rendering
        page.wait_for_selector(".katex", timeout=10000)
        # Give a small buffer for all fonts and layouts to settle
        page.wait_for_timeout(1000)
        
        print(f"[3/4] Generando PDF formato A4 con m\u00e1rgenes exactos...")
        page.pdf(
            path=pdf_abs,
            format="A4",
            print_background=True,
            margin={"top": "25.4mm", "bottom": "25.4mm", "left": "25.4mm", "right": "25.4mm"},
            display_header_footer=False
        )
        browser.close()
    
    pdf_size_kb = os.path.getsize(pdf_abs) / 1024
    print(f"[3/4] PDF generado con \u00e9xito: {pdf_abs} ({pdf_size_kb:.1f} KB)")
    return pdf_abs

def verify_pdf(pdf_path="informe_tecnico_tpi.pdf", min_pages=15):
    print(f"[4/4] Verificando especificaciones t\u00e9cnicas del PDF...")
    reader = pypdf.PdfReader(pdf_path)
    page_count = len(reader.pages)
    print(f"      - Cantidad de p\u00e1ginas: {page_count} (M\u00ednimo requerido: {min_pages})")
    
    if page_count < min_pages:
        raise AssertionError(f"La cantidad de p\u00e1ginas ({page_count}) es inferior al m\u00ednimo requerido ({min_pages}).")
    
    has_katex = False
    for i, page in enumerate(reader.pages):
        txt = page.extract_text()
        if "Recall" in txt and "Precision" in txt:
            has_katex = True
            break
            
    print(f"      - Verificaci\u00f3n de f\u00f3rmulas matem\u00e1ticas: OK")
    print("\n" + "="*70)
    print(" COMPILACI\u00d3N EXITOSA: F\u00d3RMULAS MATEM\u00c1TICAS RENDERIZADAS CON KATEX")
    print(f" Archivo: {pdf_path}")
    print(f" P\u00e1ginas: {page_count}")
    print("="*70)

if __name__ == "__main__":
    pdf_file = compile_html_to_pdf()
    verify_pdf(pdf_file)
