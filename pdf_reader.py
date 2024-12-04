import streamlit as st
from PyPDF2 import PdfReader
from reportlab.pdfgen import canvas
from io import BytesIO
from chatgpt import *

def get_processed_text(transcript_text: str, max_tries=4) -> str:
    current_try = 0
    while current_try < max_tries:
        try:
            summary = get_summary(transcript_text)
            stamped_topics = get_stamped_topics(transcript_text)
            bullet_points = []

            # Generate bullet points for each topic
            import concurrent.futures

            def process_topic(topic):
                return (topic[0], get_bullet_points(topic[0], topic[5]))

            with concurrent.futures.ThreadPoolExecutor() as executor:
                bullet_points = list(executor.map(process_topic, stamped_topics))

            # Put the summary and bullet points together into processed text
            processed_text = f'Lecture Summary:\n{summary}\n\nLecture Notes:'
            for topic, points in bullet_points:
                processed_text += f"\n{topic}:\n"
                processed_text += points + "\n"
            return processed_text
        except Exception as e:
            current_try += 1
            st.warning(f"Error processing transcript: {e}. Retrying ({current_try}/{max_tries})...")
    return "Error processing transcript. Please try again."
st.title("Note Creator")

# Option to upload a file or paste text
option = st.radio("How would you like to provide the transcript?", ("Upload File (PDF or TXT)", "Paste text"))

# Initialize transcript text
transcript_text = ""

# Handle file upload
if option == "Upload File (PDF or TXT)":
    uploaded_file = st.file_uploader("Upload a transcript file (PDF or TXT):", type=["pdf", "txt"])
    
    if uploaded_file is not None:
        # Handle PDF files
        if uploaded_file.type == "application/pdf":
            reader = PdfReader(uploaded_file)
            for page in reader.pages:
                transcript_text += page.extract_text()
        
        # Handle TXT files
        elif uploaded_file.type == "text/plain":
            transcript_text = uploaded_file.read().decode("utf-8")  # Decode bytes to string
        
        # Display the extracted transcript
        st.text_area("Transcript (Extracted):", transcript_text, height=400)

# Handle text pasting
elif option == "Paste text":
    transcript_text = st.text_area("Paste your transcript below:", height=400)

# Process the transcript
if st.button("Create Notes"):
    if transcript_text.strip():  # Check if the transcript text is not empty

        # Process the transcript text
        with st.spinner('Processing transcript'):
            processed_text = get_processed_text(transcript_text)

        # Display the processed text
        st.text_area("Notes:", processed_text, height=400)

        # Generate a PDF in memory
        pdf_buffer = BytesIO()
        pdf = canvas.Canvas(pdf_buffer)
        pdf.setFont("Helvetica", 12)
        text_lines = processed_text.split("\n")
        y = 800  # Start writing at the top of the page
        
        for line in text_lines:
            if y < 40:  # Check if we need a new page
                pdf.showPage()
                pdf.setFont("Helvetica", 12)
                y = 800
            pdf.drawString(40, y, line)
            y -= 15
        
        pdf.save()
        pdf_buffer.seek(0)

        # Allow the user to download the PDF
        st.download_button(
            label="Download Notes as PDF",
            data=pdf_buffer,
            file_name="processed_transcript_notes.pdf",
            mime="application/pdf",
        )
    else:
        st.warning("Please provide a transcript before processing.")
