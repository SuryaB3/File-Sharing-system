import os
import json
import streamlit as st
from datetime import datetime

# Custom CSS for background color
st.markdown(
    """
    <style>
    /* Set the background color for the main content */
    .main {
        background-color: #f5f7fa; /* Light blue-gray background */
    }
    
    /* Customize the background for the app container */
    .stApp {
        background-color: #e6eef5; /* Slightly darker blue-gray for contrast */
        color: #3b3b3b; /* Dark gray text color */
    }

    /* Customize headers and subheaders */
    .css-18e3th9 {
        color: #007acc; /* Primary blue for headers */
    }

    /* Style upload button and success messages */
    .css-1cpxqw2 {
        background-color: #d9e9ff; /* Light blue for buttons */
    }
    .css-8xv9th {
        color: #00509e; /* Darker blue for messages */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Directory to save uploaded files
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# JSON file to store file metadata
METADATA_FILE = "file_metadata.json"

# Load metadata from JSON file if it exists
def load_metadata():
    if os.path.exists(METADATA_FILE):
        with open(METADATA_FILE, "r") as f:
            return json.load(f)
    return {}

# Save metadata to JSON file
def save_metadata(metadata):
    with open(METADATA_FILE, "w") as f:
        json.dump(metadata, f)

# Initialize metadata dictionary
file_metadata = load_metadata()

# Function for Uploading Files
def upload_file():
    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None:
        filename = uploaded_file.name
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        unique_filename = f"{timestamp}_{filename}"
        file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
        
        # Save the file to the uploads folder
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Store file metadata and save to JSON
        file_metadata[unique_filename] = {
            "filename": filename,
            "path": file_path,
            "size": uploaded_file.size,
            "upload_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        save_metadata(file_metadata)  # Save updated metadata to JSON
        st.success(f"File '{filename}' uploaded successfully!")

# Function to Display Uploaded Files
def display_files():
    st.subheader("Uploaded Files")
    if not file_metadata:
        st.write("No files uploaded yet.")
    else:
        for file_id, metadata in file_metadata.items():
            st.write(f"{metadata['filename']}** ({metadata['size']} bytes) - {metadata['upload_date']}")
            with open(metadata['path'], "rb") as file:
                st.download_button("Download", data=file, file_name=metadata['filename'])

# Main App Structure
st.title("File Sharing System")
upload_file()
display_files()