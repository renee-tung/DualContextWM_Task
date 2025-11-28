import re
import requests

COMMENT_SERVER_URL = "http://comment-server.example.com/api/comments"

def send_blackrock_comment(event: str, task: str, additional_text: str = ""):
    """
    Sends a comment to the Blackrock comment server.

    Args:
        event (str): The event identifier.
        task (str): The task identifier.
        additional_text (str): Additional text to include in the comment.
    """
    payload = {
        "event": event,
        "task": task,
        "additional_text": additional_text
    }

    try:
        response = requests.post(COMMENT_SERVER_URL, json=payload, timeout=0.5)
        if not response.ok:
            print("Comment server error: ", response.status_code, response.text)
    except Exception as e:
        print(f"Failed to send comment: {e}")