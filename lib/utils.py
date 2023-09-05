# Stuff that will be shared by more than one lib

import os


def copy_to_clipboard(string_to_copy):
    try:
        import pyperclip
        pyperclip.copy(string_to_copy)
    except ImportError:
        # Don't crash if pyperclip not installed
        # TODO: log that copy wont work because pyperclip is not installed
        pass


# Helper for easy way of coloring terminal output
class Color:
    RESET = "\x1b[00m"
    BOLD = "\x1b[1m"
    FAINT = "\x1b[2m"
    ITALIC = "\x1b[3m"
    UNDERLINE = "\x1b[4m"
    BLINK = "\x1b[5m"
    INVERT = "\x1b[7m"
    STRIKE = "\x1b[9m"
    BLACK = "\x1b[30m"
    RED = "\x1b[31m"
    GREEN = "\x1b[32m"
    GOLD = "\x1b[33m"
    BLUE = "\x1b[34m"
    PINK = "\x1b[35m"
    CYAN = "\x1b[36m"
    GRAY = "\x1b[90m"
    LIGHT_RED = "\x1b[91m"
    LIGHT_GREEN = "\x1b[92m"
    YELLOW = "\x1b[93m"
    PURPLE = "\x1b[94m"
    LIGHT_PINK = "\x1b[95m"
    LIGHT_BLUE = "\x1b[96m"
    WHITE = "\x1b[97m"


class LogUrgency:
    INFO = Color.GREEN + "INFO"
    WARNING = Color.YELLOW + "WARNING"
    ERROR = Color.RED + "ERROR"


IS_DEBUG_ENV_VAR_SET = os.environ.get("DEBUG") is not None


def log(string_to_log, urgency=LogUrgency.INFO):
    if IS_DEBUG_ENV_VAR_SET:
        import datetime
        timestamp = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print(f"{Color.GRAY}[{timestamp}] [{urgency}{Color.GRAY}]{Color.WHITE} {string_to_log}")


def cli_error(message: str):
    import sys
    print(f"[{Color.RED}!{Color.RESET}] {message}", file=sys.stderr)
    exit(1)


class MessageType:
    NEW_ITEM = Color.GREEN + "+"
    INFO = Color.LIGHT_GREEN + "!"


def cli_print(message: str, message_type: MessageType):
    print(f"[{message_type}{Color.RESET}] {message}")
