
import pypdfium2 as pdfium

def remove_left_margin_content(input_pdf, output_pdf):
    # Open the PDF
    doc = pdfium.PdfDocument(input_pdf)
    
    # For each page, create a white rectangle covering the left margin
    for page in doc:
        # Create white rectangle covering left 60 points (roughly 20mm)
        page.draw_rect(0, 0, 60, 842, color=(255, 255, 255), fill=True)
    
    # Save intermediate result
    doc.save(output_pdf)
    return output_pdf

def add_logo_to_pages(input_pdf, logo_path, output_pdf):
    # Open the PDF
    doc = pdfium.PdfDocument(input_pdf)
    img = pdfium.PdfImage(logo_path)
    
    # Calculate scale for 10mm at 300dpi
    # 10mm = ~28.35 points, assuming 300dpi
    target_size = 28.35  # 10mm in points
    original_size = 120  # assuming original is 120px
    scale = target_size / original_size
    
    # Add logo to each page
    for page in doc:
        page.insert_image(img, x=10, y=800, scale=scale)  # Positioned at top-left
    
    # Save final result
    doc.save(output_pdf)

# Execute the process
input_pdf = "assets/May_2025_blank.pdf"
temp_pdf = "assets/temp_cleaned.pdf"
logo_path = "assets/ScribeSync_Intent_to_Sync.png"
output_pdf = "assets/May_2025_blank_ScribeSync_Logo.pdf"

# First remove existing logos
remove_left_margin_content(input_pdf, temp_pdf)

# Then add new logo
add_logo_to_pages(temp_pdf, logo_path, output_pdf)
