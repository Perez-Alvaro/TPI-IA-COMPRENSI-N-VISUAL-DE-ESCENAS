import pypdf

reader = pypdf.PdfReader('TPI_IA_2025-TEMPLATE.pdf')

print("Page bounding box analysis:")
for i, page in enumerate(reader.pages):
    mb = page.mediabox
    w, h = float(mb.width), float(mb.height)
    
    xs = []
    ys = []
    def visitor(text, cm, tm, font_dict, font_size):
        if text.strip():
            x = tm[4] * cm[0] + tm[5] * cm[2] + cm[4]
            y = tm[4] * cm[1] + tm[5] * cm[3] + cm[5]
            xs.append(x)
            ys.append(y)
    page.extract_text(visitor_text=visitor)
    
    if xs and ys:
        left_m = min(xs)
        right_m = w - max(xs)
        bottom_m = min(ys)
        top_m = h - max(ys)
        print(f"Page {i+1:2d} (w={w:.1f}, h={h:.1f}): Left={left_m:.1f}pt ({left_m/72*25.4:.1f}mm), Right_limit={max(xs):.1f}pt, Bottom={bottom_m:.1f}pt ({bottom_m/72*25.4:.1f}mm), Top_first_baseline={max(ys):.1f}pt (dist from top={top_m:.1f}pt)")
    else:
        print(f"Page {i+1:2d}: No text elements")
