import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim
from PIL import Image

def compare_handwriting(img1, img2):
    """Compare two handwriting images and return similarity percentage."""
    try:
        # Convert PIL images to numpy arrays
        img1_array = np.array(img1)
        img2_array = np.array(img2)

        # Convert to grayscale if RGB/RGBA
        if len(img1_array.shape) == 3:
            img1_gray = cv2.cvtColor(img1_array, cv2.COLOR_RGB2GRAY)
        else:
            img1_gray = img1_array
        if len(img2_array.shape) == 3:
            img2_gray = cv2.cvtColor(img2_array, cv2.COLOR_RGB2GRAY)
        else:
            img2_gray = img2_array

        # Resize img2 to match img1 dimensions with minimal distortion
        if img1_gray.shape != img2_gray.shape:
            img2_gray = cv2.resize(img2_gray, (img1_gray.shape[1], img1_gray.shape[0]), interpolation=cv2.INTER_NEAREST)

        # Check for identical images first
        if np.array_equal(img1_gray, img2_gray):
            return 100.0

        # Calculate SSIM with minimal preprocessing
        similarity_score = ssim(img1_gray, img2_gray, data_range=255)

        # Convert to percentage
        similarity_percent = round(similarity_score * 100, 2)
        
        return similarity_percent
    except Exception as e:
        raise Exception(f"Comparison failed: {str(e)}")