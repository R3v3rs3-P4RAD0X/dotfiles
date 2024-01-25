# Aliases
alias ls="exa -a -l -h --group-directories-first"
alias cat="bat"
alias pacman="sudo pacman"

# Check if SSH agent is already running
if not set -q SSH_AGENT_PID
    eval (ssh-agent -c)
    set -x SSH_AUTH_SOCK $HOME/.ssh/agent.sock
    set -x SSH_AGENT_PID $SSH_AGENT_PID
end

function load_ssh_keys
    for keyfile in ~/.ssh/*.pub
        set private_key (string replace -r '\.pub$' '' $keyfile)
        if test -f $private_key
            ssh-add $private_key
        end
    end
end

load_ssh_keys


# Function to load keys
starship init fish | source
