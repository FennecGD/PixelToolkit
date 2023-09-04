#!/bin/python3
import argparse
from lib.pass_gen import PasswordGenerator
import multiprocessing
import sys


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PixelToolkit - Collection of computer tools")
    subparsers = parser.add_subparsers(title="subcommands", dest="subcommand")

    pass_gen = subparsers.add_parser("pass-gen", help="Password Generator")
    pass_gen.add_argument("--length", "-l", type=int, help="Length of the password", default=10)

    port_scan = subparsers.add_parser("port-scan", help="Port Scanner")
    port_scan.add_argument("--host", type=str, help="Host to scan", default="127.0.0.1")
    port_scan.add_argument("--ports", "-p", type=str, dest="port_range", default="1-65535",
                           help="Port range to scan. Default is from 1 to 65535 (every port)")
    port_scan.add_argument("--threads", "-t", type=int, dest="threads", default=multiprocessing.cpu_count(),
                           help="Amount of threads that will be used for port scanning")

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

            scan_port_range(host, start_port, end_port, threads)
