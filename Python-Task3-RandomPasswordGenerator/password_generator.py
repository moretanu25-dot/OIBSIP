import tkinter as tk
from tkinter import messagebox
import secrets
import string
import pyperclip


# ---------------- Password Generation ----------------

def generate_password():
    try:
        length = int(length_var.get())
    except ValueError:
        messagebox.showerror("Invalid Length", "Please enter a valid password length.")
        return

    if length < 8:
        messagebox.showerror(
            "Invalid Length",
            "Password length must be at least 8 characters."
        )
        return

    selected_types = []

    if uppercase_var.get():
        selected_types.append("uppercase")

    if lowercase_var.get():
        selected_types.append("lowercase")

    if numbers_var.get():
        selected_types.append("numbers")

    if symbols_var.get():
        selected_types.append("symbols")

    if len(selected_types) < 2:
        messagebox.showerror(
            "Character Types",
            "Please select at least 2 character types."
        )
        return

    # Character sets
    uppercase = string.ascii_uppercase
    lowercase = string.ascii_lowercase
    numbers = string.digits
    symbols = string.punctuation

    # Remove ambiguous characters if selected
    if exclude_ambiguous_var.get():
        ambiguous = "0Ol1"

        uppercase = "".join(c for c in uppercase if c not in ambiguous)
        lowercase = "".join(c for c in lowercase if c not in ambiguous)
        numbers = "".join(c for c in numbers if c not in ambiguous)

    character_sets = {
        "uppercase": uppercase,
        "lowercase": lowercase,
        "numbers": numbers,
        "symbols": symbols
    }

    # Make sure every selected character set has characters
    for char_type in selected_types:
        if not character_sets[char_type]:
            messagebox.showerror(
                "Error",
                f"No usable characters available for {char_type}."
            )
            return

    # Guarantee at least one character from each selected type
    password_characters = []

    for char_type in selected_types:
        password_characters.append(
            secrets.choice(character_sets[char_type])
        )

    # Create combined character pool
    all_characters = "".join(
        character_sets[char_type] for char_type in selected_types
    )

    # Fill remaining positions
    remaining_length = length - len(password_characters)

    for _ in range(remaining_length):
        password_characters.append(
            secrets.choice(all_characters)
        )

    # Securely shuffle the generated characters
    for i in range(len(password_characters) - 1, 0, -1):
        j = secrets.randbelow(i + 1)
        password_characters[i], password_characters[j] = (
            password_characters[j],
            password_characters[i]
        )

    password = "".join(password_characters)

    # Display password
    password_var.set(password)

    # Copy automatically to clipboard
    pyperclip.copy(password)

    # Update strength
    update_strength(password, len(selected_types))

    # Add to history
    history.insert(0, password)

    # Keep only last 5 passwords
    if len(history) > 5:
        history.pop()

    update_history()


# ---------------- Password Strength ----------------

def update_strength(password, type_count):
    length = len(password)

    if length >= 12 and type_count >= 3:
        strength = "Strong"
    elif length >= 10 and type_count >= 2:
        strength = "Medium"
    else:
        strength = "Weak"

    strength_var.set(f"Strength: {strength}")


# ---------------- Clipboard ----------------

def copy_password():
    password = password_var.get()

    if not password:
        messagebox.showwarning(
            "No Password",
            "Generate a password first."
        )
        return

    pyperclip.copy(password)

    messagebox.showinfo(
        "Copied",
        "Password copied to clipboard."
    )


# ---------------- History ----------------

def update_history():
    history_listbox.delete(0, tk.END)

    for password in history:
        history_listbox.insert(tk.END, password)


# ---------------- Clear Password ----------------

def clear_password():
    password_var.set("")
    strength_var.set("Strength: -")


# ---------------- Main Window ----------------

root = tk.Tk()

root.title("Advanced Random Password Generator")
root.geometry("650x650")
root.resizable(False, False)


# Variables

length_var = tk.StringVar(value="12")

uppercase_var = tk.BooleanVar(value=True)
lowercase_var = tk.BooleanVar(value=True)
numbers_var = tk.BooleanVar(value=True)
symbols_var = tk.BooleanVar(value=True)

exclude_ambiguous_var = tk.BooleanVar(value=False)

password_var = tk.StringVar()
strength_var = tk.StringVar(value="Strength: -")

history = []


# ---------------- Title ----------------

title_label = tk.Label(
    root,
    text="Random Password Generator",
    font=("Arial", 20, "bold")
)

title_label.pack(pady=15)


subtitle = tk.Label(
    root,
    text="Generate strong and secure passwords",
    font=("Arial", 11)
)

subtitle.pack()


# ---------------- Length ----------------

length_frame = tk.Frame(root)
length_frame.pack(pady=15)

tk.Label(
    length_frame,
    text="Password Length:",
    font=("Arial", 11)
).pack(side=tk.LEFT, padx=5)

length_spinbox = tk.Spinbox(
    length_frame,
    from_=8,
    to=100,
    textvariable=length_var,
    width=8
)

length_spinbox.pack(side=tk.LEFT)


# ---------------- Character Types ----------------

types_frame = tk.LabelFrame(
    root,
    text="Character Types",
    padx=15,
    pady=10
)

types_frame.pack(pady=10)

tk.Checkbutton(
    types_frame,
    text="Uppercase Letters (A-Z)",
    variable=uppercase_var
).grid(row=0, column=0, sticky="w")

tk.Checkbutton(
    types_frame,
    text="Lowercase Letters (a-z)",
    variable=lowercase_var
).grid(row=1, column=0, sticky="w")

tk.Checkbutton(
    types_frame,
    text="Numbers (0-9)",
    variable=numbers_var
).grid(row=0, column=1, sticky="w", padx=20)

tk.Checkbutton(
    types_frame,
    text="Symbols (!@#$...)",
    variable=symbols_var
).grid(row=1, column=1, sticky="w", padx=20)


# ---------------- Security Option ----------------

security_frame = tk.Frame(root)
security_frame.pack(pady=5)

tk.Checkbutton(
    security_frame,
    text="Exclude ambiguous characters (0, O, l, 1)",
    variable=exclude_ambiguous_var
).pack()


# ---------------- Password Display ----------------

password_frame = tk.Frame(root)
password_frame.pack(pady=15)

password_entry = tk.Entry(
    password_frame,
    textvariable=password_var,
    width=45,
    font=("Arial", 12),
    justify="center"
)

password_entry.pack()


# ---------------- Strength ----------------

strength_label = tk.Label(
    root,
    textvariable=strength_var,
    font=("Arial", 12, "bold")
)

strength_label.pack(pady=5)


# ---------------- Buttons ----------------

button_frame = tk.Frame(root)
button_frame.pack(pady=10)

generate_button = tk.Button(
    button_frame,
    text="Generate Password",
    command=generate_password,
    width=18
)

generate_button.grid(row=0, column=0, padx=5)

copy_button = tk.Button(
    button_frame,
    text="Copy to Clipboard",
    command=copy_password,
    width=18
)

copy_button.grid(row=0, column=1, padx=5)

clear_button = tk.Button(
    button_frame,
    text="Clear",
    command=clear_password,
    width=10
)

clear_button.grid(row=0, column=2, padx=5)


# ---------------- History ----------------

history_frame = tk.LabelFrame(
    root,
    text="Last 5 Generated Passwords",
    padx=10,
    pady=10
)

history_frame.pack(pady=15)

history_listbox = tk.Listbox(
    history_frame,
    width=55,
    height=6
)

history_listbox.pack()


# ---------------- Start Application ----------------

root.mainloop()
