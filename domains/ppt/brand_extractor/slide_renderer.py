"""Render representative slides of each PPTX in source_dir to PNG thumbs.

Strategy:
  1. Convert each .pptx -> temp .pdf via `soffice --headless --convert-to pdf`
  2. Convert each PDF page -> PNG via pdftoppm (poppler-utils) at 100 dpi
  3. Drop into <out_dir>/<pptx_stem>-NN.png

Subprocess only, no python-pptx render. Falls back to a silent skip if
soffice/pdftoppm aren't installed.
"""
from pathlib import Path
import shutil
import subprocess
import tempfile


def render_thumbs(source_dir: Path, out_dir: Path) -> list[Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    if not shutil.which("soffice") or not shutil.which("pdftoppm"):
        return []

    written: list[Path] = []
    for pptx in sorted(source_dir.glob("*.pptx")):
        with tempfile.TemporaryDirectory(dir="/data/tmp") as scratch_str:
            scratch = Path(scratch_str)
            r = subprocess.run(
                [
                    "soffice",
                    "--headless",
                    "--convert-to",
                    "pdf",
                    "--outdir",
                    str(scratch),
                    str(pptx),
                ],
                capture_output=True,
                timeout=120,
            )
            pdf = scratch / (pptx.stem + ".pdf")
            if r.returncode != 0 or not pdf.exists():
                continue

            stem = pptx.stem.replace(" ", "_")
            r2 = subprocess.run(
                ["pdftoppm", "-png", "-r", "100", str(pdf), str(out_dir / stem)],
                capture_output=True,
                timeout=120,
            )
            if r2.returncode == 0:
                written.extend(sorted(out_dir.glob(f"{stem}-*.png")))
    return written
