# Dotfiles

This repo will hold all my dotfiles from across my different operating systems/machines.


## How to automatically link the dotfiles

Running the python script does the following:

- Creates backups of files if user wants
- Write old links into a txt file inside of the .dotfiles/links.txt file
- Links dotfiles from .dotfiles into .config


Usage:

```bash
python setup.py
```