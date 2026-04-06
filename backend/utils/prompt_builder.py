from backend.config import settings
from backend.core.memory import get_history


def build_prompt(session_id: str, user_message: str):
    history = get_history(session_id)

    prompt = settings.SYSTEM_PROMPT + "\n"

    for msg in history[-30:]:
        prompt += f"<user>{msg['user']}</user>\n"
        prompt += f"<assistant>{msg['bot']}</assistant>\n"

    prompt += f"<user>{user_message}</user>\n<assistant>"

    return prompt