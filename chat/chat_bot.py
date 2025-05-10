import streamlit as st
import requests
from dotenv import load_dotenv

load_dotenv("fun_load.env") 
# API_KEY = ("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")

API_KEY = st.secrets["openrouter"]["api_key"]

API_URL = "https://openrouter.ai/api/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "HTTP-Referer": "http://localhost:8501",  
    "X-Title": "DeepSeek Test",
    "Content-Type": "application/json",
    "X-Allow-Logging": "false"
}


st.title("DeepSeek R1 Chat via OpenRouter")

if "messages" not in st.session_state:
    st.session_state.messages = []


for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])


if prompt := st.chat_input("Message DeepSeek R1..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

  
    data = {
        "model": "deepseek/deepseek-r1",  
        "messages": st.session_state.messages,
    }

   
    with st.spinner("Thinking..."):
        try:
            response = requests.post(API_URL, headers=headers, json=data)
            response.raise_for_status()  
            result = response.json()
            reply = result["choices"][0]["message"]["content"]
        except Exception as e:
            reply = f"Error: {str(e)}"
            if hasattr(e, "response") and e.response is not None:
                st.error(e.response.text)


    st.chat_message("assistant").write(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})
    

