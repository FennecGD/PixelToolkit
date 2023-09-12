from lib.pass_gen import PasswordGenerator
from lib.web_bruteforcer import WebBruteforcer
from lib.wordlist_generator import WordlistGenerator
from lib.utils import copy_to_clipboard
from lib.port_scanner import scan_port_range
from lib.hash import hash_input
import multiprocessing
import tkinter as tk
from tkinter import messagebox


# This class allows us to create entries with placeholders
# so it can provide more detail to use wihout additional labels.
class EntryWithPlaceholder(tk.Entry):
    def __init__(
        self, master=None, placeholder="PLACEHOLDER", textvariable=None, color="grey"
    ):
        super().__init__(master)

        self.placeholder = placeholder
        self.placeholder_color = color
        self.default_fg_color = self["fg"]

        if textvariable:
            self.configure(textvariable=textvariable)

        self.bind("<FocusIn>", self.focus_in)
        self.bind("<FocusOut>", self.focus_out)

        self.put_placeholder()

    def put_placeholder(self):
        self.insert(0, self.placeholder)
        self["fg"] = self.placeholder_color

    def focus_in(self, *args):
        if self["fg"] == self.placeholder_color:
            self.delete("0", "end")
            self["fg"] = self.default_fg_color

    def focus_out(self, *args):
        if not self.get():
            self.put_placeholder()


DEFAULT_BG_COLOR = "#222"
DEFAULT_WIDTH = 800
DEFAULT_HEIGHT = 600
# Functions will be invoked after clicking button in main PixelToolkitFile


def make_password_generator(main_window):
    font = ("Tahoma", 15)
    password_generator_window = tk.Toplevel(
        main_window, bg=DEFAULT_BG_COLOR, width=600, height=600
    )
    password_generator_window.resizable(False, False)
    password_generator_window.title("Password Generator")

    user_input = tk.StringVar()
    password_label = tk.Label(
        password_generator_window,
        text="Provide password length:",
        font=font,
        fg="#EEE",
        bg=DEFAULT_BG_COLOR,
        padx=10,
        pady=10,
        wraplength=250,
    )
    password_label.grid(row=0, column=0, columnspan=3)

    numeric_entry = EntryWithPlaceholder(
        password_generator_window, "Only numbers bigger than 1", textvariable=user_input
    )
    numeric_entry.grid(row=1, column=0, columnspan=3)

    def is_input_correct(user_input):
        data = user_input.get()
        return data.isdigit() and int(data) in range(1, 257)

    generator = PasswordGenerator()

    copy_button = tk.Button(password_generator_window, text="Copy")

    def on_submit():
        if is_input_correct(user_input):
            # Set the label text to the password generated
            password = generator.gen(int(user_input.get()))
            password_label.config(text=f"Password generated: {password}")
            copy_button.config(command=lambda: copy_to_clipboard(password))
            copy_button.grid(row=3, column=2)
            submit_button.grid(row=3, column=0)

        else:
            password_label.config(text="Invalid input provided!")
            # We shouldn't be able to copy if input was incorrect
            copy_button.grid_remove()
            submit_button.grid(row=3, column=1)

    submit_button = tk.Button(
        password_generator_window, text="Submit", command=on_submit
    )
    submit_button.grid(row=3, column=1)


def make_port_scan(main_window):
    port_scan_window = tk.Toplevel(main_window, bg=DEFAULT_BG_COLOR, width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT)
    port_scan_window.resizable(False, False)
    port_scan_window.title("Port Scanner")

    port_scan_frame = tk.Frame(port_scan_window)
    port_scan_frame.pack(fill=tk.BOTH, expand=True)

    host = tk.StringVar(value="127.0.0.1")
    port_range = tk.StringVar(value="1-65535")
    threads = tk.StringVar(value=multiprocessing.cpu_count())

    scan_label = tk.Label(port_scan_frame, text="Select scanning options", bg=DEFAULT_BG_COLOR, fg="#FFF")
    scan_label.pack(fill=tk.X, expand=True)

    def validate_input(host_address, ports_range, n_threads):
        host_address = host_address.replace("default: ", "")
        ports_range = ports_range.replace("default: ", "")
        n_threads = n_threads.replace("default: ", "")
        import re
        regex = r"^((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4}$"
        ports = ports_range.split("-")

        lower_port = ports[0]
        upper_port = ports[1]
        if not re.match(regex, host_address):
            messagebox.showerror("Error", "Invalid host adress")
        elif len(ports) != 2 or \
            (lower_port.isdigit() is False or upper_port.isdigit() is False) or \
            (int(lower_port) < 0 or int(upper_port) < 0) or \
            (int(upper_port) < int(lower_port)) or \
                (int(lower_port) > 65535 or int(upper_port) > 65535):
            messagebox.showerror("Error", "Invalid port range")
        elif n_threads.isdigit() is False or int(n_threads) < 1:
            messagebox.showerror("Error", "Invalid thread number")

        else:
            result = scan_port_range(host_address, int(lower_port), int(upper_port), int(n_threads))
            if len(result) == 0:
                result_label.config(text="There were not any open ports on specified range")
            else:
                result_label.config(text="Open ports for specified host\n" +
                                    "\n".join(list(map(lambda x: str(x), result))))

    entries = [
        tk.Label(port_scan_frame, text="Enter host adress: "),
        EntryWithPlaceholder(port_scan_frame, "default: ", textvariable=host),
        tk.Label(port_scan_frame, text="Enter ports range to scan: "),
        EntryWithPlaceholder(port_scan_frame, "default: ", textvariable=port_range),
        tk.Label(port_scan_frame, text="Enter amount of threads that will be used for scanning: "),
        EntryWithPlaceholder(port_scan_frame, "default: ", textvariable=threads),
        tk.Button(
            port_scan_frame,
            text="Scan Ports",
            command=lambda: validate_input(host.get(), port_range.get(), threads.get()),
        ),
    ]
    for entry in entries:
        entry.pack(fill=tk.X, expand=True)

    result_label = tk.Label(port_scan_frame)
    result_label.pack(fill=tk.X, expand=True)


