#!/usr/bin/env python3

import subprocess
import argparse
import pathlib
import os, glob

def get_args():
    parser = argparse.ArgumentParser(description='ブックマーク管理')
    parser.add_argument('-t','--text_files',default=[],nargs='*', help='title,urlのcsv形式が基本、md形式にも対応予定。')
    return parser.parse_args()


def main():
    args = get_args()
    text_files = args.text_files

    wofi_dict = {}
    for text_file in text_files:
        wofi_dict.update(get_wofi_dict(text_file))
    title_list = list(wofi_dict.keys())

    user_input = subprocess.run(get_wofi_cmd(title_list), shell=True, capture_output=True, text=True).stdout

    if not user_input:
        print('Null')
        exit()
    elif wofi_dict.get(user_input.rstrip('\n')):
        cmd = wofi_dict.get(user_input.rstrip('\n'))
    else:
        cmd = ""
        for title in title_list:
            if user_input.rstrip('\n').lower() in title.lower():
                cmd = wofi_dict.get(title.rstrip('\n'))
                break

    if cmd.startswith('http'):
        cmd = 'xdg-open ' + cmd
    #proc = subprocess.run(cmd, shell=True)
    # バックグラウンドで独立して実行し、標準入出力を切り離す
    subprocess.Popen(
        cmd,
        shell=True,
        start_new_session=True, # 親プロセスとプロセスグループを分離
        stdout=subprocess.DEVNULL, # 出力を捨てる
        stderr=subprocess.DEVNULL  # エラー出力を捨てる
    )



def get_wofi_dict(text_file):
    text_list = []
    with open(text_file) as f:
        text_list = [s.strip() for s in f.readlines()]
        text_list = [s for s in text_list if not s.startswith('#')]
        text_list = [s for s in text_list if not s == '']

    wofi_dict = {}
    for text in text_list:
        # CSV形式: title,url
        title, cmd = text.split(',')

        # 共通のクリーンアップ
        title = name_repair(title.strip())
        wofi_dict[title] = cmd.strip()

    return wofi_dict



def get_wofi_cmd(title_list):
    ttl = '"\n"'.join(title_list)
    wofi_cmd = f'echo {ttl}| wofi --show dmenu -p wofimenu -disable-history -s ~/.config/wofi/*.css'
    return wofi_cmd



def name_repair(name):
    ## タイトルに使えない文字の排除
    for i in '\\' , '\"' , '\'' , '/' , ':' , '*' , '?' , '<' , '>' , '|' , '[' , ']' , ' ', '(', ')':
        name = name.replace(i,'_')
    while '__' in name:
        name = name.replace('__','_')
    return name
    

main()
