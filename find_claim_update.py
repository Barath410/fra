import pathlib
root = pathlib.Path('D:/fra/vanaadhikar-drishti/backend')
for path in root.rglob('*.py'):
    try:
        text = path.read_text(encoding='utf-8')
    except Exception:
        continue
    if 'update_claim' in text or 'updateClaim' in text:
        print(path)
