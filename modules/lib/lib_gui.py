import tkinter as tk
from tkinter import messagebox
from lib_pass_gen import PasswordGenerator
from utils import copy_to_clipboard


# This class allows us to create entries with placeholders so it can provide more detail to use wihout additional labels.
class EntryWithPlaceholder(tk.Entry):
    def __init__(self, master=None, placeholder="PLACEHOLDER", textvariable=None, color="grey"):
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


# Functions will be invoked after clicking button in main PixelToolkitFile
def password_gen_top_level(main_window):
    font = ("Tahoma", 15)
    password_generator_window = tk.Toplevel(main_window, bg="#282828")
    password_generator_window.title("Password Generator")

    user_input = tk.StringVar()
    password_label = tk.Label(password_generator_window, text="Provide password length:", font=font)

    # TODO: packs -> grids

    password_label.pack()

    numeric_entry = EntryWithPlaceholder(password_generator_window, "Only numbers bigger than 1", textvariable=user_input)
    numeric_entry.pack()

    def is_input_correct(user_input):
        data = user_input.get()
        return data.isdigit() and int(data) in range(1, 257)

    generator = PasswordGenerator()
    def on_submit():
        if is_input_correct(user_input):
            # Set the label text to the password generated 
            password = generator.gen(int(user_input.get()))
            password_label.config(text=f"Password generated: {password}")
            copy_button = tk.Button(password_generator_window, text='Copy to clipboard', command=lambda: copy_to_clipboard(password))
            copy_button.pack()
        else:
            password_label.config(text="Invalid input provided!")  # Update the label text

    submit_button = tk.Button(password_generator_window, text="Submit", command=on_submit)
    submit_button.pack()
