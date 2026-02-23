import pathlib
import itertools
root = pathlib.Path('D:/fra/vanaadhikar-drishti/src')
target = 'PaginatedResponse'
count = 0
for path in root.rglob('*.ts*'):
    try:
        text = path.read_text(encoding='utf-8')
    except Exception:
        continue
    for idx,line in enumerate(text.splitlines(), 1):
        if target in line:
            print(f"{path}:{idx}:{line.strip()}")
            count += 1
            if count >= 20:
                raise SystemExit
