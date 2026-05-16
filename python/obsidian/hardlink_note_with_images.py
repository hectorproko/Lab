

from hardlink_creator2 import * # to create hard links
from image_mover_OOP import Note # to extract image references from markdown notes
import os

def to_camel_case(filename: str) -> str:
    """Convert filename (no extension) to camelCase."""
    name = os.path.splitext(filename)[0]
    words = name.split()
    return words[0].lower() + "".join(w.capitalize() for w in words[1:])

def main():
    print("Hello, World!")

    target_files = FileSelector.ask_files("Select files to hard-link")
    if not target_files:
        print("No files selected. Exiting.")
        return

    destination = FileSelector.ask_destination("Select destination folder")
    if not destination:
        print("No destination selected. Exiting.")
        return

    for note in target_files: 
        note_obj = Note(note)
        images = note_obj.extract_images()
        print(f"Note: {note}")
        note_base_dir = os.path.dirname(note)
        image_list = [img for img in images if img.endswith(".png")] # cleaning, images is a set containing garbage strings mixed in
        #print(f"The images: {images}")
        # assumes the image is in the same directory as the note
        image_paths = [os.path.join(note_base_dir, img) for img in image_list] 
        all_paths = image_paths + [note]
        all_paths = [p for p in all_paths if "\n" not in p] # further cleaning, similar issue as above
        
        if images:
            folder_name = to_camel_case(os.path.basename(note))
            note_destination = os.path.join(destination, folder_name)
            os.makedirs(note_destination, exist_ok=True)
        else:
            note_destination = destination

        creator = HardLinkCreator(note_destination)
        results = creator.link_many(all_paths)

        success = sum(results.values())
        print(f"\nDone: {success}/{len(results)} hard links created.")



if __name__ == "__main__":
    main()