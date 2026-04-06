from backend.services.memory_service import get_history

def build_prompt(session_id, user_message):
    history = get_history(session_id)

    prompt = (
        "Você é um assistente técnico.\n"
        "Responda sempre em português do Brasil.\n"
        "Seja direto e objetivo.\n"
        "NÃO invente contexto.\n"
        "NÃO continue a conversa após responder.\n\n"
    )

    for msg in history:
        prompt += f"<user>{msg.user_message}</user>\n"
        prompt += f"<assistant>{msg.bot_response}</assistant>\n"

    prompt += f"<user>{user_message}</user>\n<assistant>"

    return prompt