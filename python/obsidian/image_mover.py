from email.mime import text
import re
import shutil
from time import sleep
from typing import List, Union, Iterable, Dict
from pathlib import Path


root_folder = r"C:\MainTechnicalVault_test"
single_note = r"C:\MainTechnicalVault_test\IntelliPaat\1Live SessionCopy.md"
# root_folder: str = r"E:\Capgemini\Capgemini\MainTechnicalVault"
# single_note: str = r"E:\Capgemini\Capgemini\MainTechnicalVault\IntelliPaat\1 Live Session.md"

def list_all_markdown_files(root_folder: Union[str, Path], single_note: Union[str, Path]) -> List[Path]:
    # Recursively find all .md files under the given root directory.
    #execludes the single note
    root_folder = Path(root_folder).expanduser().resolve() #path normalization
    single_note_path = Path(single_note).expanduser().resolve()

    if not root_folder.exists():
        raise FileNotFoundError(f"Root path does not exist: {root_folder}")
    if not root_folder.is_dir():
        raise NotADirectoryError(f"Root path is not a directory: {root_folder}")
    print("------------------------------------------------")
    print(f"Root folder: {root_folder}")
    #md_files = [*root_folder.rglob("*.md")]
    md_files: List[Path] = list(root_folder.rglob("*.md"))
    #md_files = [f for f in md_files if f != single_note_path] #list comprehension to exclude single note, ensure is file
    md_files = [f for f in md_files if f.is_file() and f != single_note_path]
    #print(md_files)
    #print("Listing all markdown files...")
    print(f"Total markdown files found: {len(md_files)}")
   
    return md_files

def list_all_images(root_folder: Union[str, Path]) -> List[Path]:
    # Recursively find all image files under the given root directory.
    root_folder = Path(root_folder).expanduser().resolve() #path normalization

    image_extensions = [".png", ".jpeg", ".jpg", ".gif", ".bmp", ".tiff", ".svg"]

    image_files: list[Path] = [
        p
        for ext in image_extensions
        for p in root_folder.rglob(f"*{ext}")
        if p.is_file()
    ]
    print(f"Total image files found: {len(image_files)}")
    return image_files

def exract_images_referenced_in_file(single_note_path: str) -> set[str]:
    # Extracts a list of unique .png filenames
    # from Obsidian-style Markdown image links in the file.
    # need to udpate to use .jpeg as well
    single_note_path = Path(single_note_path).expanduser().resolve() #normalization

    # DYNAMIC APPROACH TO CREATE PATTERN
    #image_extensions = [".png", ".jpeg", ".jpg", ".gif", ".bmp", ".tiff", ".svg"]
    #ext_pattern = "|".join([re.escape(ext) for ext in image_extensions]) #e.g \.png|\.jpeg|\.jpg|\.gif|\.bmp|\.tiff|\.sv
    #pattern = rf"[\w\s\-_]+({ext_pattern})"

    #pattern = r"[\w\s\-_]+\.png|jpeg|jpg|gif|bmp|tiff|svg" #update to create dynamically
    pattern = r"[\w\s\-_]+\.(?:png|jpe?g|gif|bmp|tiff|svg)"
    
    with open(single_note_path, 'r', encoding='utf-8') as file:
        note_content = file.read()
        matches: set = set(re.findall(pattern, note_content)) #we dont have duplicates
        #print(f"Found {len(matches)} unique image references in {single_note_path.name}")
    
    cleaned = { # make sure to strip whitespace, was getting \n\ntest.jpg
            match.strip() 
            for match in matches 
            if match.strip()          # skip empty strings or pure whitespace
        }

    return cleaned

def extract_all_image_references(all_mardown_files: List[Path]) -> set[str]:
    # extracts all image references from all markdown files given
    all_images = set()
    for file_path in all_mardown_files: #seems like1_Live_Session.md
        images_extraced: set[str] = exract_images_referenced_in_file(file_path) #This causes the error, seems like1_Live_Session.md
        all_images.update(images_extraced)
        #print(f"Extracting images from {file_path.name}...")
        #print(file_path) #type path)

    print(f"Total unique images found across all notes: {len(all_images)}")
    print("------------------------------------------------")
    return all_images

def check_png_references(note_pngs: set[str], all_notes_pngs: set[str]) -> set[str]:
    # compares pngs from the note to all other notes
    # retunrs the once only referenced in the note
    safe_to_move = set()
    no_move = set()

    for png in note_pngs:
        #print("Checking PNG reference:", png)
        if png not in all_notes_pngs:
            print(f"No other references: {png}")
            safe_to_move.add(png)
        else:
            print(f"Found: {png} in other notes. <----")
            no_move.add(png)
    print("------------------------------------------------")
    print(f"Total images safe to move: {len(safe_to_move)}")
    print(safe_to_move)
    print("------------------------------------------------")
    #print(f"Total images NOT to move: {len(no_move)}")
    #print(no_move)
    return safe_to_move

def create_destination(single_note: str) -> Path:
    #creates a folder nameed after the notename
    #accepts folder path
    #retunrns the new path
    print("Creating destination folder...")
    single_note: Path = Path(single_note).expanduser().resolve() #path normalization
    folder_name = single_note.stem #get the name without extension
    #print(single_note)
    #print(single_note.name.replace(" ", "_"))
    #print(single_note.parent)
    
    default_folder = single_note.stem.replace(" ", "_") #filename
    user_input = input(f"Enter folder name [{default_folder}]: ").strip()
    folder_name = user_input if user_input else default_folder

    # Build the full target path
    target_folder = single_note.parent / folder_name
    print(f"Target folder path: {target_folder}")

    # Create the folder (safe: won't error if already exists)
    try:
        target_folder.mkdir(parents=True, exist_ok=True)
        print(f"Folder created (or already exists): {target_folder}")
        print(f"Full absolute path: {target_folder.resolve()}")
    except Exception as e:
        print(f"Error creating folder: {e}")
    print(target_folder)
    return target_folder

def move_png_files(pngs_to_move: set[str], root_folder: Union[str, Path], new_destination: Path, all_images: List[Path], single_note_path: str):
    #gets the paths of the pngs to move
    #moves the png to the folder
    #accepts folder path
    root_folder: Path = Path(root_folder).expanduser().resolve() #path normalization
    paths_to_move: List[Path] = []

    for img in all_images:
        if img.name in pngs_to_move:
            paths_to_move.append(img)
            print(img)
    
    paths_to_move.append(Path(single_note_path)) # we also want to move the note itself
    destination = Path(new_destination).expanduser().resolve()
    destination.mkdir(parents=True, exist_ok=True)
    
    for src in paths_to_move:
        dest = destination / src.name
        shutil.move(src, dest)
        
def main():
    all_mardown_files: List[Path] = list_all_markdown_files(root_folder, single_note) #done
    #for file_path in all_mardown_files: #seems like1_Live_Session.md
    #    print(file_path) #type path)
    single_note_images: set[str] = exract_images_referenced_in_file(single_note)
    all_note_images: set[str] = extract_all_image_references(all_mardown_files)
    pngs_to_move: set[str] = check_png_references(single_note_images, all_note_images)
    new_destination: Path = create_destination(single_note)
    all_images: List[Path] = list_all_images(root_folder)
    move_png_files(pngs_to_move, root_folder, new_destination, all_images, single_note)
    
main()

