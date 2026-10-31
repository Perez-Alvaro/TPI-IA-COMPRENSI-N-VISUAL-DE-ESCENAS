import pypdf

reader = pypdf.PdfReader('TPI_IA_2025-TEMPLATE.pdf')
page1 = reader.pages[0]

# Inspect content stream of page 1 to see how X5 is placed
content = page1.get_contents()
raw = content.get_data().decode('latin1', errors='ignore')
print("Page 1 Content stream snippet:")
for line in raw.split('\n'):
    if 'X5' in line or 'Do' in line or 'cm' in line:
        print(line)
