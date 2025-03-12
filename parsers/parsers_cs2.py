# Constants for block types
BINDINGS_BLOCK = "bindings"
CONVARS_BLOCK = "convars"
BLOCK_END = "}"


def parse_vcfg(file_path, block_type):
    """
    Parses a VCFG file and extracts data from the specified block type.
    Args:
        file_path (str): The path to the VCFG file.
        block_type (str): The type of block to parse (e.g., "bindings" or "convars").
    Returns:
        dict: A dictionary containing the parsed data.
    """
    data = {}
    in_block = False
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                stripped_line = line.strip()
                if stripped_line == f'"{block_type}"':
                    in_block = True
                    continue
                if in_block and stripped_line == BLOCK_END:
                    break
                if in_block and stripped_line.startswith('"'):
                    parts = stripped_line.split('"')
                    if len(parts) >= 5:
                        key = parts[1].strip()
                        value = parts[3].strip()
                        data[key] = value
    except FileNotFoundError:
        print(f"[!] File not found: {file_path}")
    except Exception as error:
        print(f"[!] Error reading file {file_path}: {error}")
    return data


def parse_vcfg_bindings(file_path):
    return parse_vcfg(file_path, BINDINGS_BLOCK)


def parse_vcfg_convars(file_path):
    return parse_vcfg(file_path, CONVARS_BLOCK)
