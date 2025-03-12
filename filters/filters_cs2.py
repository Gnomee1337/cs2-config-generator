from constants import *


def filter_dict(bindings, condition):
    return {k: v for k, v in bindings.items() if condition(k, v)}


def filter_movement_bindings(bindings):
    return filter_dict(bindings, lambda k, v: v in MOVEMENT_ACTIONS)


def filter_grenade_bindings(bindings):
    grenade_slots = set(GRENADE_SLOT_MAP.keys())
    return filter_dict(bindings, lambda k, v: v in grenade_slots)


def filter_demo_bindings(bindings):
    return filter_dict(bindings, lambda k, v: v.startswith(DEMO_PREFIX))


def filter_unbind_bindings(bindings):
    return [
        f'unbind "{k.lower()}"'
        for k, v in bindings.items()
        if v.strip().lower() == UNBIND_VALUE
    ]


def filter_other_bindings(bindings):
    return filter_dict(
        bindings,
        lambda k, v: v not in MOVEMENT_ACTIONS
        and v not in GRENADE_SLOT_MAP
        and v != UNBIND_VALUE,
    )


def filter_convars(convars, prefix):
    return filter_dict(convars, lambda k, v: k.startswith(prefix))


def filter_crosshair_convars(convars):
    return filter_convars(convars, CROSSHAIR_PREFIX)


def filter_mouse_convars(convars):
    return filter_dict(convars, lambda k, v: k in MOUSE_SETTINGS)


def filter_radar_convars(convars):
    return filter_dict(
        convars, lambda k, v: any(k.startswith(prefix) for prefix in RADAR_PREFIXES)
    )


def filter_viewmodel_convars(convars):
    return filter_convars(convars, VIEWMODEL_PREFIX)


def filter_damage_prediction_convars(convars):
    return filter_convars(convars, DAMAGE_PREDICTION_PREFIX)


def filter_sound_convars(convars):
    return filter_dict(
        convars, lambda k, v: any(k.startswith(prefix) for prefix in SOUND_PREFIXES)
    )


def filter_mute_convars(convars):
    return filter_dict(convars, lambda k, v: k in MUTE_SETTINGS)


def filter_grenade_crosshair_convars(convars):
    return filter_convars(convars, GRENADE_CROSSHAIR_PREFIX)


def filter_background_convars(convars):
    return filter_dict(
        convars,
        lambda k, v: any(k.startswith(base_key) for base_key in BACKGROUND_SETTINGS),
    )


def filter_hud_convars(convars):
    return filter_dict(
        convars, lambda k, v: any(k.startswith(base_key) for base_key in HUD_SETTINGS)
    )


def filter_telemetry_convars(convars):
    return filter_convars(convars, TELEMETRY_PREFIX)


def filter_other_convars(convars, used_keys):
    return filter_dict(convars, lambda k, v: k not in used_keys)


def combine_other_settings(convars):
    used_keys = set()
    filters = [
        filter_crosshair_convars,
        filter_grenade_crosshair_convars,
        filter_mouse_convars,
        filter_radar_convars,
        filter_viewmodel_convars,
        filter_sound_convars,
        filter_hud_convars,
        filter_damage_prediction_convars,
        filter_mute_convars,
        filter_background_convars,
        filter_telemetry_convars,
    ]
    for filter_func in filters:
        used_keys.update(filter_func(convars).keys())
    return used_keys
