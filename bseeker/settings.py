import os
import sys

base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, base)

from bseeker.utils.config import get, get_int, get_bool

BOT_NAME = 'bseeker'
SPIDER_MODULES = ['bseeker.spiders']
NEWSPIDER_MODULE = 'bseeker.spiders'

ROBOTSTXT_OBEY = False

CONCURRENT_REQUESTS = get_int('CONCURRENT_REQUESTS', 8)
CONCURRENT_REQUESTS_PER_DOMAIN = get_int('CONCURRENT_REQUESTS_PER_DOMAIN', 4)
DOWNLOAD_DELAY = get_int('DOWNLOAD_DELAY', 1)

COOKIES_ENABLED = get_bool('COOKIES_ENABLED', False)

DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
}

DOWNLOADER_MIDDLEWARES = {
    'bseeker.middlewares.BseekerDownloaderMiddleware': 543,
}

ITEM_PIPELINES = {
    'bseeker.pipelines.DuplicateFilterPipeline': 100,
    'bseeker.pipelines.CleanDataPipeline': 200,
    'bseeker.pipelines.SaveToJsonPipeline': 300,
}

REQUEST_FINGERPRINTER_IMPLEMENTATION = '2.7'
TWISTED_REACTOR = 'twisted.internet.asyncioreactor.AsyncioSelectorReactor'
FEED_EXPORT_ENCODING = 'utf-8'

LOG_LEVEL = get('LOG_LEVEL', 'INFO')
