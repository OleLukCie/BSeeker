import os
import json
import pandas as pd
from bseeker.utils.config import get


def get_paths():
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    processed = os.path.join(base, get('DATA_PROCESSED_PATH', 'data/processed'))
    reports = os.path.join(base, get('DATA_REPORTS_PATH', 'data/reports'))
    os.makedirs(reports, exist_ok=True)
    return processed, reports


def load_cleaned():
    processed_dir, _ = get_paths()
    filepath = os.path.join(processed_dir, 'books_cleaned.csv')
    if not os.path.exists(filepath):
        return pd.DataFrame()
    return pd.read_csv(filepath)


def analyze_price(df):
    return {
        'mean': round(df['price'].mean(), 2),
        'median': round(df['price'].median(), 2),
        'min': round(df['price'].min(), 2),
        'max': round(df['price'].max(), 2),
        'std': round(df['price'].std(), 2),
    }


def analyze_publisher(df):
    top = df['publisher'].value_counts().head(10)
    return top.to_dict()


def analyze_rating(df):
    return {
        'mean': round(df['rating'].mean(), 2),
        'distribution': df['rating'].value_counts().sort_index().to_dict(),
    }


def analyze_sales(df):
    return {
        'total': int(df['sales'].sum()),
        'mean': round(df['sales'].mean(), 2),
        'top_sellers': df.nlargest(10, 'sales')[['title', 'sales']].to_dict('records'),
    }


def analyze_category(df):
    return df['category'].value_counts().head(10).to_dict()


def run():
    df = load_cleaned()
    if df.empty:
        return None
    report = {
        'total_books': len(df),
        'price_analysis': analyze_price(df),
        'top_publishers': analyze_publisher(df),
        'rating_analysis': analyze_rating(df),
        'sales_analysis': analyze_sales(df),
        'top_categories': analyze_category(df),
    }
    _, reports_dir = get_paths()
    filepath = os.path.join(reports_dir, 'analysis_report.json')
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    return filepath


if __name__ == '__main__':
    result = run()
    print(result)
