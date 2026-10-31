import sys
import pypdf

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

reader = pypdf.PdfReader("IA-Resumen-Completo.pdf")
print("=== PAGE 23 (Metrics & F1 / Harmonic Mean) ===")
print(reader.pages[22].extract_text()[:1500])

print("\n=== PAGE 44 (CNNs & Convolutions) ===")
print(reader.pages[43].extract_text()[:1500])
