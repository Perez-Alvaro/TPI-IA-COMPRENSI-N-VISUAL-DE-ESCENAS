import pypdf

reader = pypdf.PdfReader('TPI_IA_2025-TEMPLATE.pdf')

with open('.agents/teamwork/explorer_survey_3/pdf_images_info.txt', 'w', encoding='utf-8') as out:
    for page_idx, page in enumerate(reader.pages):
        imgs = list(page.images)
        out.write(f"=== PAGE {page_idx + 1} ({len(imgs)} images) ===\n")
        for img in imgs:
            out.write(f"  Name: {img.name}, len(data): {len(img.data)} bytes\n")
        
print("Images info written to pdf_images_info.txt")
