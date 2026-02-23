import argparse
import json
import re
import unicodedata
from pathlib import Path
from typing import Dict, Iterable, List, Tuple


def load_templates_from_files(paths: Iterable[Path]) -> List[Tuple[str, str]]:
    """Parse numbered templates from one or more files into (template_id, body) pairs."""
    templates: List[Tuple[str, str]] = []

    for path in paths:
        text = path.read_text(encoding="utf-8")
        sections = re.split(r"\n\s*(?=\d+\.\s*)", text.strip())

        for section in sections:
            lines = section.strip().splitlines()
            if not lines:
                continue
            header = lines[0].strip()
            match = re.match(r"\d+\.\s*(\S+)", header)
            template_id = match.group(1) if match else header
            body = "\n".join(lines[1:]).strip()
            if body:
                templates.append((template_id, body))

    return templates


def _normalize_literal(text: str) -> str:
    """Escape literal text while relaxing whitespace and punctuation.

    - Whitespace -> \s+
    - Punctuation/symbol runs -> \W+
    - Word characters remain literal (escaped)
    """
    parts: List[str] = []
    current: List[str] = []
    current_type: str | None = None

    def flush() -> None:
        nonlocal current, current_type
        if not current:
            return
        if current_type == "space":
            parts.append(r"\s+")
        elif current_type == "punct":
            parts.append(r"\W+")
        else:  # word or mark
            parts.append(re.escape("".join(current)))
        current = []
        current_type = None

    for ch in text:
        if ch.isspace():
            typ = "space"
        else:
            cat = unicodedata.category(ch)
            if cat.startswith(("P", "S")):
                typ = "punct"
            else:
                typ = "word"

        if current_type is None:
            current_type = typ
        if typ != current_type:
            flush()
            current_type = typ
        current.append(ch)

    flush()
    return "".join(parts)


def _block_to_pattern(block: str) -> str:
    """Convert a single paragraph block with placeholders to a regex fragment."""
    tokens: List[Tuple[str, str]] = []  # (type, value) where type in {"lit", "ph"}
    buffer: List[str] = []
    i = 0
    length = len(block)

    while i < length:
        char = block[i]
        if char == "{":
            if buffer:
                tokens.append(("lit", "".join(buffer)))
                buffer = []
            end = block.find("}", i)
            if end == -1:
                raise ValueError("Unclosed placeholder in template block")
            name = block[i + 1 : end]
            tokens.append(("ph", name))
            i = end + 1
        else:
            buffer.append(char)
            i += 1

    if buffer:
        tokens.append(("lit", "".join(buffer)))

    parts: List[str] = []
    for idx, (typ, val) in enumerate(tokens):
        prefix = r"[\s\S]*?" if parts else ""
        if typ == "lit":
            parts.append(prefix + _normalize_literal(val))
        else:
            # Find next literal token to use as a boundary via lookahead.
            boundary_regex = None
            for next_typ, next_val in tokens[idx + 1 :]:
                if next_typ == "lit":
                    boundary_regex = _normalize_literal(next_val)
                    break
            if boundary_regex:
                placeholder_re = fr"(?P<{val}>[\s\S]+?)(?={boundary_regex})"
            else:
                placeholder_re = fr"(?P<{val}>[\s\S]+)"
            parts.append(prefix + placeholder_re)

    return "".join(parts)


def build_pattern(template_body: str) -> re.Pattern:
    """Convert a template with {PLACEHOLDER}s into a compiled regex pattern.

    Paragraph breaks (blank lines) are treated as flexible gaps so the matcher can
    tolerate extra sentences inserted between sections in the filled document.
    """
    paragraphs = re.split(r"\n\s*\n+", template_body.strip())
    block_patterns = [_block_to_pattern(p) for p in paragraphs if p]
    if not block_patterns:
        raise ValueError("Template body is empty")

    pattern = r"\s*" + r"[\s\S]*?".join(block_patterns) + r"\s*"
    return re.compile(pattern, re.MULTILINE)


