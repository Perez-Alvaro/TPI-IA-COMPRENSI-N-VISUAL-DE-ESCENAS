import pypdf

reader = pypdf.PdfReader('TPI_IA_2025-TEMPLATE.pdf')

def analyze_columns(page_idx):
    page = reader.pages[page_idx]
    blocks = []
    def visitor(text, cm, tm, font_dict, font_size):
        if text.strip():
            blocks.append((tm[4], tm[5], font_size, text.strip()))
    page.extract_text(visitor_text=visitor)
    
    xs = [b[0] for b in blocks]
    # Check distribution of x coordinates
    left_col = [b for b in blocks if b[0] < 280]
    right_col = [b for b in blocks if b[0] >= 280]
    return len(blocks), min(xs) if xs else 0, max(xs) if xs else 0, len(left_col), len(right_col), blocks

print("Page layout analysis:")
for i in range(len(reader.pages)):
    total, min_x, max_x, left_cnt, right_cnt, blocks = analyze_columns(i)
    print(f"Page {i+1:2d}: min_x={min_x:5.1f}, max_x={max_x:5.1f}, left_tokens={left_cnt:3d}, right_tokens={right_cnt:3d}")
