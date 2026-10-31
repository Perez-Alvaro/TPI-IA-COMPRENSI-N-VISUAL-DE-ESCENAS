import sys
import pypdf

reader = pypdf.PdfReader('TPI_IA_2025-TEMPLATE.pdf')
print(f"Total pages: {len(reader.pages)}")

def analyze_page(page_idx):
    page = reader.pages[page_idx]
    elements = []
    def visitor(text, cm, tm, font_dict, font_size):
        if text.strip():
            font_name = 'None'
            if font_dict:
                font_name = str(font_dict.get('/BaseFont', 'Unknown'))
            elements.append({
                'text': text,
                'x': round(tm[4], 2),
                'y': round(tm[5], 2),
                'size': round(font_size, 2) if font_size else 0,
                'font': font_name
            })
    page.extract_text(visitor_text=visitor)
    return elements

with open('.agents/teamwork/explorer_survey_3/pdf_structure.txt', 'w', encoding='utf-8') as out:
    for idx in range(len(reader.pages)):
        els = analyze_page(idx)
        out.write(f"=== PAGE {idx+1} (elements: {len(els)}) ===\n")
        # Find min/max x, y
        if els:
            xs = [e['x'] for e in els]
            ys = [e['y'] for e in els]
            out.write(f"  X-range: min={min(xs):.1f}, max={max(xs):.1f}\n")
            out.write(f"  Y-range: min={min(ys):.1f}, max={max(ys):.1f}\n")
            # Distinct font sizes
            sizes = sorted(list(set(e['size'] for e in els)))
            out.write(f"  Font sizes: {sizes}\n")
            # Distinct fonts
            fonts = sorted(list(set(e['font'] for e in els)))
            out.write(f"  Fonts: {fonts}\n")
            # Print sample elements or headings
            out.write("  First 10 elements:\n")
            for e in els[:10]:
                out.write(f"    [{e['x']}, {e['y']}] sz={e['size']} font={e['font']}: {e['text']}\n")
            # Print elements with size >= 13 or bold
            headings = [e for e in els if e['size'] >= 12 or 'Bold' in e['font']]
            out.write(f"  Headings / Bold items ({len(headings)}):\n")
            for h in headings:
                out.write(f"    [{h['x']}, {h['y']}] sz={h['size']} font={h['font']}: {h['text']}\n")
        out.write("\n")

print("Analysis written to pdf_structure.txt")
