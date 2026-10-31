"""
verify_empirical_claims.py
Independent Empirical Verification Script for TPI IA 2026 Deliverables
Extracts ground truth from tpi-ia-2026p-21.ipynb outputs and compares with:
- informe_tecnico_tpi.md
- documento_explicativo_no_tecnico.md
- guia_defensa_oral_tpi.md
"""

import json
import re
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


WORKSPACE = Path(__file__).resolve().parent

def load_notebook(nb_path):
    with open(nb_path, "r", encoding="utf-8") as f:
        return json.load(f)

def find_outputs_with_text(nb, keywords):
    matches = []
    for idx, cell in enumerate(nb["cells"]):
        text_sources = "".join(cell.get("source", []))
        text_outputs = ""
        for out in cell.get("outputs", []):
            if "text" in out:
                text_outputs += "".join(out["text"])
            elif "data" in out and "text/plain" in out["data"]:
                text_outputs += "".join(out["data"]["text/plain"])
        
        combined = (text_sources + "\n" + text_outputs).lower()
        if any(kw.lower() in combined for kw in keywords):
            matches.append({
                "cell_idx": idx,
                "cell_type": cell.get("cell_type"),
                "source": text_sources,
                "outputs": text_outputs
            })
    return matches

if __name__ == "__main__":
    nb = load_notebook(WORKSPACE / "tpi-ia-2026p-21.ipynb")
    print(f"Loaded notebook with {len(nb['cells'])} cells.")
    
    keywords = [
        "0.6464", "0.6722", "0.6132", "0.6351", "0.6053", "0.7895",
        "0.6615", "0.6763", "0.6800", "1790", "1,790", "1.790",
        "71.06", "24.02", "4.92", "2.44", "0.43", "0.28", "3.25",
        "pad_fix", "multimask", "owlv2"
    ]
    
    for c_idx in [86, 89, 90, 92, 93]:
        cell = nb["cells"][c_idx]
        print(f"\n==================== CELL {c_idx} ({cell.get('cell_type')}) ====================")
        src = "".join(cell.get("source", []))
        print(src)
        outs = cell.get("outputs", [])
        if outs:
            for out in outs:
                if "text" in out:
                    print("".join(out["text"]))
                elif "data" in out and "text/plain" in out["data"]:
                    print("".join(out["data"]["text/plain"]))








