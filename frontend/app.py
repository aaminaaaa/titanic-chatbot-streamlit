import streamlit as st
import requests
import base64
from PIL import Image
from io import BytesIO

st.title("🚢 Titanic Chatbot")
st.write("Ask any question about the Titanic dataset!")

question = st.text_input("Enter your question:")

if st.button("Ask"):
    if question:
        response = requests.get("http://127.0.0.1:8000/query", params={"question": question}).json()
        
        st.write("**Response:**", response["response"])

        if response["image"]:
            image_data = base64.b64decode(response["image"])
            image = Image.open(BytesIO(image_data))
            st.image(image, caption="Visualization", use_column_width=True)