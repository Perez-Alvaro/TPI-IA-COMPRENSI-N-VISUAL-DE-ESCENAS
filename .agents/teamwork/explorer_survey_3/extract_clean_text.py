import pypdf

reader = pypdf.PdfReader('TPI_IA_2025-TEMPLATE.pdf')

with open('.agents/teamwork/explorer_survey_3/template_clean_text.txt', 'w', encoding='utf-8') as out:
    for page_idx in range(len(reader.pages)):
        page = reader.pages[page_idx]
        tokens = []
        def visitor(text, cm, tm, font_dict, font_size):
            if text:
                x = tm[4] * cm[0] + tm[5] * cm[2] + cm[4]
                y = tm[4] * cm[1] + tm[5] * cm[3] + cm[5]
                font_name = ''
                if font_dict:
                    font_name = str(font_dict.get('/BaseFont', ''))
                tokens.append((round(y, 1), round(x, 1), round(font_size, 1) if font_size else 0, font_name, text))
        page.extract_text(visitor_text=visitor)
        
        # Sort by y descending, then x ascending
        tokens.sort(key=lambda t: (-t[0], t[1]))
        
        out.write(f"\n==================== PAGE {page_idx + 1} ====================\n")
        
        # Group into lines
        current_y = None
        current_line = []
        line_fonts = []
        line_sizes = []
        for y, x, sz, font, text in tokens:
            if current_y is None or abs(y - current_y) > 2.5:
                if current_line:
                    line_str = "".join(current_line).strip()
                    if line_str:
                        avg_sz = sum(line_sizes)/len(line_sizes)
                        out.write(f"[{current_y:.1f} | sz={avg_sz:.1f}] {line_str}\n")
                current_y = y
                current_line = [text]
                line_fonts = [font]
                line_sizes = [sz]
            else:
                current_line.append(text)
                line_fonts.append(font)
                line_sizes.append(sz)
        if current_line:
            line_str = "".join(current_line).strip()
            if line_str:
                avg_sz = sum(line_sizes)/len(line_sizes)
                out.write(f"[{current_y:.1f} | sz={avg_sz:.1f}] {line_str}\n")

print("Clean text extracted to template_clean_text.txt")
