import os

GRENADE_SLOT_MAP = {
    "slot6": "HE Grenade",
    "slot7": "Flash",
    "slot8": "Smoke",
    "slot9": "Decoy",
    "slot10": "Molotov"
}

MOVEMENT_ACTIONS = {
    "+jump",
    "+left",
    "+right",
    "+forward",
    "+back",
    "+duck",
    "+sprint"
}

MOUSE_SETTINGS = {
    "sensitivity",
    "zoom_sensitivity_ratio",
    "m_yaw",
    "m_pitch",
    "mouse_inverty"
}

HUD_SETTINGS = {
    "cl_hud_color",
    "cl_showfps",
    "cl_deathnotices_show_numbers",
    "cl_teamid_overhead_colors_show",
    "cl_hide_avatar_images",
    "cl_teamid_overhead_mode"
}

MUTE_SETTINGS = {
    "cl_mute_all_but_friends_and_party",
    "cl_mute_enemy_team",
    "cl_player_ping_mute",
    "cl_sanitize_muted_players",
    "voice_modenable_toggle"
}

BACKGROUND_SETTINGS = {
    "ui_mainmenu_bkgnd_movie_9CA40421",
    "ui_vanitysetting_team",
    "ui_vanitysetting_loadoutslot_ct"
}

CROSSHAIR_PREFIX = "cl_crosshair"
GRENADE_CROSSHAIR_PREFIX = "cl_grenadecrosshair"
RADAR_PREFIXES = ["cl_radar_", "cl_hud_radar_", "cl_teammate_colors_show"]
VIEWMODEL_PREFIX = "viewmodel_"
DAMAGE_PREDICTION_PREFIX = "cl_predict_"
SOUND_PREFIXES = ["snd_", "volume"]
TELEMETRY_PREFIX = "cl_hud_telemetry_"
DEMO_PREFIX = "demo_"
UNBIND_VALUE = "<unbound>"

STEAMID_LOOKUP = "https://steamid.io/lookup/"
STEAM_USERDATA_PATH = r"C:\Program Files (x86)\Steam\userdata"
STEAM_BASE_PATH_TEMPLATE = r"C:\Program Files (x86)\Steam\userdata\{my_id}\730"
VCFG_FILES_TEMPLATE = [
    os.path.join(STEAM_BASE_PATH_TEMPLATE, "local", "cfg", "cs2_user_keys_0_slot0.vcfg"),
    os.path.join(STEAM_BASE_PATH_TEMPLATE, "remote", "cs2_user_keys.vcfg"),
]
CONVAR_FILES_TEMPLATE = [
    os.path.join(STEAM_BASE_PATH_TEMPLATE, "local", "cfg", "cs2_machine_convars.vcfg"),
    os.path.join(STEAM_BASE_PATH_TEMPLATE, "remote", "cs2_user_convars.vcfg"),
]
