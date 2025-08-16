# src/extract.py

import os
import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
from typing import Tuple

# Directory where text files will be saved
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'output', 'texts')
os.makedirs(OUTPUT_DIR, exist_ok=True)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (compatible; DataExtractionBot/1.0; +https://blackcoffer.com)'
}

def scrape_article(url: str) -> Tuple[str, str]:
    """
    Fetches the HTML at `url` and extracts the article title and body text.
    Returns a tuple (title, body_text).
    """
    resp = requests.get(url, headers=HEADERS, timeout=10)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, 'lxml')

    # Attempt to extract title
    title_tag = soup.find('h1') or soup.find('title')
    title = title_tag.get_text(strip=True) if title_tag else ''

    # Attempt to extract article content
    # Common container tags: <article>, <div class="content">, <div class="post-content">
    container = (
        soup.find('article') or
        soup.find('div', class_='content') or
        soup.find('div', class_='post-content') or
        soup.body
    )
    # Collect all paragraphs within container
    paragraphs = container.find_all('p') if container else []
    body_text = '\n\n'.join(p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True))

    return title, body_text

def scrape_all(df: pd.DataFrame, url_col: str = 'URL', id_col: str = 'URL_ID') -> None:
    """
    Iterates over DataFrame rows, scrapes each URL, and writes the result
    to a text file named {URL_ID}.txt under output/texts/.
    """
    for idx, row in df.iterrows():
        url_id = str(row[id_col]).strip()
        url = str(row[url_col]).strip()
        if not url_id or not url:
            continue

        try:
            title, body = scrape_article(url)
        except Exception as e:
            print(f"[ERROR] {url_id}: Failed to fetch {url}: {e}")
            continue

        # Write the title and body
        file_path = os.path.join(OUTPUT_DIR, f"{url_id}.txt")
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(title + '\n\n' + body)

        print(f"[SCRAPED] {url_id} -> {file_path}")
        # Be polite to server
        time.sleep(1)

if __name__ == '__main__':
    input_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'Input.xlsx')
    df_input = pd.read_excel(input_path, engine='openpyxl')
    scrape_all(df_input)
