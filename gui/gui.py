import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import webbrowser

from constants import STEAMID_LOOKUP, STEAM_USERDATA_PATH, VCFG_FILES_TEMPLATE, CONVAR_FILES_TEMPLATE
from utils.file_ops import generate_autoexec
from utils.utils import write_to_text_widget

def on_generate(steam_id_var, config_name_var, config_path_var, log_text):
    my_id = steam_id_var.get()
    if not my_id:
        messagebox.showerror("Error", "Please select a Steam ID")
        return
    config_name = config_name_var.get()
    config_path = config_path_var.get()
    if not config_name or not config_path:
        messagebox.showerror("Error", "Please enter a config name and path")
        return
    if not config_name.endswith(".cfg"):
        config_name += ".cfg"
    vcfg_files = [path.format(my_id=my_id) for path in VCFG_FILES_TEMPLATE]
    convar_files = [path.format(my_id=my_id) for path in CONVAR_FILES_TEMPLATE]
    output_file = os.path.join(config_path, config_name)
    generate_autoexec(output_file, vcfg_files, convar_files, log_text)

def select_config_path(config_path_var):
    path = filedialog.askdirectory()
    if path:
        config_path_var.set(path)

def open_steamid_lookup():
    webbrowser.open(STEAMID_LOOKUP)

def create_main_window():
    root = tk.Tk()
    root.title("CS2 Config Generator")
    
    steam_id_var = tk.StringVar()
    config_name_var = tk.StringVar()
    config_path_var = tk.StringVar()
    
    # Steam ID selection
    ttk.Label(root, text="Select Steam ID:").pack(pady=5)
    steam_id_combobox = ttk.Combobox(root, textvariable=steam_id_var)
    steam_id_combobox.pack(pady=5)
    steam_ids = [d for d in os.listdir(STEAM_USERDATA_PATH) if os.path.isdir(os.path.join(STEAM_USERDATA_PATH, d))]
    steam_id_combobox['values'] = steam_ids
    
    ttk.Button(root, text="How to find my id?", command=open_steamid_lookup).pack(pady=5)
    
    # Config name entry
    ttk.Label(root, text="Config Name:").pack(pady=5)
    ttk.Entry(root, textvariable=config_name_var, width=50).pack(pady=5)
    
    # Config path selection
    ttk.Label(root, text="Config Path:").pack(pady=5)
    config_path_frame = ttk.Frame(root)
    config_path_frame.pack(pady=5, fill='x')
    ttk.Entry(config_path_frame, textvariable=config_path_var, width=50).pack(side=tk.LEFT, fill='x', expand=True)
    ttk.Button(config_path_frame, text="Browse", command=lambda: select_config_path(config_path_var)).pack(side=tk.LEFT)
    
    ttk.Button(root, text="Generate autoexec.cfg", command=lambda: on_generate(steam_id_var, config_name_var, config_path_var, log_text)).pack(pady=20)
    
    # Logs label
    ttk.Label(root, text="Logs:", anchor='w').pack(pady=5, fill='x')
    # Log text widget
    log_text = tk.Text(root, height=10, wrap='word')
    log_text.pack(pady=5, fill='x')
    log_text.config(state=tk.DISABLED)
    sys.stdout.write = lambda message: write_to_text_widget(log_text, message)
    
    return root
