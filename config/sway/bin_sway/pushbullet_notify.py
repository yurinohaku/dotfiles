#!/usr/bin/env python3
## sudo pacman -S python-websocket-client libnotify

import pathlib
import json
import subprocess
from websocket import WebSocketApp

## API_KEY
script_dir = pathlib.Path(__file__).resolve().parent
with open(script_dir/'pushbullet.key') as f:
    API_KEY = f.read().rstrip()

def notify(title, body):
    subprocess.run([
        "notify-send",
        title,
        body
    ])

def on_message(ws, message):
    data = json.loads(message)

    if data.get("type") != "tickle":
        return

    if data.get("subtype") != "push":
        return

    # 最新push取得
    import urllib.request

    req = urllib.request.Request(
        "https://api.pushbullet.com/v2/pushes?limit=1",
        headers={"Access-Token": API_KEY}
    )

    with urllib.request.urlopen(req) as res:
        pushes = json.loads(res.read())

    push = pushes["pushes"][0]

    title = push.get("title", "Pushbullet")
    body = push.get("body", "")

    notify(title, body)

ws = WebSocketApp(
    f"wss://stream.pushbullet.com/websocket/{API_KEY}",
    on_message=on_message
)

ws.run_forever()
