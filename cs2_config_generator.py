import os
from parsers.parsers_cs2 import parse_vcfg_bindings, parse_vcfg_convars
from filters.filters_cs2 import *
from writers.writers_cs2 import *


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


if __name__ == '__main__':
    my_id = ""  # Your Steam ID
    base_path = rf"C:\Program Files (x86)\Steam\userdata\{my_id}\730"
    vcfg_files = [
        os.path.join(base_path, "local", "cfg", "cs2_user_keys_0_slot0.vcfg"),
        os.path.join(base_path, "remote", "cs2_user_keys.vcfg"),
    ]
    convar_files = [
        os.path.join(base_path, "local", "cfg", "cs2_machine_convars.vcfg"),
        os.path.join(base_path, "remote", "cs2_user_convars.vcfg"),
    ]
    output_file = os.path.join(os.getcwd(), "configs", "testconfig3.cfg")
    generate_autoexec(output_file, vcfg_files, convar_files)
