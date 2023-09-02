#!/bin/python3

from lib.pass_gen import PasswordGenerator
import argparse
import sys


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PixelToolkit - Collection of computer tools")
    subparsers = parser.add_subparsers(title="subcommands", dest="subcommand")

    pass_gen = subparsers.add_parser("pass-gen", help="Password Generator")
    pass_gen.add_argument("--length", "-l", type=int, help="Length of the password", default=10)

    args = parser.parse_args()

    if len(sys.argv) == 1:  # If no arguments passed -> GUI
        from lib.gui import main_window_generator
        main_window_generator()
    else:
        if args.subcommand == "pass-gen":
            generator = PasswordGenerator()
            print("Password: " + generator.gen(args.length))
