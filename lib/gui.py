from lib.pass_gen import PasswordGenerator
from lib.utils import copy_to_clipboard
from lib.port_scanner import scan_port_range
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
    width = 800
    height = 600
    port_scan_window = tk.Toplevel(main_window, bg=DEFAULT_BG_COLOR, width=width, height=height)
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
        elif len(ports) != 2 or\
            (lower_port.isdigit() == False and upper_port.isdigit() == False) or\
            (int(lower_port) < 0 and int(upper_port) < 0) or \
            (int(upper_port) < int(lower_port)) or\
            (int(lower_port) > 65535 or int(upper_port) > 65535):
            messagebox.showerror("Error", "Invalid port range")
        elif n_threads.isdigit() == False or int(n_threads) < 1:
            messagebox.showerror("Error", "Invalid thread number")

        else:
            result = scan_port_range(host_address, int(lower_port), int(upper_port), int(n_threads))
            if len(result) == 0:
                result_label.config(text="There were not any open ports on specified range")
            else:
                result_label.config(text="Open ports for specified host\n" + "\n".join(list(map(lambda x: str(x), result))))


    entries = [
        tk.Label(port_scan_frame, text="Enter host adress: "),
        EntryWithPlaceholder(port_scan_frame, "default: ", textvariable=host),
        tk.Label(port_scan_frame, text="Enter ports range to scan: "),
        EntryWithPlaceholder(port_scan_frame, "default: ", textvariable=port_range),
        tk.Label(port_scan_frame, text="Enter amount of threads that will be used for scanning: ",),
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


def main_window_generator():
    root = tk.Tk()

    # For time we don't know full extent of this app, buttons will be placed manually
    # When we'll know how we'll want to set them up, I'll automate placing them and generating them with class
    # Maybe we could group buttons by categories like networking, cryptography, visualization and display them with for loop
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

    root.mainloop()
