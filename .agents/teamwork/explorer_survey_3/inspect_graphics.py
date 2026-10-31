import pypdf

reader = pypdf.PdfReader('TPI_IA_2025-TEMPLATE.pdf')

with open('.agents/teamwork/explorer_survey_3/pdf_graphics_info.txt', 'w', encoding='utf-8') as out:
    for page_idx, page in enumerate(reader.pages):
        contents = page.get_contents()
        raw = b""
        if isinstance(contents, list):
            for c in contents:
                raw += c.get_data()
        elif contents:
            raw = contents.get_data()
        
        # Look for table borders, lines: 're' (rectangle), 'm' (moveto), 'l' (lineto), 'S' (stroke), 'f' (fill)
        ops = raw.split()
        re_count = ops.count(b're')
        l_count = ops.count(b'l')
        m_count = ops.count(b'm')
        s_count = ops.count(b'S') + ops.count(b's')
        f_count = ops.count(b'f') + ops.count(b'F') + ops.count(b'f*')
        out.write(f"Page {page_idx + 1}: 're'={re_count}, 'l'={l_count}, 'm'={m_count}, 'S'={s_count}, 'f'={f_count}\n")

print("Graphics info written to pdf_graphics_info.txt")
