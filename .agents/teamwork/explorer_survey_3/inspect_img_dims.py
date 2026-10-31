import pypdf
from PIL import Image
import io

reader = pypdf.PdfReader('TPI_IA_2025-TEMPLATE.pdf')

for page_idx in range(len(reader.pages)):
    page = reader.pages[page_idx]
    for img_idx, img in enumerate(page.images):
        im = Image.open(io.BytesIO(img.data))
        print(f"Page {page_idx+1} Img {img.name}: format={im.format}, size={im.size}, mode={im.mode}")
