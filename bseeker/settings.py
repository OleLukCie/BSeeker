import os
import sys

base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, base)

# Import configuration helpers to load settings from .env file
from bseeker.utils.config import get, get_int, get_bool


BOT_NAME = 'bseeker'
# Modules where spiders are located
SPIDER_MODULES = ['bseeker.spiders']
NEWSPIDER_MODULE = 'bseeker.spiders'

# robots.txt compliance 
ROBOTSTXT_OBEY = False

# Maximum concurrent requests sent by the crawler
CONCURRENT_REQUESTS = get_int('CONCURRENT_REQUESTS', 8)

# Maximum concurrent requests per domain
CONCURRENT_REQUESTS_PER_DOMAIN = get_int('CONCURRENT_REQUESTS_PER_DOMAIN', 4)

# Delay between consecutive requests to the same domain (prevents server overload)
DOWNLOAD_DELAY = get_int('DOWNLOAD_DELAY', 1)

# Disable cookies by default to reduce request footprint
COOKIES_ENABLED = get_bool('COOKIES_ENABLED', False)

# Default HTTP request headers for all requests
DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
}

# Custom downloader middleware configuration
DOWNLOADER_MIDDLEWARES = {
    'bseeker.middlewares.BseekerDownloaderMiddleware': 543,
}

# Enable and order Scrapy pipelines
# Lower number = executed earlier
ITEM_PIPELINES = {
    'bseeker.pipelines.DuplicateFilterPipeline': 100,   # Filter duplicates first
    'bseeker.pipelines.CleanDataPipeline': 200,         # Clean data next
    'bseeker.pipelines.SaveToJsonPipeline': 300,        # Save to JSON last
}


# ///////////////////////////////////////////////////////////////////////


# Use stable request fingerprint implementation
REQUEST_FINGERPRINTER_IMPLEMENTATION = '2.7'

# Use asyncio reactor for better async performance
TWISTED_REACTOR = 'twisted.internet.asyncioreactor.AsyncioSelectorReactor'

# Set default export encoding to UTF-8
FEED_EXPORT_ENCODING = 'utf-8'

# Logging level (INFO, DEBUG, WARNING, ERROR)
LOG_LEVEL = get('LOG_LEVEL', 'INFO')
