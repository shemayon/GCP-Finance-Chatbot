# main.py
import os
import streamlit as st
import google.generativeai as genai
import fitz 
from utils.embedding_utils import embed_text_chunks
from utils.search_utils import search_similar_chunks

# either hard-code (for quick test) or set GEMINI_API_KEY in your env
genai.configure(api_key="<your GEMINI_API_KEY")

st.title("📄 GCP Gemini PDF Finance Assistant")

pdf_file = st.file_uploader("Upload a financial PDF", type=["pdf"])
query    = st.text_input("Ask a question from the document:")

def load_pdf_text_chunks(pdf_file, max_chunk_size=500):
    text = ""
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    for page in doc:
        text += page.get_text()
    doc.close()
    return [text[i : i + max_chunk_size] for i in range(0, len(text), max_chunk_size)]

def query_gemini(prompt: str, context: str) -> str:
    model = genai.GenerativeModel("gemini-2.0-flash")  
    full_prompt = f"{context}\n\nUser: {prompt}\nAssistant:"
    response = model.generate_content(full_prompt)
    return response.text

if pdf_file and query:
    with st.spinner("Processing…"):
        chunks, vectors = embed_text_chunks(load_pdf_text_chunks(pdf_file))
        top = search_similar_chunks(query, chunks, vectors)
        context = "\n\n---\n\n".join(top)
        answer = query_gemini(query, context)
        st.markdown("### 💬 Gemini Response:")
        st.write(answer)
