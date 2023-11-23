# Hash cracking library (Part of the PixelToolkit project)
import hashlib
from lib.utils import log


def crack(hash: str, wordlist_path: str, hash_type: str = "md5"):
    log(f"hash: {hash}, wordlist_path: {wordlist_path}, hash_type: {hash_type}")

    # TODO: bruteforce option

    hash_func = None
    if hash_type.lower() == "md5":
        hash_func = hashlib.md5
    elif hash_type.lower() == "sha1":
        hash_func = hashlib.sha1
    elif hash_type.lower() == "sha224":
        hash_func = hashlib.sha224
    elif hash_type.lower() == "sha256":
        hash_func = hashlib.sha256
    elif hash_type.lower() == "sha384":
        hash_func = hashlib.sha384
    elif hash_type.lower() == "sha512":
        hash_func = hashlib.sha512
    elif hash_type.lower() == "blake2b":
        hash_func = hashlib.blake2b
    elif hash_type.lower() == "blake2s":
        hash_func = hashlib.blake2s

    wordlist = open(wordlist_path, "r").read().splitlines()
    for word in wordlist:
        if str(hash_func(word.encode()).hexdigest()) == hash:
            return word

    return None
