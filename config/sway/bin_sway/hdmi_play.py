#!/usr/bin/env python3
import os
import signal
import subprocess
import cv2
import pygame

# --- 設定パラメータ ---
# 1. 映像デバイス番号 (/dev/videoX のインデックス番号)
#    確認用コマンド: v4l2-ctl --list-devices
VIDEO_DEVICE = 0

# 2. 音声ソース名 (PipeWire / PulseAudio の入力ノード名)
#    確認用コマンド: pw-cli list-objects Node | grep -E "node.name|media.class"
#                  または wpctl status / pactl list sources short
AUDIO_SRC = "alsa_input.usb-MACROSILICON_UGREEN_15390_82370521-02.analog-stereo"

# 3. 再生パフォーマンス設定
LATENCY_SETTING = "128/48000"  # PipeWire 超低遅延設定 (128サンプル ≒ 約2.6ms)
DEFAULT_VOLUME = 0.6  # 初期音量 (0.6 = 60%)

# --- 1. PipeWire 超低遅延音声ループバック (C言語レベル処理) の起動 ---
pw_cmd = (
    f'PIPEWIRE_LATENCY="{LATENCY_SETTING}" pw-loopback '
    f'--capture-props=\'node.name="{AUDIO_SRC}"\''
)

audio_process = subprocess.Popen(pw_cmd, shell=True, preexec_fn=os.setsid)
pw_pid = str(audio_process.pid)
print(f"[Audio] PipeWire 低遅延ループバック起動 (PID: {pw_pid})")

# 単体プロセスの音量を初期化
volume = DEFAULT_VOLUME
is_muted = False
subprocess.run(["wpctl", "set-volume", "-p", pw_pid, str(volume)])

# --- 2. OpenCV 映像キャプチャの初期化 ---
cap = cv2.VideoCapture(VIDEO_DEVICE, cv2.CAP_V4L2)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
cap.set(cv2.CAP_PROP_FPS, 60)
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))

# --- 3. Pygame 画面描画の初期化 ---
pygame.init()
win_w, win_h = 1280, 720
screen = pygame.display.set_mode((win_w, win_h), pygame.RESIZABLE)
pygame.display.set_caption("HDMI Capture")
clock = pygame.time.Clock()

print("\n[操作方法]")
print("  9       : 音量ダウン (-5%)")
print("  0       : 音量アップ (+5%)")
print("  m       : ミュート / 解除")
print("  f       : フルスクリーン切り替え")
print("  q / ESC : 終了\n")

is_fullscreen = False
run_flag = True

# --- 4. メインループ ---
try:
  while run_flag and cap.isOpened():
    # イベント処理
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        run_flag = False

      elif event.type == pygame.VIDEORESIZE and not is_fullscreen:
        win_w, win_h = event.w, event.h
        screen = pygame.display.set_mode((win_w, win_h), pygame.RESIZABLE)

      elif event.type == pygame.KEYDOWN:
        if event.key in (pygame.K_q, pygame.K_ESCAPE):
          run_flag = False

        elif event.key == pygame.K_9:  # 音量ダウン
          volume = max(0.0, volume - 0.05)
          subprocess.run(
              ["wpctl", "set-volume", "-p", pw_pid, f"{volume:.2f}"]
          )
          print(f"音量: {int(volume * 100)}%")

        elif event.key == pygame.K_0:  # 音量アップ
          volume = min(1.5, volume + 0.05)
          subprocess.run(
              ["wpctl", "set-volume", "-p", pw_pid, f"{volume:.2f}"]
          )
          print(f"音量: {int(volume * 100)}%")

        elif event.key == pygame.K_m:  # ミュート切り替え
          is_muted = not is_muted
          subprocess.run(["wpctl", "set-mute", "-p", pw_pid, "toggle"])
          print("ミュート:" + (" ON" if is_muted else " OFF"))

        elif event.key == pygame.K_f:  # フルスクリーン
          is_fullscreen = not is_fullscreen
          display_mode = (
              pygame.FULLSCREEN if is_fullscreen else pygame.RESIZABLE
          )
          display_size = (0, 0) if is_fullscreen else (win_w, win_h)
          screen = pygame.display.set_mode(display_size, display_mode)

    # 映像フレーム取得
    ret, frame = cap.read()
    if not ret:
      print("[Error] 映像フレームを取得できませんでした")
      break

    # 色空間変換 (BGR -> RGB)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img_h, img_w, _ = frame_rgb.shape
    cur_w, cur_h = screen.get_size()

    # アスペクト比を維持したスケーリング計算
    scale = min(cur_w / img_w, cur_h / img_h)
    new_w, new_h = int(img_w * scale), int(img_h * scale)

    frame_resized = cv2.resize(
        frame_rgb, (new_w, new_h), interpolation=cv2.INTER_NEAREST
    )
    surface = pygame.surfarray.make_surface(frame_resized.swapaxes(0, 1))

    # 背景黒塗り & 中央配置描画
    screen.fill((0, 0, 0))
    pos_x = (cur_w - new_w) // 2
    pos_y = (cur_h - new_h) // 2
    screen.blit(surface, (pos_x, pos_y))

    pygame.display.flip()
    clock.tick(60)

finally:
  # リソースの解放（PipeWireループバックプロセスを確実にシャットダウン）
  if audio_process:
    os.killpg(os.getpgid(audio_process.pid), signal.SIGTERM)
    print("[Audio] 音声プロセスを終了しました")

  cap.release()
  pygame.quit()
  print("[System] 正常終了しました")
