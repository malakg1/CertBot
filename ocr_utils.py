# ocr_utils.py
from state import State
from PIL import Image
import pytesseract
import pdfplumber
from pdf2image import convert_from_path

def extract_certificate_text(state: State) -> State:
    cert_path = state.get("cert_image_path")
    if not cert_path:
        return {"ocr_text": ""}

    text = ""
    try:
        if cert_path.lower().endswith(".pdf"):
            # Try direct PDF text extraction first (vector PDFs)
            try:
                with pdfplumber.open(cert_path) as pdf:
                    for page in pdf.pages:
                        page_text = page.extract_text()
                        if page_text:
                            text += page_text + "\n"
            except Exception as e:
                print(f"[WARN] PDFplumber extraction failed: {e}")

            # If no text was extracted, fallback to OCR
            if not text.strip():
                pages = convert_from_path(cert_path, dpi=300)
                for page in pages:
                    page = page.convert("L")  # convert to grayscale
                    text += pytesseract.image_to_string(page, config="--psm 6") + "\n"
        else:
            # It's an image
            img = Image.open(cert_path).convert("L")
            text = pytesseract.image_to_string(img, config="--psm 6")
    except Exception as e:
        print(f"[WARN] OCR failed: {e}")
        text = ""

    return {"ocr_text": text.strip()}
