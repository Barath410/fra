import argparse
import json
import os
from pathlib import Path
from typing import List, Optional

from google.cloud import vision
from google.cloud import translate_v2 as translate

import extract_entities


def run_ocr(image_path: Path, language_hints: Optional[List[str]] = None) -> str:
    # If the input is a plain text file, bypass OCR.
    if image_path.suffix.lower() in {".txt"}:
        return image_path.read_text(encoding="utf-8")

    client = vision.ImageAnnotatorClient()
    content = image_path.read_bytes()
    image = vision.Image(content=content)
    response = client.document_text_detection(
        image=image,
        image_context={"language_hints": language_hints or []},
    )
    if response.error.message:
        raise RuntimeError(f"Vision API error: {response.error.message}")
    return response.full_text_annotation.text


def translate_text(text: str, target_language: str = "en") -> str:
    translator = translate.Client()
    result = translator.translate(text, target_language=target_language)
    return result["translatedText"]


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "OCR -> rule-based entity extraction -> English translation pipeline."
        )
    )
    parser.add_argument("--input", required=True, type=Path, help="Path to scanned/PDF/image file for OCR.")
    parser.add_argument(
        "--lang-hints",
        nargs="*",
        default=None,
        help="Optional language hints for OCR (e.g., ta, hi, bn, te, or).",
    )
    parser.add_argument(
        "--templates",
        nargs="*",
        type=Path,
        help="Optional template files; if omitted, auto-loads template_*.txt in cwd.",
    )
    parser.add_argument(
        "--translate",
        action="store_true",
        help="Translate extracted entity values to English using Cloud Translation.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Write JSON output to file; default prints to stdout.",
    )
    parser.add_argument(
        "--credentials",
        type=Path,
        help="Path to Google service account JSON. Overrides GOOGLE_APPLICATION_CREDENTIALS env."
    )
    args = parser.parse_args()

    # Handle credentials: explicit flag > existing env > default known path
    if args.credentials:
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = str(args.credentials)
    elif "GOOGLE_APPLICATION_CREDENTIALS" not in os.environ:
        default_key = Path(r"D:\documents\ocr-project-471010-8ec72b217dc3.json")
        if default_key.exists():
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = str(default_key)
        else:
            raise SystemExit(
                "GOOGLE_APPLICATION_CREDENTIALS not set and no credentials file provided. "
                "Use --credentials or set env var."
            )

    # Run OCR
    ocr_text = run_ocr(args.input, language_hints=args.lang_hints)

    # Load templates (supports multi-language template_*.txt auto-discovery)
    template_paths = args.templates if args.templates else list(Path.cwd().glob("template_*.txt"))
    templates = extract_entities.load_templates_from_files(template_paths)

    # Extract entities
    matches = extract_entities.extract_entities(templates, ocr_text)

    # Optionally translate each entity value to English
    if args.translate and matches:
        translated_matches = []
        for item in matches:
            entities = {
                k: (translate_text(v) if isinstance(v, str) and v else v)
                for k, v in item["entities"].items()
            }
            translated_matches.append({"template_id": item["template_id"], "entities": entities})
        matches = translated_matches

    payload = json.dumps(matches, ensure_ascii=False, indent=2)

    if args.output:
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload)


if __name__ == "__main__":
    # Set credentials in your shell before running, e.g. (PowerShell):
    #   $env:GOOGLE_APPLICATION_CREDENTIALS = "D:\\documents\\ocr-project-471010-8ec72b217dc3.json"
    # or (cmd.exe):
    #   set GOOGLE_APPLICATION_CREDENTIALS=D:\documents\ocr-project-471010-8ec72b217dc3.json
    # or export on Linux/macOS:
    #   export GOOGLE_APPLICATION_CREDENTIALS=/path/to/key.json
    main()
