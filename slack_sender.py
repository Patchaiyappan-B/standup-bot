import json
import random
from pathlib import Path
import requests
import os
from dotenv import load_dotenv

load_dotenv()

SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_CHANNEL_NAME ="#standup-test"

QUESTIONS_FILE = Path(__file__).parent/"questions.json"

def get_random_questions(filepath: Path) -> str:
    with open(filepath, "r", encoding="utf-8") as f:
        questions = json.load(f)

    item= random.choice(questions)
    return f"*[{item['category'].upper()}]* {item['text']}"

def post_to_slack(token: str, channelname: str, textmessage: str) -> None:
    url = "https://slack.com/api/chat.postMessage"
    headers={
        "Authorization":f"Bearer {token}",
        "content-type":"application/json"
    }
    payload ={
        "channel":channelname,
        "text":textmessage
    }

    postrespone = requests.post(url, headers=headers, json=payload)
    data = postrespone.json()

    if postrespone.status_code == 200 and data.get("ok"):
        print(f"Message delivered to {channelname} successfully!")
    else:
        print(f"Failed to post to Slack: {data.get('error', postrespone.text)}")


def main():
    prompt = get_random_questions(QUESTIONS_FILE)
    standup_text = (
        f" Good morning team! Here is your standup question for today:\n\n"
        f"> {prompt}\n\n"
        f"_Please reply to this thread with your update!_"
    )
    post_to_slack(SLACK_BOT_TOKEN, SLACK_CHANNEL_NAME,standup_text)

if __name__ == "__main__":
    main()
