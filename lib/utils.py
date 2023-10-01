# Functionality that will be shared by more than one library

import math
import os
import re


def copy_to_clipboard(string_to_copy):
    try:
        import pyperclip

        pyperclip.copy(string_to_copy)
    except ImportError:
        # Don't crash if pyperclip not installed
        log(
            "Pyperclip not installed. Clipboard related functionality won't work",
            LogUrgency.WARNING,
        )


def is_valid_url(url: str) -> bool:
    return re.match(
        re.compile(
            r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
        ),
        url,
    )


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
        print(
            f"{Color.GRAY}[{timestamp}] [{urgency}{Color.GRAY}]{Color.WHITE} {string_to_log}"
        )


def cli_error(message: str):
    import sys

    print(f"[{Color.RED}!{Color.RESET}] {message}", file=sys.stderr)
    exit(1)


class MessageType:
    NEW_ITEM = Color.GREEN + "+"
    INFO = Color.LIGHT_GREEN + "!"


def cli_print(message: str, message_type: MessageType):
    print(f"[{message_type}{Color.RESET}] {message}")


# Calculate TF (Term Frequency)
def calculate_tf(document: str):
    tokenized_doc = document.lower().split()
    term_frequency = {}
    for term in tokenized_doc:
        if term in term_frequency:
            term_frequency[term] += 1
        else:
            term_frequency[term] = 1
    return term_frequency


# Calculate IDF (Inverse Document Frequency)
def calculate_idf(documents: [str], term: str):
    document_count = len(documents)
    document_with_term = sum(1 for doc in documents if term in doc.lower().split())
    if document_with_term == 0:
        return 0  # Term not present in any document
    return math.log(document_count / document_with_term)


# Calculate TF-IDF (Term Frequency - Inverse Document Frequency)
def calculate_tf_idf(document: str, documents: [str]):
    tf = calculate_tf(document)
    tf_idf = {}
    for term, freq in tf.items():
        idf = calculate_idf(documents, term)
        tf_idf[term] = freq * idf
    return tf_idf


def remove_special_characters(text: str):
    return "".join(
        char
        for char in text
        if char.isalnum() or char.isspace() or char in ["_", "-", "@", "$"]
    )


# Function to extract keywords from the provided text
def extract_keywords(text: str, min: int = 1, max: int = 100):
    keywords = calculate_tf_idf(
        text, [text]
    )  # Treat the entire text as a single document
    keywords = [
        remove_special_characters(keyword) for keyword in keywords
    ]  # Remove special characters
    # Remove empty elements + filter the keywords length to the expected range
    keywords = [
        keyword
        for keyword in keywords
        if keyword and len(keyword) in range(min, max + 1)
    ]
    keywords = list(set(keywords))  # Remove duplicates
    return keywords
