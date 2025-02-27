import streamlit as st
import requests
import base64
from PIL import Image
from io import BytesIO

# Set page config
st.set_page_config(page_title="Titanic Chatbot", page_icon="🚢", layout="wide")

# Custom CSS for wavy animated background and responsive design
st.markdown(
    """
    <style>
    @keyframes moveWaves {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    body {
        background: linear-gradient(-45deg, #001f3f, #003366, #004080, #001f3f);
        background-size: 400% 400%;
        animation: moveWaves 10s ease infinite;
        color: white;
        font-family: 'Arial', sans-serif;
    }
    .main-container {
        background-color: rgba(255, 255, 255, 0.15);
        padding: 40px;
        border-radius: 15px;
        box-shadow: 0px 4px 15px rgba(255, 255, 255, 0.2);
        max-width: 800px;
        margin: auto;
    }
    .title {
        text-align: center;
        color: #FFD700;
        font-size: 40px;
        font-weight: bold;
        text-shadow: 3px 3px 15px rgba(255, 215, 0, 0.8);
    }
    .subtitle {
        text-align: center;
        font-size: 20px;
        color: #B0C4DE;
    }
    .stTextInput>div>div>input {
        border: 2px solid #1E90FF !important;
        border-radius: 10px !important;
        padding: 14px;
        font-size: 18px;
        background-color: rgba(255, 255, 255, 0.2);
        color: black;
    }
    .stTextInput>div>div>input::placeholder {
        color: black;
    }
    .stButton>button {
        background: linear-gradient(135deg, #FFD700, #FFA500) !important;
        color: #1f1f1f !important;
        font-size: 20px !important;
        font-weight: bold !important;
        border-radius: 12px !important;
        padding: 14px 28px !important;
        transition: all 0.3s ease-in-out;
        border: none;
        box-shadow: 2px 2px 10px rgba(255, 215, 0, 0.5);
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #00CED1, #1E90FF) !important;
        transform: scale(1.07);
    }
    .response-box {
        background-color: rgba(255, 255, 255, 0.2);
        padding: 25px;
        border-radius: 12px;
        font-size: 20px;
        text-align: center;
        margin-top: 25px;
        box-shadow: 0px 4px 15px rgba(255, 255, 255, 0.2);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title and subtitle
st.markdown("<div class='title'>🚢 Titanic Chatbot</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Ask any question about the Titanic dataset!</div>", unsafe_allow_html=True)

# Main content container
with st.container():
    st.markdown("<div class='main-container'>", unsafe_allow_html=True)
    
    # Input field
    question = st.text_input("Enter your question:")
    
    # Button and response section
    if st.button("🚢 Ask"):  
        if question:
            response = requests.get("http://127.0.0.1:8000/query", params={"question": question}).json()
            
            # Display response
            st.markdown(f"<div class='response-box'><b>Response:</b> {response['response']}</div>", unsafe_allow_html=True)
            
            # Display image if available
            if response.get("image"):
                image_data = base64.b64decode(response["image"])
                image = Image.open(BytesIO(image_data))
                st.image(image, caption="Visualization", use_column_width=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
