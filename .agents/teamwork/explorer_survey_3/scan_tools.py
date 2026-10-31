import os, shutil

candidates = [
    r'C:\Program Files\Typst\typst.exe',
    os.path.expandvars(r'%LOCALAPPDATA%\Programs\typst\typst.exe'),
    os.path.expandvars(r'%CARGO_HOME%\bin\typst.exe'),
    os.path.expanduser(r'~/.cargo/bin/typst.exe'),
    r'C:\Program Files\Pandoc\pandoc.exe',
    os.path.expandvars(r'%LOCALAPPDATA%\Pandoc\pandoc.exe'),
    r'C:\Program Files\MiKTeX\miktex\bin\x64\pdflatex.exe',
    os.path.expandvars(r'%LOCALAPPDATA%\Programs\MiKTeX\miktex\bin\x64\pdflatex.exe'),
    r'C:\texlive\2024\bin\windows\pdflatex.exe',
    r'C:\texlive\2023\bin\win32\pdflatex.exe',
    r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
    r'C:\Program Files\Google\Chrome\Application\chrome.exe'
]

print("Scanning candidate binaries:")
for c in candidates:
    exists = os.path.isfile(c)
    print(f"  {c} -> {'EXISTS' if exists else 'NOT FOUND'}")

tools_in_path = ['typst', 'pandoc', 'pdflatex', 'xelatex', 'lualatex', 'latex', 'weasyprint', 'msedge', 'chrome', 'python', 'node', 'npm']
print("\nScanning PATH:")
for t in tools_in_path:
    found = shutil.which(t)
    print(f"  {t} -> {found if found else 'NOT IN PATH'}")
