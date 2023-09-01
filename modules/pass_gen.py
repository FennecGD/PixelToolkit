#!/bin/python3

# Password Generator (Part of the PixelToolkit project)

from lib.lib_pass_gen import PasswordGenerator
import argparse
import sys


def generate_password(length):
    generator = PasswordGenerator()
    print("Password: " + generator.gen(length))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Password Generator", epilog="Part of the PixelToolkit project")
    parser.add_argument("--length", type=int, help="Length of the password", default=10)
    args = parser.parse_args()

    if len(sys.argv) == 1:
        print("GUI")
    else:
        generate_password(args.length)
