import google.generativeai as genai
import os
from dotenv import load_dotenv
import streamlit as st

# Load environment variables from .env file
load_dotenv()

# Get the API key from the environment variables using the new name
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("GEMINI_API_KEY not found in environment variables or .env file.")
    st.stop()

# Configure the Gemini API key
genai.configure(api_key=api_key)

# List available models (run this once to find the correct model name)
available_models = list(genai.list_models())
print("Available Gemini Models:")
for model_info in available_models:
    print(model_info)

# --- After running the above once and noting the correct model name, ---
# --- replace 'YOUR_CHOSEN_MODEL_NAME' below with the actual name you found. ---
chosen_model_name = 'models/gemini-1.5-flash'  # <--- REPLACE THIS WITH THE CORRECT MODEL NAME

# Select the Gemini model
model = genai.GenerativeModel(chosen_model_name)

# Initialize chat history in Streamlit session state
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Hello! How can I help you today?"}]

# Display chat messages from history
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Get user input
prompt = st.chat_input("You:")
if prompt:
    # Add user message to chat history
    st.session_state["messages"].append({"role": "user", "content": prompt})
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Format chat history for Gemini API
    history_for_gemini = []
    for msg in st.session_state["messages"][:-1]:  # Exclude the current prompt
        history_for_gemini.append({
            "role": msg["role"],
            "parts": [msg["content"]]
        })

    # Get Gemini response
    try:
        chat = model.start_chat(history=history_for_gemini)
        response = chat.send_message(prompt)
        gemini_response = response.text
        # Add Gemini response to chat history
        st.session_state["messages"].append({"role": "assistant", "content": gemini_response})
        # Display Gemini response
        with st.chat_message("assistant"):
            st.markdown(gemini_response)
    except Exception as e:
        st.error(f"An error occurred: {e}")
        st.error("Please check your API key and network connection.")
