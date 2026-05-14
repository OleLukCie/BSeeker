# BSeeker\analysis\cleaner.py
# J.C.  2026.5.14

import os
import json
import pandas as pd

# Import custom configuration helper
from bseeker.utils.config import get


def get_paths():
    '''
    Construct and return project data directories
    '''
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    raw = os.path.join(base, get('DATA_RAW_PATH', 'data/raw'))
    processed = os.path.join(base, get('DATA_PROCESSED_PATH', 'data/processed'))
    os.makedirs(processed, exist_ok=True)
    return raw, processed


def load_raw():
    '''
    Load raw book dataset from JSON file
    '''
    raw_dir, _ = get_paths()
    filepath = os.path.join(raw_dir, 'books_raw.json')

    if not os.path.exists(filepath):
        return pd.DataFrame()

    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    return pd.DataFrame(data)


def clean(df):
    '''
    Clean and standardize the raw book data
    - Remove rows with missing titles
    - Remove duplicate entries
    - Convert numberic columns to proper types
    - Clean whitespace from text columns
    - Fill missing numeric values with 0
    '''
    df = df.dropna(subset=['title'])
    df = df.drop_duplicates(subset=['title', 'author', 'publisher'], keep='first')
    df['price'] = pd.to_numeric(df['price'], errors='coerce').fillna(0)
    df['rating'] = pd.to_numeric(df['rating'], errors='coerce').fillna(0)
    df['sales'] = pd.to_numeric(df['sales'], errors='coerce').fillna(0).astype(int)
    df['title'] = df['title'].str.strip()
    df['author'] = df['author'].str.strip()
    df['publisher'] = df['publisher'].str.strip()
    df['category'] = df['category'].str.strip()
    return df


def save_cleaned(df):
    '''
    Save the cleaned DataFrame to a CSV file
    '''
    _, processed_dir = get_paths()
    filepath = os.path.join(processed_dir, 'books_cleaned.csv')
    df.to_csv(filepath, index=False, encoding='utf-8-sig')
    return filepath


def run():
    '''
    load -> clean -> save
    '''
    df = load_raw()
    if df.empty:
        return None
    df = clean(df)
    path = save_cleaned(df)
    return path


if __name__ == '__main__':
    result = run()
    print(result)