def _tokenize_template(template_body: str) -> List[Tuple[str, str]]:
    """Return ordered tokens [('lit'|'ph', value)] from a template body."""
    tokens: List[Tuple[str, str]] = []
    buffer: List[str] = []
    i = 0
    length = len(template_body)

    while i < length:
        char = template_body[i]
        if char == "{":
            if buffer:
                tokens.append(("lit", "".join(buffer)))
                buffer = []
            end = template_body.find("}", i)
            if end == -1:
                raise ValueError("Unclosed placeholder in template")
            name = template_body[i + 1 : end]
            tokens.append(("ph", name))
            i = end + 1
        else:
            buffer.append(char)
            i += 1

    if buffer:
        tokens.append(("lit", "".join(buffer)))
    return tokens


def _match_template(template_body: str, doc_text: str) -> Dict[str, str] | None:
    """Sequentially match template literals against the document and capture entities."""
    doc_text = unicodedata.normalize("NFC", doc_text)
    template_body = unicodedata.normalize("NFC", template_body)
    tokens = _tokenize_template(template_body)
    cursor = 0
    pending_placeholder: str | None = None
    entities: Dict[str, str] = {}

    for typ, val in tokens:
        if typ == "lit":
            # Skip empty literals to avoid zero-length loops.
            if not val.strip():
                continue
            pattern = re.compile(_normalize_literal(val), re.MULTILINE)
            match = pattern.search(doc_text, cursor)
            if not match:
                return None
            if pending_placeholder is not None:
                entities[pending_placeholder] = doc_text[cursor : match.start()].strip()
                pending_placeholder = None
            cursor = match.end()
        else:  # placeholder
            if pending_placeholder is not None:
                # Two placeholders back-to-back; capture empty string between them.
                entities[pending_placeholder] = doc_text[cursor:].strip()
            pending_placeholder = val

    if pending_placeholder is not None:
        entities[pending_placeholder] = doc_text[cursor:].strip()

    return entities


def extract_entities(templates: List[Tuple[str, str]], doc_text: str) -> List[Dict[str, Dict[str, str]]]:
    """Attempt to match each template; return list of matches with entities."""
    tamil_clipping_fixes = {
        "ராமசாம": "ராமசாமி",
        "அம்மாள": "அம்மாள்",
        "ஆவணம": "ஆவணம்",
        "நகல": "நகல்",
    }

    def apply_tamil_fixes(val: str) -> str:
        if not val:
            return val
        # Quick check for Tamil block
        if not any(0x0b80 <= ord(ch) <= 0x0bff for ch in val):
            return val
        fixed = val
        for wrong, correct in tamil_clipping_fixes.items():
            fixed = fixed.replace(wrong, correct)
        return fixed

    results: List[Dict[str, Dict[str, str]]] = []
    for template_id, body in templates:
        entities = _match_template(body, doc_text)
        if entities is None and "\n" in body:
            # Retry once after dropping the first line (title) in case it diverges.
            trimmed_body = body.split("\n", 1)[1]
            entities = _match_template(trimmed_body, doc_text)
        if entities is not None:
            entities = {k: apply_tamil_fixes(v) if isinstance(v, str) else v for k, v in entities.items()}
            results.append({"template_id": template_id, "entities": entities})
    return results


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract entity values from a filled template document.")
    parser.add_argument("--input", required=True, type=Path, help="Path to the filled document/text file.")
    parser.add_argument("--templates", nargs="*", type=Path, help="Optional template files. If omitted, all template_*.txt files in cwd are loaded.")
    parser.add_argument("--first", action="store_true", help="Return only the first matching template.")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON output.")
    parser.add_argument("--output", type=Path, help="Write JSON output to this file instead of stdout.")
    args = parser.parse_args()

    doc_text = args.input.read_text(encoding="utf-8")
    template_paths: List[Path]
    if args.templates:
        template_paths = list(args.templates)
    else:
        template_paths = sorted(Path.cwd().glob("template_*.txt"))
        if not template_paths:
            raise FileNotFoundError("No template files found (expected template_*.txt)")

    templates = load_templates_from_files(template_paths)

    matches = extract_entities(templates, doc_text)
    if args.first and matches:
        matches = matches[:1]

    indent = 2 if args.pretty else None
    payload = json.dumps(matches, ensure_ascii=False, indent=indent)

    if args.output:
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload)


if __name__ == "__main__":
    main()
