conversations = {}


def get_history(session_id: str):
    return conversations.get(session_id, [])


def save_message(session_id: str, user: str, bot: str):
    conversations.setdefault(session_id, []).append({
        "user": user,
        "bot": bot
    })


def clear(session_id: str):
    conversations.pop(session_id, None)