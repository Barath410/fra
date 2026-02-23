from pathlib import Path

import re
from extract_entities import _match_template, _normalize_literal, load_templates, _tokenize_template


text = Path('input.txt').read_text(encoding='utf-8')
templates = load_templates(Path('template_tamil.txt'))

for idx, (tid, body) in enumerate(templates, 1):
    entities = _match_template(body, text)
    print(idx, tid, 'MATCH' if entities else 'no')
    if entities:
        for k, v in entities.items():
            snippet = v if v is None or len(v) < 120 else v[:117] + '...'
            print(f'  {k}: {snippet!r}')

    if tid == 'DOC_TITLE_COMMUNITY_FOREST_RESOURCES':
        tokens = _tokenize_template(body)
        literal_count = sum(1 for t, _ in tokens if t == 'lit')
        placeholder_count = sum(1 for t, _ in tokens if t == 'ph')
        print('Token counts -> literals:', literal_count, 'placeholders:', placeholder_count)
        cursor = 0
        for ttype, tval in tokens:
            if ttype == 'lit':
                if not tval.strip():
                    continue
                pat = re.compile(_normalize_literal(tval), re.MULTILINE)
                m = pat.search(text, cursor)
                print('  LIT', repr(tval[:60]), '->', 'found' if m else 'missing')
                if not m:
                    print('    pattern snippet:', pat.pattern[:120])
                if not m:
                    break
                cursor = m.end()
            else:
                print('  PH', tval)
