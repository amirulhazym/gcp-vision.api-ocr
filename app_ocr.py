# Step 1: Import necessary libraries
import streamlit as st
import io
from google.cloud import vision
import pandas as pd # For CSV export
from PIL import Image # For displaying image info, though Streamlit handles display
import os # 

# --- Page Configuration (Modern Touch) ---
# JIT Learning: st.set_page_config() is used to customize the browser tab title, icon,
# and layout. 'wide' layout gives more space. It must be the first Streamlit command.
st.set_page_config(
    page_title="GCP Vision API: OCR Extractor",
    page_icon="📄", # any emoji 
    layout="wide",
    initial_sidebar_state="auto"
)

# --- GCP Vision API Client Initialization (Cached for efficiency) ---
# JIT Learning: @st.cache_resource tells Streamlit to cache the output of this function.
# This means the Vision API client is created only once, not on every script rerun
# (which happens with every user interaction in Streamlit), making the app more efficient.
@st.cache_resource # Using cache_resource for client objects
def get_vision_client():
    """Initializes and returns a Vision API client."""
    try:
        client = vision.ImageAnnotatorClient()
        return client
    except Exception as e:
        st.error(f"Error initializing GCP Vision API client: {e}")
        st.error("Please ensure Application Default Credentials (ADC) are set up correctly and the Vision API is enabled.")
        return None

vision_client = get_vision_client()

# --- Core OCR Function ---
# JIT Learning: This function encapsulates the logic to call the Vision API.
# It's good practice to keep core logic separate from UI rendering.
def perform_ocr_on_image_bytes(image_bytes, client):
    """
    Performs OCR on image bytes using the provided Vision API client.

    Args:
        image_bytes (bytes): The byte content of the image.
        client: The initialized google.cloud.vision.ImageAnnotatorClient.

    Returns:
        str: The extracted text, or None if an error occurs or no text is found.
    """
    if not client:
        st.error("Vision API client not available. Cannot perform OCR.")
        return None

    try:
        image_for_api = vision.Image(content=image_bytes)
        st.info("Sending image to Google Cloud Vision API...") # User feedback
        response = client.document_text_detection(image=image_for_api)

        if response.error.message:
            st.error(f"Vision API Error: {response.error.message}")
            return None
        if response.full_text_annotation:
            return response.full_text_annotation.text
        else:
            st.warning("No text found in the image by the API.")
            return None
    except Exception as e:
        # Catching potential proxy/network errors here again for robustness within Streamlit
        st.error(f"An error occurred during the Vision API request: {e}")
        st.error("Please check your internet connection and proxy settings (if any).")
        return None

# --- Streamlit User Interface ---

# --- Header and Title ---
st.title("📄 GCP Vision OCR - Text Extractor")
st.markdown("""
Upload an image file (PNG, JPG, JPEG) to extract text using Google Cloud's Vision API.
This tool demonstrates a simple application of cloud-based Optical Character Recognition.
""")
st.divider() # Visual separator for a cleaner look

# --- Session State Initialization (Modern UI Best Practice) ---
# JIT Learning: st.session_state allows you to store variables across reruns of the script.
# This is crucial for keeping data (like extracted text) persistent when a user interacts
# with different widgets (e.g., after extracting text, the text remains for download).
if "extracted_text" not in st.session_state:
    st.session_state.extracted_text = None
if "uploaded_file_name" not in st.session_state:
    st.session_state.uploaded_file_name = None

# --- File Uploader Section ---
st.subheader("1. Upload Your Image")
uploaded_file = st.file_uploader(
    "Choose an image file",
    type=["png", "jpg", "jpeg"],
    help="Supported formats: PNG, JPG, JPEG. Max file size: ~4MB for Vision API synchronous requests."
)

