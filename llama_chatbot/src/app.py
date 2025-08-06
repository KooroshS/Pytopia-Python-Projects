import streamlit as st
from call_llama import call_llama


st.title(":zap: Llama ChatBot")
st.caption("A streamlit chatbot power by :llama: Llama")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    msg = call_llama("gemma3:1b", prompt)["choices"][0]["message"]["content"]
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assitant").write(msg)