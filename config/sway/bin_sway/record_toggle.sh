#!/bin/bash

# wf-recorder存在確認
if ! command -v wf-recorder >/dev/null 2>&1; then
    echo "wf-recorder not installed"
    exit 1
fi

PIDFILE=/tmp/wf-recorder.pid
OUTDIR=~/Videos
mkdir -p $OUTDIR

if [ -f "$PIDFILE" ]; then
    kill "$(cat "$PIDFILE")"
    rm "$PIDFILE"
    notify-send "動画を保存しました"
else
    notify-send -t 1000 "録画を開始します"
    sleep 1

    FILE="$OUTDIR/rec_$(date +%Y%m%d_%H%M%S).mp4"
    wf-recorder --audio -f "$FILE" &
    echo $! > "$PIDFILE"
fi
