import pypdfium2 as pdfium

doc  = pdfium.PdfDocument("template.pdf")
img  = pdfium.PdfImage("logo_patch.png")        # 120 px PNG
scale = 95 / 120                                # shrink to 8 mm at 300 dpi

for page in doc:
    # (50, 30) is your top-right corner in user-space points
    page.insert_image(img, x=50, y=800, scale=scale)
doc.save("out.pdf")
