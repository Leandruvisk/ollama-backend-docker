from backend.db.database import SessionLocal
from backend.db.models import Conversation


def save_message(session_id, user, bot):
    db = SessionLocal()

    conv = Conversation(
        session_id=session_id,
        user_message=user,
        bot_response=bot
    )

    db.add(conv)
    db.commit()
    db.close()


def get_history(session_id, limit=30):
    db = SessionLocal()

    results = (
        db.query(Conversation)
        .filter(Conversation.session_id == session_id)
        .order_by(Conversation.id.desc())
        .limit(limit)
        .all()
    )

    db.close()

    return list(reversed(results))

def clear_session(session_id):
    db = SessionLocal()

    db.query(Conversation).filter(
        Conversation.session_id == session_id
    ).delete()

    db.commit()
    db.close()