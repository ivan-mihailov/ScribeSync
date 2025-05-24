import cv2
import numpy as np
from PIL import Image

def check_checkbox(image_path, checkbox_position, checkbox_size):
    # Load image
    image = cv2.imread(image_path)

    # Crop the region of interest (ROI) for the checkbox
    x, y, width, height = checkbox_position
    roi = image[y:y + height, x:x + width]

    # Convert to grayscale
    gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

    # Apply Otsu's thresholding
    _, binary_roi = cv2.threshold(gray_roi, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Count dark pixels (assuming dark is the checkbox being ticked)
    dark_pixel_count = cv2.countNonZero(binary_roi == 0)
    
    # Save debug image to check ROI
    cv2.imwrite('debug_checkbox_roi.png', binary_roi)
    print(f"Dark pixel count: {dark_pixel_count}")

    # Based on testing, a tick typically has > 400 dark pixels in a 35x35 ROI
    N = 400  # Threshold calibrated for 35x35 checkbox at 300 DPI

    if dark_pixel_count > N:
        return True  # Checkbox ticked
    else:
        return False  # Checkbox not ticked

# Usage example
image_path = "assets/May_2025_with_handwriting_ScribeSync_Logo.pdf"
# Calculate position based on logo placement (at 300 DPI)
x_offset_px = int(3 * 300 / 25.4)  # 3mm from left
y_offset_px = int(3 * 300 / 25.4)  # 3mm from top
checkbox_size = (35, 35)  # Size in pixels at 300 DPI
checkbox_position = (x_offset_px + 20, y_offset_px + 20, checkbox_size[0], checkbox_size[1])  # Offset within logo
is_checked = check_checkbox(image_path, checkbox_position, checkbox_size)

if is_checked:
    print("Checkbox is ticked.")
else:
    print("Checkbox is not ticked.")
    