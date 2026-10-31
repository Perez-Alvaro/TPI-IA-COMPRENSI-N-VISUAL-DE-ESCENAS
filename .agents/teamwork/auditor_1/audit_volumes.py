import os
import re
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

deliverables = {
    "informe_tecnico_tpi.html": "informe_tecnico_tpi.html",
    "informe_tecnico_tpi.md": "informe_tecnico_tpi.md",
    "documento_explicativo_no_tecnico.md": "documento_explicativo_no_tecnico.md",
    "guia_defensa_oral_tpi.md": "guia_defensa_oral_tpi.md",
}

for name, fname in deliverables.items():
    size = os.path.getsize(fname)
    with open(fname, "r", encoding="utf-8") as f:
        content = f.read()
    words = len(re.findall(r"\b\w+\b", content))
    lines = len(content.splitlines())
    h1 = len(re.findall(r"^#\s+", content, re.MULTILINE))
    h2 = len(re.findall(r"^##\s+", content, re.MULTILINE))
    h3 = len(re.findall(r"^###\s+", content, re.MULTILINE))
    print(f"\n=== {name} ===")
    print(f"  Size: {size:,} bytes")
    print(f"  Lines: {lines:,}")
    print(f"  Words: {words:,}")
    print(f"  Headings: {h1} H1, {h2} H2, {h3} H3")
