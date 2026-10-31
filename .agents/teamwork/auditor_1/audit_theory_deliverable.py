import re
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

with open("informe_tecnico_tpi.md", "r", encoding="utf-8") as f:
    text = f.read()

patterns = [
    ("Convolución / Jerarquía", r"(?i)(convoluci[oó]n|convolucional|kernel|mapa\s+de\s+caracter[ií]sticas)"),
    ("Campo receptivo", r"(?i)(campo\s+receptivo|receptive\s+field)"),
    ("Transfer learning", r"(?i)(transfer\s+learning|transferencia|preentrenad|fundacional)"),
    ("Media armónica", r"(?i)(media\s+arm[oó]nica|harmonic\s+mean)"),
    ("Desbalance / Long-tail", r"(?i)(desbalance|cola\s+larga|long[\-\s]tail|federad)"),
    ("Regularización / Sobreajuste", r"(?i)(sobreajuste|overfitting|generalizaci[oó]n|regularizaci[oó]n)")
]

print("=== Theoretical Concepts in informe_tecnico_tpi.md ===")
for label, pat in patterns:
    matches = list(re.finditer(pat, text))
    print(f"\n--- {label} ({len(matches)} matches) ---")
    for m in matches[:3]:
        snippet = text[max(0, m.start()-50):min(len(text), m.end()+80)].replace("\n", " ")
        print(f"  [{m.start()}]: ...{snippet}...")
