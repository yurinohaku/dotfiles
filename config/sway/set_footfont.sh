#!/usr/bin/env bash

FONT_CONFIG=$(cat <<'EOF'
font=Droid Sans Mono:size=13
letter-spacing=0.5
EOF
)

mkdir -p ~/.config/foot
echo "$FONT_CONFIG" > ~/.config/foot/foot.ini
