import PyPDF2
from docx import Document
from rake_nltk import Rake
import re
import os
import nltk
import numpy as np

nltk.download('stopwords')

def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text()
    return text

def extract_text_from_docx(docx_path):
    doc = Document(docx_path)
    return "\n".join([paragraph.text for paragraph in doc.paragraphs])


def clean_text(text):
    text = re.sub(r'\W+', ' ', text)  
    return text


def extract_keywords(text):
    rake = Rake() 
    rake.extract_keywords_from_text(text)
    return rake.get_ranked_phrases()[:10]

def process_resume(file_path):
    file_extension = os.path.splitext(file_path)[1].lower()

    if file_extension == ".pdf":
        raw_text = extract_text_from_pdf(file_path)
    elif file_extension == ".docx":
        raw_text = extract_text_from_docx(file_path)
    else:
        raise ValueError("Unsupported file type. Use a PDF(.pdf) or Word (.docx) file.")

    cleaned_text = clean_text(raw_text)
    keywords = extract_keywords(cleaned_text)

    return keywords


resume_path = "data/resumes/Sarah_Johnson_Resume.pdf"
keywords = process_resume(resume_path)
keywords_array = np.array(keywords)
print("Extracted Keywords:", keywords_array)
print(type(keywords_array))
