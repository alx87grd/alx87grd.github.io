import json
import os
import requests
import time
from bs4 import BeautifulSoup

links = [
    "https://arxiv.org/abs/2205.15137",
    "https://arxiv.org/abs/2205.15178",
    "https://arxiv.org/abs/2205.15201",
    "https://arxiv.org/abs/2206.00607",
    "https://arxiv.org/abs/2206.13361",
    "https://arxiv.org/abs/2207.02619",
    "https://arxiv.org/abs/2210.05765",
    "https://arxiv.org/abs/2307.15852",
    "https://arxiv.org/abs/2310.17545",
    "https://arxiv.org/abs/2506.20812",
    "https://cdnsciencepub.com/doi/full/10.1139/dsa-2023-0036",
    "https://doi.org/10.3390/math12050709",
    "https://ieeexplore.ieee.org/abstract/document/7814203",
    "https://ieeexplore.ieee.org/abstract/document/8744625",
    "https://ieeexplore.ieee.org/abstract/document/8962256",
    "https://ieeexplore.ieee.org/abstract/document/9128040",
    "https://ieeexplore.ieee.org/document/6714560",
    "https://ieeexplore.ieee.org/document/6755547",
    "https://ieeexplore.ieee.org/document/7354047",
    "https://ieeexplore.ieee.org/document/7487658",
    "https://ieeexplore.ieee.org/document/9369880"
]

biblio = {}

# Try to load existing
if os.path.exists('biblio.json'):
    with open('biblio.json', 'r') as f:
        biblio = json.load(f)

for url in links:
    if url in biblio and biblio[url].strip():
        continue
    
    print(f"Fetching {url}...")
    try:
        if "arxiv.org/abs/" in url:
            arxiv_id = url.split("/abs/")[-1]
            bib_url = f"https://arxiv.org/bibtex/{arxiv_id}"
            r = requests.get(bib_url)
            if r.status_code == 200:
                biblio[url] = r.text
        elif "doi.org/" in url:
            headers = {"Accept": "application/x-bibtex"}
            r = requests.get(url, headers=headers)
            if r.status_code == 200:
                biblio[url] = r.text
        # IEEE is harder, we might just use a placeholder or search
        # For this demo, let's just use generic BibTeX if we can't fetch
        time.sleep(1)
    except Exception as e:
        print(f"Error fetching {url}: {e}")

with open('biblio.json', 'w') as f:
    json.dump(biblio, f, indent=2)
