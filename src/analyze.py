# src/analyze.py

import os
import re
import pandas as pd
import nltk

from nltk.tokenize import word_tokenize, sent_tokenize

# Check NLTK data is loaded
nltk.download('punkt', quiet=True)

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
OUTPUT_TEXTS_DIR = os.path.join(BASE_DIR, 'output', 'texts')

# === Load dictionaries ===
def load_words_from_file(filepath):
    with open(filepath, 'r', encoding='ISO-8859-1') as f:
        return set(w.strip().lower() for w in f if w.strip())

POSITIVE_WORDS = load_words_from_file(os.path.join(DATA_DIR, 'MasterDictionary', 'positive-words.txt'))
NEGATIVE_WORDS = load_words_from_file(os.path.join(DATA_DIR, 'MasterDictionary', 'negative-words.txt'))

# === Load stop words (combine all files) ===
STOP_WORDS = set()
STOP_DIR = os.path.join(DATA_DIR, 'StopWords')
for fname in os.listdir(STOP_DIR):
    if fname.lower().endswith('.txt'):
        STOP_WORDS |= load_words_from_file(os.path.join(STOP_DIR, fname))

# Helper: Count syllables in a word
def count_syllables(word):
    word = word.lower()
    vowels = "aeiou"
    count = 0
    if word and word[0] in vowels:
        count += 1
    for i in range(1, len(word)):
        if word[i] in vowels and word[i-1] not in vowels:
            count += 1
    if word.endswith(("es", "ed")):
        count -= 1
    return max(1, count)

def count_complex_words(words):
    return sum(1 for w in words if count_syllables(w) > 2)

def count_personal_pronouns(text):
    # Exclude 'US' as per instructions
    pronoun_pattern = r'\b(I|we|my|ours|us)\b'
    return len(re.findall(pronoun_pattern, text, flags=re.I))

# Main analysis function
def analyze_single_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()

    sentences = sent_tokenize(text)
    words_all = word_tokenize(text)

    # Clean words: remove punctuation/numbers, lowercase
    words_clean = [
        w.lower() for w in words_all
        if w.isalpha()
    ]

    # Remove stop words
    words_no_stop = [w for w in words_clean if w not in STOP_WORDS]

    # Sentiment scores
    positive_score = sum(1 for w in words_no_stop if w in POSITIVE_WORDS)
    negative_score = sum(1 for w in words_no_stop if w in NEGATIVE_WORDS)
    negative_score = abs(negative_score)

    polarity_score = (positive_score - negative_score) / ((positive_score + negative_score) + 1e-6)
    subjectivity_score = (positive_score + negative_score) / (len(words_no_stop) + 1e-6)

    # Average sentence length
    avg_sentence_length = len(words_no_stop) / len(sentences) if sentences else 0

    # Complex words
    complex_word_count = count_complex_words(words_no_stop)
    pct_complex_words = complex_word_count / len(words_no_stop) if words_no_stop else 0

    # Fog index
    fog_index = 0.4 * (avg_sentence_length + pct_complex_words)

    # Avg number of words per sentence
    avg_words_per_sentence = avg_sentence_length  # same as above

    # Word count
    word_count = len(words_no_stop)

    # Syllables per word
    syllable_per_word = sum(count_syllables(w) for w in words_no_stop) / word_count if word_count else 0

    # Personal pronouns
    personal_pronouns = count_personal_pronouns(text)

    # Avg word length
    avg_word_length = sum(len(w) for w in words_no_stop) / word_count if word_count else 0

    return {
        'POSITIVE SCORE': positive_score,
        'NEGATIVE SCORE': negative_score,
        'POLARITY SCORE': polarity_score,
        'SUBJECTIVITY SCORE': subjectivity_score,
        'AVG SENTENCE LENGTH': avg_sentence_length,
        'PERCENTAGE OF COMPLEX WORDS': pct_complex_words,
        'FOG INDEX': fog_index,
        'AVG NUMBER OF WORDS PER SENTENCE': avg_words_per_sentence,
        'COMPLEX WORD COUNT': complex_word_count,
        'WORD COUNT': word_count,
        'SYLLABLE PER WORD': syllable_per_word,
        'PERSONAL PRONOUNS': personal_pronouns,
        'AVG WORD LENGTH': avg_word_length
    }

def analyze_texts(df_input):
    """
    df_input: DataFrame with columns URL_ID and URL.
    Returns DataFrame with all columns in output structure.
    """
    records = []
    for _, row in df_input.iterrows():
        url_id = str(row['URL_ID']).strip()
        file_path = os.path.join(OUTPUT_TEXTS_DIR, f"{url_id}.txt")
        if not os.path.exists(file_path):
            print(f"[WARN] Missing scraped file for {url_id}")
            continue
        metrics = analyze_single_file(file_path)
        record = {
            'URL_ID': url_id,
            'URL': row['URL']
        }
        record.update(metrics)
        records.append(record)

    # Return DataFrame with columns in the required order
    cols_order = [
        'URL_ID', 'URL', 'POSITIVE SCORE', 'NEGATIVE SCORE', 'POLARITY SCORE',
        'SUBJECTIVITY SCORE', 'AVG SENTENCE LENGTH', 'PERCENTAGE OF COMPLEX WORDS',
        'FOG INDEX', 'AVG NUMBER OF WORDS PER SENTENCE', 'COMPLEX WORD COUNT',
        'WORD COUNT', 'SYLLABLE PER WORD', 'PERSONAL PRONOUNS', 'AVG WORD LENGTH'
    ]
    return pd.DataFrame(records, columns=cols_order)
