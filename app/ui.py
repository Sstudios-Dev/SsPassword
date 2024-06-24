import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import font
from app.manager import store_password, retrieve_passwords
from app.encryption import check_or_create_key, create_key
from .version import get_latest_release_info, check_for_updates,  CURRENT_VERSION
import os
import ctypes
import getpass
import json
import webbrowser
import requests
import shutil

CONFIG_FILE = 'integrity/config.json'
FAILED_ATTEMPTS_LIMIT = 5
failed_attempts = 0

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
    global failed_attempts
    username = getpass.getuser()
    password = entry_password.get()

    if verify_windows_password(username, password):
        failed_attempts = 0
        login_window.destroy()
        run_main_app()
    else:
        failed_attempts += 1
        if failed_attempts >= FAILED_ATTEMPTS_LIMIT:
            messagebox.showerror("Login Failed", "Too many failed attempts. The application will now close.")
            login_window.destroy()
        else:
            messagebox.showerror("Login Failed", f"Incorrect password. {FAILED_ATTEMPTS_LIMIT - failed_attempts} attempts remaining.")

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

def open_settings():
    settings_window = tk.Toplevel()
    settings_window.title("Style Chooser")
    settings_window.geometry("400x300")
    settings_window.configure(bg="#f0f0f0")
    settings_window.resizable(False, False)

    title_label = ttk.Label(settings_window, text="Settings styles", font=('Arial', 24, 'bold'), background="#f0f0f0", foreground="#333")
    title_label.pack(pady=(20, 10))

    use_default_var = tk.BooleanVar()
    use_default_check = ttk.Checkbutton(settings_window, text="Use default style", variable=use_default_var, style='Custom.TCheckbutton')
    use_default_check.pack(anchor='w', padx=20, pady=5)

    theme_label = ttk.Label(settings_window, text="Choose Theme", font=('Arial', 18, 'bold'), background="#f0f0f0", foreground="#333")
    theme_label.pack(anchor='w', padx=20, pady=(20, 5))

    theme_var = tk.StringVar(settings_window)
    themes = get_themes()
    theme_menu = ttk.Combobox(settings_window, textvariable=theme_var, values=themes, state='readonly', font=('Arial', 12), width=20)
    theme_menu.pack(anchor='w', padx=20, pady=5)

    config = load_config()
    theme_var.set(config.get('theme', 'azure-default.tcl'))

    button_frame = ttk.Frame(settings_window, padding=(0, 20))
    button_frame.pack(fill='x', padx=20)

    save_button = ttk.Button(button_frame, text="Save", command=lambda: save_settings(settings_window, theme_var.get(), use_default_var.get()), style='TButton', width=10)
    save_button.pack(side='left', padx=(0, 10))

    cancel_button = ttk.Button(button_frame, text="Cancel", command=settings_window.destroy, style='TButton', width=10)
    cancel_button.pack(side='left')

def get_themes():
    theme_path = os.path.join(os.path.dirname(__file__), "..", "integrity", "theme")
    themes = [f for f in os.listdir(theme_path) if f.endswith('.tcl')]
    return themes

def save_settings(settings_window, selected_theme, use_default):
    if use_default:
        selected_theme = 'azure-default.tcl'
    
    theme_path = os.path.join(os.path.dirname(__file__), "..", "integrity", "theme", selected_theme)
    if os.path.exists(theme_path):
        try:
            app.tk.call('source', theme_path)
            style.theme_use(selected_theme.split('.')[0])
            save_config({'theme': selected_theme})
            messagebox.showinfo("Settings Saved", "Your settings have been saved successfully.")
            settings_window.destroy()
        except tk.TclError as e:
            messagebox.showerror("Theme Error", f"Failed to use theme: {e}")
    else:
        messagebox.showerror("Theme Error", f"Theme file not found: {theme_path}")

def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f)

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return {}

