# Import necessary libraries
import io # for handling in-memory binary streams (our image file)
import os # for interaction with os
from google.cloud import vision # google cloud visiom lib

def
extract_text_from_image(image_path_from_script_location):
    """
    Detects and extracts text from a local image file using Google Cloud Vision API.

    Args:
        image_path_from_script_location (str): The path to the local image file,
                                               relative to where this script is located.
                                               Example: "sample_images/my_image.png"

    Returns:
        str: The extracted text, or None if no text is found or an error occurs.
    """
    print(f"Attempting to process image: {image_path_from_script_location}")

# Construct the absolute path to the image file
    script_dir = os.path.dirname(os.path.abspath(__file__)) # os.path.dirname() gets the directory part of that path, os.path.abspath(__file__) gives the path of the current script
    absolute_image_path = os.path.join(script_dir, image_path_from_script_location)  # os.path.join() safely combines directory and file names to form a full path

    if not os.path.exists(absolute_image_path): 
        print(f"Error: Image file not found at resolved path: {absolute_image_path}")
        return None

# Instantiate Vision API client
    try:
        client = vision.ImageAnnotatorClient()
    except Exception as e:
        print(f"Error creating Vision API client: {e}")
        print("Ensure you have authenticated with `gcloud auth application-default login` "
              "and the Vision API is enabled in your GCP project.")
        return None

# Load the image into memory
    try:
        with io.open(absolute_image_path, 'rb') as image_file:
            content = image_file.read()
        image_for_api = vision.Image(content=content)
        print(f"Image '{absolute_image_path}' loaded successfully.")
    except Exception as e:
        print(f"Error loading image file {absolute_image_path}: {e}")
        return None

# Perform text detection using Vision API
    print("Sending request to Google Cloud Vision API for text detection...")
    try:
        response = client.document_text_detection(image=image_for_api)
    except Exception as e:
        print(f"Error during Vision API request: {e}")
        return None

# Process API response
    if response.error.message:
        print(f"Vision API Error: {response.error.message}")
        print("For more info on error messages, check: "
              "https://cloud.google.com/apis/design/errors")
        return None

    if response.full_text_annotation:
        extracted_text = response.full_text_annotation.text
        print("Text extraction successful!")
        return extracted_text
    else:
        print("No text found in the image by the API.")
        return None

# Main part of script
if __name__ == "__main__":
    print("--- GCP OCR Text Extractor ---")

# Define the path to your sample image (relative to this script's location)
    relative_image_path_to_process = "sample_images/receipt1.jpg"

    extracted_text_result = extract_text_from_image(relative_image_path_to_process)

    if extracted_text_result:
        print("\n----- Extracted Text -----")
        print(extracted_text_result.strip()) # .strip() removes leading/trailing whitespace
        print("--------------------------")
    else:
        print(f"Could not extract text from {relative_image_path_to_process}")

# To process another image:
    print("\n--- Processing another image ---")
    relative_image_path_2 = "sample_images/receipt2.jpg" # receipt 2
    extracted_text_result_2 = extract_text_from_image(relative_image_path_2)
    if extracted_text_result_2:
        print("\n----- Extracted Text (Image 2) -----")
        print(extracted_text_result_2.strip())
        print("----------------------------------")

# Try process OCR from PDF file
    print("\n--- Processing text from PDF ---")
    relative_image_path_3 = "sample_images/malaysia on china open source ai revolution.pdf" # receipt 2
    extracted_text_result_3 = extract_text_from_image(relative_image_path_2)
    if extracted_text_result_3:
        print("\n----- Extracted Text (Image 3 - PDF 1) -----")
        print(extracted_text_result_3.strip())
        print("----------------------------------")