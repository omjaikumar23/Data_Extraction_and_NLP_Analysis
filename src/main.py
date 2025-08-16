import nltk
nltk.download('punkt')  # To convert text into words and sentences

import os
import pandas as pd
from extract import scrape_all
from analyze import analyze_texts  # The analyze_texts will be implemented in analyze.py

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(__file__))  # go up to the main folder
DATA_DIR = os.path.join(BASE_DIR, 'data')              # this is where all starting stuff is kept
OUTPUT_DIR = os.path.join(BASE_DIR, 'output')          # this is where we will keep our finished work


INPUT_FILE = os.path.join(DATA_DIR, 'Input.xlsx')      # the list of links to get articles from
OUTPUT_FILE = os.path.join(OUTPUT_DIR, 'output.csv')   # the place where we  will save the final table

def main():
    # 1. First, open our file with all the links to articles
    df_input = pd.read_excel(INPUT_FILE, engine='openpyxl')

    # 2. SCRAPE ARTICLES
    print("===Starting Web Scraping===")
    scrape_all(df_input)  # saves each article as output/texts/{URL_ID}.txt

    # 3. ANALYZE TEXTS
    print("===Starting Text Analysis===")
    df_analysis = analyze_texts(df_input) # Returns DataFrame with computed metrics

    # 4. SAVE RESULTS
    print("===Saving Final Output==")
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    df_analysis.to_csv(OUTPUT_FILE, index=False)
    print(f"Output saved to: {OUTPUT_FILE}")

# This means: run my main() function if we click 'Run'
if __name__ == '__main__':
    main()
