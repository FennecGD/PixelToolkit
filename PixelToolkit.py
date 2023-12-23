#!/bin/python3

import argparse
from lib.pass_gen import PasswordGenerator
from lib.web_bruteforcer import WebBruteforcer
from lib.wordlist_generator import WordlistGenerator
from lib.web_crawler import WebCrawler
from lib.utils import Color, cli_print, MessageType, cli_error
import multiprocessing
import sys


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="PixelToolkit - Collection of computer tools"
    )
    subparsers = parser.add_subparsers(title="subcommands", dest="subcommand")

    pass_gen = subparsers.add_parser("pass-gen", help="Password Generator")
    pass_gen.add_argument(
        "--length", "-l", type=int, help="Length of the password", default=10
    )

    port_scan = subparsers.add_parser("port-scan", help="Port Scanner")
    port_scan.add_argument("--host", type=str, help="Host to scan", default="127.0.0.1")
    port_scan.add_argument(
        "--ports",
        "-p",
        type=str,
        dest="port_range",
        default="1-65535",
        help="Port range to scan. Default is from 1 to 65535 (every port)",
    )
    port_scan.add_argument(
        "--threads",
        "-t",
        type=int,
        dest="threads",
        default=multiprocessing.cpu_count(),
        help="Amount of threads that will be used for port scanning",
    )

    web_brute = subparsers.add_parser(
        "web-brute",
        help="Web Content Bruteforcer",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""\nexamples:
  {sys.argv[0]} web-brute --url http://localhost:3000/FUZZ""",
    )
    web_brute.add_argument(
        "--url",
        "-u",
        type=str,
        help="URL to scan. Use 'FUZZ' to indicate scanning point",
        required=True,
    )
    web_brute.add_argument(
        "--wordlist",
        "-w",
        type=str,
        help="Wordlist to use (uses builtin most_common.txt wordlist by default)",
    )
    web_brute.add_argument(
        "--threads",
        "-t",
        type=int,
        default=multiprocessing.cpu_count(),
        help="Ammount of threads that will be used for scanning (CPU threads by default)",
    )

    wordlist_gen = subparsers.add_parser("wordlist-gen", help="Wordlist Generator")
    wordlist_gen.add_argument(
        "--url", "-u", type=str, help="URL to generate wordlist from"
    )
    wordlist_gen.add_argument(
        "--file", "-f", type=str, help="File to generate wordlist from"
    )
    wordlist_gen.add_argument(
        "--min", type=int, help="Minimum keyword length", default=1
    )
    wordlist_gen.add_argument(
        "--max", type=int, help="Maximum keyword length", default=100
    )

    hash = subparsers.add_parser("hash", help="Text hashing")
    # TODO replace current input with file and text arguments.
    hash.add_argument("--input", "-i", required=True, help="File or text to be hashed.")
    hash.add_argument("--algorithm", "-a", default="SHA256")
    # TODO Implement automatic setting of buffer or remove buffer
    hash.add_argument("--buf", "-b", help="Size of chunks", default=4096, type=int)
    hash.add_argument("--output", "-o", help="Name for file containing output")

    web_crawler = subparsers.add_parser("web-crawler", help="Web Crawler")
    web_crawler.add_argument(
        "--url", "-u", type=str, help="URL to crawl", required=True
    )
    web_crawler.add_argument(
        "--depth", "-d", type=int, help="Max crawling depth", default=3
    )
    web_crawler.add_argument("--output", "-o", help="Output file")

    hash_crack = subparsers.add_parser("hash-crack", help="Crack hashes")
    hash_crack.add_argument("--hash", type=str, help="Hash to crack", required=True)
    hash_crack.add_argument("--type", "-t", type=str, help="Hash type", default="md5")
    hash_crack.add_argument(
        "--wordlist",
        "-w",
        type=str,
        help="Path to a wordlist",
        default="lib/wordlist.txt",
    )

    remote_shell = subparsers.add_parser("remote-shell", help="Remote Shell")
    remote_shell.add_argument('-c', '--command', action='store_true', help='command shell')
    remote_shell.add_argument('-e', '--execute', help='execute specified command')
    remote_shell.add_argument('-l', '--listen', action='store_true', help='listen')
    remote_shell.add_argument('-p', '--port', type=int, default=5555, help='specified port')
    remote_shell.add_argument('-t', '--target', default='192.168.0.189', help='specified IP')
    remote_shell.add_argument('-u', '--upload', help='upload file')

    # TODO: hash_crack bruteforce

    args = parser.parse_args()
    if len(sys.argv) == 1:  # If no arguments passed -> GUI
        from lib.gui import main_window_generator

        main_window_generator()
    else:
        if args.subcommand == "pass-gen":
            generator = PasswordGenerator()
            print("Password: " + generator.gen(args.length))

        elif args.subcommand == "port-scan":
            from lib.port_scanner import scan_port_range

            host, port_range = args.host, args.port_range
            threads = args.threads

            start_port, end_port = port_range.split("-")
            start_port, end_port = int(start_port), int(end_port)

            open_ports = scan_port_range(host, start_port, end_port, threads)
            if len(open_ports) == 0:
                cli_print(
                    "There were no open ports on specified range", MessageType.INFO
                )
            else:
                cli_print("Port scan finished", MessageType.INFO)

        elif args.subcommand == "web-brute":
            scanner = WebBruteforcer(cli=True)
            scanner.scan(args.url, args.wordlist, args.threads)

        elif args.subcommand == "wordlist-gen":
            generator = WordlistGenerator(cli=True)
            if args.url:
                generator.gen(url=args.url, min=args.min, max=args.max)
            elif args.file:
                generator.gen(file=args.file, min=args.min, max=args.max)
            else:
                cli_error("You need to either provide a URL or a File path!")
            # Here we use print instead of cli_print because we want a plain text output
            print("\n".join(generator.results))

        elif args.subcommand == "hash":
            from lib.hash import hash_input

            hashed = hash_input(
                input=args.input,
                buf_size=args.buf,
                algorithm=args.algorithm,
                output=args.output,
            )
            GREEN = Color.GREEN
            cli_print(f"{GREEN}Your hash: {hashed}", MessageType.NEW_ITEM)

        elif args.subcommand == "web-crawler":
            crawler = WebCrawler(cli=True)
            crawler.crawl(args.url, args.depth)
            if args.output:
                with open(args.output, "w") as f:
                    f.write("\n".join(crawler.crawled))

        elif args.subcommand == "hash-crack":
            from lib.hash_crack import crack

            cracked = crack(
                hash=args.hash, wordlist_path=args.wordlist, hash_type=args.type
            )

            if cracked is None:
                cli_print(
                    "Failed to crack the hash. Try using a different wordlist or bruteforce.",
                    MessageType.NEW_ITEM,
                )
            else:
                cli_print(
                    f"Cracked hash: {Color.GREEN}{cracked}{Color.RESET}",
                    MessageType.NEW_ITEM,
                )

        elif args.subcommand == "remote-shell":
            from lib.remote_shell import RemoteShell

            if args.listen:
                buffer = ""
            else:
                buffer = sys.stdin.read()

            rs = RemoteShell(args, buffer.encode())
            rs.run()
