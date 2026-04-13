#!/usr/bin/env python3
"""Fetch BibTeX for known publication URLs into biblio.json (run from repo root or tools/)."""
from __future__ import annotations

import json
import time
from pathlib import Path

import requests

SCRIPT_DIR = Path(__file__).resolve().parent
BIBLIO_PATH = SCRIPT_DIR / "biblio.json"

LINKS = [
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
    "https://ieeexplore.ieee.org/document/9369880",
]


def main() -> None:
    biblio: dict[str, str] = {}
    if BIBLIO_PATH.exists():
        with BIBLIO_PATH.open(encoding="utf-8") as f:
            biblio = json.load(f)

    for url in LINKS:
        if url in biblio and biblio[url].strip():
            continue

        print(f"Fetching {url}...")
        try:
            if "arxiv.org/abs/" in url:
                arxiv_id = url.split("/abs/")[-1]
                bib_url = f"https://arxiv.org/bibtex/{arxiv_id}"
                r = requests.get(bib_url, timeout=30)
                if r.status_code == 200:
                    biblio[url] = r.text
            elif "doi.org/" in url:
                headers = {"Accept": "application/x-bibtex"}
                r = requests.get(url, headers=headers, timeout=30)
                if r.status_code == 200:
                    biblio[url] = r.text
            time.sleep(1)
        except OSError as e:
            print(f"Error fetching {url}: {e}")

    with BIBLIO_PATH.open("w", encoding="utf-8") as f:
        json.dump(biblio, f, indent=2)
    print(f"Wrote {BIBLIO_PATH}")


if __name__ == "__main__":
    main()
