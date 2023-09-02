# Stuff that will be shared by more than one lib

# TODO add log function


def copy_to_clipboard(string_to_copy):
    try:
        import pyperclip
        pyperclip.copy(string_to_copy)
    except ImportError:
        # Don't crash if pyperclip not installed
        # TODO: log that copy wont work because pyperclip is not installed
        pass
