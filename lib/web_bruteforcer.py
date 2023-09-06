# Web Content Bruteforcer library (Part of the PixelToolkit project)

from lib.utils import cli_error, log, LogUrgency, cli_print, MessageType, Color
import requests
import threading

DEFAULT_WORDLIST = "lib/wordlist.txt"


class WebBruteforcer():
    def __init__(self, cli=False):
        self.cli = cli
        self.results = []

    def scan(self, url: str, wordlist: str, n_threads: int):
        log(f"Starting web bruteforcer. URL={url} threads={n_threads}", LogUrgency.INFO)
        # TODO: support multiple FUZZ parameters in the URL
        if "FUZZ" not in url:
            if self.cli:
                cli_error("You need to specify the fuzzing point using the 'FUZZ' keyword")
            return False
        wordlist = open(wordlist or DEFAULT_WORDLIST).read().strip().split()

        threads = []
        for i in range(n_threads):
            thread = threading.Thread(target=self.scanning_thread, args=(url, wordlist, i, n_threads))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        if self.cli:
            cli_print("Web content bruteforce finished", MessageType.INFO)

        return self.results

    # I *think* python will pass the wordlist by reference. This is quite important as this wordlist object
    # can be multiple hundreds of Megabytes or even Gigabytes in size and cloning it for each thread is not
    # ideal to say the least.

    def scanning_thread(self, url: str, wordlist: list, starting_index: int, n_threads: int):
        wordlist_len = len(wordlist)
        i = starting_index
        while i < wordlist_len:
            word = wordlist[i]
            url_to_scan = url.replace("FUZZ", word)
            if self.scan_url(url_to_scan) is True:
                self.results.append(url_to_scan)
            i += n_threads

    def scan_url(self, url_to_scan: str):
        try:
            req = requests.get(url_to_scan)
            if req.ok:
                if self.cli:
                    cli_print(url_to_scan, MessageType.NEW_ITEM)
                return True
        except requests.ConnectionError as e:
            if "RemoteDisconnected" in str(e):
                # Server aborted the connection. This means the server did something interesting. Log that
                if self.cli:
                    cli_print(f"{Color.GRAY}(connection aborted){Color.RESET} {url_to_scan}", MessageType.NEW_ITEM)
                return True
            else:
                if self.cli:
                    cli_error(f"Can not connect to: {url_to_scan}")
                return False
