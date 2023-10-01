# Hashing library (Part of the PixelToolkit project)
import hashlib


def hash_input(input, buf_size, algorithm="SHA256", output=None):
    if (
        algorithm.lower() not in hashlib.algorithms_guaranteed
        or buf_size.isdigit() is False
        or input is None
    ):
        return False

    output = None if output == "" else output
    buf_size = int(buf_size)
    try:
        h = hashlib.new(algorithm)
        with open(input, "rb") as f:
            while True:
                data = f.read(buf_size)
                if not data:
                    break
                h.update(data)

        if output is None:
            return h.hexdigest()
        elif output is not None:
            f = open(output, "w").write(h.hexdigest())

        return h.hexdigest()

    # If the file open failed treat the input as a text
    except Exception:
        h = hashlib.new(algorithm)
        h.update(input.encode())
        input_hash = h.hexdigest()

        if output is None:
            return h.hexdigest()
        elif output is not None:
            f = open(output, "w").write(input_hash)

        return input_hash
