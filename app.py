import streamlit as st
import google.generativeai as genai
from pypdf import PdfReader

# Configure Page
st.set_page_config(
    page_title="StudyGenie AI",
    page_icon="🎓",
    layout="centered"
)

# Gemini API Setup
api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-2.5-flash")

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

# PDF Upload
uploaded_file = st.file_uploader(
    "📄 Upload PDF Notes",
    type=["pdf"]
)

# Extract PDF Text
def extract_text(pdf):
    reader = PdfReader(pdf)
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text


if uploaded_file:

    text = extract_text(uploaded_file)

    # Limit text size for faster Gemini responses
    text = text[:10000]

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
                    Summarize these notes in less than 300 words.

                    Include:

                    1. Key Concepts
                    2. Important Points
                    3. Quick Revision Notes

                    Notes:
                    {text}
                    """

                elif option == "Important Questions":

                    prompt = f"""
                    Generate 15 important exam questions.

                    Include:
                    - Short Questions
                    - Long Questions
                    - Theory Questions

                    Notes:
                    {text}
                    """

                else:

                    prompt = f"""
                    Generate 15 MCQs with answers.

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
