# BSeeker\analysis\Visualizer.py
# J.C.  2026.5.14


import os
import pandas as pd

import matplotlib
# Set non-interactive backend for server-side plotting
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Import custom configuration utility
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


def plot_price_distribution(df, reports_dir):
    '''
    Generate and save a histogram for book price distribution
    '''
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.hist(df['price'], bins=20, color='#3498db', edgecolor='white')
    ax.set_xlabel('Price')
    ax.set_ylabel('Count')
    ax.set_title('Book Price Distribution')
    fig.tight_layout()
    path = os.path.join(reports_dir, 'price_distribution.png')
    fig.savefig(path, dpi=150)
    plt.close(fig)
    return path


def plot_top_publishers(df, reports_dir):
    '''
    Generate and save a bar chart for the top 10 publishers by book count.
    '''
    top = df['publisher'].value_counts().head(10)

    # Handle empty data case
    if top.empty:
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.text(0.5, 0.5, 'No publisher data available', ha='center', va='center', fontsize=14)
        ax.set_title('Top 10 Publishers')
        ax.axis('off')
        fig.tight_layout()
        path = os.path.join(reports_dir, 'top_publishers.png')
        fig.savefig(path, dpi=150)
        plt.close(fig)
        return path

    # Plot bar chart
    fig, ax = plt.subplots(figsize=(12, 6))
    top.plot(kind='bar', ax=ax, color='#2ecc71')
    ax.set_xlabel('Publisher')
    ax.set_ylabel('Count')
    ax.set_title('Top 10 Publishers')
    ax.tick_params(axis='x', rotation=45)
    fig.tight_layout()
    path = os.path.join(reports_dir, 'top_publishers.png')
    fig.savefig(path, dpi=150)
    plt.close(fig)
    return path


def plot_rating_distribution(df, reports_dir):
    '''
    Generate and save a bar chart for book rating distribution.
    '''
    dist = df['rating'].value_counts().sort_index()
    if dist.empty:
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.text(0.5, 0.5, 'No rating data available', ha='center', va='center', fontsize=14)
        ax.set_title('Rating Distribution')
        ax.axis('off')
        fig.tight_layout()
        path = os.path.join(reports_dir, 'rating_distribution.png')
        fig.savefig(path, dpi=150)
        plt.close(fig)
        return path

    # Plot bar chart
    fig, ax = plt.subplots(figsize=(8, 6))
    dist.plot(kind='bar', ax=ax, color='#e74c3c')
    ax.set_xlabel('Rating')
    ax.set_ylabel('Count')
    ax.set_title('Rating Distribution')
    ax.tick_params(axis='x', rotation=0)
    fig.tight_layout()
    path = os.path.join(reports_dir, 'rating_distribution.png')
    fig.savefig(path, dpi=150)
    plt.close(fig)
    return path


def plot_sales_distribution(df, reports_dir):
    fig, ax = plt.subplots(figsize=(10, 6))

    # Check if sales data is empty
    if df['sales'].sum() == 0:
        ax.text(0.5, 0.5, 'No sales data available', ha='center', va='center', fontsize=14)
        ax.set_title('Sales Distribution')
        ax.axis('off')
    else:
        # Plot sales histogram
        ax.hist(df['sales'], bins=20, color='#9b59b6', edgecolor='white')
        ax.set_xlabel('Sales')
        ax.set_ylabel('Count')
        ax.set_title('Sales Distribution')

    fig.tight_layout()
    path = os.path.join(reports_dir, 'sales_distribution.png')
    fig.savefig(path, dpi=150)
    plt.close(fig)
    return path


def plot_category_distribution(df, reports_dir):
    '''
    Generate and save a horizontal bar chart for the top 10 book categories.
    '''
    top = df['category'].value_counts().head(10)

    if top.empty:
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.text(0.5, 0.5, 'No category data available', ha='center', va='center', fontsize=14)
        ax.set_title('Top 10 Categories')
        ax.axis('off')
        fig.tight_layout()
        path = os.path.join(reports_dir, 'category_distribution.png')
        fig.savefig(path, dpi=150)
        plt.close(fig)
        return path

    fig, ax = plt.subplots(figsize=(12, 6))
    top.plot(kind='barh', ax=ax, color='#f39c12')
    ax.set_xlabel('Count')
    ax.set_ylabel('Category')
    ax.set_title('Top 10 Categories')
    fig.tight_layout()
    path = os.path.join(reports_dir, 'category_distribution.png')
    fig.savefig(path, dpi=150)
    plt.close(fig)
    return path


def run():
    df = load_cleaned()
    if df.empty:
        return []
    _, reports_dir = get_paths()
    paths = []
    paths.append(plot_price_distribution(df, reports_dir))
    paths.append(plot_top_publishers(df, reports_dir))
    paths.append(plot_rating_distribution(df, reports_dir))
    paths.append(plot_sales_distribution(df, reports_dir))
    paths.append(plot_category_distribution(df, reports_dir))
    return paths


if __name__ == '__main__':
    result = run()
    print(result)