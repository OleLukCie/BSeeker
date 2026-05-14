# BSeeker\analysis\analyzer.py
# J.C.  2026.5.14

import os   # OS for file paths
import json # Json for file paths
import pandas as pd     # Pandas for data analysis

from bseeker.utils.config import get    # Import custom configuration utility


def get_paths():
    '''
    Get and create necessary directory paths for the project
    Returns: tuple: (processed_data_directory, reports_directory)
    '''
    # Get the base directory of the project
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # Define path for processed data files
    processed = os.path.join(base, get('DATA_PROCESSED_PATH', 'data/processed'))
    # Define path for analysis report output
    reports = os.path.join(base, get('DATA_REPORTS_PATH', 'data/reports'))
    # Create directory if it doesn't exist
    os.makedirs(reports, exist_ok=True)
    return processed, reports


def load_cleaned():
    '''
    Load the cleaned books dataset from CSV file
    Returns: DataFrame: Pandas DataFrame with cleaned book data
    '''
    processed_dir, _ = get_paths()
    filepath = os.path.join(processed_dir, 'books_cleaned.csv')
    # Return empty DataFrame if file doesn't exist
    if not os.path.exists(filepath):
        return pd.DataFrame()

    return pd.read_csv(filepath)


def analyze_price(df):
    '''
    Perform statistical analysis on book prices
    Args: df (DataFrame): Cleaned book data
    Returns: dict: Price statistics (mean, median, min, max, standard deviation)
    '''
    return {
        'mean': round(df['price'].mean(), 2),
        'median': round(df['price'].median(), 2),
        'min': round(df['price'].min(), 2),
        'max': round(df['price'].max(), 2),
        'std': round(df['price'].std(), 2),
    }


def analyze_publisher(df):
    '''
    Get top 10 publishers by number of books
    Returns: dict: Top publishers and their book counts
    '''
    top = df['publisher'].value_counts().head(10)
    return top.to_dict()


def analyze_rating(df):
    '''
    Analyze book rating statistics and distribution
    Returns: dict: Average rating and rating frequency distribution
    '''
    return {
        'mean': round(df['rating'].mean(), 2),
        'distribution': df['rating'].value_counts().sort_index().to_dict(),
    }


def analyze_sales(df):
    '''
    Analyze book sales performance
    Returns: dict: Total sales, average sales, and top 10 best-selling books
    '''
    return {
        'total': int(df['sales'].sum()),
        'mean': round(df['sales'].mean(), 2),
        'top_sellers': df.nlargest(10, 'sales')[['title', 'sales']].to_dict('records'),
    }


def analyze_category(df):
    '''
    Get top 10 book categories by count
    Returns: dict: Top categories and their book counts
    '''
    return df['category'].value_counts().head(10).to_dict()


def run():
    '''
    1. Load cleaned data
    2. Run all analysis functions
    3. Save results as JSON report file
    Returns: str: Path to the generated JSON report (None if no data)
    '''
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