def make_web_brute(main_window):
    web_brute_window = tk.Toplevel(main_window, bg=DEFAULT_BG_COLOR, width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT)
    web_brute_window.resizable(False, False)
    web_brute_window.title("Web Content Bruteforcer")

    web_brute_frame = tk.Frame(web_brute_window)
    web_brute_frame.pack(fill=tk.BOTH, expand=True)

    url = tk.StringVar()
    wordlist = tk.StringVar()
    n_threads = tk.StringVar(value=multiprocessing.cpu_count())

    scan_label = tk.Label(web_brute_frame, text="Select fuzzing options", bg=DEFAULT_BG_COLOR, fg="#FFF")
    scan_label.pack(fill=tk.X, expand=True)

    def start_web_brute(url: str, wordlist: str, n_threads: int):
        wordlist = wordlist.replace("Default: builtin wordlist", "")
        n_threads = int(n_threads.replace("Default: ", ""))
        web_bruteforcer = WebBruteforcer()
        results = web_bruteforcer.scan(url, wordlist, n_threads)
        if results is False:
            messagebox.showerror("Error", "You need to specify a correct URL, including the 'FUZZ' keyword")
        elif len(results) == 0:
            result_label.insert(tk.END, "Fuzzing finished, no results.")
        else:
            # TODO: Find a way to gradually append more results as they are discovered instead of waiting for
            #       the whole scan to finish.
            result_label.insert(tk.END, "Discovered endpoints:\n" + "\n".join(results))

    entries = [
        tk.Label(web_brute_frame, text="URL (insert 'FUZZ' keyword to specify fuzzing point): "),
        EntryWithPlaceholder(web_brute_frame, "", textvariable=url),
        tk.Label(web_brute_frame, text="Wordlist path: "),
        EntryWithPlaceholder(web_brute_frame, "Default: builtin wordlist", textvariable=wordlist),
        tk.Label(web_brute_frame, text="Enter amount of threads that will be used for fuzzing: "),
        EntryWithPlaceholder(web_brute_frame, "Default: ", textvariable=n_threads),
        tk.Button(
            web_brute_frame,
            text="Start fuzzing",
            command=lambda: start_web_brute(url.get(), wordlist.get(), n_threads.get()),
        ),
    ]
    for entry in entries:
        entry.pack(fill=tk.X, expand=True)

    result_label = tk.Text(web_brute_frame)
    result_label.pack(fill=tk.X, expand=True)

    copy_button = tk.Button(web_brute_window, text="Copy",
                            command=lambda: copy_to_clipboard(result_label.get("1.0", "end-1c")))
    copy_button.pack()


