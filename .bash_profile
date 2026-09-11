## ~/.bash_profileに以下を追記
if [[ -z $DISPLAY ]] && [[ $(tty) = /dev/tty1 ]] && command -v sway &>/dev/null; then
    exec sway
fi
