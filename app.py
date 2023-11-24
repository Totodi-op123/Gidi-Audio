# import required libraries
import streamlit as st
import requests
import os
from dotenv import load_dotenv

# load .env file variables
load_dotenv()
API_TOKEN = os.getenv("API_TOKEN")

# The API URL and headers
headers = {"Authorization": f"Bearer {API_TOKEN}"}
API_URL = "https://api-inference.huggingface.co/models/HyperMoon/wav2vec2-base-960h-finetuned-deepfake"

# Set page config with custom icon and title
st.set_page_config(page_title='Gidi Audio Scanner', layout='wide', page_icon='🎵')

# Custom CSS for aesthetics
custom_css = """
<style>
body {
    color: #fff;
    background-color: #4F8BF9;
}
.sidebar .sidebar-content {
    background-color: #306998;
}
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

# Company name header
st.markdown('<h1 style="color: #ffffff;">Gidi Audio</h1>', unsafe_allow_html=True)

# Function to make API request and get result
def query(filename):
    with open(filename, "rb") as f:
        data = f.read()
    response = requests.post(API_URL, headers=headers, data=data, params={"wait_for_model": True})
    return response.json()

# File uploader allows the user to add their own audio
st.sidebar.header("Upload Audio")
uploaded_file = st.sidebar.file_uploader("", type=['wav', 'mp3', 'flac'], key='file_uploader')

# Temporary directory for uploaded files
TEMP_DIR = "tempDir"
os.makedirs(TEMP_DIR, exist_ok=True)

# Process the uploaded file
if uploaded_file is not None:
    file_path = os.path.join(TEMP_DIR, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Button to analyze the uploaded file
    if st.sidebar.button('Analyze'):
        # Call the query function
        result = query(file_path)
        
        # Display results
        st.subheader("Analysis Result:")
        st.json(result)
else:
    st.sidebar.warning("Please upload an audio file.")

# Clear cache button
if st.sidebar.button('Clear Cache'):
    st.legacy_caching.clear_cache()
    st.sidebar.success('Cache Cleared Successfully!')

# Ensure the footer and main block have a white text color
st.markdown('<style>#MainMenu {visibility: hidden;} footer {color: #fff;} </style>', unsafe_allow_html=True)
