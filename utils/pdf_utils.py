import fitz  # PyMuPDF
import tempfile
from PIL import Image

from .ocr_utils import is_scanned_page, paddleocr_text


def save_uploaded_file(uploaded_file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_file.read())
        return tmp_file.name


def extract_text_from_pdf(pdf_path, max_pages=2):
    full_text = ""
    doc = fitz.open(pdf_path)

    for i in range(min(max_pages, len(doc))):
        page = doc[i]
        if is_scanned_page(page):
            try:
                pix = page.get_pixmap(dpi=200)
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                ocr_text = paddleocr_text(img)
                full_text += ocr_text + "\n"
            except Exception as e:
                full_text += f"\n[OCR failed on page {i+1}: {e}]\n"
        else:
            full_text += page.get_text() + "\n"

    return full_text
