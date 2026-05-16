import os
import subprocess
import tkinter as tk
from tkinter import filedialog


# ─────────────────────────────────────────────
# FILE SELECTOR — GUI input, reusable
# ─────────────────────────────────────────────

class FileSelector:
    """Reusable GUI dialogs for selecting files and folders."""

    @staticmethod
    def _root() -> tk.Tk:
        root = tk.Tk()
        root.withdraw()
        return root

    @staticmethod
    def ask_files(title: str = "Select files") -> list[str]:
        """Prompt the user to select one or more files.

        Returns:
            List of normalised file paths, or empty list if cancelled.
        """
        FileSelector._root()
        files = filedialog.askopenfilenames(title=title)
        return [os.path.normpath(f) for f in files]

    @staticmethod
    def ask_destination(title: str = "Select destination folder") -> str | None:
        """Prompt the user to select a destination folder.

        Returns:
            Normalised folder path, or None if cancelled.
        """
        FileSelector._root()
        folder = filedialog.askdirectory(title=title)
        return os.path.normpath(folder) if folder else None


# ─────────────────────────────────────────────
# HARD LINK CREATOR — logic, importable
# ─────────────────────────────────────────────

class HardLinkCreator:
    """Creates hard links on Windows using mklink."""

    def __init__(self, destination: str):
        """
        Args:
            destination: Directory where hard links will be created.
        """
        self.destination = os.path.normpath(destination)

    def link(self, target_file: str) -> bool:
        """Create a single hard link for target_file in self.destination.

        Args:
            target_file: Full path to the source file.

        Returns:
            True on success, False on failure.
        """
        file_name = os.path.basename(target_file)
        link_path = os.path.join(self.destination, file_name)

        try:
            command = ["cmd.exe", "/c", "mklink", "/H", link_path, target_file]
            subprocess.run(command, check=True, shell=False)
            print(f"\033[92mHard link created: {link_path}\033[0m")
            return True
        except subprocess.CalledProcessError as error:
            print(f"\033[91mFailed to create hard link: {error}\033[0m")
            return False

    def link_many(self, target_files: list[str]) -> dict[str, bool]:
        """Create hard links for multiple files into self.destination.

        Args:
            target_files: List of full file paths to link.

        Returns:
            Dict mapping each file path to True (success) or False (failure).
        """
        return {
            os.path.normpath(f): self.link(os.path.normpath(f))
            for f in target_files
        }


# ─────────────────────────────────────────────
# ENTRY POINT — runs when executed directly
# ─────────────────────────────────────────────

def main():
    target_files = FileSelector.ask_files("Select files to hard-link")
    if not target_files:
        print("No files selected. Exiting.")
        return

    destination = FileSelector.ask_destination("Select destination folder")
    if not destination:
        print("No destination selected. Exiting.")
        return

    creator = HardLinkCreator(destination)
    results = creator.link_many(target_files)

    success = sum(results.values())
    print(f"\nDone: {success}/{len(results)} hard links created.")


if __name__ == "__main__":
    main()