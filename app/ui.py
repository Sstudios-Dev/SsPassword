import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from app.manager import store_password, retrieve_passwords
from app.encryption import check_or_create_key, create_key
import os

def add_password():
    website = entry_website.get()
    username = entry_username.get()
    password = entry_password.get()
    
    if website and username and password:
        store_password(website, username, password)
        messagebox.showinfo("Success", "Password stored successfully")
        entry_website.delete(0, tk.END)
        entry_username.delete(0, tk.END)
        entry_password.delete(0, tk.END)
    else:
        messagebox.showwarning("Input Error", "All fields are required")

def show_passwords():
    passwords = retrieve_passwords()
    text_passwords.config(state=tk.NORMAL)  # Enable the text widget to allow updates
    text_passwords.delete(1.0, tk.END)  # Clear the text widget
    for website, username, password in passwords:
        text_passwords.insert(tk.END, f"Website: {website}, Username: {username}, Password: {password}\n")
    text_passwords.config(state=tk.DISABLED)  # Disable the text widget to prevent user edits

def check_key():
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    if not check_or_create_key():
        response = messagebox.askyesno("No Key Found", "The secret.key file does not exist. Do you want to create it?")
        if response:
            create_key()
            messagebox.showinfo("Key Created", "The secret.key file has been created.")
        else:
            messagebox.showwarning("Key Required", "The application cannot run without a secret.key file.")
            root.destroy()
            return False
    root.destroy()
    return True

def main():
    global entry_website, entry_username, entry_password, text_passwords
    
    app = tk.Tk()
    app.title("SsPassword")
    
    # Custom styles
    style = ttk.Style(app)
    theme_path = os.path.join(os.path.dirname(__file__), "theme", "azure-dark.tcl")
    if os.path.exists(theme_path):
        try:
            app.tk.call('source', theme_path)  # Load the azure-dark theme from the specified path
            style.theme_use('azure-dark')
        except tk.TclError as e:
            messagebox.showerror("Theme Error", f"Failed to use theme: {e}")
            return
    else:
        messagebox.showerror("Theme Error", f"Theme file not found: {theme_path}")
        return

    # Set window size
    screen_width = app.winfo_screenwidth()
    screen_height = app.winfo_screenheight()
    window_width = int(screen_width * 0.8)
    window_height = int(screen_height * 0.8)
    app.geometry(f"{window_width}x{window_height}")

    # Configure grid weights
    app.grid_rowconfigure(5, weight=1)
    app.grid_columnconfigure(0, weight=1)
    app.grid_columnconfigure(1, weight=1)

    ttk.Label(app, text="Website").grid(row=0, column=0, sticky="w")
    ttk.Label(app, text="Username").grid(row=1, column=0, sticky="w")
    ttk.Label(app, text="Password").grid(row=2, column=0, sticky="w")

    entry_website = ttk.Entry(app)
    entry_username = ttk.Entry(app)
    entry_password = ttk.Entry(app, show="*")

    entry_website.grid(row=0, column=1, sticky="ew")
    entry_username.grid(row=1, column=1, sticky="ew")
    entry_password.grid(row=2, column=1, sticky="ew")

    ttk.Button(app, text="Add Password", command=add_password).grid(row=3, column=0, columnspan=2, sticky="ew")
    ttk.Button(app, text="Show Passwords", command=show_passwords).grid(row=4, column=0, columnspan=2, sticky="ew")

    text_passwords = tk.Text(app, bg="#2E2E2E", fg="#00FF00", insertbackground="white")
    text_passwords.grid(row=5, column=0, columnspan=2, sticky="nsew")
    text_passwords.config(state=tk.DISABLED)  # Initially disable the text widget

    app.mainloop()

def run_app():
    if check_key():
        main()
