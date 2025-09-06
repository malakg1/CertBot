# linkedin_utils.py
import os
import json
from datetime import date
import google.genai as genai
from state import State

def generate_linkedin_post(state: State) -> State:
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("[WARN] No Gemini API key found. Falling back.")
        return {"post_draft": "(missing – no Gemini API key configured)"}

    title = state.get("certificate_title", "")
    program = state.get("program_name", "")
    program_details = state.get("program_details", "")
    role = state.get("role", "")
    sponsors = ", ".join(state.get("sponsors", [])) if state.get("sponsors") else ""
    learnings_list = state.get("key_learnings", [])

    skills_text = "\n".join([f"• {s}" for s in learnings_list]) if learnings_list else "• Skills relevant to the field"

    try:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"""
Write a concise, engaging LinkedIn post (under 120 words) announcing the achievement of this certificate.

Certificate: {title}
Program: {program}
Role: {role}
Sponsors: {sponsors if sponsors else "N/A"}
Program details: {program_details}
Key learnings/skills (format them as a bulleted list, each starting with "•"):
{skills_text}

Guidelines:
- Use a professional but celebratory tone.
- Start with enthusiasm (e.g., "Thrilled to share…").
- Mention program name and role explicitly.
- Present the key learnings as a clear bullet list (1 skill per line).
- Thank sponsors/organizers if available.
- End with 4–6 relevant hashtags.
Return only the LinkedIn post text, no extra explanation.
"""
        )

        linkedin_post = (
            response.candidates[0].content.parts[0].text.strip()
            if response and response.candidates else ""
        )

        return {"post_draft": linkedin_post or "(missing – Gemini returned empty)"}

    except Exception as e:
        print(f"[WARN] Gemini post generation failed: {e}")
        return {"post_draft": "(missing – Gemini error)"}


def polish_post(state: State) -> State:
    draft = state.get("post_draft", "")
    issued_on = state.get("issued_on", "")

    try:
        issued_date = date.fromisoformat(issued_on)
        today = date.today()
        if issued_date <= today:
            draft = draft.replace("on track to soon receive", "thrilled to have received")
            draft = draft.replace("will be issued on", "was issued on")
        else:
            draft = draft.replace("thrilled to have received", "excited to be on track for")
    except Exception:
        pass

    draft = draft.replace("---", "").strip()
    return {"post_draft": draft}
