
import pypdfium2 as pdfium

def remove_left_margin_content(input_pdf, output_pdf):
    # Open the PDF
    doc = pdfium.PdfDocument(input_pdf)
    
    # Create a bitmap for each page and draw white rectangle
    for i in range(len(doc)):
        page = doc[i]
        bitmap = page.render(
            scale=1.0,
            rotation=0
        )
        # Draw white rectangle on the left margin
        for y in range(bitmap.height):
            for x in range(min(60, bitmap.width)):
                bitmap.set_pixel(x, y, (255, 255, 255))
        
        # Update the page with modified bitmap
        page.set_bitmap(bitmap)
    
    # Save intermediate result
    doc.save(output_pdf)
    return output_pdf

def add_logo_to_pages(input_pdf, logo_path, output_pdf):
    # Open the PDF and logo
    doc = pdfium.PdfDocument(input_pdf)
    logo_doc = pdfium.PdfDocument(logo_path)
    
    # Calculate scale for 10mm at 300dpi
    target_size = 28.35  # 10mm in points
    logo_page = logo_doc[0]
    original_width = logo_page.get_width()
    scale = target_size / original_width
    
    # Add logo to each page
    for page in doc:
        # Create bitmap of logo
        logo_bitmap = logo_page.render(scale=scale)
        # Get page dimensions
        page_width = page.get_width()
        page_height = page.get_height()
        
        # Position logo at top-left (10, page_height - 50)
        page_bitmap = page.render(scale=1.0)
        page_bitmap.paste(logo_bitmap, 10, page_height - 50)
        page.set_bitmap(page_bitmap)
    
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
