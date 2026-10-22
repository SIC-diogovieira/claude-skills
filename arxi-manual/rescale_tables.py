#!/usr/bin/env python3
"""Force every table in a pandoc-generated .docx to span the full page width.

Why this exists: pandoc sets each table's width as a percentage
(w:tblW type="pct") and its column widths (w:tblGrid) as absolute twips
computed from the source Markdown's column content. Word honors the
percentage; several other readers (observed with Google Docs' .docx import)
instead trust the literal w:tblGrid sum, which is almost always narrower
than the page. Recomputing w:tblGrid so its columns sum to the real usable
page width (pgSz - pgMar, read from the document itself) fixes it everywhere.

Usage: python3 rescale_tables.py FILE.docx [FILE2.docx ...]
Edits each file in place.
"""
import re
import shutil
import sys
import zipfile

GRID_RE = re.compile(r'<w:tblGrid>((?:<w:gridCol w:w="\d+" ?/>)+)</w:tblGrid>')
COL_RE = re.compile(r'w:gridCol w:w="(\d+)" ?/>')


def usable_width(doc_xml: str) -> int:
    pg_sz = re.search(r'<w:pgSz[^/]*w:w="(\d+)"', doc_xml)
    pg_mar = re.search(r'<w:pgMar[^/]*w:left="(\d+)"[^/]*w:right="(\d+)"', doc_xml)
    if not pg_mar:
        pg_mar = re.search(r'<w:pgMar[^/]*/>', doc_xml)
        left = re.search(r'w:left="(\d+)"', pg_mar.group(0))
        right = re.search(r'w:right="(\d+)"', pg_mar.group(0))
        return int(pg_sz.group(1)) - int(left.group(1)) - int(right.group(1))
    return int(pg_sz.group(1)) - int(pg_mar.group(1)) - int(pg_mar.group(2))


def rescale(fname: str) -> None:
    with zipfile.ZipFile(fname, "r") as zin:
        items = zin.infolist()
        data = {i.filename: zin.read(i.filename) for i in items}

    doc = data["word/document.xml"].decode("utf-8")
    width = usable_width(doc)

    def rescale_grid(m: re.Match) -> str:
        cols = [int(x) for x in COL_RE.findall(m.group(1))]
        total = sum(cols)
        scaled = [round(c * width / total) for c in cols]
        scaled[-1] += width - sum(scaled)  # fix rounding drift
        return "<w:tblGrid>" + "".join(f'<w:gridCol w:w="{w}" />' for w in scaled) + "</w:tblGrid>"

    n_tables = len(GRID_RE.findall(doc))
    doc = GRID_RE.sub(rescale_grid, doc)
    doc = re.sub(
        r'<w:tblW w:type="(?:pct|auto)" w:w="\d+" ?/>',
        f'<w:tblW w:type="dxa" w:w="{width}" />',
        doc,
    )
    data["word/document.xml"] = doc.encode("utf-8")

    tmp = fname + ".tmp"
    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
        for i in items:
            zout.writestr(i, data[i.filename])
    shutil.move(tmp, fname)
    print(f"{fname}: rescaled {n_tables} table(s) to {width} twips (full page width)")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("usage: rescale_tables.py FILE.docx [FILE2.docx ...]")
    for path in sys.argv[1:]:
        rescale(path)