def make_wordlist_gen(main_window):
    wordlist_gen_window = tk.Toplevel(main_window, bg=DEFAULT_BG_COLOR, width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT)
    wordlist_gen_window.resizable(False, False)
    wordlist_gen_window.title("Wordlist Generator")

    wordlist_gen_frame = tk.Frame(wordlist_gen_window)
    wordlist_gen_frame.pack(fill=tk.BOTH, expand=True)

    url = tk.StringVar()
    file = tk.StringVar()
    min = tk.StringVar(value=1)
    max = tk.StringVar(value=100)

    scan_label = tk.Label(wordlist_gen_frame, text="Select Wordlist Generator Options", bg=DEFAULT_BG_COLOR, fg="#FFF")
    scan_label.pack(fill=tk.X, expand=True)

    def start_wordlist_gen(url: str, file: str, min: int, max: int):
        # TODO: validate input
        generator = WordlistGenerator()
        res = generator.gen(url, file, int(min), int(max))
        if not res:
            messagebox.showerror("Error", "Something went wrong")
        results = generator.results
        if len(results) == 0:
            result_label.insert(tk.END, "Generation finished, no keywords found")
        else:
            result_label.insert(tk.END, "\n".join(results))

    entries = [
        tk.Label(wordlist_gen_frame, text="URL (choose either URL or File):"),
        EntryWithPlaceholder(wordlist_gen_frame, "", textvariable=url),
        tk.Label(wordlist_gen_frame, text="File (choose either URL or File):"),
        EntryWithPlaceholder(wordlist_gen_frame, "", textvariable=file),
        tk.Label(wordlist_gen_frame, text="Minimum keyword length:"),
        EntryWithPlaceholder(wordlist_gen_frame, "", textvariable=min),
        tk.Label(wordlist_gen_frame, text="Maximum keyword length:"),
        EntryWithPlaceholder(wordlist_gen_frame, "", textvariable=max),
        tk.Button(
            wordlist_gen_frame,
            text="Generate Wordlist",
            command=lambda: start_wordlist_gen(url.get(), file.get(), min.get(), max.get()),
        ),
    ]
    for entry in entries:
        entry.pack(fill=tk.X, expand=True)

    result_label = tk.Text(wordlist_gen_frame)
    result_label.pack(fill=tk.X, expand=True)

    copy_button = tk.Button(wordlist_gen_window, text="Copy",
                            command=lambda: copy_to_clipboard(result_label.get("1.0", "end-1c")))
    copy_button.pack()


def make_hash(main_window):
    hash_window = tk.Toplevel(main_window, bg=DEFAULT_BG_COLOR, width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT)
    hash_window.resizable(False, False)
    hash_window.title("File and text hasher")

    hash_frame = tk.Frame(hash_window)
    hash_frame.pack(fill=tk.BOTH, expand=True)

    input_to_hash = tk.StringVar(value=None)
    algorithm = tk.StringVar(value="SHA256")
    buf_size = tk.StringVar(value=4096)
    output = tk.StringVar(value="")

    def forward_and_insert_hash_result(input, buf_size, algorithm, output):
        result = hash_input(input=input, buf_size=buf_size, algorithm=algorithm, output=output)
        result_label.config(text=result)
        copy_button.config(command=lambda: copy_to_clipboard(result))
        copy_button.pack()

    entries = [
        tk.Label(hash_frame, text="File/String to hash"),
        EntryWithPlaceholder(hash_frame, "", textvariable=input_to_hash),
        tk.Label(hash_frame, text="Choose hashing algorithm:"),
        EntryWithPlaceholder(hash_frame, "", textvariable=algorithm),
        tk.Label(hash_frame, text="Prefered buf size"),
        EntryWithPlaceholder(hash_frame, "", textvariable=buf_size),
        tk.Label(hash_frame, text="Output file name. If empty, program will display your hash below and a copy button"),
        EntryWithPlaceholder(hash_frame, "", textvariable=output),
        tk.Button(
            hash_frame,
            text="Submit Input",
            command=lambda: forward_and_insert_hash_result(input=input_to_hash.get(
            ), buf_size=buf_size.get(), algorithm=algorithm.get(), output=output.get()),
        ),
    ]
    for entry in entries:
        entry.pack(fill=tk.X, expand=True)

    result_label = tk.Label(hash_frame, text="")
    result_label.pack()
    copy_button = tk.Button(hash_frame, text="Copy hash")


def main_window_generator():
    root = tk.Tk()
    root.title("PixelToolkit")

    # For time we don't know full extent of this app, buttons will be placed manually
    # When we'll know how we'll want to set them up, I'll automate placing them and generating them with class
    # Maybe we could group buttons by categories like networking, cryptography, visualization and display them
    # with for loop
    password_button = tk.Button(
        root,
        text="Password generator",
        command=lambda: make_password_generator(root),
    )
    password_button.grid(row=1, column=1)

    port_scan_button = tk.Button(
        root,
        text="Port Scanner",
        command=lambda: make_port_scan(root),
    )
    port_scan_button.grid(row=1, column=2)

    web_brute_button = tk.Button(
        root,
        text="Web Content Bruteforcer",
        command=lambda: make_web_brute(root),
    )
    web_brute_button.grid(row=1, column=3)

    wordlist_gen_button = tk.Button(
        root,
        text="Wordlist Generator",
        command=lambda: make_wordlist_gen(root),
    )
    wordlist_gen_button.grid(row=2, column=1)

    hash_button = tk.Button(
        root,
        text="Hash file or string",
        command=lambda: make_hash(root),
    )
    hash_button.grid(row=2, column=2)

    root.mainloop()
