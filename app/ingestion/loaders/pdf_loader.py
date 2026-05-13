"""PDF document loader."""
import fitz  # PyMuPDF


class PDFLoader:

    @staticmethod
    def load(file_path: str) -> str:
        """Load a PDF document and return its text content."""
        try:
            doc = fitz.open(file_path)
            text = ""
            for page in doc:
                text += page.get_text()
            return text
        except Exception as e:
            print(f"Error loading PDF: {e}")
            return ""