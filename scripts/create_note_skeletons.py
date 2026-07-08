#!/usr/bin/env python
"""Create Markdown note skeletons with one section per slide.

This script does not translate or explain anything. It only creates a stable structure
that ChatGPT and the user can fill in later.
"""
from __future__ import annotations

import argparse
import hashlib
import re
from pathlib import Path

import fitz


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


def extract_title(page: fitz.Page) -> str:
    text = page.get_text("text")
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    # Try to ignore headers/footers and select a plausible title.
    for line in lines[:10]:
        if "Data Driven Decision Making" in line:
            continue
        if "©" in line or "Page" in line:
            continue
        if len(line) <= 80:
            return line
    return ""


def make_note(pdf: Path, slides_dir: Path, notes_dir: Path, overwrite: bool = False) -> None:
    lecture_id = slugify(pdf)
    out_path = notes_dir / f"{lecture_id}.md"
    if out_path.exists() and not overwrite:
        print(f"Keep existing: {out_path}")
        return

    doc = fitz.open(pdf)
    rel_prefix = Path("../assets/slides") / lecture_id
    lines: list[str] = [
        "---",
        f"lecture_id: {lecture_id}",
        f"source_pdf: {pdf.as_posix()}",
        f"slides: {len(doc)}",
        "status: skeleton",
        "---",
        "",
        f"# {lecture_id}",
        "",
        "> このファイルは自動生成された雛形です。翻訳・解説・試験対策ポイントはChatGPTと手作業で埋めます。",
        "",
    ]
    for i, page in enumerate(doc, start=1):
        title = extract_title(page)
        image_path = rel_prefix / f"{lecture_id}_p{i:03d}.png"
        lines.extend([
            f"## Slide {i:03d}" + (f": {title}" if title else ""),
            "",
            f"![Slide {i:03d}]({image_path.as_posix()})",
            "",
            "### 日本語訳",
            "",
            "TODO",
            "",
            "### 解説",
            "",
            "TODO",
            "",
            "### 試験で確実に理解すべき点",
            "",
            "TODO",
            "",
            "### 過去問との関連",
            "",
            "TODO",
            "",
            "### 確認問題",
            "",
            "1. TODO",
            "",
        ])
    notes_dir.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {out_path}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pdf-dir", default="Materials/2026")
    parser.add_argument("--slides-dir", default="assets/slides")
    parser.add_argument("--notes-dir", default="notes")
    parser.add_argument("--skip-duplicates", action="store_true")
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()

    # Default batch mode processes lecture slide decks only.
    # 3DM_Schedule_SS26.pdf remains a source document but is skipped here.
    pdfs = sorted(p for p in Path(args.pdf_dir).glob("*.pdf") if re.match(r"3DM_\d{2}_", p.name))
    seen: dict[str, Path] = {}
    for pdf in pdfs:
        digest = sha256(pdf)
        if args.skip_duplicates and digest in seen:
            print(f"Skip duplicate: {pdf} == {seen[digest]}")
            continue
        seen[digest] = pdf
        make_note(pdf, Path(args.slides_dir), Path(args.notes_dir), args.overwrite)


if __name__ == "__main__":
    main()
