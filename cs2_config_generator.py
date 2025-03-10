import os

GRENADE_SLOT_MAP = {
    "slot6": "HE Grenade",
    "slot7": "Flash",
    "slot8": "Smoke",
    "slot9": "Decoy",
    "slot10": "Molotov"
}

MOVEMENT_ACTIONS = {"+jump", "+left", "+right", "+forward", "+back", "+duck", "+sprint"}


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
                    bindings[key] = action
    return bindings


def filter_movement_bindings(bindings):
    return {k: v for k, v in bindings.items() if v in MOVEMENT_ACTIONS}


def filter_grenade_bindings(bindings):
    grenade_slots = set(GRENADE_SLOT_MAP.keys())
    return {key: value for key, value in bindings.items() if value in grenade_slots}


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


def generate_autoexec(output_file: str):
    merged_bindings = {}
    # Load and merge bindings from vcfg files
    for file in vcfg_files:
        if os.path.exists(file):
            print(f"[+] Loading bindings from: {file}")
            bindings = parse_vcfg_bindings(file)
            merged_bindings.update(bindings)
        else:
            print(f"[!] File not found: {file}")
    # Open future autoconfig.cfg file to write config
    with open(output_file, 'w', encoding='utf-8') as out:
        # Unbinds section
        unbinds = filter_unbind_bindings(merged_bindings)
        write_unbind_section(out, "Unbinds", unbinds)
        # Movement section
        movement = filter_movement_bindings(merged_bindings)
        write_bind_section(out, "Movement", movement)
        # Grenades section
        grenades = filter_grenade_bindings(merged_bindings)
        write_grenade_section(out, "Grenade", grenades)
        # Other section
        other_binds = filter_other_bindings(merged_bindings)
        write_bind_section(out, "Other", other_binds)
    print(f"[✔] autoexec.cfg created at: {output_file}")


if __name__ == '__main__':
    my_id = ""  # Your Steam ID
    base_path = rf"C:\Program Files (x86)\Steam\userdata\{my_id}\730"
    vcfg_files = [
        os.path.join(base_path, "remote", "cs2_user_keys.vcfg"),
        os.path.join(base_path, "local", "cfg", "cs2_user_keys_0_slot0.vcfg")
    ]
    # output_file = os.path.join(base_path, "testconfig1.cfg")
    output_file = os.path.join(os.getcwd(), "testconfig1.cfg")
    generate_autoexec(output_file)
