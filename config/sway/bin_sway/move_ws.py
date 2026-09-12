#!/usr/bin/env python3

import argparse
import json
import subprocess

BASE_WORKSPACES = [str(i) for i in range(1, 10)]  # 基本のワークスペース "1"〜"9"


def fetch_workspaces():
    """Swayからワークスペース情報（名前一覧、フォーカス中の名前）を取得する。"""
    res = subprocess.run(["swaymsg", "-t", "get_workspaces"], capture_output=True, text=True, check=True)
    workspaces = json.loads(res.stdout)

    all_names = [w["name"] for w in workspaces]
    focused_name = next((w["name"] for w in workspaces if w["focused"]), BASE_WORKSPACES[0])

    return all_names, focused_name


def build_workspace_ring(active_names):
    """1〜9を基本とし、存在するその他のワークスペースを末尾に追加した環状リストを作成する。"""
    extra_names = [name for name in active_names if name not in BASE_WORKSPACES]
    return BASE_WORKSPACES + extra_names


def calculate_next_workspace(ws_ring, current_ws, direction):
    """現在の位置と移動方向に基づき、次のワークスペース名を計算する（環状移動）。"""
    current_index = ws_ring.index(current_ws) if current_ws in ws_ring else 0
    step = 1 if direction == "right" else -1

    next_index = (current_index + step) % len(ws_ring)
    return ws_ring[next_index]


def switch_workspace(target_ws, move_container=False):
    """指定したワークスペースに移動（オプションでコンテナも移動）する。"""
    if move_container:
        subprocess.run(["swaymsg", "move", "container", "to", "workspace", target_ws], check=True)
    subprocess.run(["swaymsg", "workspace", target_ws], check=True)


def main():
    parser = argparse.ArgumentParser(description="Swayのワークスペース間をループ移動するスクリプト")
    parser.add_argument("-d", "--direction", choices=["left", "right"], required=True, help="移動方向 (left/right)")
    parser.add_argument("-m", "--move", action="store_true", help="フォーカス中のコンテナも一緒に移動させる")
    args = parser.parse_args()

    # 1. データの取得
    active_names, current_ws = fetch_workspaces()

    # 2. ワークスペースの環状リストを構築
    ws_ring = build_workspace_ring(active_names)

    # 3. 移動先の計算
    target_ws = calculate_next_workspace(ws_ring, current_ws, args.direction)

    # 4. 実行
    switch_workspace(target_ws, move_container=args.move)


if __name__ == "__main__":
    main()
