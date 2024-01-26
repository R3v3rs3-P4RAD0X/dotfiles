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

# Ensure packages | change this to have the script auto install the packages required
ensure_packages = False

# Create a class for the files
class Linker:
    """
    A class that represents a linker for creating symbolic links from a source directory to a destination directory.
    """

    def __init__(self):
        self.files = []
        self.walk(os.getcwd())

    def walk(self, directory):
        """
        Recursively walks through the given directory and its subdirectories to find files.

        Args:
            directory (str): The directory to start the walk from.
        """
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
        """
        Runs the linker by creating symbolic links for the files in the `files` list.
        """
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

    def ensure_packages(self) -> None:
        """
        Ensures that the required packages are installed.
        """
        # If the user is using Arch Linux, install the packages using pacman
        if os.path.exists("/etc/arch-release"):
            os.system("sudo pacman -S --needed - < packages.txt")

        # If the user is using Ubuntu, install the packages using apt
        elif os.path.exists("/etc/debian_version"):
            os.system("sudo apt install -y $(cat packages.txt)")

        # If the user is using Fedora, install the packages using dnf
        elif os.path.exists("/etc/fedora-release"):
            os.system("sudo dnf install -y $(cat packages.txt)")

        # If the user is using macOS, install the packages using brew
        elif os.path.exists("/usr/local/bin/brew"):
            os.system("brew install $(cat packages.txt)")

        # If the user is using Windows, install the packages using chocolatey
        elif os.path.exists("C:/ProgramData/chocolatey/bin/choco.exe"):
            os.system("choco install $(cat packages.txt)")
        

if __name__ == "__main__":
    linker = Linker()
    linker.run()

    if ensure_packages:
        linker.ensure_packages()    
