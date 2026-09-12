#!/usr/bin/env python3
import json
import subprocess

def swaymsg(cmd):
    return json.loads(subprocess.check_output(["swaymsg", "-t", cmd]))

# OUTPUT取得
outputs = swaymsg("get_outputs")
output = None

for o in outputs:
    if o.get("active") and o["name"].startswith("eDP"):
        output = o
        break

if not output:
    for o in outputs:
        if o.get("active"):
            output = o
            break

OUTPUT = output["name"]
CURRENT = output["transform"]

# TOUCH取得（identifier優先）
inputs = swaymsg("get_inputs")
touch = None
for i in inputs:
    if i.get("type") == "touch":
        touch = i.get("identifier") or i.get("name")
        break

# トグル
if CURRENT == "normal":
    subprocess.run(["swaymsg", "output", OUTPUT, "transform", "180"])
    if touch:
        subprocess.run([
            "swaymsg", "input", touch,
            "calibration_matrix", "--", "-1", "0", "1", "0", "-1", "1"
        ])
else:
    subprocess.run(["swaymsg", "output", OUTPUT, "transform", "normal"])
    if touch:
        subprocess.run([
            "swaymsg", "input", touch,
            "calibration_matrix", "--", "1", "0", "0", "0", "1", "0"
        ])
