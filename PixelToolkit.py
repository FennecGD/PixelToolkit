#!/bin/python3

from lib.pass_gen import PasswordGenerator
import argparse
import sys


def generate_password(length):
    generator = PasswordGenerator()
    print("Password: " + generator.gen(length))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Password Generator", epilog="Part of the PixelToolkit project")
    parser.add_argument("--length", type=int, help="Length of the password", default=10)
    args = parser.parse_args()

    if len(sys.argv) == 1:  # If no arguments passed -> GUI
        from lib.gui import main_window_generator
        main_window_generator()

    else:
        generate_password(args.length)
