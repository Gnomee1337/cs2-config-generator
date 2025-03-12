from constants import GRENADE_SLOT_MAP


def write_section(outfile, section_title, items, formatter_func):
    """
    Write a section to the output file.
    """
    outfile.write(f"// {section_title}\n")
    for item in items:
        outfile.write(formatter_func(item) + "\n")
    outfile.write("\n")


def write_bind_section(outfile, section_title, bindings):
    write_section(
        outfile,
        section_title,
        bindings.items(),
        lambda item: f'bind "{item[0].lower()}" "{item[1]}"',
    )


def write_unbind_section(outfile, section_title, unbinds):
    write_section(outfile, section_title, unbinds, lambda item: item)


def write_grenade_section(outfile, section_title, bindings):
    write_section(
        outfile,
        section_title,
        bindings.items(),
        lambda item: f'bind "{item[0].lower()}" "{item[1]}" // {GRENADE_SLOT_MAP.get(item[1], "")}',
    )


def write_crosshair_section(outfile, section_title, crosshair_settings):
    write_section(
        outfile,
        section_title,
        crosshair_settings.items(),
        lambda item: f"{item[0]} {item[1]}",
    )


def write_mouse_section(outfile, section_title, mouse_settings):
    write_section(
        outfile,
        section_title,
        mouse_settings.items(),
        lambda item: f"{item[0]} {item[1]}",
    )


def write_radar_section(outfile, section_title, radar_settings):
    write_section(
        outfile,
        section_title,
        radar_settings.items(),
        lambda item: f"{item[0]} {item[1]}",
    )


def write_viewmodel_section(outfile, section_title, viewmodel_settings):
    write_section(
        outfile,
        section_title,
        viewmodel_settings.items(),
        lambda item: f"{item[0]} {item[1]}",
    )


def write_sound_section(outfile, section_title, sound_settings):
    write_section(
        outfile,
        section_title,
        sound_settings.items(),
        lambda item: f"{item[0]} {item[1]}",
    )


def write_damage_prediction_section(outfile, section_title, damage_prediction_settings):
    write_section(
        outfile,
        section_title,
        damage_prediction_settings.items(),
        lambda item: f"{item[0]} {item[1]}",
    )


def write_mute_section(outfile, section_title, mute_settings):
    write_section(
        outfile,
        section_title,
        mute_settings.items(),
        lambda item: f"{item[0]} {item[1]}",
    )


def write_grenade_crosshair_section(
    outfile, section_title, grenade_crossxhair_settings
):
    write_section(
        outfile,
        section_title,
        grenade_crossxhair_settings.items(),
        lambda item: f"{item[0]} {item[1]}",
    )


def write_background_section(outfile, section_title, background_settings):
    write_section(
        outfile,
        section_title,
        background_settings.items(),
        lambda item: f"{item[0]} {item[1]}",
    )


def write_hud_section(outfile, section_title, hud_settings):
    write_section(
        outfile,
        section_title,
        hud_settings.items(),
        lambda item: f"{item[0]} {item[1]}",
    )


def write_telemetry_section(outfile, section_title, telemetry_settings):
    write_section(
        outfile,
        section_title,
        telemetry_settings.items(),
        lambda item: f"{item[0]} {item[1]}",
    )


def write_other_settings_section(outfile, section_title, other_settings):
    write_section(
        outfile,
        section_title,
        other_settings.items(),
        lambda item: f'{item[0]} "{item[1]}"',
    )
