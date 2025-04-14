import streamlit as st
import google.generativeai as genai

# Configure Gemini API
genai.configure(api_key="AIzaSyBn04Ow1RYHjHeJt-swFkPO5RS7cW2g_HQ")
model = genai.GenerativeModel("gemini-2.0-flash")

# Set Streamlit page config
st.set_page_config(page_title="AI Medical Chatbot", layout="centered")

st.markdown("""
    <style>
    .main-title {
        text-align: center;
        margin: 10px auto 15px;
        font-size: 28px;
        width: 80%;
    }
    .chat-container {
        height: 65vh;
        overflow-y: auto;
        padding: 10px 15px;
        margin-bottom: 15px;
        width: 90%;
        margin-left: auto;
        margin-right: auto;
    }
    .user-bubble, .bot-bubble {
        padding: 8px 12px;
        border-radius: 10px;
        margin: 6px 0;
        max-width: 80%;
    }
    .user-bubble {
        background-color: #00332e;
        color: white;
        margin-left: auto;
    }
    .bot-bubble {
        background-color: #0c1a70;
        color: white;
    }
    .chat-input-container {
        display: flex;
        gap: 8px;
        width: 60%;
        margin: 0 auto;
        padding: 10px 0;
    }
    @media (max-width: 768px) {
        .chat-input-container {
            width: 90%;
        }
    }
    </style>
""", unsafe_allow_html=True)


if "history" not in st.session_state:
    st.session_state.history = []

st.markdown("<h1 class='main-title'>🧑‍⚕️ AI Medical Assistant</h1>", unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    for sender, msg in st.session_state.history:
        bubble_class = "user-bubble" if sender == "Patient" else "bot-bubble"
        icon = "👤" if sender == "Patient" else "🧑🏻‍⚕️"
        st.markdown(f'<div class="{bubble_class}">{icon} <b>{sender}:</b> {msg}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Chat input form
with st.form("chat_form", clear_on_submit=True):
    cols = st.columns([4, 1])
    with cols[0]:
        user_input = st.text_input(
            "Your message",
            placeholder="Type your health question here...",
            label_visibility="collapsed",
            key="chat_input"
        )
    with cols[1]:
        send_button = st.form_submit_button("Send", use_container_width=True)

# Handle submission
if send_button and user_input:
    # Add user message to history
    st.session_state.history.append(("Patient", user_input))
    
    try:
        response = model.generate_content(user_input)
        bot_reply = response.text
    except Exception as e:
        bot_reply = f"Error: {str(e)}"

    st.session_state.history.append(("Doctor", bot_reply))
    
    st.rerun()  
