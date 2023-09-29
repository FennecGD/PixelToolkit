# Web Crawler library (Part of the PixelToolkit project)

from lib.utils import log, LogUrgency
import requests
import re

class WebCrawler:
    def __init__(self, cli=False):
        self.cli = cli
        self.crawled = []

    def crawl(self, url: str, max_depth=3, depth=0):
        if url.endswith("/"):
            url = url[:-1]
        if url in self.crawled:
            return
        self.crawled.append(url)
        log(f"Crawning {url}", LogUrgency.INFO)
        try:
            request_data = requests.get(url)
            if request_data and self.cli:
                print(url)
        except:
            log(f"Can not reach {url}", LogUrgency.WARNING)
            return
        if depth < max_depth:
            new_urls = self.extract_urls(request_data.text)
            for url in new_urls:
                self.crawl(url, max_depth, depth + 1)

    def extract_urls(self, text: str):
        url_pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
        raw_urls = re.findall(url_pattern, text)
        urls = [u[:-1] if u.endswith(")") else u for u in raw_urls] # HACK
        return urls
