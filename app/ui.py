import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from app.manager import store_password, retrieve_passwords
from app.encryption import check_or_create_key, create_key
import os
import ctypes
import getpass

def verify_windows_password(username, password):
    LOGON32_LOGON_NETWORK = 3
    LOGON32_PROVIDER_DEFAULT = 0

    token = ctypes.c_void_p()
    success = ctypes.windll.advapi32.LogonUserW(
        username, None, password, LOGON32_LOGON_NETWORK, LOGON32_PROVIDER_DEFAULT, ctypes.byref(token)
    )
    if success:
        ctypes.windll.kernel32.CloseHandle(token)
    return success

def toggle_password():
    if entry_password.cget('show') == '*':
        entry_password.config(show='')
    else:
        entry_password.config(show='*')

def login():
    username = getpass.getuser()
    password = entry_password.get()

    if verify_windows_password(username, password):
        login_window.destroy()
        run_main_app()
    else:
        messagebox.showerror("Login Failed", "Incorrect password. Please try again.")

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
        show_passwords(censored=True)  # Update the treeview with censored data
    else:
        messagebox.showwarning("Input Error", "All fields are required")

def show_passwords(filter_term=None, censored=True):
    passwords = retrieve_passwords()
    for i in treeview.get_children():
        treeview.delete(i)  # Clear the treeview

    for website, username, password in passwords:
        if filter_term:
            if filter_term.lower() in website.lower() or filter_term.lower() in username.lower():
                display_password = '*' * len(password) if censored else password
                treeview.insert("", "end", values=(website, username, display_password))
        else:
            display_password = '*' * len(password) if censored else password
            treeview.insert("", "end", values=(website, username, display_password))

def search_passwords():
    filter_term = entry_search.get()
    show_passwords(filter_term, censored=button_show_passwords.config('text')[-1] == "Show Passwords")

def toggle_passwords():
    if button_show_passwords.config('text')[-1] == "Show Passwords":
        show_passwords(censored=False)
        button_show_passwords.config(text="Hide Passwords")
    else:
        show_passwords(censored=True)
        button_show_passwords.config(text="Show Passwords")

def check_key():
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    if not check_or_create_key():
        response = messagebox.askyesno("No Key Found", "The secret.key file does not exist. Do you want to create it?")
        if response:
            create_key()
            messagebox.showinfo("Key Created", "The secret.key file has been created.")
        else:
            messagebox.showerror("Key Required", "The application cannot run without a secret.key file for security reasons.")
            root.destroy()
            return False
    root.destroy()
    return True

def run_main_app():
    global entry_website, entry_username, entry_password, treeview, entry_search, button_show_passwords

    app = tk.Tk()
    app.title("SsPassword - Home")
    
    # Custom styles
    style = ttk.Style(app)
    theme_path = os.path.join(os.path.dirname(__file__), "theme", "azure-default.tcl")
    if os.path.exists(theme_path):
        try:
            app.tk.call('source', theme_path)  # Load the azure-default theme from the specified path
            style.theme_use('azure-default')
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
    app.grid_rowconfigure(1, weight=1)
    app.grid_columnconfigure(0, weight=1)
    app.grid_columnconfigure(1, weight=2)

    # Sidebar for password list
    frame_sidebar = ttk.Frame(app, padding=(10, 10))
    frame_sidebar.grid(row=0, column=0, rowspan=2, sticky="nswe")

    label_search = ttk.Label(frame_sidebar, text="Search Vault")
    label_search.pack(fill='x', pady=(0, 5))

    entry_search = ttk.Entry(frame_sidebar)
    entry_search.pack(fill='x')
    entry_search.bind("<KeyRelease>", lambda event: search_passwords())  # Update the treeview on key release

    treeview = ttk.Treeview(frame_sidebar, columns=('Website', 'Username', 'Password'), show='headings')
    treeview.heading('Website', text='Website')
    treeview.heading('Username', text='Username')
    treeview.heading('Password', text='Password')
    treeview.pack(fill='both', expand=True, pady=(10, 10))

    button_show_passwords = ttk.Button(frame_sidebar, text="Show Passwords", command=toggle_passwords)
    button_show_passwords.pack(fill='x')

    # Main area for adding passwords
    frame_main = ttk.Frame(app, padding=(10, 10))
    frame_main.grid(row=0, column=1, sticky="nswe")

    ttk.Label(frame_main, text="Website").grid(row=0, column=0, sticky="w", pady=(0, 5))
    ttk.Label(frame_main, text="Username").grid(row=1, column=0, sticky="w", pady=(0, 5))
    ttk.Label(frame_main, text="Password").grid(row=2, column=0, sticky="w", pady=(0, 5))

    entry_website = ttk.Entry(frame_main)
    entry_username = ttk.Entry(frame_main)
    entry_password = ttk.Entry(frame_main, show="*")

    entry_website.grid(row=0, column=1, sticky="ew", pady=(0, 5))
    entry_username.grid(row=1, column=1, sticky="ew", pady=(0, 5))
    entry_password.grid(row=2, column=1, sticky="ew", pady=(0, 5))

    ttk.Button(frame_main, text="Add Password", command=add_password).grid(row=3, column=0, columnspan=2, sticky="ew", pady=(10, 0))

    frame_notes = ttk.Frame(app, padding=(10, 10))
    frame_notes.grid(row=1, column=1, sticky="nswe")

    text_passwords = tk.Text(frame_notes, bg="#2E2E2E", fg="#00FF00", insertbackground="white")
    text_passwords.pack(fill='both', expand=True)
    text_passwords.config(state=tk.DISABLED)  # Initially disable the text widget

    show_passwords(censored=True)  # Display all passwords initially censored

    app.mainloop()

def start_login():
    global entry_password, login_window

    login_window = tk.Tk()
    login_window.title("SsPassword - Login")

    tk.Label(login_window, text="Enter your Windows password to access the SsPassword:").pack(pady=10)
    entry_password = tk.Entry(login_window, show="*")
    entry_password.pack(pady=10)

    show_password_var = tk.BooleanVar()
    show_password_checkbutton = tk.Checkbutton(login_window, text="Show Password", variable=show_password_var, command=toggle_password)
    show_password_checkbutton.pack(pady=5)

    tk.Button(login_window, text="Login", command=login).pack(pady=10)

    login_window.mainloop()

def run_app():
    if check_key():
        start_login()
    else:
        messagebox.showerror("Key Required", "The application cannot run without a secret.key file for security reasons.")
