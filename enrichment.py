# metadata_utils.py
import os
import json
import re
import google.genai as genai
from state import State

def enrich_certificate_metadata(state: State) -> State:
    cert_text = state.get("ocr_text", "")
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")

    role = "Participant"
    sponsors = []
    key_learnings = ["Extracted from certificate text (OCR summary)"]
    program_name = state.get("program_name", "Program (from email)")
    program_details = ""

    if not cert_text.strip() or not api_key:
        return {
            "role": role,
            "sponsors": sponsors,
            "key_learnings": key_learnings,
            "program_name": program_name,
            "program_details": program_details,
        }

    try:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"""
Extract structured metadata from the following certificate text:

{cert_text}

Return only JSON with these fields:
- program_name (short)
- program_details (1–2 sentence description of the program goals or scope, if known or inferable)
- role (e.g., Participant, Student, Graduate, Trainee)
- sponsors (list of organizations if mentioned)
- key_learnings (2–3 bullet points, skills or topics learned)
Additionally, infer 3–5 extra skills commonly associated with the detected role, under "role_based_skills".
"""
        )

        gemini_text = (
            response.candidates[0].content.parts[0].text
            if response and response.candidates else ""
        ).strip()

        if gemini_text:
            cleaned = re.sub(r"^```(json)?|```$", "", gemini_text, flags=re.MULTILINE).strip()
            parsed = json.loads(cleaned)
            program_name = parsed.get("program_name", program_name)
            role = parsed.get("role", role)
            sponsors = parsed.get("sponsors", sponsors)
            program_details = parsed.get("program_details", program_details)
            key_learnings = parsed.get("key_learnings", key_learnings) + parsed.get("role_based_skills", [])

    except Exception as e:
        print(f"[WARN] Gemini enrichment failed: {e}")

    return {
        "role": role,
        "sponsors": sponsors,
        "key_learnings": key_learnings,
        "program_name": program_name,
        "program_details": program_details,
    }
