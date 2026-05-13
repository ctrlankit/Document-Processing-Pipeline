"""Excel document loader."""
import pandas as pd

class ExcelLoader:

    @staticmethod
    def extract_text(file_path: str) -> str:
        """Load an Excel document and return its text content."""
        try:
            excel_data = pd.read_excel(
                file_path,
                sheet_name=None
            )

            combined_text = ""

            for sheet_name, df in excel_data.items():

                combined_text += f"\nSheet: {sheet_name}\n"

                combined_text += df.to_string()

            return combined_text
        except Exception as e:
            print(f"Error loading Excel: {e}")
            return ""