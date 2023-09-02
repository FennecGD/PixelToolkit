# Password generator library (Part of the PixelToolkit project)

from string import ascii_letters, digits, punctuation
import random

printable = ascii_letters + digits + punctuation


class PasswordGenerator:
    def gen(self, length):
        return "".join([random.choice(printable) for _ in range(length)])
