import arxiv
import os
import requests
from tqdm import tqdm

SAVE_DIR = "../data/raw_pdfs"
MAX_RESULTS = 60

os.makedirs(SAVE_DIR, exist_ok=True)

query = """
(cat:cs.LG OR cat:cs.CL OR cat:cs.CV)
AND submittedDate:[20190101 TO 20251231]
"""

search = arxiv.Search(
    query=query,
    max_results=MAX_RESULTS,
    sort_by=arxiv.SortCriterion.SubmittedDate
)

print("Downloading papers...")

for result in tqdm(search.results()):
    pdf_url = result.pdf_url
    paper_id = result.get_short_id()
    
    response = requests.get(pdf_url)
    
    with open(f"{SAVE_DIR}/{paper_id}.pdf", "wb") as f:
        f.write(response.content)

print("Download complete.")