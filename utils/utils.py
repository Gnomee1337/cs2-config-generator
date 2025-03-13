import tkinter as tk
import winreg


def write_to_text_widget(widget, message):
    widget.config(state=tk.NORMAL)
    widget.insert(tk.END, message)
    widget.config(state=tk.DISABLED)
    widget.see(tk.END)


def get_steam_path():
    try:
        reg_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Valve\Steam")
        steam_path, _ = winreg.QueryValueEx(reg_key, "InstallPath")
        winreg.CloseKey(reg_key)
        return steam_path
    except FileNotFoundError:
        return r"C:\Program Files (x86)\Steam"