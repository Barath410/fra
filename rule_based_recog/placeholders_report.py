import re
from pathlib import Path
from collections import defaultdict, OrderedDict


def parse_templates(path: Path):
    text = path.read_text(encoding="utf-8")
    sections = re.split(r"\n\s*(?=\d+\.\s*)", text.strip())
    templates = []
    for section in sections:
        lines = section.strip().splitlines()
        if not lines:
            continue
        header = lines[0].strip()
        m = re.match(r"\d+\.\s*(\S+)", header)
        template_id = m.group(1) if m else header
        body = "\n".join(lines[1:])
        placeholders = list(OrderedDict.fromkeys(re.findall(r"{([^}]+)}", body)))
        templates.append((template_id, placeholders))
    return templates


def main():
    cwd = Path.cwd()
    template_files = sorted(cwd.glob("template_*.txt"))
    if not template_files:
        raise SystemExit("No template_*.txt files found")

    report_lines = []
    report_lines.append("Placeholders by template and language\n")

    # Collect per template_id across languages
    per_template = defaultdict(lambda: defaultdict(list))

    for path in template_files:
        lang = path.stem.replace("template_", "")
        for template_id, placeholders in parse_templates(path):
            per_template[template_id][lang] = placeholders

    # For each template, compute reference set (union across langs)
    for template_id in sorted(per_template.keys()):
        report_lines.append(f"=== {template_id} ===")
        all_placeholders = set()
        for phs in per_template[template_id].values():
            all_placeholders.update(phs)

        for lang in sorted(per_template[template_id].keys()):
            phs = per_template[template_id][lang]
            missing = sorted(all_placeholders - set(phs))
            extra = sorted(set(phs) - all_placeholders)
            report_lines.append(f"[{lang}] count={len(phs)}")
            report_lines.append("  " + ", ".join(phs))
            if missing:
                report_lines.append(f"  MISSING: {', '.join(missing)}")
            if extra:
                report_lines.append(f"  EXTRA: {', '.join(extra)}")
        report_lines.append("")

    out_path = cwd / "placeholders_report.txt"
    out_path.write_text("\n".join(report_lines), encoding="utf-8")
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()