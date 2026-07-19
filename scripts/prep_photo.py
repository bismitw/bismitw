import cv2
import numpy as np
from rembg import remove
from PIL import Image
import sys

def prep_image(input_path, output_path="source-prepped.png"):
    print(f"Processing {input_path}...")
    
    # 1. Remove background using rembg
    input_img = Image.open(input_path)
    subject_only = remove(input_img)
    
    # Convert PIL image to OpenCV format (numpy array)
    cv_img = np.array(subject_only)
    
    # Extract color (BGR) and Alpha channels
    if cv_img.shape[2] == 4:
        bgr = cv_img[:, :, :3]
        alpha = cv_img[:, :, 3]
    else:
        print("Error: Image has no alpha channel after rembg.")
        sys.exit(1)

    # 2. Convert to Grayscale and boost contrast
    gray = cv2.cvtColor(bgr, cv2.COLOR_RGB2GRAY)
    
    # CLAHE (Contrast Limited Adaptive Histogram Equalization)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
    contrast_boosted = clahe.apply(gray)
    
    # 3. Composite onto pure white
    # White background ensures it maps to the "blank" end of our ASCII ramp
    white_bg = np.ones_like(contrast_boosted) * 255
    alpha_float = alpha.astype(float) / 255.0
    
    composited = (contrast_boosted * alpha_float + white_bg * (1.0 - alpha_float)).astype(np.uint8)
    
    cv2.imwrite(output_path, composited)
    print(f"Success! Prepped image saved to {output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scripts/prep_photo.py ")
        sys.exit(1)
    prep_image(sys.argv[1])