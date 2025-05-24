import cv2
import numpy as np
from PIL import Image
import pypdfium2 as pdfium

def process_pdf_pages(pdf_path, checkbox_position, checkbox_size):
    # Load PDF
    pdf = pdfium.PdfDocument(pdf_path)
    results = []
    
    # Process each page
    for page_number in range(len(pdf)):
        page = pdf[page_number]
        # Render page at 300 DPI (same as logo placement)
        bitmap = page.render(scale=300/72)
        # Convert to OpenCV format
        pil_image = bitmap.to_pil()
        opencv_image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
        
        # Check checkbox on this page
        is_checked = check_checkbox(opencv_image, checkbox_position, checkbox_size)
        results.append({
            'page': page_number + 1,
            'checked': is_checked
        })
    
    return results

def check_checkbox(image, checkbox_position, checkbox_size):
    # Use the image directly (it's already loaded)
    print(f"Image shape: {image.shape}")
    print(f"Checkbox position: {checkbox_position}")
    
    # Crop the region of interest (ROI) for the checkbox
    x, y, width, height = checkbox_position
    roi = image[y:y + height, x:x + width]
    print(f"ROI shape: {roi.shape}")

    # Convert to grayscale
    gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    print(f"Gray ROI shape: {gray_roi.shape}")
    cv2.imwrite('debug_gray_roi.png', gray_roi)

    # Apply adaptive thresholding instead of Otsu
    binary_roi = cv2.adaptiveThreshold(
        gray_roi, 
        255, 
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV, 
        11, 
        2
    )

    # Count dark pixels (assuming dark is the checkbox being ticked)
    dark_pixel_count = cv2.countNonZero(binary_roi)
    
    # Save debug images
    cv2.imwrite('debug_checkbox_roi.png', binary_roi)
    cv2.imwrite('debug_original_roi.png', roi)
    print(f"Dark pixel count: {dark_pixel_count}")
    print(f"Mean pixel value in gray ROI: {np.mean(gray_roi)}")

    # Based on testing, a tick typically has > 400 dark pixels in a 35x35 ROI
    N = 400  # Threshold calibrated for 35x35 checkbox at 300 DPI

    if dark_pixel_count > N:
        return True  # Checkbox ticked
    else:
        return False  # Checkbox not ticked

if __name__ == "__main__":
    # Usage example
    pdf_path = "assets/May_2025_with_handwriting_ScribeSync_Logo_Ticked.pdf"
    # Calculate position based on logo placement (at 300 DPI)
    x_offset_px = int(3 * 300 / 25.4)  # 3mm from left
    y_offset_px = int(3 * 300 / 25.4)  # 3mm from top
    checkbox_size = (35, 35)  # Size in pixels at 300 DPI
    checkbox_position = (x_offset_px + 90, y_offset_px + 90, checkbox_size[0], checkbox_size[1])  # Adjusted offset
    
    results = process_pdf_pages(pdf_path, checkbox_position, checkbox_size)
    for result in results:
        print(f"Page {result['page']}: {'Checked' if result['checked'] else 'Not checked'}")
    