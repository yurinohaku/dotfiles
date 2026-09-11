#!/usr/bin/bash

SCRIPT_DIR=$(cd $(dirname $0) && pwd)
FISH_DIR=$HOME/.config/fish

mkdir -p $FISH_DIR
cp -v $SCRIPT_DIR/config.fish $FISH_DIR
cp -v $SCRIPT_DIR/alias.fish $FISH_DIR

# ファイルが存在しない場合のみコピー（存在する場合は上書きせず無視）
cp -v -n $SCRIPT_DIR/custom.fish $FISH_DIR
