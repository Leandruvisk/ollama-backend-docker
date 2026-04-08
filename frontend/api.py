import requests

API_URL = "http://backend:8000/chat"


def send_message_stream(message, session_id):
    response = requests.post(
        API_URL,
        json={
            "message": message,
            "session_id": session_id,
            "model": "phi3"
        },
        stream=True
    )

    for chunk in response.iter_content(chunk_size=None):
        if chunk:
            yield chunk.decode("utf-8")


