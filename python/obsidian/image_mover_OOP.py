import re
import shutil
from pathlib import Path
from typing import List, Set, Union

class Vault:
    def __init__(self, root_folder: Union[str, Path]):
        self.root = Path(root_folder).expanduser().resolve()
        if not self.root.is_dir():
            raise NotADirectoryError(f"Root folder does not exist: {self.root}")

    def list_markdown_files(self, exclude: Path | None = None) -> List[Path]:
        """List all markdown files under the root folder, optionally excluding one file."""
        md_files = [p for p in self.root.rglob("*.md") if p.is_file()]
        if exclude:
            exclude = exclude.resolve()
            md_files = [p for p in md_files if p != exclude]
        print(f"Total markdown files found: {len(md_files)}")
        return md_files

    def list_images(self) -> List[Path]:
        """List all images under the root folder."""
        image_extensions = {".png", ".jpeg", ".jpg", ".gif", ".bmp", ".tiff", ".svg"}
        image_files = [
            p for p in self.root.rglob("*")
            if p.is_file() and p.suffix.lower() in image_extensions
        ]
        print(f"Total image files found: {len(image_files)}")
        return image_files

class ImageMover:
    def __init__(self, all_images: list[Path]):
        self.image_lookup = {img.name: img for img in all_images}
    
    def create_destination(self, note_name: str, parent: Path) -> Path:
        """Create a folder for moving images."""
        default_folder = note_name.replace(" ", "_")
        user_input = input(f"Enter folder name [{default_folder}]: ").strip()
        folder_name = user_input or default_folder

        target_folder = parent / folder_name
        target_folder.mkdir(parents=True, exist_ok=True)
        return target_folder

    def find_safe_images(
        self,
        note_images: set[str],
        other_images: set[str]
    ) -> set[str]:
        return {img for img in note_images if img not in other_images}

    def move(self, files: list[Path], destination: Path):
        for src in files:
            dest = destination / src.name
            shutil.move(src, dest)

class Note:
    IMAGE_PATTERN = re.compile(
        r"[\w\s\-_]+\.(?:png|jpe?g|gif|bmp|tiff|svg)",
        re.IGNORECASE
    )

    def __init__(self, path: Union[str, Path]):
        self.path = Path(path).expanduser().resolve()
        if not self.path.is_file():
            raise FileNotFoundError(f"Note file not found: {self.path}")

    def extract_images(self) -> Set[str]:
        """Extract all unique image names referenced in the markdown note."""
        content = self.path.read_text(encoding="utf-8")
        matches = self.IMAGE_PATTERN.findall(content)
        cleaned = {m.strip() for m in matches if m.strip()}
        print(f"Found {len(cleaned)} unique images in {self.path.name}")
        return cleaned
    

def main():
    # Configure vault and note
    root_folder = r"C:\MainTechnicalVault_test"
    single_note_path = r"C:\MainTechnicalVault_test\IntelliPaat\1Live SessionCopy.md"

    vault: Vault = Vault(root_folder)
    note: Note = Note(single_note_path)

    # List files
    markdown_files: List[Path] = vault.list_markdown_files(exclude=note.path)
    all_images: List[Path] = vault.list_images()

    # Extract images
    note_images: set[str] = note.extract_images()
    other_images = set()
    for md_file in markdown_files:
        other_images.update(Note(md_file).extract_images())

    # Determine safe images
    mover: ImageMover = ImageMover(all_images)
    safe_images: set[str] = mover.find_safe_images(note_images, other_images)

    # Create destination folder
    destination = mover.create_destination(note.path.stem, note.path.parent)

    # Collect paths to move
    paths_to_move = [
        mover.image_lookup[name]
        for name in safe_images
        if name in mover.image_lookup
    ]
    paths_to_move.append(note.path)  # include the note itself

    # Move files
    mover.move(paths_to_move, destination)
    print("All files moved successfully.")


if __name__ == "__main__":
    main()


