# GCP Vision API OCR: Interactive Text Extractor (Mini-Project)

An interactive web application built with Python and Streamlit that leverages Google Cloud Vision API to perform Optical Character Recognition (OCR) and extract text from uploaded **image files**. This project demonstrates a user-friendly interface for a practical cloud AI service, initially developed as a one-day mini-project to gain experience with GCP and document processing.

**(Screenshot of Streamlit App in action will be upload here!)**
<!-- Example: ![OCR App Demo](docs/images/ocr_app_demo.gif) -->

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [How It Works](#how-it-works)
    - [Core OCR Logic (`ocr_tool.py`)](#core-ocr-logic-ocr_toolpy)
    - [Streamlit Web Application (`app_ocr.py`)](#streamlit-web-application-app_ocrpy)
- [Project Structure](#project-structure)
- [Setup and Usage](#setup-and-usage)
    - [Prerequisites](#prerequisites)
    - [Installation & Running the Web App](#installation--running-the-web-app)
    - [Running the Command-Line Script (Optional)](#running-the-command-line-script-optional)
- [Sample Output (from Web App)](#sample-output-from-web-app)
- [Learnings & Key Takeaways](#learnings--key-takeaways)
- [Future Considerations & Next Steps](#future-considerations--next-steps)

## Overview
This project provides two ways to interact with the GCP Vision API for OCR:
1.  A **command-line script (`ocr_tool.py`)** for direct text extraction from local image files.
2.  An **interactive Streamlit web application (`app_ocr.py`)** that allows users to upload an image, view it, extract text, and download the results as a `.txt` or line-by-line `.csv` file.

The primary goal was to build a functional and demonstrable AI application, practice integrating with cloud services, troubleshoot common development hurdles, and create a portfolio-ready piece.

## Features (Web Application - `app_ocr.py`)
-   User-friendly interface for uploading image files (PNG, JPG, JPEG).
-   Displays the uploaded image for review.
-   "Extract Text" button to trigger OCR via GCP Vision API.
-   Shows clear status messages (processing, success, errors).
-   Displays the full extracted text in a scrollable text area.
-   Buttons to download the extracted text as:
    -   A plain `.txt` file (containing the full text block).
    -   A `.csv` file (where each detected line of text is a separate row).
-   Responsive layout suitable for web browsers.

## Technologies Used
-   **Cloud Provider:** Google Cloud Platform (GCP)
-   **Core AI Service:** GCP Cloud Vision API (`document_text_detection` method)
-   **Web Framework:** Streamlit
-   **Language:** Python 3.x
-   **Key Python Libraries:**
    -   `google-cloud-vision` (GCP Vision API client)
    -   `streamlit` (for the web application)
    -   `pandas` (for CSV data preparation)
    -   `os` (for operating system interactions, e.g., file paths)
    -   `io` (for handling in-memory binary streams)
    -   `Pillow` (implicitly used by Streamlit for image handling)
-   **Development Environment:**
    -   Python Virtual Environment (`gcp1env` or `venv`)
    -   `pip` for package management (`requirements.txt`)
-   **Version Control:** Git & GitHub
-   **Local Terminal:** PowerShell (for execution and `gcloud` CLI)

## How It Works

### Core OCR Logic (`ocr_tool.py` & reused in `app_ocr.py`)
1.  **Client Instantiation:** An instance of `vision.ImageAnnotatorClient` is created, using Application Default Credentials (ADC) for GCP authentication.
2.  **Image Loading:** Image file bytes are read into memory.
3.  **API Request:** `client.document_text_detection(image=vision.Image(content=...))` sends the image data to the Vision API.
4.  **Response Handling:** Checks for API errors. If successful, `response.full_text_annotation.text` provides the extracted text.

### Streamlit Web Application (`app_ocr.py`)
1.  **Page Configuration:** Sets up the page title, icon, and layout using `st.set_page_config()`.
2.  **Cached API Client:** The `vision.ImageAnnotatorClient` is cached using `@st.cache_resource` for efficiency, preventing re-initialization on every interaction.
3.  **Session State:** `st.session_state` is used to store the uploaded file name and extracted text across Streamlit script reruns, ensuring data persistence during user interaction.
4.  **File Uploader:** `st.file_uploader` allows users to select an image.
5.  **Image Display & OCR Trigger:**
    -   The uploaded image is displayed using `st.image`.
    -   An "Extract Text" button (`st.button`) triggers the OCR process.
    -   A spinner (`st.spinner`) provides visual feedback during API calls.
6.  **Text Display:** The extracted text is shown in a `st.text_area`.
7.  **Download Functionality:** `st.download_button` provides options to download the text as a `.txt` file or a line-by-line `.csv` file (prepared using `pandas`).

## Project Structure
gcp-vision-ocr/
├── .git/ # Git repository data (hidden)
├── gcp1env/ # Python virtual environment (e.g., venv/) - in .gitignore
├── sample_images/ # Directory for sample images
│ ├── receipt1.jpg
│ └── receipt2.jpg
│ └── ... (your other test images)
├── .gitignore # Specifies intentionally untracked files for Git
├── app_ocr.py # The Streamlit web application script
├── ocr_tool.py # The command-line Python script for OCR
├── requirements.txt # Python package dependencies
└── README.md # This file


## Setup and Usage

### Prerequisites
*   A Google Cloud Platform Account with an active project.
*   The **Cloud Vision API enabled** within your GCP project.
*   Google Cloud SDK (`gcloud` CLI) installed and configured on your local machine.
*   Authenticated with Application Default Credentials:
    ```bash
    gcloud auth application-default login
    ```
*   Python 3.x installed.
*   Git installed.

### Installation & Running the Web App (`app_ocr.py`)
1.  **Clone the Repository (if viewing on GitHub):**
    ```bash
    git clone https://github.com/amirulhazym/gcp-vision.api-ocr.git # Replace with YOUR actual repository URL
    cd gcp-vision.api-ocr # Navigate into the cloned directory
    ```
2.  **Create and Activate a Python Virtual Environment:**
    ```bash
    # Navigate to the project root directory
    python -m venv gcp1env  # Or your preferred venv name
    # Activate it:
    # Windows PowerShell:
    .\gcp1env\Scripts\activate
    # macOS/Linux or Git Bash on Windows:
    # source gcp1env/bin/activate
    ```
3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Proxy Configuration (If Required by Your Network):**
    If your internet connection requires a proxy, set the `HTTPS_PROXY` environment variable in your terminal session *before* running the Streamlit app.
    ```powershell
    # Example for PowerShell:
    $env:HTTPS_PROXY = "http://your_proxy_address.com:PROXY_PORT_NUMBER" # Replace with actual proxy details
    ```
5.  **Run the Streamlit Web Application:**
    Execute from the project root directory:
    ```bash
    streamlit run app_ocr.py
    ```
    Streamlit will typically open the application in your default web browser (usually at `http://localhost:8501`).

### Running the Command-Line Script (Optional - `ocr_tool.py`)
1.  Ensure steps 1-4 from the "Installation & Running the Web App" section are completed (cloning, venv, dependencies, proxy if needed).
2.  Prepare images in the `sample_images/` directory.
3.  Modify the image path variables at the bottom of `ocr_tool.py` to point to your desired images.
4.  Execute from the project root directory:
    ```bash
    python ocr_tool.py
    ```

## Sample Output (from Web App)
After uploading `sample_images/receipt1.jpg` and clicking "Extract Text":

*(Consider adding a good screenshot of your Streamlit app showing the uploaded image and the extracted text area with download buttons here. This is very impactful!)*
<!-- Example: ![Streamlit App Screenshot](docs/images/streamlit_app_output.png) -->

The extracted text displayed (and available for download) would be similar to:
```text
LOREM IPSUM DOLOR SIT AMET
*** RECEIPT ***
CASHIER #3
... (rest of the receipt text) ...
THANK YOU FOR SHOPPING!
$135.00
$150.00
$15.00
```

## Learnings & Key Takeaways
This mini-project provided valuable hands-on experience in several key areas:

**Cloud AI Service Integration:** Successfully integrated a Python application with GCP Cloud Vision API.

**Interactive Web Application Development:** Built a user-friendly web interface using Streamlit, enhancing the usability and demonstrability of the OCR tool. This included learning about Streamlit's layout options, widgets, session state management, and file download capabilities.

**GCP Environment & Authentication:** Mastered the setup of gcloud CLI and Application Default Credentials (ADC).

## Problem-Solving (Network & Proxy Configuration):

**Challenge:** Initially faced network connectivity errors.

**Solution:** Diagnosed and resolved issues related to a proxy server required by the internet connection by setting the HTTPS_PROXY environment variable for both Python script execution and git operations. This was a critical real-world troubleshooting experience.

Practical OCR Application: Gained practical understanding of OCR, observed how image quality influences extraction, and provided useful export options (TXT and line-by-line CSV).

**Python for Cloud & Web:** Utilized Python effectively with google-cloud-vision, streamlit, and pandas.

**API Interaction & Error Handling:** Practiced handling API responses and providing user feedback.

**Version Control & Documentation:** Employed Git/GitHub for version control and comprehensive project documentation.

**Foundation for Document Processing:** This project builds a solid foundation for more complex document automation tasks.

## Future Considerations & Next Steps
PDF Text Extraction: Implement more robust OCR for PDF documents, potentially using GCS uploads and batch_annotate_files for complex PDFs.

**Advanced UI Features:** Add features like image rotation, contrast adjustment within the Streamlit app, or selection of specific OCR languages.

**Structured Data Extraction:** Explore methods to extract specific fields (e.g., total, date, items) from receipts/invoices, possibly by integrating regex or looking into GCP's Document AI.

**Deployment of Streamlit App:** Deploy the Streamlit application to a cloud service (e.g., Streamlit Community Cloud, Google Cloud Run) for public accessibility.

