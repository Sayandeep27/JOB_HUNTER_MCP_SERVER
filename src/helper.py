import fitz  # PyMuPDF
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

# Load Groq API Key
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)


def extract_text_from_pdf(uploaded_file):
    """
    Extracts text from a PDF file.

    Args:
        uploaded_file: Uploaded PDF file from Streamlit

    Returns:
        str: Extracted text
    """
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text


def ask_groq(prompt, max_tokens=500):
    """
    Sends a prompt to Groq LLM and returns the response.

    Args:
        prompt (str): Prompt text
        max_tokens (int): Max tokens for response

    Returns:
        str: Model response
    """

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.5,
        max_tokens=max_tokens
    )

    return response.choices[0].message.content
