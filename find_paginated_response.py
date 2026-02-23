import pathlib
root = pathlib.Path('D:/fra/vanaadhikar-drishti/src')
for path in root.rglob('*.ts*'):
    try:
        text = path.read_text(encoding='utf-8')
    except Exception:
        continue
    if 'PaginatedResponse' in text:
        print(path)
        lines = text.splitlines()
        for idx,line in enumerate(lines,1):
            if 'PaginatedResponse' in line:
                print(f"  {idx}: {line.strip()}")
