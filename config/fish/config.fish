## ~/.config/fish/config.fish
# ==============================================================================
# 基本設定 & エイリアス読み込み
# ==============================================================================

# Greeting（起動時のウェルカムメッセージ）を非表示にする
set -g fish_greeting

# ~/.bin が存在する場合のみ PATH に追加
test -d $HOME/.bin; and fish_add_path $HOME/.bin

# エイリアスファイルの読み込み
test -f ~/.config/fish/alias.fish; and source ~/.config/fish/alias.fish

# ==============================================================================
# カラー設定
# ==============================================================================

# 1. デフォルトカラーの設定
set -g prompt_color '#90D7EC' # スカイブルー（デフォルト）

# 2. custom.fish が存在すれば読み込んで上書きする
test -f ~/.config/fish/custom.fish; and source ~/.config/fish/custom.fish


# ==============================================================================
# Git プロンプト表示設定
# ==============================================================================

# 各種ステータスの表示を有効化
set -g __fish_git_prompt_showdirtystate 'yes'
set -g __fish_git_prompt_showstashstate 'yes'
set -g __fish_git_prompt_showuntrackedfiles 'yes'
set -g __fish_git_prompt_showupstream 'yes'

# プロンプト内のカラー設定
set -g __fish_git_prompt_color_branch yellow
set -g __fish_git_prompt_color_upstream_ahead green
set -g __fish_git_prompt_color_upstream_behind red

# ステータスを表す記号（お好みの文字や絵文字に変更可能）
set -g __fish_git_prompt_char_dirtystate '*Dirt'        # 未コミットの変更あり
set -g __fish_git_prompt_char_stagedstate '+Added'        # ステージ済み
set -g __fish_git_prompt_char_untrackedfiles '?Untrack'     # 未追跡ファイルあり
set -g __fish_git_prompt_char_stashstate '$Stash'         # スタッシュあり
set -g __fish_git_prompt_char_upstream_ahead ' >Commited+'    # リモートより先行
set -g __fish_git_prompt_char_upstream_behind ' <Commited-'   # リモートより遅れ


# ==============================================================================
# プロンプト関数定義
# ==============================================================================

function fish_prompt --description 'シンプルなプロンプト表示設定'
    # カレントディレクトリの表示形式を設定（フルパスにする場合は 'no'）
    set -q fish_prompt_pwd_dir_length; or set -g fish_prompt_pwd_dir_length 1

    # root ユーザーの場合
    if test "$USER" = "root" -o "$USER" = "toor"
        echo -n -s (set_color red) "$USER" @ (prompt_hostname) ' ' (prompt_pwd)
        echo ''
        echo (set_color normal) '# '
        return
    end

    # 一般ユーザーの場合
    # 1行目: [ユーザー名@ホスト名:ディレクトリ] (Gitステータス)
    echo -n -s (set_color $prompt_color) '[' "$USER" @ (prompt_hostname) ':' (prompt_pwd) ']' (__fish_git_prompt)
    echo ''
    # 2行目: 入力プロンプト記号
    echo (set_color normal) '$ '
end

# ==============================================================================
# 外部ツール連携
# ==============================================================================

# zoxide がインストールされている場合のみ初期化
## sudo pacman -S zoxide
type -q zoxide; and zoxide init fish | source
