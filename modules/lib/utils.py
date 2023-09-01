# Stuff that will be shared by more than one lib
import pyperclip


def copy_to_clipboard(string_to_copy):
    pyperclip.copy(string_to_copy)
