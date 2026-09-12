#!/usr/bin/env python3

from pathlib import Path
import shutil
import subprocess

script_dir = Path(__file__).resolve().parent
config_dir = Path.home() / '.config/sway/'
config_dir.mkdir(parents=True, exist_ok=True)

subprocess.run(f"cp -vur {script_dir}/bin_sway {config_dir}", shell=True)
subprocess.run(f"cp -vur {script_dir}/config {config_dir}", shell=True)
subprocess.run("swaymsg reload", shell=True)
