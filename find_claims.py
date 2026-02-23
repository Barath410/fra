import os
import pathlib
import re

root = pathlib.Path('D:/fra/vanaadhikar-drishti/src')
pattern = re.compile(r'createClaim')
for path in root.rglob('*.ts'):
    try:
        text = path.read_text(encoding='utf-8')
    except Exception:
        continue
    for idx, line in enumerate(text.splitlines(), 1):
        if pattern.search(line):
            print(f"{path}:{idx}:{line.strip()}")
