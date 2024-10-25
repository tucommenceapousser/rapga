import streamlit as st
import os
import json

# Constants
UPLOAD_FOLDER = 'uploads'
DATA_FILE = 'data.json'
MESSAGES_FILE = 'messages.json'
RAP_TEXTS = []
MESSAGES = {'messages': []}

# Make sure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Load data from JSON files on startup
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'r') as file:
        RAP_TEXTS = json.load(file)

if os.path.exists(MESSAGES_FILE):
    with open(MESSAGES_FILE, 'r') as file:
        MESSAGES = json.load(file)

# Streamlit app layout
st.title("🅰️ TRHACKNON Rap Texts Manager")

# Function to add a message
def add_message():
    st.markdown("## 💬 Leave a Message", unsafe_allow_html=True)
    st.markdown("<p style='color: #FFA500;'>Feel free to leave a comment below!</p>", unsafe_allow_html=True)
    message_text = st.text_area("Enter your message here:")
    
    if st.button("Submit Message", key="submit_message", help="Click to add your message"):
        if message_text:
            MESSAGES['messages'].append(message_text)
            # Save to messages.json
            with open(MESSAGES_FILE, 'w') as file:
                json.dump(MESSAGES, file, indent=2)
            st.success("Message submitted successfully!")
        else:
            st.error("Please enter a message before submitting.")

# Function to upload audio files
def upload_file():
    st.markdown("## 📁 Upload an Audio File")
    uploaded_file = st.file_uploader("Choose an audio file", type=["mp3", "wav"], help="Supported formats: mp3, wav")
    if uploaded_file is not None:
        file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success(f"File uploaded successfully: {uploaded_file.name}")

# Function to add rap text
def add_rap_text():
    st.markdown("## 📝 Add a Rap Text", unsafe_allow_html=True)
    rap_text = st.text_area("Enter your rap text", "")
    audio_file = st.file_uploader("Optional: Choose an accompanying audio file", type=["mp3", "wav"])
    
    if st.button("Add Rap Text", key="add_rap"):
        if rap_text:
            RAP_TEXTS.append({
                'rapText': rap_text, 
                'audioFilename': audio_file.name if audio_file else ''
            })
            # Write updated data to JSON file
            with open(DATA_FILE, 'w') as file:
                json.dump(RAP_TEXTS, file, indent=2)
            st.success("Rap text added successfully")
        else:
            st.error("Please enter a rap text before submitting.")

# Function to display stored messages
def show_messages():
    st.markdown("## 💬 Stored Messages")
    if MESSAGES['messages']:
        for msg in MESSAGES['messages']:
            st.markdown(f"<p style='color:#39FF14; background-color:#1A1D21; padding:5px; border-radius:5px;'>{msg}</p>", unsafe_allow_html=True)
    else:
        st.write("No messages stored yet.")

# Function to display stored rap texts
def display_rap_texts():
    st.markdown("## 🎵 Stored Rap Texts", unsafe_allow_html=True)
    if RAP_TEXTS:
        for rap in RAP_TEXTS:
            st.markdown(f"<p style='color:#FF4B4B;'><b>Rap Text:</b> {rap['rapText']}</p>", unsafe_allow_html=True)
            if rap['audioFilename']:
                st.audio(os.path.join(UPLOAD_FOLDER, rap['audioFilename']))
    else:
        st.write("No rap texts stored yet.")

# Run functions
add_message()
show_messages()
upload_file()
add_rap_text()
display_rap_texts()
