import streamlit as st
from PyPDF2 import PdfReader



transcript = st.file_uploader("Upload lecture transcript here", type = ["pdf"])

if transcript is not None:
    reader = PdfReader(transcript)
    pdf_text = ""
    for page in reader.pages:
        pdf_text += page.extract_text()

    st.text_area("Transcript:", pdf_text, height =400)
