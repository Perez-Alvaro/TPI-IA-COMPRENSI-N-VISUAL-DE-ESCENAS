import pypdf
import sys
sys.stdout.reconfigure(encoding='utf-8')
from collections import defaultdict

reader = pypdf.PdfReader('TPI_IA_2025-TEMPLATE.pdf')

style_counts = defaultdict(list)

for page_idx, page in enumerate(reader.pages):
    tokens = []
    def visitor(text, cm, tm, font_dict, font_size):
        if text.strip():
            font_name = 'Unknown'
            if font_dict:
                font_name = str(font_dict.get('/BaseFont', 'Unknown'))
            tokens.append((font_size, font_name, text.strip(), page_idx + 1))
    page.extract_text(visitor_text=visitor)
    for sz, font, txt, pno in tokens:
        style_counts[(round(sz, 1), font)].append((pno, txt))

print("Typography Summary:")
for (sz, font), occurrences in sorted(style_counts.items(), key=lambda x: -len(x[1])):
    # Convert sz (in 96dpi/google docs units) to typical points:
    # Google docs uses 96 dpi coordinate system internally or pt?
    # Let's see: 34.7 * 0.75 = 26 pt, 14.7 * 0.75 = 11 pt, 16.0 * 0.75 = 12 pt, 17.3 * 0.75 = 13 pt
    pt_equiv = sz * 0.75
    sample_texts = [f"p{p}:{t[:25]}" for p, t in occurrences[:5]]
    print(f"Size {sz:4.1f} ({pt_equiv:4.1f} pt) | Font {font:25s} | Count {len(occurrences):4d} | Samples: {', '.join(sample_texts)}")
