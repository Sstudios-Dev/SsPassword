import requests
import webbrowser
from tkinter import messagebox

GITHUB_API_URL = "https://api.github.com/repos/Sstudios-Dev/SsPassword/releases/latest"
CURRENT_VERSION = "1.0"

def get_latest_release_info():
    try:
        response = requests.get(GITHUB_API_URL)
        response.raise_for_status()
        release_info = response.json()
        latest_version = release_info['tag_name']
        release_notes = release_info['body']
        download_url = release_info['assets'][0]['browser_download_url'] if release_info['assets'] else None
        return latest_version, release_notes, download_url
    except requests.RequestException as e:
        messagebox.showerror("Error", f"No se encontró una versión disponible. Error: {e}")
        return None, None, None

# Modify check_for_updates in the ui.py file
def check_for_updates():
    latest_version, release_notes, download_url = get_latest_release_info()

    if latest_version and latest_version > CURRENT_VERSION:
        if messagebox.askyesno("Update Available", f"La versión {latest_version} está disponible. ¿Deseas descargarla?"):
            if download_url:
                webbrowser.open(download_url)
            else:
                messagebox.showerror("Error", "No se encontró una URL de descarga.")
    elif latest_version is None:
        messagebox.showerror("Update Error", "No se pudo comprobar si hay actualizaciones. Por favor, inténtalo más tarde.")
    else:
        messagebox.showinfo("Up-to-date", "Estás utilizando la última versión de la aplicación.")
