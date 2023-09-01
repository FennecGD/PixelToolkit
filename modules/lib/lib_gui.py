import tkinter as tk
import pyperclip
from tkinter import messagebox
from lib_pass_gen import PasswordGenerator

# This class allows us to create entries with placeholders so it can provide more detail to use wihout additional labels.
class EntryWithPlaceholder(tk.Entry):
    def __init__(self, master=None, placeholder="PLACEHOLDER", textvariable=None, color="grey"):
        super().__init__(master)

        self.placeholder = placeholder
        self.placeholder_color = color
        self.default_fg_color = self["fg"]

        if textvariable:
            self.configure(textvariable=textvariable)

        self.bind("<FocusIn>", self.foc_in)
        self.bind("<FocusOut>", self.foc_out)

        self.put_placeholder()

    def put_placeholder(self):
        self.insert(0, self.placeholder)
        self["fg"] = self.placeholder_color



    def foc_in(self, *args):
        if self["fg"] == self.placeholder_color:
            self.delete("0", "end")
            self["fg"] = self.default_fg_color

    def foc_out(self, *args):
        if not self.get():
            self.put_placeholder()


# I assume user will need to type in a number in few modules so this creating entry with validation if input is stricly number may be handy
def is_number(user_input):
    if user_input.get().isdigit():
        return True
    else:
        return False


def copy_to_clipboard(string_to_copy):
    pyperclip.copy(string_to_copy)


# Functions will be invoked after clicking button in main PixelToolkitFile
def password_gen_top_level(main_window):
    font = ("Tahoma", 15)
    password_generator_window = tk.Toplevel(main_window, bg="#282828")
    password_generator_window.title("Password Generator")

    user_input = tk.StringVar()
    password_label = tk.Label(password_generator_window, text="Provide password length:", font=font)
    password_label.pack()

    numeric_entry = EntryWithPlaceholder(password_generator_window, "Only numbers bigger than 1", textvariable=user_input)
    numeric_entry.pack()

    def on_submit():
        global is_valid
        
        if is_number(user_input):
            # Set the label text to the password generated 
            password = PasswordGenerator().gen(int(user_input.get()))
            password_label.config(text=f"Password generated: {password}")
            print(type(password))
            copy_button = tk.Button(password_generator_window, text='Copy to clipboard', command=lambda: copy_to_clipboard(password))
            copy_button.pack()
        else:
            password_label.config(text="Invalid input provided!")  # Update the label text

    submit_button = tk.Button(password_generator_window, text="Submit", command=on_submit)
    submit_button.pack()

