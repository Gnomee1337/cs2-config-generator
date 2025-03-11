from constants import GRENADE_SLOT_MAP


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


def write_sound_section(outfile, section_title: str, sound_settings: dict):
    def sound_formatter(key, value):
        return f'{key} {value}'

    write_section(outfile, section_title, sound_settings, sound_formatter)


def write_damage_prediction_section(outfile, section_title: str, damage_prediction_settings: dict):
    def damage_prediction_formatter(key, value):
        return f'{key} {value}'

    write_section(outfile, section_title, damage_prediction_settings, damage_prediction_formatter)


def write_mute_section(outfile, section_title: str, mute_settings: dict):
    def mute_formatter(key, value):
        return f'{key} {value}'

    write_section(outfile, section_title, mute_settings, mute_formatter)


def write_grenade_crosshair_section(outfile, section_title: str, grenade_xhair_settings: dict):
    def grenade_crosshair_formatter(key, value):
        return f'{key} {value}'

    write_section(outfile, section_title, grenade_xhair_settings, grenade_crosshair_formatter)


def write_background_section(outfile, section_title: str, background_settings: dict):
    def background_formatter(key, value):
        return f"{key} {value}"

    write_section(outfile, section_title, background_settings, background_formatter)


def write_hud_section(outfile, section_title: str, hud_settings: dict):
    def hud_formatter(key, value):
        return f"{key} {value}"

    write_section(outfile, section_title, hud_settings, hud_formatter)


def write_telemetry_section(outfile, section_title: str, telemetry_settings: dict):
    def telemetry_formatter(key, value):
        return f'{key} {value}'

    write_section(outfile, section_title, telemetry_settings, telemetry_formatter)


def write_other_settings_section(outfile, section_title: str, other_settings: dict):
    def other_settings_formatter(key, value):
        return f'{key} "{value}"'

    write_section(outfile, section_title, other_settings, other_settings_formatter)
