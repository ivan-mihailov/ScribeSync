
import pypdfium2 as pdfium

def remove_left_margin_content(input_pdf, output_pdf):
    # Open the PDF
    doc = pdfium.PdfDocument(input_pdf)
    
    # For each page, add a white overlay on the left margin
    for page in doc:
        # Create a form XObject for the white overlay
        form = page.new_form_xobject(0, 0, 60, 842)  # left margin area
        form.fill_rect(0, 0, 60, 842, (255, 255, 255))  # white rectangle
    
    # Save intermediate result
    doc.save(output_pdf)
    return output_pdf

def add_logo_to_pages(input_pdf, logo_path, output_pdf):
    # Open the PDF
    doc = pdfium.PdfDocument(input_pdf)
    logo = pdfium.PdfDocument.new_from_file(logo_path)
    
    # Calculate scale for 10mm at 300dpi
    target_size = 28.35  # 10mm in points
    original_width = logo.get_page(0).get_width()
    scale = target_size / original_width
    
    # Add logo to each page
    for page in doc:
        form = page.new_form_xobject(10, 800, target_size, target_size)
        form.insert_object(logo.get_page(0), scale=scale)
    
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
