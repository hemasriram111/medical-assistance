import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
from PIL import Image

# Load environment variables
load_dotenv()

# Configure Google Gemini API key
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    st.error("🚨 Please set your Google Gemini API key in the environment variables.")
    st.stop()

genai.configure(api_key=api_key)

# Set Streamlit page layout
st.set_page_config(page_title="Medical AI Agent", page_icon="🏥", layout="wide")

# Custom CSS for enhanced UI
def set_custom_css():
    st.markdown(
        """
        <style>
            .stApp { background-color: #f0f2f6; }
            .stButton>button { background-color: #0066cc; color: white; border-radius: 10px; }
            .stTextInput>div>div>input { border-radius: 10px; }
        </style>
        """,
        unsafe_allow_html=True,
    )
set_custom_css()

# Sidebar Navigation
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Caduceus.svg/768px-Caduceus.svg.png", width=100)
st.sidebar.title("Medical AI Agent 🏥")
st.sidebar.write("An AI-powered assistant for medical inquiries.")
st.sidebar.warning("⚠️ **Disclaimer:** This AI is for informational purposes only. Always consult a doctor.")

# Main Header
st.title("💡 AI-Powered Medical Assistant")
st.write("🔹 Ask medical questions, upload prescriptions, or analyze medical images.")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
st.subheader("📜 Chat History")
chat_placeholder = st.container()
with chat_placeholder:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

# File uploader for medical images or prescriptions
st.subheader("📂 Upload Medical File")
uploaded_file = st.file_uploader("Upload a medical image or prescription", type=["jpg", "jpeg", "png", "pdf"])
if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="📌 Uploaded File", use_column_width=True)
    st.session_state.uploaded_image = image

# User input for medical queries
st.subheader("💬 Ask Your Medical Question")
user_input = st.text_input("Describe symptoms or ask a medical question:", "", key="user_input")

if st.button("🔍 Analyze") and user_input:
    with st.chat_message("user"):
        st.write(user_input)
    
    # Add user message to session state
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Loading animation
    with st.spinner("Analyzing... 🩺"):
        model = genai.GenerativeModel("gemini-1.5-flash")
        medical_prompt = (
            "You are a highly specialized medical AI assistant. "
            "You only provide responses related to medical topics, patient symptoms, diagnoses, treatments, and medication analysis. "
            "Ignore any non-medical queries and focus solely on medical image analysis and symptom interpretation. "
            "If a question is unrelated to medicine, respond with 'I only provide medical-related information.'"
        )
        
        if uploaded_file:
            response = model.generate_content([medical_prompt + user_input, image])
        else:
            response = model.generate_content(medical_prompt + user_input)
        
        bot_reply = response.text if response.text else "I'm sorry, I couldn't generate a response. Please consult a doctor."
    
    with st.chat_message("assistant"):
        st.write(bot_reply)
    
    # Add bot response to session state
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
