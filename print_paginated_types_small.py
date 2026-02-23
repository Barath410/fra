path = 'D:/fra/vanaadhikar-drishti/src/types/index.ts'
count = 0
with open(path, encoding='utf-8') as fh:
    for idx, line in enumerate(fh, 1):
        if 'Paginated' in line:
            print(f"{idx}: {line.strip()}")
            count += 1
            if count >= 20:
                break
