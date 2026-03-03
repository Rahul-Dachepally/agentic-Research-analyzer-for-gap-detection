import os
from pdfminer.high_level import extract_text
from tqdm import tqdm

PDF_DIR = "../data/raw_pdfs"
OUTPUT_DIR = "../data/parsed_text"

os.makedirs(OUTPUT_DIR, exist_ok=True)

pdf_files = [f for f in os.listdir(PDF_DIR) if f.endswith(".pdf")]

for pdf_file in tqdm(pdf_files):
    pdf_path = os.path.join(PDF_DIR, pdf_file)
    try:
        text = extract_text(pdf_path)
        
        if not text.strip():
            print(f"Empty extraction: {pdf_file}")
            continue
        
        output_file = pdf_file.replace(".pdf", ".txt")
        output_path = os.path.join(OUTPUT_DIR, output_file)
        
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(text)
            
    except Exception as e:
        print(f"Error with {pdf_file}: {e}")

print("Text extraction complete.")