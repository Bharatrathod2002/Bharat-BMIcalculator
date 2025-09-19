import tkinter as tk
from tkinter import messagebox
import random
import string
import pyperclip  # Install via: pip install pyperclip

class AdvancedPasswordGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Password Generator")
        self.root.geometry("450x500")
        self.root.resizable(False, False)

        self.build_ui()

    def build_ui(self):
        # Title
        tk.Label(self.root, text="Password Generator", font=("Arial", 16, "bold")).pack(pady=10)

        # Password Length
        frame_length = tk.Frame(self.root)
        frame_length.pack(pady=5)
        tk.Label(frame_length, text="Password Length: ").pack(side=tk.LEFT)
        self.length_var = tk.IntVar(value=12)
        self.length_spin = tk.Spinbox(frame_length, from_=4, to=64, textvariable=self.length_var, width=5)
        self.length_spin.pack(side=tk.LEFT)

        # Character Type Options
        self.use_upper = tk.BooleanVar(value=True)
        self.use_lower = tk.BooleanVar(value=True)
        self.use_digits = tk.BooleanVar(value=True)
        self.use_symbols = tk.BooleanVar(value=True)

        tk.Checkbutton(self.root, text="Include Uppercase Letters (A-Z)", variable=self.use_upper).pack(anchor='w', padx=20)
        tk.Checkbutton(self.root, text="Include Lowercase Letters (a-z)", variable=self.use_lower).pack(anchor='w', padx=20)
        tk.Checkbutton(self.root, text="Include Numbers (0-9)", variable=self.use_digits).pack(anchor='w', padx=20)
        tk.Checkbutton(self.root, text="Include Symbols (!@#$...)", variable=self.use_symbols).pack(anchor='w', padx=20)

        # Exclude Characters Input
        frame_exclude = tk.Frame(self.root)
        frame_exclude.pack(pady=10)
        tk.Label(frame_exclude, text="Exclude Characters: ").pack(side=tk.LEFT)
        self.exclude_var = tk.StringVar()
        self.exclude_entry = tk.Entry(frame_exclude, textvariable=self.exclude_var, width=25)
        self.exclude_entry.pack(side=tk.LEFT)

        # Generate Button
        tk.Button(self.root, text="Generate Password", command=self.generate_password).pack(pady=15)

        # Output Entry
        self.password_entry = tk.Entry(self.root, font=("Courier", 12), justify='center', width=30)
        self.password_entry.pack(pady=10)

        # Copy Button
        tk.Button(self.root, text="Copy to Clipboard", command=self.copy_to_clipboard).pack()

    def generate_password(self):
        length = self.length_var.get()
        excluded = set(self.exclude_var.get())

        # Build character sets
        char_sets = []
        chosen_sets = []

        if self.use_upper.get():
            char_sets.append([c for c in string.ascii_uppercase if c not in excluded])
        if self.use_lower.get():
            char_sets.append([c for c in string.ascii_lowercase if c not in excluded])
        if self.use_digits.get():
            char_sets.append([c for c in string.digits if c not in excluded])
        if self.use_symbols.get():
            char_sets.append([c for c in string.punctuation if c not in excluded])

        if not char_sets:
            messagebox.showerror("Error", "Please select at least one character type.")
            return

        # Flatten all valid characters
        all_chars = [c for subset in char_sets for c in subset]
        if not all_chars:
            messagebox.showerror("Error", "No characters left to use after exclusions.")
            return

        if length < len(char_sets):
            messagebox.showerror("Error", f"Password length must be at least {len(char_sets)} for selected options.")
            return

        # Security Rule: include at least one from each selected type
        password_chars = [random.choice(s) for s in char_sets]
        remaining_length = length - len(password_chars)
        password_chars += random.choices(all_chars, k=remaining_length)

        random.shuffle(password_chars)
        final_password = ''.join(password_chars)

        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, final_password)

    def copy_to_clipboard(self):
        password = self.password_entry.get()
        if password:
            pyperclip.copy(password)
            messagebox.showinfo("Copied", "Password copied to clipboard.")
        else:
            messagebox.showwarning("Warning", "No password to copy.")

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = AdvancedPasswordGenerator(root)
    root.mainloop()
