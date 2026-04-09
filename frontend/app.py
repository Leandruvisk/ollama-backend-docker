import os
import streamlit as st
import requests

BACKEND_URL = os.environ.get("BACKEND_URL", "http://backend:8000")

# Inicializa sessão de chat
if "session_id" not in st.session_state:
    st.session_state.session_id = st.query_params.get("sid", "default")
if "history" not in st.session_state:
    st.session_state.history = []

st.title("Chat Ollama 🚀")

# Entrada de usuário
user_input = st.text_input("Você:", "")

if st.button("Enviar") and user_input:
    payload = {
        "message": user_input,
        "model": "llama3",
        "session_id": st.session_state.session_id
    }

    try:
        response = requests.post(f"{BACKEND_URL}/chat", json=payload, timeout=30)
        answer = response.json().get("response", "Sem resposta.")
    except Exception as e:
        answer = f"Erro ao conectar com backend: {e}"

    # Atualiza histórico
    st.session_state.history.append(("Você", user_input))
    st.session_state.history.append(("Assistente", answer))
    user_input = ""

# Mostra histórico
for speaker, msg in st.session_state.history:
    if speaker == "Você":
        st.markdown(f"**{speaker}:** {msg}")
    else:
        st.markdown(f"**{speaker}:** {msg}")