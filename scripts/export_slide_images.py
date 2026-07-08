#!/usr/bin/env python
"""Export PDF pages as slide images with stable names.

Example:
    python scripts/export_slide_images.py --pdf-dir Materials/2026 --out-dir assets/slides --dpi 180 --skip-duplicates
    python scripts/export_slide_images.py --pdf Materials/2026/3DM_01_Overview_SS26.pdf --out-dir assets/slides
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import re
from pathlib import Path

import fitz  # PyMuPDF


def slugify(path: Path) -> str:
    name = path.stem.lower()
    name = re.sub(r"[^a-z0-9]+", "_", name).strip("_")
    # Keep IDs compatible with the existing note skeletons.
    name = name.replace("information_and_decision_modeling", "information_decision_modeling")
    return name


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def collect_pdfs(args: argparse.Namespace) -> list[Path]:
    if args.pdf:
        return [Path(args.pdf)]
    pdf_dir = Path(args.pdf_dir)
    # Default batch mode processes lecture slide decks only.
    # 3DM_Schedule_SS26.pdf stays in Materials as a source document but is not exported
    # into one-slide-one-note lecture pages unless explicitly passed via --pdf.
    return sorted(p for p in pdf_dir.glob("*.pdf") if re.match(r"3DM_\d{2}_", p.name))


def export_pdf(pdf_path: Path, out_dir: Path, dpi: int) -> list[dict[str, str | int]]:
    lecture_id = slugify(pdf_path)
    lecture_dir = out_dir / lecture_id
    lecture_dir.mkdir(parents=True, exist_ok=True)

    doc = fitz.open(pdf_path)
    zoom = dpi / 72
    matrix = fitz.Matrix(zoom, zoom)
    rows: list[dict[str, str | int]] = []

    for page_index in range(len(doc)):
        page_no = page_index + 1
        filename = f"{lecture_id}_p{page_no:03d}.png"
        image_path = lecture_dir / filename
        if not image_path.exists():
            pix = doc[page_index].get_pixmap(matrix=matrix, alpha=False)
            pix.save(image_path)
        rows.append({
            "lecture_id": lecture_id,
            "source_pdf": str(pdf_path),
            "page": page_no,
            "image_path": str(image_path),
        })
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pdf", help="Single PDF to export")
    parser.add_argument("--pdf-dir", default="Materials/2026", help="Directory containing lecture PDFs")
    parser.add_argument("--out-dir", default="assets/slides", help="Output directory for slide PNGs")
    parser.add_argument("--dpi", type=int, default=180, help="Rendering DPI")
    parser.add_argument("--skip-duplicates", action="store_true", help="Skip PDFs with identical SHA-256 hash")
    parser.add_argument("--index", default="data/slide_image_index.csv", help="CSV index path")
    args = parser.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    seen_hashes: dict[str, Path] = {}
    all_rows: list[dict[str, str | int]] = []
    for pdf in collect_pdfs(args):
        if not pdf.exists():
            raise FileNotFoundError(pdf)
        digest = sha256(pdf)
        if args.skip_duplicates and digest in seen_hashes:
            print(f"Skip duplicate: {pdf} == {seen_hashes[digest]}")
            continue
        seen_hashes[digest] = pdf
        print(f"Exporting {pdf} ...")
        all_rows.extend(export_pdf(pdf, out_dir, args.dpi))

    index_path = Path(args.index)
    index_path.parent.mkdir(parents=True, exist_ok=True)
    with index_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["lecture_id", "source_pdf", "page", "image_path"])
        writer.writeheader()
        writer.writerows(all_rows)
    print(f"Wrote {index_path}")


if __name__ == "__main__":
    main()
