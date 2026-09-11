# ==============================================================================
# エイリアス (Aliases) - 画面の見た目をスッキリさせたいもの
# ==============================================================================

# --- ls 系 (展開させず画面をきれいに保つ) ---
alias ls="ls -v -F --group-directories-first --color=auto"
alias l="ls"
alias ll="ls -tl"
alias lll="ls -l"
alias la="ls -a"
alias lla="ls -la"
alias lt="ls -t"
alias llt="ls -tl"

# --- コマンド拡張・上書き ---
alias mv="mv -v"
alias cp="cp -vr"
alias vi="nvim"
alias vim="nvim"


# --- 長い Git Log 系 ---
alias gl="git log --graph --decorate --name-status --color --date=format:'[%m/%d %H:%M]' --pretty=format:'%C(auto)%h %C(green)%ad%Creset %C(auto)%d %s'"
alias gll="git log -p"
alias gdl="git log --oneline --graph --decorate --diff-filter=D --summary"


# ==============================================================================
# 略称設定 (Abbreviations) - 展開して引数を付け足すもの
# ==============================================================================

# --- 基本操作 ---
abbr -a c     "cd"
abbr -a :q    "exit"
abbr -a q     "exit"

# --- ネットワーク / ツール ---
abbr -a scp   "scp -rp"
abbr -a rsync "rsync -avzuh"
abbr -a r     "ranger"

# --- パッケージマネージャ / 言語 ---
abbr -a pac   "sudo pacman"
abbr -a pip   "python3 -m pip"
abbr -a python "python3"

# --- Git 操作 ---
abbr -a ga    "git add"
abbr -a gu    "git add -u"
abbr -a gall  "git add -A"

abbr -a gc    "git checkout"
abbr -a gch   "git checkout HEAD ."
abbr -a gcma  "git commit --amend"

abbr -a gs    "git status"
abbr -a gd    "git diff"
abbr -a gdd   "git diff --cached"
abbr -a gm    "git mv"

abbr -a gp    "git push"
abbr -a gpl   "git pull --rebase"

# ==============================================================================
# 削除コマンド設定（trash-cli / rip があれば優先使用）
# ==============================================================================

if type -q rip
    ## sudo pacman -S rip2
    # 1. rip が存在する場合
    alias rm="rip"
    abbr -a undo "rip -u"

else if type -q trash-put
    # 2. trash-cli が存在する場合
    alias rm="trash-put"
    abbr -a tp "trash-put"
    abbr -a tl "trash-list"
    abbr -a tr "trash-restore"
    abbr -a te "trash-empty"

else
    # 3. どちらも存在しない場合（標準 rm に安全オプションを付与）
    alias rm="rm -iv"
end


# ==============================================================================
# カスタム関数 (Functions)
# ==============================================================================

# 引数を結合してコミット
function gcm --description 'git commit -m "$argv"'
    test (count $argv) -gt 0; and git commit -m "$argv"; or echo "エラー: コミットメッセージが必要です"
end

# 複数の圧縮ファイルをまとめて展開
function unars --description 'unar for multiple files'
    test (count $argv) -gt 0; and for f in $argv; unar $f; end; or echo "エラー: ファイルを指定してください"
end
