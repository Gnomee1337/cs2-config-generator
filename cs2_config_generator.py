import os

GRENADE_SLOT_MAP = {
    "slot6": "HE Grenade",
    "slot7": "Flash",
    "slot8": "Smoke",
    "slot9": "Decoy",
    "slot10": "Molotov"
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
                    bindings[key] = action
    return bindings

def filter_movement_bindings(bindings):
    movement_actions = {"+jump", "+left", "+right", "+forward", "+back", "+duck", "+sprint"}
    return {k: v for k, v in bindings.items() if v in movement_actions}

def filter_grenade_bindings(bindings):
    grenade_slots = set(GRENADE_SLOT_MAP.keys())
    return {key: value for key, value in bindings.items() if value in grenade_slots}

def write_bind_section(outfile, section_title, bindings):
    outfile.write(f"// {section_title} Keys\n")
    for key, action in bindings.items():
        outfile.write(f'bind "{key.lower()}" "{action}"\n')
    outfile.write("\n")

def write_grenade_section(outfile, bindings):
    outfile.write("// Grenade Binds\n")
    for key, action in bindings.items():
        comment = GRENADE_SLOT_MAP.get(action, "")
        comment_str = f" // {comment}" if comment else ""
        outfile.write(f'bind "{key.lower()}" "{action}"{comment_str}\n')
    outfile.write("\n")

def generate_autoexec():
    merged_bindings = {}
    for file in vcfg_files:
        if os.path.exists(file):
            print(f"[+] Loading bindings from: {file}")
            bindings = parse_vcfg_bindings(file)
            merged_bindings.update(bindings)
        else:
            print(f"[!] File not found: {file}")
    with open(output_file, 'w', encoding='utf-8') as out:
        # Movement
        movement = filter_movement_bindings(merged_bindings)
        write_bind_section(out, "Movement", movement)
        # Grenades
        grenades = filter_grenade_bindings(merged_bindings)
        write_grenade_section(out, grenades)
    print(f"[✔] autoexec.cfg created at: {output_file}")

if __name__ == '__main__':
    my_id = ""  # Your Steam ID
    base_path = rf"C:\Program Files (x86)\Steam\userdata\{my_id}\730"
    vcfg_files = [
        os.path.join(base_path, "remote", "cs2_user_keys.vcfg"),
        os.path.join(base_path, "local", "cfg", "cs2_user_keys_0_slot0.vcfg")
    ]
    # output_file = os.path.join(base_path, "testconfig1.cfg")
    output_file = os.path.join(os.getcwd(), "autoexec.cfg")
    generate_autoexec()