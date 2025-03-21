import streamlit as st
from PIL import Image
import compare
import logging

# Configure logging
logging.basicConfig(
    filename="handwriting_app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Streamlit app layout
st.title("Handwriting Comparison App")

# Main image input
st.subheader("Main Handwriting Sample")
main_option = st.radio("Choose input method for main sample:", ("Upload", "Camera"), key="main_option")
main_image = None

if main_option == "Upload":
    uploaded_main = st.file_uploader("Upload main handwriting image", type=["png", "jpg", "jpeg"], key="main_upload")
    if uploaded_main:
        main_image = Image.open(uploaded_main)
        st.image(main_image, caption="Main Handwriting Sample", use_column_width=True)
        logger.info("Main image uploaded successfully")
elif main_option == "Camera":
    camera_main = st.camera_input("Capture main handwriting sample", key="main_camera")
    if camera_main:
        main_image = Image.open(camera_main)
        st.image(main_image, caption="Main Handwriting Sample", use_column_width=True)
        logger.info("Main image captured via camera")

# Comparison image input
st.subheader("Comparison Handwriting Sample")
comp_option = st.radio("Choose input method for comparison sample:", ("Upload", "Camera"), key="comp_option")
comp_image = None

if comp_option == "Upload":
    uploaded_comp = st.file_uploader("Upload comparison handwriting image", type=["png", "jpg", "jpeg"], key="comp_upload")
    if uploaded_comp:
        comp_image = Image.open(uploaded_comp)
        st.image(comp_image, caption="Comparison Handwriting Sample", use_column_width=True)
        logger.info("Comparison image uploaded successfully")
elif comp_option == "Camera":
    camera_comp = st.camera_input("Capture comparison handwriting sample", key="comp_camera")
    if camera_comp:
        comp_image = Image.open(camera_comp)
        st.image(comp_image, caption="Comparison Handwriting Sample", use_column_width=True)
        logger.info("Comparison image captured via camera")

# Compare button
if st.button("🔍 Compare", key="compare_button"):
    if main_image and comp_image:
        try:
            logger.info("Starting comparison between main and comparison images")
            similarity = compare.compare_handwriting(main_image, comp_image)
            st.success(f"Similarity Score: {similarity}%")
            logger.info(f"Comparison completed: Similarity = {similarity}%")
        except Exception as e:
            st.error(f"Error: {str(e)}")
            logger.error(f"Comparison failed: {str(e)}")
    else:
        st.warning("Please provide both main and comparison images.")
        logger.warning("Comparison attempted without both images")