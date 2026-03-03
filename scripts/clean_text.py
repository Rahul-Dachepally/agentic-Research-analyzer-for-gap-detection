import os
import re
from tqdm import tqdm

INPUT_DIR = "../data/parsed_text"
OUTPUT_DIR = "../data/cleaned_text"

os.makedirs(OUTPUT_DIR, exist_ok=True)

files = [f for f in os.listdir(INPUT_DIR) if f.endswith(".txt")]
print("Found files:", len(files))


def clean_text(text):
    # 1️⃣ Remove everything before "Abstract"
    abstract_match = re.search(r'\bAbstract\b', text)
    if abstract_match:
        text = text[abstract_match.start():]

    # 2️⃣ Remove References section
    ref_match = re.search(r'\bReferences\b|\bREFERENCES\b', text)
    if ref_match:
        text = text[:ref_match.start()]

    # 3️⃣ Remove standalone page numbers (lines with only digits)
    lines = text.split('\n')
    cleaned_lines = []
    for line in lines:
        stripped = line.strip()
        if stripped.isdigit():
            continue
        if len(stripped) <= 2:
            continue
        cleaned_lines.append(line)

    text = '\n'.join(cleaned_lines)

    # 4️⃣ Fix broken line wraps
    lines = text.split('\n')
    merged_lines = []
    buffer = ""

    for line in lines:
        line = line.strip()

        if not line:
            if buffer:
                merged_lines.append(buffer.strip())
                buffer = ""
            continue

        # If previous line does not end with punctuation, merge
        if buffer and not re.search(r'[.!?]$', buffer):
            buffer += " " + line
        else:
            if buffer:
                merged_lines.append(buffer.strip())
            buffer = line

    if buffer:
        merged_lines.append(buffer.strip())

    text = '\n\n'.join(merged_lines)

    # 5️⃣ Normalize whitespace
    text = re.sub(r'[ \t]+', ' ', text)
    text = re.sub(r'\n{3,}', '\n\n', text)

    return text.strip()


def process_files():
    files = [f for f in os.listdir(INPUT_DIR) if f.endswith(".txt")]

    for file in tqdm(files):
        input_path = os.path.join(INPUT_DIR, file)
        output_path = os.path.join(OUTPUT_DIR, file)

        with open(input_path, "r", encoding="utf-8") as f:
            text = f.read()

        cleaned = clean_text(text)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(cleaned)

    print("Cleaning complete.")


if __name__ == "__main__":
    process_files()