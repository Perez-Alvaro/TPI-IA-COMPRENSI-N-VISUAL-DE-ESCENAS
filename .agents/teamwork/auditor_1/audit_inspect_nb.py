import json
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

with open("tpi-ia-2026p-21.ipynb", "r", encoding="utf-8") as f:
    nb = json.load(f)

print("Inspecting QA / LLM cells in notebook:")
for idx in range(48, 62):
    c = nb["cells"][idx]
    ctype = c.get("cell_type")
    src = "".join(c.get("source", []))
    print(f"\n=== CELL {idx} ({ctype}) ===")
    lines = src.split("\n")
    for l in lines[:10]:
        print("  ", l)
