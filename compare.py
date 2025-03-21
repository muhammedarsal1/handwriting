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

        # If images are RGBA or RGB, convert to grayscale
        if len(img1_array.shape) == 3:
            img1_gray = cv2.cvtColor(img1_array, cv2.COLOR_RGB2GRAY)
        else:
            img1_gray = img1_array
        if len(img2_array.shape) == 3:
            img2_gray = cv2.cvtColor(img2_array, cv2.COLOR_RGB2GRAY)
        else:
            img2_gray = img2_array

        # Ensure images are the same size without excessive interpolation
        if img1_gray.shape != img2_gray.shape:
            # Resize img2 to match img1 dimensions using INTER_AREA for better quality
            img2_gray = cv2.resize(img2_gray, (img1_gray.shape[1], img1_gray.shape[0]), interpolation=cv2.INTER_AREA)

        # Calculate SSIM with adjusted parameters for better sensitivity
        similarity_score = ssim(img1_gray, img2_gray, data_range=255, gaussian_weights=True, sigma=1.5)

        # Convert to percentage and ensure identical images get near 100%
        similarity_percent = round(similarity_score * 100, 2)
        
        # Debugging: If images are identical (byte-for-byte), force 100%
        if np.array_equal(img1_gray, img2_gray):
            similarity_percent = 100.0

        return similarity_percent
    except Exception as e:
        raise Exception(f"Comparison failed: {str(e)}")