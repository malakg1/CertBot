# slack_utils.py
import os
import requests
from datetime import datetime
from state import State

def send_slack_preview(state: State) -> State:
    webhook = os.getenv("SLACK_WEBHOOK_URL")
    if not webhook:
        print("[WARN] No Slack webhook configured.")
        return {"slack_response": {"ok": False, "error": "no webhook"}}

    blocks = [
        {
            "type": "header",
            "text": {"type": "plain_text", "text": "🎉 New certificate draft", "emoji": True},
        },
        {
            "type": "section",
            "fields": [
                {"type": "mrkdwn", "text": f"*Title:* {state.get('certificate_title','-')}"},
                {"type": "mrkdwn", "text": f"*Program:* {state.get('program_name','-')}"},
            ],
        },
    ]

    if state.get("program_details"):
        blocks.append({
            "type": "section",
            "text": {"type": "mrkdwn", "text": f"*About the program:* {state['program_details']}"},
        })

    blocks.extend([
        {
            "type": "section",
            "text": {"type": "mrkdwn", "text": f"*Draft:*\n{state.get('post_draft','(missing)')}"},
        },
        {
            "type": "context",
            "elements": [
                {"type": "mrkdwn", "text": f"Generated {datetime.now().isoformat()}Z"},
            ],
        }
    ])

    resp = requests.post(webhook, json={"blocks": blocks})
    return {"slack_response": {"status_code": resp.status_code, "text": resp.text, "ok": resp.ok}}
