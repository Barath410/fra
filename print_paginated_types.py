path = 'D:/fra/vanaadhikar-drishti/src/types/index.ts'
with open(path, encoding='utf-8') as fh:
    lines = fh.readlines()
for idx,line in enumerate(lines,1):
    if 'Paginated' in line:
        print(f"{idx}: {line.strip()}")