# --- Image Display and OCR Trigger Section ---
if uploaded_file is not None:
    # Display the uploaded image
    st.markdown("---") # Visual separator
    st.subheader("2. Review Image & Extract Text")
    
    # JIT Learning: Using columns can help organize layout.
    col1, col2 = st.columns([1, 2]) # Image in smaller column, details/button in larger

    with col1:
        try:
            # JIT Learning: Displaying the image using Streamlit's st.image.
            # 'caption' provides context. 'use_column_width' makes it fit the column.
            st.image(uploaded_file, caption=f"Uploaded: {uploaded_file.name}", use_column_width=True)
        except Exception as e:
            st.error(f"Error displaying image: {e}")

    with col2:
        st.write(f"**File name:** `{uploaded_file.name}`")
        st.write(f"**File type:** `{uploaded_file.type}`")
        st.write(f"**File size:** `{uploaded_file.size / 1024:.2f} KB`")

        if st.button("🔍 Extract Text from Image", type="primary", use_container_width=True):
            if vision_client:
                # JIT Learning: st.spinner provides a visual cue that processing is happening.
                with st.spinner("Processing image and extracting text... Please wait."):
                    image_bytes = uploaded_file.getvalue() # Get bytes from the uploaded file
                    extracted_text = perform_ocr_on_image_bytes(image_bytes, vision_client)
                    
                    if extracted_text:
                        st.session_state.extracted_text = extracted_text
                        st.session_state.uploaded_file_name = uploaded_file.name # Store for CSV filename
                        st.success("✅ Text extraction successful!")
                    else:
                        # Error messages are handled within perform_ocr_on_image_bytes
                        # but we clear previous results if extraction fails
                        st.session_state.extracted_text = None 
                        st.session_state.uploaded_file_name = None
            else:
                st.error("Vision API client is not initialized. Cannot extract text.")
else:
    # If no file is uploaded yet, ensure session state is clear
    st.session_state.extracted_text = None
    st.session_state.uploaded_file_name = None
    st.info("☝️ Upload an image to begin.")


# --- Display Extracted Text and Download Section ---
if st.session_state.extracted_text:
    st.markdown("---") # Visual separator
    st.subheader("3. Extracted Text")

    # JIT Learning: st.text_area is good for displaying larger blocks of text and allows users to select/copy.
    # 'height' can be adjusted. 'disabled=True' makes it read-only if desired, but for copy, keep it enabled.
    st.text_area(
        "OCR Result:",
        value=st.session_state.extracted_text,
        height=300,
        key="ocr_result_text_area" # Unique key can be useful for more complex apps
    )

# --- TXT Export Button ---
    try:
        # The extracted text is already a string, perfect for a .txt file
        txt_data = st.session_state.extracted_text.encode('utf-8') # Encode to bytes for download
        
        base_filename = os.path.splitext(st.session_state.uploaded_file_name or "ocr_output")[0]
        txt_filename = f"{base_filename}_extracted_text.txt"

        st.download_button(
            label="📄 Download Text as TXT", # Clear label
            data=txt_data,
            file_name=txt_filename,
            mime="text/plain", # MIME type for plain text
            use_container_width=True,
            key="download_txt_button" # Add a key if you have multiple download buttons
        )
    except Exception as e:
        st.error(f"Error preparing TXT for download: {e}")

    # --- CSV Export Button (Line-by-Line as discussed in Option 1 previously) ---
    # Keep this if you want to offer both options
    try:
        lines = st.session_state.extracted_text.split('\n')
        df = pd.DataFrame(lines, columns=["LineText"])
        csv_data = df.to_csv(index=False).encode('utf-8')
        
        base_filename = os.path.splitext(st.session_state.uploaded_file_name or "ocr_output")[0]
        csv_filename = f"{base_filename}_extracted_lines.csv"

        st.download_button(
            label="📊 Download Text Lines as CSV",
            data=csv_data,
            file_name=csv_filename,
            mime="text/csv",
            use_container_width=True,
            key="download_csv_button" # Add a key
        )
    except Exception as e:
        st.error(f"Error preparing CSV for download: {e}")

st.divider()
st.markdown("<p style='text-align: center; color: grey;'>Mini-Project by Amirulhazym</p>", unsafe_allow_html=True)