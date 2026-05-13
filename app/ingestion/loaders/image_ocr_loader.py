"""Image OCR document loader."""

import fitz
import pytesseract
from PIL import Image
import io

class ImageOCRLoader:

    @staticmethod
    def extract_text(file_path: str) -> str:
        """Extract text from an image file using OCR."""
        try:
            pdf = fitz.open(file_path)
            text = ""
            for page in pdf:
                pix = page.get_pixmap()
                img_bytes = pix.tobytes("png")
                img = Image.open(io.BytesIO(img_bytes))
                text += pytesseract.image_to_string(img)
            return text
        except Exception as e:
            print(f"Error loading image: {e}")
            return ""
