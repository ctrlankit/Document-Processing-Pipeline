"""DOCX document loader."""

from docx import Document

class DOCXLoader:

    @staticmethod
    def load(file_path: str) -> str:
        """Load a DOCX document and return its text content."""
        try:
            doc = Document(file_path)
            full_text = []  

            for para in doc.paragraphs:
                full_text.append(para.text)

            return '\n'.join(full_text)
        except Exception as e:
            print(f"Error loading DOCX: {e}")
            return ""