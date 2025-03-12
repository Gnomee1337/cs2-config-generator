import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import webbrowser
from parsers.parsers_cs2 import parse_vcfg_bindings, parse_vcfg_convars
from filters.filters_cs2 import *
from writers.writers_cs2 import *


def write_to_text_widget(widget, message):
    widget.insert(tk.END, message)
    widget.see(tk.END)


def load_vcfg_files(file_paths, parse_function):
    data = {}
    for file in file_paths:
        if os.path.exists(file):
            write_to_text_widget(log_text, f"[+] Loading data from: {file}\n")
            parsed_data = parse_function(file)
            data.update(parsed_data)
        else:
            write_to_text_widget(log_text, f"[!] File not found: {file}\n")
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
    write_to_text_widget(log_text, f"[✔] autoexec.cfg created at: {output_file}\n")


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


def create_main_window():
    # Create the main window
    root = tk.Tk()
    root.title("CS2 Config Generator")
    create_widgets(root)
    return root


def create_widgets(root):
    global steam_id_var, config_name_var, config_path_var, log_text
    steam_id_var = tk.StringVar()
    config_name_var = tk.StringVar()
    config_path_var = tk.StringVar()
    # Steam ID selection
    ttk.Label(root, text="Select Steam ID:").pack(pady=5)
    steam_id_combobox = ttk.Combobox(root, textvariable=steam_id_var)
    steam_id_combobox.pack(pady=5)
    steam_userdata_path = r"C:\Program Files (x86)\Steam\userdata"
    steam_ids = [d for d in os.listdir(steam_userdata_path) if os.path.isdir(os.path.join(steam_userdata_path, d))]
    steam_id_combobox['values'] = steam_ids
    # 'How to find' button
    ttk.Button(root, text="How to find my id?", command=open_steamid_lookup).pack(pady=5)
    # Config name
    ttk.Label(root, text="Config Name:").pack(pady=5)
    ttk.Entry(root, textvariable=config_name_var, width=50).pack(pady=5)
    # Config path
    ttk.Label(root, text="Config Path:").pack(pady=5)
    config_path_frame = ttk.Frame(root)
    config_path_frame.pack(pady=5, fill='x')
    ttk.Entry(config_path_frame, textvariable=config_path_var, width=50).pack(side=tk.LEFT, fill='x', expand=True)
    ttk.Button(config_path_frame, text="Browse", command=select_config_path).pack(side=tk.LEFT)
    # Generate button
    ttk.Button(root, text="Generate autoexec.cfg", command=on_generate).pack(pady=20)
    # Log
    ttk.Label(root, text="Log:").pack(pady=5)
    log_text = tk.Text(root, height=10, wrap='word')
    log_text.pack(pady=5, fill='x')
    sys.stdout.write = lambda message: write_to_text_widget(log_text, message)


# Run the application
if __name__ == "__main__":
    root = create_main_window()
    root.mainloop()
