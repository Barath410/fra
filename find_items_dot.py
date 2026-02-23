import pathlib
import re
root = pathlib.Path('D:/fra/vanaadhikar-drishti/src')
pattern = re.compile(r'response\.data\?\.items')
for path in root.rglob('*.ts*'):
    try:
        for idx,line in enumerate(path.read_text(encoding='utf-8').splitlines(),1):
            if pattern.search(line):
                print(f"{path}:{idx}:{line.strip()}")
    except Exception:
        continue
