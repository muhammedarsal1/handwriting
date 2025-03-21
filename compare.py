import cv2
import numpy as np
from PIL import Image
import logging

# Set up logging within compare.py
logging.basicConfig(
    filename="handwriting_app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def compare_handwriting(img1, img2):
    """Compare two handwriting images and return similarity percentage."""
    try:
        # Convert PIL images to numpy arrays
        img1_array = np.array(img1)
        img2_array = np.array(img2)
        logger.info(f"Image 1 shape: {img1_array.shape}, Image 2 shape: {img2_array.shape}")

        # Convert to grayscale if RGB/RGBA
        if len(img1_array.shape) == 3:
            img1_gray = cv2.cvtColor(img1_array, cv2.COLOR_RGB2GRAY)
        else:
            img1_gray = img1_array
        if len(img2_array.shape) == 3:
            img2_gray = cv2.cvtColor(img2_array, cv2.COLOR_RGB2GRAY)
        else:
            img2_gray = img2_array

        # Resize img2 to match img1 dimensions
        if img1_gray.shape != img2_gray.shape:
            img2_gray = cv2.resize(img2_gray, (img1_gray.shape[1], img1_gray.shape[0]), interpolation=cv2.INTER_NEAREST)
            logger.info(f"Resized Image 2 to match Image 1: {img2_gray.shape}")

        # Check if images are identical
        if np.array_equal(img1_gray, img2_gray):
            logger.info("Images are byte-for-byte identical")
            return 100.0

        # Pixel-based difference comparison
        diff = cv2.absdiff(img1_gray, img2_gray)
        non_zero_count = np.count_nonzero(diff)
        total_pixels = img1_gray.size
        similarity_score = 1.0 - (non_zero_count / total_pixels)
        similarity_percent = round(similarity_score * 100, 2)

        logger.info(f"Non-zero diff pixels: {non_zero_count}/{total_pixels}, Similarity: {similarity_percent}%")
        return similarity_percent

    except Exception as e:
        logger.error(f"Comparison failed: {str(e)}")
        raise Exception(f"Comparison failed: {str(e)}")