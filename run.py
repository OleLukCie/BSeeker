import os
import sys
import subprocess

base = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, base)


def has_raw_data():
    raw_file = os.path.join(base, 'data', 'raw', 'books_raw.json')
    return os.path.exists(raw_file) and os.path.getsize(raw_file) > 100


def step_crawl(force=False):
    if has_raw_data() and not force:
        print('[1/4] Crawling skipped (data already exists). Use --force-crawl to override.')
        return
    print('[1/4] Crawling...')
    subprocess.run([sys.executable, '-m', 'scrapy', 'crawl', 'book_spider'], cwd=base)


def step_clean():
    print('[2/4] Cleaning...')
    from analysis.cleaner import run as clean_run
    clean_run()


def step_analyze():
    print('[3/4] Analyzing...')
    from analysis.analyzer import run as analyze_run
    analyze_run()


def step_visualize():
    print('[4/4] Visualizing...')
    from analysis.visualizer import run as visualize_run
    visualize_run()

def step_import_db():
    print('[5/5] Importing to SQLite...')
    from database.db import init_db, import_from_json
    init_db()
    count = import_from_json()
    print('  Imported %d new books to SQLite' % count)


def main():
    force = '--force-crawl' in sys.argv
    step_crawl(force=force)
    step_clean()
    step_analyze()
    step_visualize()
    step_import_db()
    print('All done.')


if __name__ == '__main__':
    main()