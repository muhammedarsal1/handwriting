import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim
from PIL import Image

def compare_handwriting(img1, img2):
    """Compare two handwriting images and return similarity percentage."""
    try:
        # Convert to grayscale
        img1 = np.array(img1.convert("L"))
        img2 = np.array(img2.convert("L"))
        # Resize comparison image to match main image dimensions
        img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))
        # Calculate SSIM
        similarity_score = ssim(img1, img2)
        return round(similarity_score * 100, 2)
    except Exception as e:
        raise Exception(f"Comparison failed: {str(e)}")