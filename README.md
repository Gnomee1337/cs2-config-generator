# CS2 Config Generator
### 🛠️ Automatically generate a clean `autoexec.cfg` file for CS2 - like it used to be in CS:GO.
<img src="https://i.imgur.com/muVWuSd.jpeg"/>

## 📦 Download:
Release: [Version 1.1](https://github.com/Gnomee1337/cs2-config-generator/releases/tag/v1.1)

## 📖 Description
CS2 Config Generator is a Python-based GUI application that helps users generate `autoexec.cfg` files for CS2.

In **CS:GO**, you could easily generate your game configuration file using a simple command in the console: `host_writeconfig <config_name>`

But in **CS2**, things got a bit more complicated. Your CS2 configuration files are now split into multiple `.vcfg` files stored in this kind of structure:
```
"C:\Program Files (x86)\Steam\userdata\{your_id}\730\local\cfg\":
    cs2_machine_convars.vcfg
    cs2_user_convars_0_slot0.vcfg
    cs2_user_convars_0_slot0.vcfg_lastclouded
    cs2_user_keys_0_slot0.vcfg
    cs2_user_keys_0_slot0.vcfg_lastclouded
    cs2_user_keys_0_slot1.vcfg
    cs2_user_keys_0_slot2.vcfg
    cs2_user_keys_0_slot3.vcfg
    cs2_video.txt
    cs2_video.txt.bak
```
These `.vcfg` files use a **JSON-like nested format**, for example:
```
"config"
{
    "bindings"
    {
        "a"     "+left"
        "d"     "+right"
        "s"     "+back"
        "w"     "+forward"
    }
}
```
Unfortunately, this JSON structure **cannot be directly used** in `autoexec.cfg`, which is the traditional and convenient way of keeping your config **organized** and **portable**.

## ✅ Purpose of This Project
This program solves that problem by:
* Automatically parsing all relevant `.vcfg` files.
* Extracting and converting all user settings and bindings.
* Generating a clean and structured `autoexec.cfg` file - fully compatible with CS2.

The final `autoexec.cfg` output looks like this, in the **classic CS:GO format**, which CS2 still supports:
```
// Movement Keys
bind "a" "+left"
bind "d" "+right"
bind "w" "+forward"
bind "s" "+back"

// Binds
bind "mouse3" "toggle cl_crosshairthickness 1.5 1 0"
bind "mouse4" "toggle cl_crosshaircolor 2 4 5 0"

// Crosshair
cl_crosshairalpha 255
cl_crosshairgap -7

// Mouse
sensitivity 0.74
zoom_sensitivity_ratio 0.8
hud_showtargetid 1
m_yaw 0.022000
m_pitch 0.022000

.....

```

## 🧩 Requirements
- Python 3.12

## ▶️ Usage
1. Run the `.exe` application (or use Python if you prefer).
2. Use the **GUI Interface** to:
    * Select your Steam ID folder
    * Enter your desired output config name
    * Choose a path where the config file should be saved
3. Click the **"Generate autoexec.cfg"**.
4. The program will generate a clean autoexec.cfg file.
5. Copy it to your CS2 config folder: `C:\Program Files (x86)\Steam\steamapps\common\Counter-Strike Global Offensive\game\csgo\cfg`
7. (Optional) Add `+exec autoexec.cfg` to your CS2 launch options in Steam.

## ⚙️ Installation (For Source Code Usage)
If you'd rather run it from source code:
1. Clone the repository:
    ```sh
    git clone https://github.com/Gnomee1337/cs2-config-generator.git
    cd cs2-config-generator
    ```
2. Install the required dependencies:
    ```sh
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    ```
3. Run application:
    ```sh
    python main.py
    ```

## 📎 Resources
- https://totalcsgo.com/commands
- https://pastebin.com/raw/EdudskLc (EliGE config structure as template)
