import pathlib,re
root=pathlib.Path('D:/fra/vanaadhikar-drishti/src')
pattern=re.compile(r'response\.data\?\.items')
count=0
for path in root.rglob('*.ts*'):
    try:
        for idx,line in enumerate(path.read_text(encoding='utf-8').splitlines(),1):
            if pattern.search(line):
                print(f"{path}:{idx}:{line.strip()}")
                count +=1
                if count>=20:
                    raise SystemExit
    except Exception:
        continue
