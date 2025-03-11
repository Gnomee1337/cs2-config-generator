from constants import *


def filter_movement_bindings(bindings):
    return {k: v for k, v in bindings.items() if v in MOVEMENT_ACTIONS}


def filter_grenade_bindings(bindings):
    grenade_slots = set(GRENADE_SLOT_MAP.keys())
    return {k: v for k, v in bindings.items() if v in grenade_slots}


def filter_demo_bindings(bindings: dict) -> dict:
    return {k: v for k, v in bindings.items() if v.startswith(DEMO_PREFIX)}


def filter_unbind_bindings(bindings: dict) -> list:
    unbinds = []
    for key, action in bindings.items():
        if action.strip().lower() == UNBIND_VALUE:
            unbinds.append(f'unbind "{key.lower()}"')
    return unbinds


def filter_other_bindings(bindings):
    other_bindings = {}
    for key, action in bindings.items():
        if action in MOVEMENT_ACTIONS or action in GRENADE_SLOT_MAP:
            continue
        elif action != UNBIND_VALUE:
            other_bindings[key] = action
    return other_bindings


def filter_crosshair_convars(convars: dict) -> dict:
    return {k: v for k, v in convars.items() if k.startswith(CROSSHAIR_PREFIX)}


def filter_mouse_convars(convars: dict) -> dict:
    return {k: v for k, v in convars.items() if k in MOUSE_SETTINGS}


def filter_radar_convars(convars: dict) -> dict:
    radar_keys = {}
    for key, value in convars.items():
        if any(key.startswith(prefix) for prefix in RADAR_PREFIXES):
            radar_keys[key] = value
    return radar_keys


def filter_viewmodel_convars(convars: dict) -> dict:
    return {k: v for k, v in convars.items() if k.startswith(VIEWMODEL_PREFIX)}


def filter_damage_prediction_convars(convars: dict) -> dict:
    return {k: v for k, v in convars.items() if k.startswith(DAMAGE_PREDICTION_PREFIX)}


def filter_sound_convars(convars: dict) -> dict:
    return {k: v for k, v in convars.items() if any(k.startswith(prefix) for prefix in SOUND_PREFIXES)}


def filter_mute_convars(convars: dict) -> dict:
    return {k: v for k, v in convars.items() if k in MUTE_SETTINGS}


def filter_grenade_crosshair_convars(convars: dict) -> dict:
    return {k: v for k, v in convars.items() if k.startswith(GRENADE_CROSSHAIR_PREFIX)}


def filter_background_convars(convars: dict) -> dict:
    result = {}
    for base_key in BACKGROUND_SETTINGS:
        for key, value in convars.items():
            if key.startswith(base_key):
                result[base_key] = value
    return result


def filter_hud_convars(convars: dict) -> dict:
    result = {}
    for base_key in HUD_SETTINGS:
        for key, value in convars.items():
            if key.startswith(base_key):
                result[base_key] = value
    return result


def filter_telemetry_convars(convars: dict) -> dict:
    return {k: v for k, v in convars.items() if k.startswith(TELEMETRY_PREFIX)}


def filter_other_convars(convars: dict, used_keys: set) -> dict:
    return {k: v for k, v in convars.items() if k not in used_keys}


def combine_other_settings(convars: dict):
    used_keys = set()
    used_keys.update(filter_crosshair_convars(convars).keys())
    used_keys.update(filter_grenade_crosshair_convars(convars).keys())
    used_keys.update(filter_mouse_convars(convars).keys())
    used_keys.update(filter_radar_convars(convars).keys())
    used_keys.update(filter_viewmodel_convars(convars).keys())
    used_keys.update(filter_sound_convars(convars).keys())
    used_keys.update(filter_hud_convars(convars).keys())
    used_keys.update(filter_damage_prediction_convars(convars).keys())
    used_keys.update(filter_mute_convars(convars).keys())
    used_keys.update(filter_background_convars(convars).keys())
    used_keys.update(filter_telemetry_convars(convars).keys())
    return used_keys
