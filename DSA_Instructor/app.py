
import streamlit as st      # to build the web app
from groq import Groq       # to use Groq's AI (like LLama3) via API
import re                   # for regex to extract the code blocks

# API key config (Creating the client which talks with Groq using API key)
import os
API_KEY = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=API_KEY)

# Groq Response Function

def get_groq_response(messages,model="llama3-8b-8192"):
    response = client.chat.completions.create(
        model=model,
        messages=messages
    )
    return response.choices[0].message.content

# Streamlit UI Setup for UI
st.set_page_config(page_title="DSA Chatbot", page_icon="🧠")
st.title("🤖 DSA Instructor Chatbot")
st.markdown("Ask me about **Data Structures & Algorithms** like Arrays, Trees, Sorting, Complexity, Recursion, etc.")

# Chat Session
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful and friendly DSA instructor . Explain clearly with examples and python code where possible."}
    ]

# Chat Input
user_input = st.chat_input("Ask me anything about DSA...")

if user_input:
    st.session_state.messages.append({"role":"user", "content": user_input})

# Show user message
with st.chat_message("user"):
    st.markdown(user_input)

# Get AI response
    try:
        response = get_groq_response(st.session_state.messages)
    except Exception as e:
        response = f"⚠️ Error: {e}"

    st.session_state.messages.append({"role": "assistant", "content": response})

    # Show assistant response with code highlighting
    with st.chat_message("assistant"):
        if response: 
           code_blocks = re.findall(r"```(?:\w+)?\n(.*?)```", response, re.DOTALL)
           if code_blocks:
            parts = re.split(r"```(?:\w+)?\n(.*?)```", response, flags=re.DOTALL)
            for i, part in enumerate(parts):
                if part.strip():
                    st.markdown(part.strip())
                if i < len(code_blocks):

                   st.code(code_blocks[i].strip(),
          language="python")
        else:
           st.markdown(response)
