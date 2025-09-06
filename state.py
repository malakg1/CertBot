from typing_extensions import TypedDict

class State(TypedDict, total=False):
    trigger: str
    certificate_title: str
    program_name: str
    issued_on: str
    role: str
    sponsors: list[str]
    key_learnings: list[str]
    post_draft: str
    slack_response: dict
    cert_image_path: str
    ocr_text: str
    program_details: str
    auto_post_linkedin: bool
