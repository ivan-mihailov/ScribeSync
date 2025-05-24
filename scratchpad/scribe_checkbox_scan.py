"""
scribe_checkbox_scan.py
-----------------------
Detect whether the ScribeSync intent-to-sync checkbox is ticked on
each page of a Kindle-Scribe PDF export.

Usage:
    python scribe_checkbox_scan.py my_planner.pdf
"""
import sys, cv2, numpy as np
import pypdfium2 as pdfium
from pathlib import Path

# ----------  EDIT ONCE, THEN KEEP  ---------- #
# relative bbox of the checkbox (fractions of full-page width/height)
REL_X  = 0.052   # left   fraction
REL_Y  = 0.081   # top    fraction
REL_W  = 0.030   # width  fraction  (≈ 3 % of page width)
REL_H  = 0.022   # height fraction  (≈ 2 % of page height)

INK_THRESHOLD = 0.095       # ≥10 % dark pixels ⇒ considered ticked
DPI           = 300
# -------------------------------------------- #

def render_page(page, dpi=DPI):
    """Return page as a BGR NumPy array at the requested DPI."""
    scale = dpi / 72  # PDF user-space is 72 dpi
    bmp   = page.render(scale=scale)
    return cv2.cvtColor(np.array(bmp.to_pil()), cv2.COLOR_RGB2BGR)

def checkbox_is_checked(img):
    h_full, w_full = img.shape[:2]

    # absolute pixel bbox
    x = int(REL_X * w_full)
    y = int(REL_Y * h_full)
    w = int(REL_W * w_full)
    h = int(REL_H * h_full)

    roi = img[y : y + h, x : x + w]

    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    _, bin_roi = cv2.threshold(
        gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU
    )

    ink_ratio = cv2.countNonZero(bin_roi) / (w * h)
    print(f"page_ratio = {ink_ratio:.3f}")    # add this
    return ink_ratio >= INK_THRESHOLD

def process_pdf(pdf_path):
    pdf = pdfium.PdfDocument(str(pdf_path))
    results = []

    for page_no in range(len(pdf)):
        img = render_page(pdf[page_no])
        checked = checkbox_is_checked(img)
        results.append((page_no + 1, checked))

    return results

# -------------------- CLI -------------------- #
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python scribe_checkbox_scan.py <file.pdf>")
        sys.exit(1)

    pdf_file = Path(sys.argv[1])
    if not pdf_file.exists():
        print(f"File not found: {pdf_file}")
        sys.exit(1)

    for page, checked in process_pdf(pdf_file):
        state = "Checked" if checked else "Not checked"
        print(f"Page {page:>3}: {state}")
