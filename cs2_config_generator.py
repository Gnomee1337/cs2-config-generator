import os

GRENADE_SLOT_MAP = {
    "slot6": "HE Grenade",
    "slot7": "Flash",
    "slot8": "Smoke",
    "slot9": "Decoy",
    "slot10": "Molotov"
}

MOVEMENT_ACTIONS = {"+jump", "+left", "+right", "+forward", "+back", "+duck", "+sprint"}

MOUSE_SETTINGS_KEYS = {
    "sensitivity",
    "zoom_sensitivity_ratio",
    "m_yaw",
    "m_pitch",
    "mouse_inverty"
}


def parse_vcfg_bindings(file_path):
    bindings = {}
    in_bindings_block = False
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            stripped = line.strip()
            if stripped == '"bindings"':
                in_bindings_block = True
                continue
            if in_bindings_block and stripped == "}":
                break
            if in_bindings_block and stripped.startswith('"'):
                parts = stripped.split('"')
                if len(parts) >= 5:
                    key = parts[1]
                    action = parts[3]
                    bindings[key.strip()] = action.strip()
    return bindings


def parse_vcfg_convars(file_path):
    convars = {}
    in_convars_block = False
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            stripped = line.strip()
            if stripped == '"convars"':
                in_convars_block = True
                continue
            if in_convars_block and stripped == "}":
                break
            if in_convars_block and stripped.startswith('"'):
                parts = stripped.split('"')
                if len(parts) >= 5:
                    key = parts[1].strip()
                    value = parts[3].strip()
                    convars[key] = value
    return convars


def filter_movement_bindings(bindings):
    return {k: v for k, v in bindings.items() if v in MOVEMENT_ACTIONS}


def filter_grenade_bindings(bindings):
    grenade_slots = set(GRENADE_SLOT_MAP.keys())
    return {k: v for k, v in bindings.items() if v in grenade_slots}


def filter_demo_bindings(bindings: dict) -> dict:
    return {k: v for k, v in bindings.items() if v.startswith("demo_")}


def filter_unbind_bindings(bindings: dict) -> list:
    unbinds = []
    for key, action in bindings.items():
        # Keys marked as <unbound>.
        if action.strip().lower() == "<unbound>":
            unbinds.append(f'unbind "{key.lower()}"')
    return unbinds


def filter_other_bindings(bindings):
    other_bindings = {}
    for key, action in bindings.items():
        # Skip if bind is Movement, Grenade or Unbdind
        if action in MOVEMENT_ACTIONS or action in GRENADE_SLOT_MAP:
            continue
        elif action != "<unbound>":
            other_bindings[key] = action  # Add remaining binds to other_binds
    return other_bindings


def filter_crosshair_convars(convars: dict) -> dict:
    return {k: v for k, v in convars.items() if k.startswith("cl_crosshair")}


def filter_mouse_convars(convars: dict) -> dict:
    return {k: v for k, v in convars.items() if k in MOUSE_SETTINGS_KEYS}


def filter_radar_convars(convars: dict) -> dict:
    radar_keys = {}
    for key, value in convars.items():
        if key.startswith("cl_radar_") or key.startswith("cl_hud_radar_") or key == "cl_teammate_colors_show":
            radar_keys[key] = value
    return radar_keys


def filter_viewmodel_convars(convars: dict) -> dict:
    return {k: v for k, v in convars.items() if k.startswith("viewmodel_")}


def write_section(outfile, section_title: str, items: dict | list, formatter_func):
    outfile.write(f"// {section_title}\n")
    if isinstance(items, dict):
        for key, value in items.items():
            outfile.write(formatter_func(key, value) + "\n")
    elif isinstance(items, list):
        for item in items:
            outfile.write(formatter_func(item) + "\n")
    outfile.write("\n")


def write_bind_section(outfile, section_title: str, bindings: dict):
    def bind_formatter(key, action):
        return f'bind "{key.lower()}" "{action}"'

    write_section(outfile, section_title, bindings, bind_formatter)