def run_main_app():
    global entry_website, entry_username, entry_password, treeview, entry_search, button_show_passwords, app, style

    app = tk.Tk()
    app.title("SsPassword - Home")
    
    # Custom styles
    style = ttk.Style(app)
    config = load_config()
    selected_theme = config.get('theme', 'azure-default.tcl')
    theme_path = os.path.join(os.path.dirname(__file__), "..", "integrity", "theme", selected_theme)
    if os.path.exists(theme_path):
        try:
            app.tk.call('source', theme_path)  # Load the selected theme from the specified path
            style.theme_use(selected_theme.split('.')[0])  # Use the theme name without extension
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

    # Menu bar
    menu_bar = tk.Menu(app)
    app.config(menu=menu_bar)

    file_menu = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Configuration", menu=file_menu)
    file_menu.add_command(label="Style Chooser", command=open_settings)
    file_menu.add_command(label="Plugin Manager", command=open_plugin_manager)

    # Sidebar for password list
    frame_sidebar = ttk.Frame(app, padding=(10, 10))
    frame_sidebar.grid(row=0, column=0, rowspan=2, sticky="nswe")

    label_search = ttk.Label(frame_sidebar, text="Search Vault")
    label_search.pack(fill='x', pady=(0, 5))

    entry_search = ttk.Entry(frame_sidebar)
    entry_search.pack(fill='x')
    entry_search.bind("<KeyRelease>", lambda event: search_passwords())  # Update the treeview on key release

    treeview = ttk.Treeview(frame_sidebar, columns=('Website', 'Username', 'Password'), show='headings')
    treeview.pack(expand=True, fill='both', pady=10)
    treeview.heading('Website', text='Website')
    treeview.heading('Username', text='Username')
    treeview.heading('Password', text='Password')

    button_show_passwords = ttk.Button(frame_sidebar, text="Show Passwords", command=toggle_passwords)
    button_show_passwords.pack(pady=(10, 0))

    # Main content area
    frame_main = ttk.Frame(app, padding=(10, 10))
    frame_main.grid(row=0, column=1, sticky="nswe")

    label_website = ttk.Label(frame_main, text="Website")
    label_website.pack(fill='x', pady=(0, 5))

    entry_website = ttk.Entry(frame_main)
    entry_website.pack(fill='x', pady=(0, 10))

    label_username = ttk.Label(frame_main, text="Username")
    label_username.pack(fill='x', pady=(0, 5))

    entry_username = ttk.Entry(frame_main)
    entry_username.pack(fill='x', pady=(0, 10))

    label_password = ttk.Label(frame_main, text="Password")
    label_password.pack(fill='x', pady=(0, 5))

    entry_password = ttk.Entry(frame_main, show='*')
    entry_password.pack(fill='x', pady=(0, 10))

    button_toggle_password = ttk.Button(frame_main, text="Show Password", command=toggle_password)
    button_toggle_password.pack(pady=(0, 10))

    button_add_password = ttk.Button(frame_main, text="Add Password", command=add_password)
    button_add_password.pack(pady=(0, 10))

    frame_version = ttk.Frame(app, padding=(10, 10))
    frame_version.grid(row=1, column=1, sticky="ew")

    label_version = ttk.Label(frame_version, text=f"Version: {CURRENT_VERSION}")
    label_version.pack(side='left')

    button_check_updates = ttk.Button(frame_version, text="Check for Updates", command=check_for_updates)
    button_check_updates.pack(side='right')

    # Load and display the initial passwords
    show_passwords()

    app.mainloop()


def open_more_info():
    response = tk.messagebox.askyesno("SsPassword", "Are you sure you want to open the web browser?")
    if response:
        webbrowser.open("https://github.com/Sstudios-Dev/SsPassword/wiki/Why-do-I-need-to-enter-my-Windows-password%3F")

def start_login():
    global entry_password, login_window

    def on_enter_pressed(event):
        login()

    login_window = tk.Tk()
    login_window.title("SsPassword - Login")
    screen_width = login_window.winfo_screenwidth()
    screen_height = login_window.winfo_screenheight()
    login_window.geometry(f"{screen_width}x{screen_height}+0+0")
    login_window.configure(bg="#2e3f4f")

    title_font = font.Font(family="Helvetica", size=36, weight="bold")
    label_font = font.Font(family="Helvetica", size=18)

    title_label = tk.Label(login_window, text="SsPassword", bg="#2e3f4f", fg="white", font=title_font)
    title_label.pack(pady=20)

    instruction_label = tk.Label(login_window, text="Enter your Windows password to access SsPassword:", bg="#2e3f4f", fg="white", font=label_font)
    instruction_label.pack(pady=20)

    entry_password = ttk.Entry(login_window, show="*", width=30, font=label_font)
    entry_password.pack(pady=20)
    entry_password.bind("<Return>", on_enter_pressed)

    show_password_var = tk.BooleanVar()
    show_password_checkbutton = ttk.Checkbutton(login_window, text="Show Password", variable=show_password_var, command=toggle_password)
    show_password_checkbutton.pack(pady=10)

    more_info_label = tk.Label(login_window, text="Why do I need to enter my Windows password?", bg="#2e3f4f", fg="blue", font=label_font, cursor="hand2")
    more_info_label.pack(pady=10)
    more_info_label.bind("<Button-1>", lambda event: open_more_info())

    style = ttk.Style()
    style.configure('TLabel', background="#2e3f4f", foreground="white", font=label_font)
    style.configure('TCheckbutton', background="#2e3f4f", foreground="white", font=label_font)

    custom_button_style = {
        'font': label_font,
        'background': '#4caf50',
        'foreground': 'white',
        'borderwidth': 0,
        'activebackground': '#388e3c',
        'activeforeground': 'white',
        'highlightthickness': 0,
        'relief': 'flat',
        'padx': 20,
        'pady': 10,
    }

    login_button = tk.Button(login_window, text="Login", command=login, **custom_button_style)
    login_button.pack(pady=20)

    login_window.mainloop()

