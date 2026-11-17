#!/usr/bin/env bash
# Builds the PDF and the arXiv source archive (tex files + numbers.tex + compiled .bbl). Nothing is uploaded.
set -euo pipefail
cd "$(dirname "$0")"
python3 -I ../analysis/make_numbers.py
pdflatex -interaction=nonstopmode main >/dev/null; bibtex main >/dev/null
pdflatex -interaction=nonstopmode main >/dev/null; pdflatex -interaction=nonstopmode main >/dev/null
if pdftotext main.pdf - | grep -q '??'; then echo "missing number in PDF"; exit 1; fi
rm -f arxiv-source.tar.gz
COPYFILE_DISABLE=1 tar czf arxiv-source.tar.gz main.tex methods.tex related.tex numbers.tex main.bbl fig1.pdf
echo "ok: main.pdf ($(pdfinfo main.pdf | awk '/Pages/{print $2}') pages), arxiv-source.tar.gz"
