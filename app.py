import streamlit as st
import google.generativeai as genai
from pypdf import PdfReader
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Gemini Model
model = genai.GenerativeModel("gemini-2.5-flash")

# Page Config
st.set_page_config(
    page_title="StudyGenie AI",
    page_icon="📚",
    layout="centered"
)

# Header
st.title("🎓 StudyGenie AI - Smart Exam Preparation Assistant")

st.markdown("""
### Features

✅ Generate Summaries

✅ Important Exam Questions

✅ MCQs from Notes

✅ AI-Powered Learning

Upload your PDF notes and prepare smarter.
""")

# Upload PDF
uploaded_file = st.file_uploader(
    "📄 Upload PDF Notes",
    type=["pdf"]
)

# Extract Text Function
def extract_text(pdf):
    reader = PdfReader(pdf)
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text

# Main App Logic
if uploaded_file:

    text = extract_text(uploaded_file)

    st.success("✅ PDF Uploaded Successfully")

    option = st.selectbox(
        "Choose Task",
        [
            "Summary",
            "Important Questions",
            "MCQ Generator"
        ]
    )

    if st.button("Generate"):

        with st.spinner("🤖 AI is working..."):

            try:

                if option == "Summary":

                    prompt = f"""
                    You are an expert teacher.

                    Summarize the following notes in simple student-friendly language.

                    Give:
                    1. Key Concepts
                    2. Important Points
                    3. Exam Revision Notes

                    Notes:
                    {text}
                    """

                elif option == "Important Questions":

                    prompt = f"""
                    You are an experienced professor.

                    Generate 15 important exam questions from these notes.

                    Include:
                    - Short Questions
                    - Long Questions
                    - Theory Questions

                    Notes:
                    {text}
                    """

                else:

                    prompt = f"""
                    Generate 15 MCQs with answers from these notes.

                    Format:

                    Q1.
                    A.
                    B.
                    C.
                    D.

                    Correct Answer:

                    Notes:
                    {text}
                    """

                response = model.generate_content(prompt)

                st.markdown("## 📌 Result")
                st.write(response.text)

            except Exception as e:
                st.error(f"Error: {e}")

# Footer
st.markdown("---")
st.write("🚀 Built for AI Vibe Coding Challenge 2026")