def create_plugins_folder():
    plugins_folder = os.path.join(os.path.dirname(__file__), "..", "plugins")
    if not os.path.exists(plugins_folder):
        os.makedirs(plugins_folder)

def open_plugin_manager():
    def on_plugin_select(event):
        if available_plugins_listbox.curselection():
            selected_plugin = available_plugins_listbox.get(available_plugins_listbox.curselection())
            download_button.config(state=tk.NORMAL)
            download_button.config(command=lambda: download_plugin(selected_plugin))

    plugin_manager_window = tk.Toplevel()
    plugin_manager_window.title("Plugin Manager")
    plugin_manager_window.geometry("400x400")
    plugin_manager_window.configure(bg="#f0f0f0")
    plugin_manager_window.resizable(False, False)

    title_label = ttk.Label(plugin_manager_window, text="Plugin Manager", font=('Arial', 24, 'bold'), background="#f0f0f0", foreground="#333")
    title_label.pack(pady=(20, 10))

    plugins_folder = os.path.join(os.path.dirname(__file__), "..", "plugins")
    if os.path.exists(plugins_folder):
        installed_plugins_frame = ttk.LabelFrame(plugin_manager_window, text="Installed Plugins", padding="10")
        installed_plugins_frame.pack(pady=(10, 5), padx=20, fill='both', expand=True)

        plugins = [f for f in os.listdir(plugins_folder) if os.path.isfile(os.path.join(plugins_folder, f))]
        if plugins:
            for plugin in plugins:
                plugin_label = ttk.Label(installed_plugins_frame, text=plugin, font=('Arial', 12), background="#f0f0f0", foreground="#333")
                plugin_label.pack(pady=5, anchor='w')
        else:
            no_plugins_label = ttk.Label(installed_plugins_frame, text="No plugins installed", font=('Arial', 12), background="#f0f0f0", foreground="#333")
            no_plugins_label.pack(pady=5)
    else:
        create_plugins_folder()
        messagebox.showinfo("Folder Created", "Plugins folder created. Please restart the application.")

    available_plugins_frame = ttk.LabelFrame(plugin_manager_window, text="Available Plugins", padding="10")
    available_plugins_frame.pack(pady=(5, 10), padx=20, fill='both', expand=True)

    custom_plugins = ["tcl_editor.py"]
    available_plugins_listbox = tk.Listbox(available_plugins_frame, font=('Arial', 12), background="#f0f0f0", foreground="#333")
    available_plugins_listbox.pack(pady=5, fill='both', expand=True)

    for plugin in custom_plugins:
        available_plugins_listbox.insert(tk.END, plugin)

    available_plugins_listbox.bind('<<ListboxSelect>>', on_plugin_select)

    download_button = ttk.Button(plugin_manager_window, text="Download", state=tk.DISABLED)
    download_button.pack(pady=10)

def download_plugin(plugin_name):
    if not plugin_name:
        messagebox.showwarning("Download Plugin", "Please enter a plugin name.")
        return

    plugin_url = f"https://raw.githubusercontent.com/Sstudios-Dev/SsPassword/main/plugins/{plugin_name}"

    plugins_folder = os.path.join(os.path.dirname(__file__), "..", "plugins")
    if not os.path.exists(plugins_folder):
        os.makedirs(plugins_folder)

    plugin_path = os.path.join(plugins_folder, plugin_name)

    try:
        response = requests.get(plugin_url, stream=True)
        response.raise_for_status()

        with open(plugin_path, 'wb') as plugin_file:
            shutil.copyfileobj(response.raw, plugin_file)

        messagebox.showinfo("Download Plugin", f"Plugin '{plugin_name}' downloaded successfully.")
    except requests.RequestException as e:
        messagebox.showerror("Download Plugin", f"Failed to download plugin: {e}")

def run_app():
    if check_key():
        start_login()
    else:
        messagebox.showerror("Key Required", "The application cannot run without a secret.key file for security reasons.")
