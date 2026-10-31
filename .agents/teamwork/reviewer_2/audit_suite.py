import os
import sys
import re
import pypdf
from PIL import Image

WORKSPACE_DIR = r"c:\Users\perez\OneDrive\Documents\Ing.Sist-NUBE\IA\TPI IA 2026"
PDF_PATH = os.path.join(WORKSPACE_DIR, "informe_tecnico_tpi.pdf")
ASSETS_DIR = os.path.join(WORKSPACE_DIR, "report_assets")

def audit_embedded_images():
    print("=== AUDIT EMBEDDED IMAGES IN PDF ===")
    reader = pypdf.PdfReader(PDF_PATH)
    total_imgs = 0
    for idx, page in enumerate(reader.pages):
        xobjs = page.get('/Resources', {}).get('/XObject', {})
        for name, obj in xobjs.items():
            if obj.get('/Subtype') == '/Image':
                total_imgs += 1
                w = obj.get('/Width')
                h = obj.get('/Height')
                print(f"Page {idx+1}: {name} -> {w}x{h}")
    print(f"Total embedded image objects found: {total_imgs}")
    return total_imgs

def audit_cross_document_consistency():
    print("\n=== AUDIT CROSS-DOCUMENT CONSISTENCY ===")
    docs = {
        "informe_tecnico_tpi.md": os.path.join(WORKSPACE_DIR, "informe_tecnico_tpi.md"),
        "informe_tecnico_tpi.html": os.path.join(WORKSPACE_DIR, "informe_tecnico_tpi.html"),
        "documento_explicativo_no_tecnico.md": os.path.join(WORKSPACE_DIR, "documento_explicativo_no_tecnico.md"),
        "guia_defensa_oral_tpi.md": os.path.join(WORKSPACE_DIR, "guia_defensa_oral_tpi.md")
    }
    
    contents = {}
    for name, path in docs.items():
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8", errors="replace") as f:
                contents[name] = f.read()
        else:
            print(f"[FAIL] Missing document: {name}")

    # Check 1: Grupo 21
    print("\n[Check 1: Group Identity]")
    for name, c in contents.items():
        has_g21 = bool(re.search(r"(?i)grupo\s*(?:n[°º\.]?\s*)?21", c))
        print(f"  {name:35s}: Grupo 21 found? {has_g21}")

    # Check 2: 5 Students and Legajos
    students = [
        ("Ocampo, Gabriel", "93368"),
        ("Pecchio, Valentina", "94416"),
        ("Lopez Quinteros, Manuel", "99026"),
        ("Chaile, Emmanuel Ricardo", "89767"),
        ("Perez, Alvaro", "97986")
    ]
    print("\n[Check 2: 5 Student Authors & Legajos]")
    for name, c in contents.items():
        print(f"  Document: {name}")
        for sname, legajo in students:
            # Check name fragment
            last_name = sname.split(",")[0].strip()
            has_name = bool(re.search(rf"(?i){last_name}", c))
            has_legajo = legajo in c
            print(f"    - {sname:30s} (Leg: {legajo}): Name={has_name}, Legajo={has_legajo}")

    # Check 3: Professors
    profs = ["Mario", "Forte", "Gramática"]
    print("\n[Check 3: Teaching Staff]")
    for name, c in contents.items():
        print(f"  Document: {name}")
        for p in profs:
            has_p = bool(re.search(rf"(?i){p}", c))
            print(f"    - Prof {p:15s}: Present={has_p}")

    # Check 4: Exact Metrics
    metrics = [
        ("Baseline Box F1 (0.6464)", r"0[\.,]6464"),
        ("Baseline Mask F1 (0.6132)", r"0[\.,]6132"),
        ("Baseline QA (0.6053)", r"0[\.,]6053"),
        ("Baseline Kaggle (0.6615)", r"0[\.,]6615"),
        ("V2 Kaggle (0.6763)", r"0[\.,]6763"),
        ("V3 Box F1 (0.6722)", r"0[\.,]6722"),
        ("V3 Mask F1 (0.6351)", r"0[\.,]6351"),
        ("V3 QA Deterministic (0.7895)", r"0[\.,]7895"),
        ("V3 Kaggle (0.6800)", r"0[\.,]6800"),
    ]
    print("\n[Check 4: Core Quantitative Metrics]")
    for name, c in contents.items():
        print(f"  Document: {name}")
        for label, pat in metrics:
            found = bool(re.search(pat, c))
            print(f"    - {label:32s}: {found}")

if __name__ == "__main__":
    audit_embedded_images()
    audit_cross_document_consistency()
