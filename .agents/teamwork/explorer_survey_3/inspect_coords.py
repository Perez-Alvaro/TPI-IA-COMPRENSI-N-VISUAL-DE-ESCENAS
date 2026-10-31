import pypdf

reader = pypdf.PdfReader('TPI_IA_2025-TEMPLATE.pdf')

def mult_matrix(m1, m2):
    # m = [a, b, c, d, e, f]
    # [a1 b1 0]   [a2 b2 0]
    # [c1 d1 0] * [c2 d2 0]
    # [e1 f1 1]   [e2 f2 1]
    a1, b1, c1, d1, e1, f1 = m1
    a2, b2, c2, d2, e2, f2 = m2
    return [
        a1*a2 + b1*c2,
        a1*b2 + b1*d2,
        c1*a2 + d1*c2,
        c1*b2 + d1*d2,
        e1*a2 + f1*c2 + e2,
        e1*b2 + f1*d2 + f2
    ]

def get_page_elements(page_idx):
    page = reader.pages[page_idx]
    elements = []
    def visitor(text, cm, tm, font_dict, font_size):
        if text.strip():
            # tm is [a, b, c, d, e, f]
            # cm is [a, b, c, d, e, f]
            # actual coordinate of (0,0) in text space is (tm[4], tm[5]) transformed by cm
            # x_eff = tm[4] * cm[0] + tm[5] * cm[2] + cm[4]
            # y_eff = tm[4] * cm[1] + tm[5] * cm[3] + cm[5]
            x = tm[4] * cm[0] + tm[5] * cm[2] + cm[4]
            y = tm[4] * cm[1] + tm[5] * cm[3] + cm[5]
            elements.append((x, y, font_size, text.strip(), cm, tm, font_dict.get('/BaseFont', '') if font_dict else ''))
    page.extract_text(visitor_text=visitor)
    return elements

for idx in [0, 1, 6]:
    els = get_page_elements(idx)
    print(f"=== PAGE {idx+1} ===")
    print(f"Total elements: {len(els)}")
    for e in els[:12]:
        print(f"  pos=({e[0]:.1f}, {e[1]:.1f}) font_size={e[2]:.1f} font={e[6]}: {e[3]}")