def write_unbind_section(outfile, section_title: str, unbinds: list[str]):
    def unbind_formatter(item):
        return item

    write_section(outfile, section_title, unbinds, unbind_formatter)


def write_grenade_section(outfile, section_title: str, bindings: dict):
    def grenade_formatter(key, action):
        comment = GRENADE_SLOT_MAP.get(action, "")
        comment_str = f" // {comment}" if comment else ""
        return f'bind "{key.lower()}" "{action}"{comment_str}'

    write_section(outfile, section_title, bindings, grenade_formatter)


def write_crosshair_section(outfile, section_title: str, crosshair_settings: dict):
    def crosshair_formatter(key, value):
        return f'{key} {value}'

    write_section(outfile, section_title, crosshair_settings, crosshair_formatter)


def write_mouse_section(outfile, section_title: str, mouse_settings: dict):
    def mouse_formatter(key, value):
        return f'{key} {value}'

    write_section(outfile, section_title, mouse_settings, mouse_formatter)


def write_radar_section(outfile, section_title: str, radar_settings: dict):
    def radar_formatter(key, value):
        return f"{key} {value}"

    write_section(outfile, section_title, radar_settings, radar_formatter)


def write_viewmodel_section(outfile, section_title: str, viewmodel_settings: dict):
    def viewmodel_formatter(key, value):
        return f'{key} {value}'

    write_section(outfile, section_title, viewmodel_settings, viewmodel_formatter)


def generate_autoexec(output_file: str):
    # Load and merge bindings from vcfg files
    merged_bindings = {}
    for file in vcfg_files:
        if os.path.exists(file):
            print(f"[+] Loading bindings from: {file}")
            bindings = parse_vcfg_bindings(file)
            merged_bindings.update(bindings)
        else:
            print(f"[!] Bindings file not found: {file}")
    # Load and merge convars from vcfg files
    crosshair_convars = {}
    for file in convar_files:
        if os.path.exists(file):
            print(f"[+] Loading convars from: {file}")
            convars = parse_vcfg_convars(file)
            crosshair_convars.update(convars)
        else:
            print(f"[!] Convar file not found: {file}")
    # Open autoconfig.cfg file to write config
    with open(output_file, 'w', encoding='utf-8') as out:
        # Unbinds hotkeys section
        unbinds = filter_unbind_bindings(merged_bindings)
        write_unbind_section(out, "Unbinds", unbinds)
        # Movement hotkeys section
        movement = filter_movement_bindings(merged_bindings)
        write_bind_section(out, "Movements binds", movement)
        # Grenades hotkeys section
        grenades = filter_grenade_bindings(merged_bindings)
        write_grenade_section(out, "Grenades binds", grenades)
        # Write Demo hotkeys section
        demo_binds = filter_demo_bindings(merged_bindings)
        write_bind_section(out, "Demo hotkeys", demo_binds)
        # Other hotkeys section
        other_binds = filter_other_bindings(merged_bindings)
        write_bind_section(out, "Other binds", other_binds)
        # Crosshair section
        crosshair_settings = filter_crosshair_convars(crosshair_convars)
        write_crosshair_section(out, "Crosshair", crosshair_settings)
        # Mouse Section
        mouse_settings = filter_mouse_convars(crosshair_convars)
        write_mouse_section(out, "Mouse", mouse_settings)
        # Radar Section
        radar_settings = filter_radar_convars(crosshair_convars)
        write_radar_section(out, "Radar", radar_settings)
        # Viewmodel Section
        viewmodel_settings = filter_viewmodel_convars(crosshair_convars)
        write_viewmodel_section(out, "Viewmodel", viewmodel_settings)
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
    # output_file = os.path.join(base_path, "testconfig1.cfg")
    output_file = os.path.join(os.getcwd(), "testconfig1.cfg")
    generate_autoexec(output_file)
