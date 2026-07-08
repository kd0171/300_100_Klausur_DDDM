#!/usr/bin/env python
"""Export the curated exam question index to Markdown.

The primary index is maintained in data/exam_question_index.csv. This script is only
for re-generating a readable Markdown table.
"""
from __future__ import annotations

import argparse
import csv
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", default="data/exam_question_index.csv")
    parser.add_argument("--out", default="docs/04_question_index.md")
    args = parser.parse_args()

    csv_path = Path(args.csv)
    rows = list(csv.DictReader(csv_path.open(encoding="utf-8")))
    lines = [
        "# 04 Past exam question index",
        "",
        "過去問PDFから作成した、設問ごとの要約インデックスです。詳細な問題文は `Materials/Altklausuren/` のPDFを参照してください。",
        "",
        "| Term | Question | Points | Topic | What to understand | Likely lecture |",
        "|---|---|---:|---|---|---|",
    ]
    for r in rows:
        lines.append(f"| {r['term']} | {r['question']} | {r['points']} | {r['topic']} | {r['what_to_understand']} | {r['likely_lecture']} |")
    Path(args.out).write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {args.out}")


if __name__ == "__main__":
    main()
