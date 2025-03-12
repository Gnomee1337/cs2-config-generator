import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import webbrowser
from parsers.parsers_cs2 import parse_vcfg_bindings, parse_vcfg_convars
from filters.filters_cs2 import *
from writers.writers_cs2 import *


class TextRedirector:
    def __init__(self, widget, tag="stdout"):
        self.widget = widget
        self.tag = tag

    def write(self, message):
        self.widget.insert(tk.END, message)
        self.widget.see(tk.END)

    def flush(self):
        pass


def load_vcfg_files(file_paths, parse_function):
    data = {}
    for file in file_paths:
        if os.path.exists(file):
            print(f"[+] Loading data from: {file}")
            parsed_data = parse_function(file)
            data.update(parsed_data)
        else:
            print(f"[!] File not found: {file}")
    return data


def write_sections(out, all_bindings, all_convars):
    sections = [
        ("Unbinds", filter_unbind_bindings(all_bindings), write_unbind_section),
        ("Movements binds", filter_movement_bindings(all_bindings), write_bind_section),
        ("Grenades binds", filter_grenade_bindings(all_bindings), write_grenade_section),
        ("Demo hotkeys", filter_demo_bindings(all_bindings), write_bind_section),
        ("Other binds", filter_other_bindings(all_bindings), write_bind_section),
        ("Crosshair", filter_crosshair_convars(all_convars), write_crosshair_section),
        ("Grenade Crosshair", filter_grenade_crosshair_convars(all_convars), write_grenade_crosshair_section),
        ("Mouse", filter_mouse_convars(all_convars), write_mouse_section),
        ("Radar", filter_radar_convars(all_convars), write_radar_section),
        ("Viewmodel", filter_viewmodel_convars(all_convars), write_viewmodel_section),
        ("Sound", filter_sound_convars(all_convars), write_sound_section),
        ("HUD", filter_hud_convars(all_convars), write_hud_section),
        ("Damage Prediction", filter_damage_prediction_convars(all_convars), write_damage_prediction_section),
        ("Mute", filter_mute_convars(all_convars), write_mute_section),
        ("Background", filter_background_convars(all_convars), write_background_section),
        ("Telemetry", filter_telemetry_convars(all_convars), write_telemetry_section),
        ("Other settings", filter_other_convars(all_convars, combine_other_settings(all_convars)),
         write_other_settings_section),
    ]
    for section_name, data, write_function in sections:
        write_function(out, section_name, data)


def generate_autoexec(output_file: str, vcfg_files: list, convar_files: list):
    all_bindings = load_vcfg_files(vcfg_files, parse_vcfg_bindings)
    all_convars = load_vcfg_files(convar_files, parse_vcfg_convars)
    with open(output_file, 'w', encoding='utf-8') as out:
        write_sections(out, all_bindings, all_convars)
    print(f"[✔] autoexec.cfg created at: {output_file}")


def on_generate():
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
    base_path = rf"C:\Program Files (x86)\Steam\userdata\{my_id}\730"
    vcfg_files = [
        os.path.join(base_path, "local", "cfg", "cs2_user_keys_0_slot0.vcfg"),
        os.path.join(base_path, "remote", "cs2_user_keys.vcfg"),
    ]
    convar_files = [
        os.path.join(base_path, "local", "cfg", "cs2_machine_convars.vcfg"),
        os.path.join(base_path, "remote", "cs2_user_convars.vcfg"),
    ]
    output_file = os.path.join(config_path, config_name)
    generate_autoexec(output_file, vcfg_files, convar_files)


def select_config_path():
    path = filedialog.askdirectory()
    if path:
        config_path_var.set(path)


def open_steamid_lookup():
    webbrowser.open("https://steamid.io/lookup")


# Create the main window
root = tk.Tk()
root.title("CS2 Config Generator")

# Steam ID selection
steam_id_var = tk.StringVar()
steam_id_label = ttk.Label(root, text="Select Steam ID:")
steam_id_label.pack(pady=5)

steam_id_combobox = ttk.Combobox(root, textvariable=steam_id_var)
steam_id_combobox.pack(pady=5)

# How to find my id button
find_id_button = ttk.Button(root, text="Which ID?", command=open_steamid_lookup)
find_id_button.pack(pady=5)

# Populate the combobox with Steam IDs
steam_userdata_path = r"C:\Program Files (x86)\Steam\userdata"
steam_ids = [d for d in os.listdir(steam_userdata_path) if os.path.isdir(os.path.join(steam_userdata_path, d))]
steam_id_combobox['values'] = steam_ids

# Config name input
config_name_var = tk.StringVar()
config_name_label = ttk.Label(root, text="Config Name:")
config_name_label.pack(pady=5)
config_name_entry = ttk.Entry(root, textvariable=config_name_var, width=50)
config_name_entry.pack(pady=5)

# Config path input
config_path_var = tk.StringVar()
config_path_label = ttk.Label(root, text="Config Path:")
config_path_label.pack(pady=5)

config_path_frame = ttk.Frame(root)
config_path_frame.pack(pady=5, fill='x')

config_path_entry = ttk.Entry(config_path_frame, textvariable=config_path_var, width=50)
config_path_entry.pack(side=tk.LEFT, fill='x', expand=True, )

# Button to open file dialog for selecting config path
config_path_button = ttk.Button(config_path_frame, text="Browse", command=select_config_path)
config_path_button.pack(side=tk.LEFT)

# Generate button
generate_button = ttk.Button(root, text="Generate autoexec.cfg", command=on_generate)
generate_button.pack(pady=20)

# Log label
log_label = ttk.Label(root, text="Log:")
log_label.pack(pady=5)

# Output log
log_text = tk.Text(root, height=10, wrap='word')
log_text.pack(pady=5, fill='x')

# Redirect stdout to the log widget
sys.stdout = TextRedirector(log_text, "stdout")

# Run the application
root.mainloop()
