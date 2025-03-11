import os
from parsers_cs2 import parse_vcfg_bindings, parse_vcfg_convars
from filters_cs2 import *
from writers_cs2 import *


def generate_autoexec(output_file: str):
    # Load and merge bindings from vcfg files
    all_bindings = {}
    for file in vcfg_files:
        if os.path.exists(file):
            print(f"[+] Loading bindings from: {file}")
            bindings = parse_vcfg_bindings(file)
            all_bindings.update(bindings)
        else:
            print(f"[!] Bindings file not found: {file}")
    # Load and merge convars from vcfg files
    all_convars = {}
    for file in convar_files:
        if os.path.exists(file):
            print(f"[+] Loading convars from: {file}")
            convars = parse_vcfg_convars(file)
            all_convars.update(convars)
        else:
            print(f"[!] Convar file not found: {file}")
    # Open autoconfig.cfg file to write config
    with open(output_file, 'w', encoding='utf-8') as out:
        # Unbinds hotkeys section
        unbinds = filter_unbind_bindings(all_bindings)
        write_unbind_section(out, "Unbinds", unbinds)
        # Movement hotkeys section
        movement = filter_movement_bindings(all_bindings)
        write_bind_section(out, "Movements binds", movement)
        # Grenades hotkeys section
        grenades = filter_grenade_bindings(all_bindings)
        write_grenade_section(out, "Grenades binds", grenades)
        # Write Demo hotkeys section
        demo_binds = filter_demo_bindings(all_bindings)
        write_bind_section(out, "Demo hotkeys", demo_binds)
        # Other hotkeys section
        other_binds = filter_other_bindings(all_bindings)
        write_bind_section(out, "Other binds", other_binds)
        # Crosshair section
        crosshair_settings = filter_crosshair_convars(all_convars)
        write_crosshair_section(out, "Crosshair", crosshair_settings)
        # Grenade Crosshair Section
        grenade_crosshair_settings = filter_grenade_crosshair_convars(all_convars)
        write_grenade_crosshair_section(out, "Grenade Crosshair", grenade_crosshair_settings)
        # Mouse Section
        mouse_settings = filter_mouse_convars(all_convars)
        write_mouse_section(out, "Mouse", mouse_settings)
        # Radar Section
        radar_settings = filter_radar_convars(all_convars)
        write_radar_section(out, "Radar", radar_settings)
        # Viewmodel Section
        sound_settings = filter_viewmodel_convars(all_convars)
        write_viewmodel_section(out, "Viewmodel", sound_settings)
        # Sound Section
        sound_settings = filter_sound_convars(all_convars)
        write_sound_section(out, "Sound", sound_settings)
        # HUD Section
        hud_settings = filter_hud_convars(all_convars)
        write_hud_section(out, "HUD", hud_settings)
        # DamagePrediction Section
        damage_prediction_settings = filter_damage_prediction_convars(all_convars)
        write_damage_prediction_section(out, "Damage Prediction", damage_prediction_settings)
        # Mute Section
        mute_settings = filter_mute_convars(all_convars)
        write_mute_section(out, "Mute", mute_settings)
        # Background Section
        background_settings = filter_background_convars(all_convars)
        write_background_section(out, "Background", background_settings)
        # Telemetry Section
        telemetry_settings = filter_telemetry_convars(all_convars)
        write_telemetry_section(out, "Telemetry", telemetry_settings)
        # Other settings section
        other_convars = filter_other_convars(all_convars, combine_other_settings(all_convars))
        write_other_settings_section(out, "Other settings", other_convars)
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
    output_file = os.path.join(os.getcwd(), "testconfig2.cfg")
    generate_autoexec(output_file)
