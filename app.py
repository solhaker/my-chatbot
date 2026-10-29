import os
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# Works locally (.env) and online (Streamlit secrets)
API_KEY = os.environ.get("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY")

client = OpenAI(
    api_key=API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    timeout=30,
)

MODEL = "gemini-3.1-flash-lite"   # use whichever model worked in your terminal version
SYSTEM_PROMPT = "You are a friendly, helpful assistant named Buddy. Keep answers clear and concise."
MAX_MESSAGES = 20

st.set_page_config(page_title="Buddy", page_icon="💬")
st.title("💬 Chat with Buddy")

with st.sidebar:
    st.header("Settings")
    if st.button("Clear conversation"):
        st.session_state.messages = []
        st.rerun()

if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

if prompt := st.chat_input("Type your message..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            with st.spinner("Thinking..."):
                response = client.chat.completions.create(
                    model=MODEL,
                    messages=[{"role": "system", "content": SYSTEM_PROMPT}]
                             + st.session_state.messages[-MAX_MESSAGES:],
                )
            reply = response.choices[0].message.content or "(empty reply)"
            st.markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})
        except Exception as e:
            st.error(f"Something went wrong: {e}")
            st.session_state.messages.pop()