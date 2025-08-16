  
## Data Extraction & NLP Analysis
 

---

## Objective  

The objective of this assignment is to extract textual data articles from the given URL and perform text analysis to compute variables that are explained below. 

---

## 1. Approach  

This project automatically collects article text from the links in `Input.xlsx` and checks them for overall sentiment, how easy they are to read, and other text details. The final Excel/CSV file is in the same format as `Output Data Structure.xlsx`.

### Approach in Stages:

#### **Data Extraction**
- Used `requests` to open each web link.  
- Used `BeautifulSoup` with the `lxml` parser to read the HTML code.  
- Picked out only the article **title** and **main story**, skipping menus, ads, and extras.  
- Saved each article’s clean text as `output/texts/{URL_ID}.txt`.  

#### **Text Analysis**
- Loaded the given lists of **positive words**, **negative words**, and **7 stopword files**.  
- Broke the text into sentences and words using **NLTK**.  
- Removed stopwords and punctuation so only useful words are left.  
- Calculated 13 values like Positive Score, Negative Score, Polarity, Subjectivity, Fog Index, word count, syllable count, number of personal pronouns, and average word length — as explained in `Text Analysis.docx`.  

#### **Output Generation**
- Added the calculated results to the original input data (`URL_ID` and `URL`).  
- Saved everything into `output/output.csv` with the same column order as `Output Data Structure.xlsx`.  

---

## 2. How to Run the Project  

Follow these steps to run the project from start to finish.

### Step 1 — Install Required Tools
- Make sure you have **Python 3.8 or newer** installed on your system.  
- Open a terminal (Command Prompt or PowerShell on Windows, Terminal on Mac/Linux).

### Install Required Python Libraries
Run this command to install all the necessary libraries:

```
pip install pandas openpyxl requests beautifulsoup4 lxml nltk
```

### Step 2 — Organize your the Project Folder as  given below

Your folder should be arranged like this:

```
Black_coffer_project/
├── data/
│ ├── Input.xlsx
│ ├── master_dictionary/
│ │ ├── positive_words.txt
│ │ └── negative_words.txt
│ ├── stop_words/
│ │ ├── stopwords_auditor.txt
│ │ ├── stopwords_currencies.txt
│ │ ├── stopwords_DatesandNumbers.txt
│ │ ├── stopwords_Generics.txt
│ │ ├── stopwords_GenricLong.txt
│ │ ├── stopwords_Geographic.txt
│ │ └── stopwords_Names.txt
├── src/
│ ├── main.py
│ ├── extract.py
│ └── analyze.py
└── output/
  ├── texts/
  └── output.csv
```
Place all input data, dictionaries, and stopword files accordingly.

### Step 3 — Download NLTK Data (once)
Run this command to install all the necessary libraries:

```
import nltk
nltk.download('punkt')
```

### Step 4 — Run the Pipeline
From the root project directory, execute:

```
python src/main.py
```

### Step 5 — Output Files
- Scraped text files will be saved under:  
  `output/texts/{URL_ID}.txt`
- The final analysis results will be saved as:  
  `output/output.csv`

---

## 3. Dependencies  

This project uses the following Python libraries:  

- **pandas** — for data handling and Excel/CSV operations  
- **openpyxl** — to read and write Excel files  
- **requests** — to fetch web page HTML content  
- **beautifulsoup4** — to parse HTML and extract article content  
- **lxml** — as a parser backend for BeautifulSoup  
- **nltk** — natural language processing for tokenization and text cleaning

Install all dependencies quickly via:

```
pip install pandas openpyxl requests beautifulsoup4 lxml nltk
```

---

**Author:** [Om Jaikumar]  
**Purpose:** Blackcoffer Test Assignment – Data Extraction & NLP Analysis
