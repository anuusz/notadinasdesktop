import re
from PyPDF2 import PdfReader
from pdf2image import convert_from_path
import pytesseract
from docx import Document

def parse_nota_dinas(file_path):
    if file_path.endswith(".pdf"):
        text = extract_text_from_pdf(file_path)
    elif file_path.endswith(".docx"):
        text = extract_text_from_docx(file_path)
    else:
        raise ValueError("Format file tidak didukung")
    
    # Parsing data dengan regex (sesuaikan pola dengan format nota dinas Anda)
    tanggal = re.search(r"Tanggal:\s*(\d{2}-\d{2}-\d{4})", text).group(1)
    pengirim = re.search(r"Dari:\s*(.*?)\n", text).group(1).strip()
    tempat = re.search(r"Tempat:\s*(.*?)\n", text).group(1).strip()
    petugas = re.search(r"Petugas:\s*(.*?)\n", text).group(1).strip()
    
    return {
        "tanggal": tanggal,
        "pengirim": pengirim,
        "tempat": tempat,
        "petugas": petugas
    }

def extract_text_from_pdf(file_path):
    # Coba ekstrak teks langsung (untuk PDF non-scan)
    try:
        reader = PdfReader(file_path)
        text = "\n".join([page.extract_text() for page in reader.pages])
        if text.strip():
            return text
    except:
        pass
    
    # Jika PDF hasil scan (gunakan OCR)
    images = convert_from_path(file_path)
    text = ""
    for img in images:
        text += pytesseract.image_to_string(img)
    return text

def extract_text_from_docx(file_path):
    doc = Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs])