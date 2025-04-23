import streamlit as st
import tempfile
import fitz  # PyMuPDF
import json
import re
import pandas as pd
from PIL import Image
from utils.ocr_utils import is_scanned_page, paddleocr_text,ocr_model
from utils.openai_utils import query_openai_json
from utils.prompt_utils import build_prompt

st.title("Boltware PDF Extractor 🔍")
st.write("Upload a PDF. OCR will run only on scanned pages.")

uploaded_file = st.file_uploader("📄 Upload your PDF", type=["pdf"])

if uploaded_file:
    with st.spinner("🔍 Processing PDF..."):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(uploaded_file.read())
            tmp_pdf_path = tmp_file.name

        try:
            doc = fitz.open(tmp_pdf_path)
        except Exception as e:
            st.error(f"Failed to open PDF: {e}")
            st.stop()

        full_text = ""
        for i in range(min(2, len(doc))):
            page = doc[i]
            st.info(f"Analyzing Page {i + 1}...")
            if is_scanned_page(page):
                try:
                    pix = page.get_pixmap(dpi=200)
                    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                    full_text += paddleocr_text(img) + "\n"
                except Exception as e:
                    st.warning(f"OCR failed on page {i + 1}: {e}")
            else:
                full_text += page.get_text() + "\n"

        # Split and query
        chunks = [full_text[i:i + 2000] for i in range(0, len(full_text), 2000)]
        all_results = []
        for chunk in chunks[:1]:  # First chunk for demo
            response = query_openai_json(build_prompt(chunk))
            if response:
                match = re.search(r'\{.*\}', response, re.DOTALL)
                if match:
                    try:
                        all_results.append(json.loads(match.group(0)))
                    except json.JSONDecodeError:
                        st.warning("⚠️ Invalid JSON format returned from OpenAI.")

        # Merge Results
        final_result = {}
        for result in all_results:
            for key, value in result.items():
                if key not in final_result or not final_result[key]:
                    final_result[key] = value

        if final_result:
            df = pd.DataFrame([final_result])
            st.subheader("✅ Extracted Information")
            st.dataframe(df)
            st.download_button("⬇️ JSON", json.dumps(final_result, indent=2), "extracted_info.json")
            st.download_button("⬇️ CSV", df.to_csv(index=False), "extracted_info.csv")
        else:
            st.error("❌ No valid data extracted.")
