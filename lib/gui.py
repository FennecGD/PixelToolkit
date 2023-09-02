import tkinter as tk
from lib.pass_gen import PasswordGenerator
from lib.utils import copy_to_clipboard


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


# Functions will be invoked after clicking button in main PixelToolkitFile
def password_gen_top_level(main_window):
    font = ("Tahoma", 15)
    password_generator_window = tk.Toplevel(
        main_window, bg="#222", width=600, height=600
    )
    password_generator_window.resizable(False, False)
    password_generator_window.title("Password Generator")

    user_input = tk.StringVar()
    password_label = tk.Label(
        password_generator_window,
        text="Provide password length:",
        font=font,
        fg="#EEE",
        bg="#222",
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

    def on_submit():
        if is_input_correct(user_input):
            # Set the label text to the password generated
            password = generator.gen(int(user_input.get()))
            password_label.config(text=f"Password generated: {password}")
            global copy_button
            copy_button = tk.Button(
                password_generator_window,
                text="Copy",
                command=lambda: copy_to_clipboard(password),
            )
            copy_button.grid(row=3, column=2)
            submit_button.grid(row=3, column=0)

        else:
            password_label.config(text="Invalid input provided!")
            # We shouldn't be able to copy if input was incorrect
            copy_button.destroy()
            submit_button.grid(row=3, column=1)

    submit_button = tk.Button(
        password_generator_window, text="Submit", command=on_submit
    )
    submit_button.grid(row=3, column=1)


def main_window_generator():
    root = tk.Tk()
    x = root.winfo_screenwidth()
    y = root.winfo_screenheight()

    # For time we don't know full extent of this app, buttons will be placed manually
    # When we'll know how we'll want to set them up, I'll automate placing them and generating them with class
    # Maybe we could group buttons by categories like networking, cryptography, visualization and display them with for loop
    password_button = tk.Button(
        root,
        text="Password generator",
        command=lambda: password_gen_top_level(root),
    )
    password_button.grid(row=1, column=1)
    root.mainloop()
