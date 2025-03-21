import cv2
import numpy as np
from PIL import Image

def compare_handwriting(img1, img2):
    """Compare two handwriting images using ORB keypoints and return similarity percentage."""
    try:
        # Convert PIL images to numpy arrays and grayscale
        img1_array = np.array(img1)
        img2_array = np.array(img2)
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

        # Check for identical images
        if np.array_equal(img1_gray, img2_gray):
            return 100.0

        # Initialize ORB detector
        orb = cv2.ORB_create(nfeatures=1000)  # Increased for more keypoints
        
        # Detect keypoints and descriptors
        kp1, des1 = orb.detectAndCompute(img1_gray, None)
        kp2, des2 = orb.detectAndCompute(img2_gray, None)

        # If no keypoints detected
        if des1 is None or des2 is None:
            return 10.0

        # Match descriptors
        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        matches = bf.match(des1, des2)
        
        # Sort matches by distance
        matches = sorted(matches, key=lambda x: x.distance)
        
        # Calculate similarity based on good matches
        if len(matches) == 0:
            return 10.0
        good_matches = [m for m in matches if m.distance < 50]  # Adjusted threshold
        similarity_percent = min(100.0, len(good_matches) / min(len(kp1), len(kp2)) * 100 * 2)
        
        return round(similarity_percent, 2)
    except Exception as e:
        raise Exception(f"Comparison failed: {str(e)}")