import pypdfium2 as pdfium
from PIL import Image

def mm_to_pixels(mm, dpi):
    return int(mm * dpi / 25.4)

def process_pdf(input_pdf, logo_path, output_pdf, margin_mm=25, logo_width_mm=30, x_offset_mm=3, y_offset_mm=3, dpi=300):
    pdf = pdfium.PdfDocument(input_pdf)
    images = []
    for i in range(len(pdf)):
        page = pdf[i]
        bitmap = page.render(scale=dpi/72)
        pil_image = bitmap.to_pil().convert("RGBA")
        images.append(pil_image)
    pdf.close()

    logo = Image.open(logo_path).convert("RGBA")
    logo_width_px = mm_to_pixels(logo_width_mm, dpi)
    aspect = logo.height / logo.width
    logo_height_px = int(logo_width_px * aspect)
    logo = logo.resize((logo_width_px, logo_height_px), Image.LANCZOS)

    margin_px = mm_to_pixels(margin_mm, dpi)
    x_offset_px = mm_to_pixels(x_offset_mm, dpi)
    y_offset_px = mm_to_pixels(y_offset_mm, dpi)
    processed_images = []
    for img in images:
        # Erase left margin
        draw = Image.new("RGBA", img.size, (255, 255, 255, 0))
        rect = Image.new("RGBA", (margin_px, img.height), (255, 255, 255, 255))
        draw.paste(rect, (0, 0))
        img = Image.alpha_composite(img, draw)
        # Paste logo
        img.paste(logo, (x_offset_px, y_offset_px), logo)
        processed_images.append(img.convert("RGB"))

    processed_images[0].save(output_pdf, save_all=True, append_images=processed_images[1:])

# Usage example
input_pdf = "assets/May_2025_with_handwriting.pdf"
logo_path = "assets/ScribeSync_Intent_to_Sync.png"
output_pdf = "assets/May_2025_with_handwriting_ScribeSync_Logo.pdf"

process_pdf(input_pdf, logo_path, output_pdf)
