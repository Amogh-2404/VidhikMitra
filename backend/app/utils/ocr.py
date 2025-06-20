from PIL import Image
import pytesseract
from pdf2image import convert_from_path


def extract_text(path: str) -> str:
    """Extract text from image or PDF using OCR."""
    try:
        if path.lower().endswith('.pdf'):
            images = convert_from_path(path, first_page=1, last_page=5)
            text = '\n'.join(pytesseract.image_to_string(img) for img in images)
            return text
        return pytesseract.image_to_string(Image.open(path))
    except Exception:
        return ""
