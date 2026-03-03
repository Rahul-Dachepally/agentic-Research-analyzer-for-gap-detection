import os
import re
import json
from tqdm import tqdm

INPUT_DIR = "../data/parsed_text"
OUTPUT_DIR = "../data/structured_text"

os.makedirs(OUTPUT_DIR, exist_ok=True)


SECTION_PATTERNS = {
    "introduction": r"\n\d+\.?\s+Introduction",
    "related_work": r"\n\d+\.?\s+(Related Work|Related Works|Background)",
    "method": r"\n\d+\.?\s+(Method|Methodology|Approach|Proposed Method)",
    "experiments": r"\n\d+\.?\s+(Experiments|Experimental Setup|Evaluation)",
    "results": r"\n\d+\.?\s+(Results|Findings)",
    "discussion": r"\n\d+\.?\s+Discussion",
    "conclusion": r"\n\d+\.?\s+(Conclusion|Conclusions)"
}


def extract_sections(text):
    sections = {}
    
    # Extract abstract
    abstract_match = re.search(r"Abstract(.*?)\n\d+\.?\s+Introduction", text, re.DOTALL)
    if abstract_match:
        sections["abstract"] = abstract_match.group(1).strip()
    else:
        sections["abstract"] = ""

    # Find section positions
    section_positions = {}
    for name, pattern in SECTION_PATTERNS.items():
        match = re.search(pattern, text)
        if match:
            section_positions[name] = match.start()

    # Sort sections by order of appearance
    sorted_sections = sorted(section_positions.items(), key=lambda x: x[1])

    # Extract content between sections
    for i in range(len(sorted_sections)):
        section_name, start_pos = sorted_sections[i]
        end_pos = sorted_sections[i + 1][1] if i + 1 < len(sorted_sections) else len(text)
        content = text[start_pos:end_pos]
        sections[section_name] = content.strip()

    return sections


def process_files():
    files = [f for f in os.listdir(INPUT_DIR) if f.endswith(".txt")]

    for file in tqdm(files):
        input_path = os.path.join(INPUT_DIR, file)
        output_path = os.path.join(OUTPUT_DIR, file.replace(".txt", ".json"))

        with open(input_path, "r", encoding="utf-8") as f:
            text = f.read()

        structured = extract_sections(text)

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(structured, f, indent=2)

    print("Section parsing complete.")


if __name__ == "__main__":
    process_files()