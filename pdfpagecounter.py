import PyPDF2
import os

def get_pdf_page_count(file_path):
    with open(file_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        return len(pdf_reader.pages)

def iterate_folder(root_folder):
    maxLen = 0
    for dirpath, dirnames, filenames in os.walk(root_folder):
        for filename in filenames:
            if filename.lower().endswith('.pdf'):
                file_path = os.path.join(dirpath, filename)
                page_count = get_pdf_page_count(file_path)
                if page_count > maxLen:
                    maxLen = page_count
                
    print(f"Max pages: {maxLen}")