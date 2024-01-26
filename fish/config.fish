function fish_greeting
  clear
  neofetch | lolcat
end

# Path variable
set -x PATH $HOME/.local/bin $PATH
set -x PATH $HOME/.cargo/bin $PATH

# Aliases
alias ls="exa -a -l -h --group-directories-first"
alias cat="bat"
alias pacman="sudo pacman"

# Check if SSH agent is already runningeval $(ssh-agent -c) > /dev/null
eval $(ssh-agent -c) > /dev/null

function load_ssh_keys
    for keyfile in ~/.ssh/*.pub
        set private_key (string replace -r '\.pub$' '' $keyfile)
        if test -f $private_key
            ssh-add $private_key 2> /dev/null
        end
    end
end

load_ssh_keys

# Function to load keys
starship init fish | source
