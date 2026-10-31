"""
check_size_breakdown.py
"""
import re
from pathlib import Path

docs = {
    "informe": Path("informe_tecnico_tpi.md").read_text(encoding="utf-8"),
    "no_tecnico": Path("documento_explicativo_no_tecnico.md").read_text(encoding="utf-8"),
    "defensa": Path("guia_defensa_oral_tpi.md").read_text(encoding="utf-8")
}

for name, text in docs.items():
    print(f"\n==================== {name} ====================")
    lines = text.splitlines()
    for i, line in enumerate(lines, 1):
        if any(term in line.lower() for term in ["small", "pequeñ", "medium", "median", "large", "grande", "escala"]):
            if any(num in line for num in ["71", "24", "4.", "4,", "5%", "1790", "1.790", "1272", "1.272", "430", "88"]):
                print(f"L{i:04d}: {line.strip()[:140]}")
