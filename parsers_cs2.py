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
