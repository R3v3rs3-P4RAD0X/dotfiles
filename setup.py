import os
import shutil

# Ignore files and directories
ignore = [".git", ".gitignore", "setup.py", "README.md"]

# The user's home directory
home = os.path.expanduser("~")

# The backup directory
backup = os.path.join(home, ".dotfiles/backup")

# Config directory
config = os.path.join(home, ".config")

# Create a class for the files
class Linker:
    def __init__(self):
        self.files = []
        self.walk(os.getcwd())

    def walk(self, directory):
        if directory in ignore:
            return
        
        for file in os.listdir(directory):
            if file in ignore:
                continue

            path = os.path.join(directory, file)

            if os.path.isdir(path):
                self.walk(path)

            else:
                self.files.append({
                    "source": path,
                    "output": path.replace(".dotfiles/", "")
                })

    def run(self):
        for file in self.files:
            src, dst = file["source"], file["output"]

            if os.path.exists(dst):
                # Check if the file is a symlink
                if os.path.islink(dst):
                    # Get the link source and link destination
                    link_src = os.readlink(dst)
                    
                    # If the link source is the same as the source, continue
                    if link_src == src:
                        continue

                    # If the link source is not the same as the source, append it into ~/.config/.dotfiles/links.txt
                    else:
                        with open(os.path.join(home, ".dotfiles/links.txt"), "a") as file:
                            file.write(f"{src} -> {link_src}\n")

                # If the file is not a symlink, move it to the backup directory
                else:
                    if not os.path.exists(backup):
                        os.makedirs(backup)

                    # Ask the user if they want to backup the file
                    answer = input(f"Backup {dst}? [Y/n] ") or "Y"

                    if answer.lower() == "y":
                        shutil.move(dst, os.path.join(backup, os.path.basename(dst)))
            
            # Get the file name
            file_name = os.path.basename(dst)

            # Remove the file name from the path
            dst = dst.replace("/" + file_name, "")

            # Remove everything from the beginning of the path until the .config/ directory
            dst = dst.replace(home + "/", "").replace(".config", "")

            # Subdirectories
            subdirectories = [d for d in dst.split("/") if len(d) > 0]

            # Create the subdirectories if > 0
            if len(subdirectories) > 0:
                for subdirectory in subdirectories:
                    if not os.path.exists(os.path.join(config, subdirectory)):
                        os.makedirs(os.path.join(config, subdirectory))

                        print(f"Created {os.path.join(config, subdirectory)}")
                    
            # Create the symlink from the file
            os.symlink(file["source"], file["output"])

            # Print the output
            print(f"Linked {file['source']} to {file['output']}")


if __name__ == "__main__":
    linker = Linker()
    linker.run()