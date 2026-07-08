#!/usr/bin/env python
"""Compile a LaTeX file to PDF using latexmk/xelatex.

Example:
    python scripts/compile_latex.py --tex latex/main.tex --out-dir output --build-dir build
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
from pathlib import Path


def run(cmd: list[str], cwd: Path | None = None) -> None:
    print(" ".join(cmd))
    proc = subprocess.run(cmd, cwd=cwd, text=True)
    if proc.returncode != 0:
        raise SystemExit(proc.returncode)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tex", default="latex/main.tex", help="Path to main .tex file")
    parser.add_argument("--out-dir", default="output", help="Directory for final PDF")
    parser.add_argument("--build-dir", default="build", help="Directory for LaTeX auxiliary files")
    parser.add_argument("--jobname", default=None, help="Optional output job name without .pdf")
    args = parser.parse_args()

    tex_path = Path(args.tex).resolve()
    if not tex_path.exists():
        raise FileNotFoundError(tex_path)

    out_dir = Path(args.out_dir).resolve()
    build_dir = Path(args.build_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    build_dir.mkdir(parents=True, exist_ok=True)

    jobname = args.jobname or tex_path.stem
    latexmk = shutil.which("latexmk")

    if latexmk:
        cmd = [
            latexmk,
            "-xelatex",
            "-interaction=nonstopmode",
            "-halt-on-error",
            f"-outdir={build_dir}",
            f"-jobname={jobname}",
            tex_path.name,
        ]
        run(cmd, cwd=tex_path.parent)
    else:
        xelatex = shutil.which("xelatex")
        if not xelatex:
            raise RuntimeError("Neither latexmk nor xelatex was found on PATH.")
        for _ in range(2):
            run([
                xelatex,
                "-interaction=nonstopmode",
                "-halt-on-error",
                f"-output-directory={build_dir}",
                f"-jobname={jobname}",
                tex_path.name,
            ], cwd=tex_path.parent)

    pdf = build_dir / f"{jobname}.pdf"
    if not pdf.exists():
        raise FileNotFoundError(pdf)
    target = out_dir / pdf.name
    shutil.copy2(pdf, target)
    print(f"Wrote {target}")


if __name__ == "__main__":
    main()
