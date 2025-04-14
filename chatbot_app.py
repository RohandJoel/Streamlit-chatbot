import streamlit as st
import google.generativeai as genai

# Configure Gemini API
genai.configure(api_key= "AIzaSyBn04Ow1RYHjHeJt-swFkPO5RS7cW2g_HQ")
model = genai.GenerativeModel("gemini-2.0-flash")

# Streamlit UI setup
st.set_page_config(page_title="Gemini Chatbot")
st.title("Chatbot")

# Store chat history
if "history" not in st.session_state:
    st.session_state.history = []

# User input
user_input = st.text_input("You:", key="user_input")

if user_input:
    st.session_state.history.append(("You", user_input))
    
    try:
        response = model.generate_content(user_input)
        bot_reply = response.text
    except Exception as e:
        bot_reply = f"Error: {str(e)}"
    
    st.session_state.history.append(("Bot", bot_reply))

# Display chat
for sender, message in st.session_state.history:
    if sender == "You":
        st.markdown(f"👨🏻‍🦱 **{sender}:** {message}")
    else:
        st.markdown(f"🧑🏻‍⚕️ **{sender}:** {message}")
