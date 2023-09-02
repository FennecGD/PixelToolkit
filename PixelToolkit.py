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
        from lib.gui import password_gen_top_level
        import tkinter as tk

        root = tk.Tk()

        password_gen = tk.Button(root, text="Password Generator", command=lambda: password_gen_top_level(root))
        password_gen.pack()

        root.mainloop()
    else:
        generate_password(args.length)
