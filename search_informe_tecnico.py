"""
search_informe_tecnico.py
Inspect contents of informe_tecnico_tpi.md for key verification items
"""

import re
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

path = Path("informe_tecnico_tpi.md")
content = path.read_text(encoding="utf-8")
lines = content.splitlines()

queries = [
    ("pad_fix / pad / reescalado", [r"pad", r"reescal"]),
    ("OWLv2 Large", [r"owlv2.*large", r"vit-l", r"large.*patch14"]),
    ("SAM2 Multimask", [r"multimask", r"multim[áa]scara", r"single.*best_score"]),
    ("Latencia / Tiempos", [r"latencia", r"2[.,]44", r"0[.,]43", r"0[.,]28", r"3[.,]25", r"cuello de botella", r"segundo"]),
    ("Distribución de tamaños", [r"71[.,]06", r"24[.,]02", r"4[.,]92", r"1272", r"430", r"88"]),
    ("Métricas", [r"0[.,]6464", r"0[.,]6722", r"0[.,]6132", r"0[.,]6351", r"0[.,]6053", r"0[.,]7895", r"0[.,]6615", r"0[.,]6763", r"0[.,]6800"]),
]

for label, patterns in queries:
    print(f"\n==================== {label} ====================")
    found = False
    for i, line in enumerate(lines, 1):
        for pat in patterns:
            if re.search(pat, line, re.IGNORECASE):
                print(f"L{i:04d}: {line.strip()[:140]}")
                found = True
                break
    if not found:
        print(">>> NONE FOUND <<<")
