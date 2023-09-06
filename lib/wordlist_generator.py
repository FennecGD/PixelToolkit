# Wordlist Generator library (Part of the PixelToolkit project)

from lib.utils import cli_error, extract_keywords, log, LogUrgency


class WordlistGenerator:
    def __init__(self, cli=False):
        self.cli = cli
        self.results = []

    def gen(self, url: str = None, file: str = None, min: int = 1, max: int = 100):
        log(f"Starting wordlist generator: url={url} file={file} min={min} max={max}", LogUrgency.INFO)
        if url:
            import requests
            try:
                content = requests.get(url).text
            except:
                if self.cli:
                    cli_error(f"Can not connect to: {url}")
                return False
        elif file:
            try:
                content = open(file).read()
            except:
                if self.cli:
                    cli_error(f"Can not read file: {file}")
                return False

        self.results = extract_keywords(content, min, max)
        return True
