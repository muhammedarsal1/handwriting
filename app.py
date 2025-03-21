import streamlit as st
import os
import shutil
from PIL import Image
from compare import compare_handwriting
import logging
import time

# Set up logging
logging.basicConfig(
    filename="handwriting_app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Folder setup
DATA_DIR = "data"
MAIN_DIR = os.path.join(DATA_DIR, "main")
COMP_DIR = os.path.join(DATA_DIR, "comparisons")
for folder in [MAIN_DIR, COMP_DIR]:
    os.makedirs(folder, exist_ok=True)

# App title and description
st.title("📝 Handwriting Comparison App")
st.markdown("Capture or upload handwriting samples to compare their similarity!")

# Input method selection
input_method = st.radio("Choose Input Method:", ["📸 Camera", "📂 Upload"], horizontal=True)

# Initialize session state
if "main_image_path" not in st.session_state:
    st.session_state["main_image_path"] = None
if "comp_image_paths" not in st.session_state:
    st.session_state["comp_image_paths"] = []

# Function to save image with unique timestamp
def save_image(image, folder, prefix="image"):
    timestamp = int(time.time() * 1000)  # Unique millisecond timestamp
    filename = f"{prefix}_{timestamp}.png"
    path = os.path.join(folder, filename)
    image.save(path)
    return path

# Main Handwriting Section
st.subheader("1. Main Handwriting Sample")
if input_method == "📸 Camera":
    if not st.session_state["main_image_path"]:  # Only show camera if main image isn’t captured yet
        st.markdown("*Use your device's back camera for best results.*")
        main_image = st.camera_input("Capture Main Handwriting (Back Camera)", key="main_camera")
        if main_image:
            main_img = Image.open(main_image)
            st.session_state["main_image_path"] = save_image(main_img, MAIN_DIR, "main")
            st.success("✅ Main handwriting captured successfully!")
            logger.info(f"Main handwriting captured: {os.path.basename(st.session_state['main_image_path'])}")
    else:
        st.info("Main sample captured. Proceed to comparison samples below.")
else:
    main_upload = st.file_uploader("Upload Main Handwriting", type=["png", "jpg", "jpeg"], key="main_upload")
    if main_upload:
        main_img = Image.open(main_upload)
        st.session_state["main_image_path"] = save_image(main_img, MAIN_DIR, "main")
        st.success("✅ Main handwriting uploaded successfully!")
        logger.info(f"Main handwriting uploaded: {os.path.basename(st.session_state['main_image_path'])}")

# Display Main Image
if st.session_state["main_image_path"]:
    st.image(st.session_state["main_image_path"], caption="Main Handwriting Sample", use_column_width=True)

# Comparison Handwriting Section (Enabled only after main sample)
st.subheader("2. Comparison Handwriting Samples")
if st.session_state["main_image_path"]:  # Only show if main image exists
    if input_method == "📸 Camera":
        st.markdown("*Use your device's back camera for best results.*")
        comp_image = st.camera_input("Capture Comparison Handwriting (Back Camera)", key="comp_camera")
        if comp_image:
            comp_img = Image.open(comp_image)
            comp_path = save_image(comp_img, COMP_DIR, "comp")
            st.session_state["comp_image_paths"].append(comp_path)
            st.success("✅ Comparison handwriting captured successfully!")
            logger.info(f"Comparison handwriting captured: {os.path.basename(comp_path)}")
    else:
        comp_uploads = st.file_uploader(
            "Upload Comparison Handwriting (multiple allowed)", 
            type=["png", "jpg", "jpeg"], 
            accept_multiple_files=True, 
            key="comp_upload"
        )
        if comp_uploads:
            for comp_upload in comp_uploads:
                comp_img = Image.open(comp_upload)
                comp_path = save_image(comp_img, COMP_DIR, "comp")
                st.session_state["comp_image_paths"].append(comp_path)
                logger.info(f"Comparison handwriting uploaded: {os.path.basename(comp_path)}")
            st.success(f"✅ {len(comp_uploads)} comparison handwriting sample(s) uploaded successfully!")
else:
    st.warning("⚠️ Please capture or upload the main handwriting sample first!")

# Display Comparison Images
if st.session_state["comp_image_paths"]:
    st.markdown("### Comparison Samples")
    cols = st.columns(3)  # 3 images per row
    for i, comp_path in enumerate(st.session_state["comp_image_paths"]):
        with cols[i % 3]:
            st.image(comp_path, caption=os.path.basename(comp_path), width=150)

# Compare Button
if st.button("🔍 Compare", use_container_width=True):
    if not st.session_state["main_image_path"]:
        st.error("❌ Please provide a main handwriting sample first!")
        logger.warning("Comparison attempted without main image")
    elif not st.session_state["comp_image_paths"]:
        st.error("❌ Please provide at least one comparison handwriting sample!")
        logger.warning("Comparison attempted without comparison images")
    else:
        main_img = Image.open(st.session_state["main_image_path"])
        st.markdown("### Similarity Scores")
        with st.spinner("Comparing handwriting..."):
            for comp_path in st.session_state["comp_image_paths"]:
                comp_img = Image.open(comp_path)
                try:
                    similarity = compare_handwriting(main_img, comp_img)
                    st.write(f"- **{os.path.basename(comp_path)}**: {similarity}% similar")
                    logger.info(f"Compared {os.path.basename(comp_path)} with main: {similarity}%")
                except Exception as e:
                    st.error(f"Error comparing {os.path.basename(comp_path)}: {str(e)}")
                    logger.error(f"Comparison failed for {os.path.basename(comp_path)}: {str(e)}")
        st.success("✅ Comparison complete!")

# Clear Button
if st.button("🔄 Clear All", use_container_width=True):
    st.session_state["main_image_path"] = None
    st.session_state["comp_image_paths"] = []
    shutil.rmtree(DATA_DIR, ignore_errors=True)
    os.makedirs(MAIN_DIR, exist_ok=True)
    os.makedirs(COMP_DIR, exist_ok=True)
    st.success("🗑️ All images and data cleared!")
    logger.info("All data cleared by user")
    st.rerun()