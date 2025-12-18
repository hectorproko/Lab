import re
from typing import List, Union
from pathlib import Path



root = r"E:\Capgemini\Capgemini\MainTechnicalVault"
single_note = r"E:\Capgemini\Capgemini\MainTechnicalVault\IntelliPaat\1 Live Session.md"

def list_markdown_files(root: Union[str, Path]) -> List[Path]:
    """
    Recursively find all .md files under the given root directory.

    Args:
        root: The root directory path (str or Path)

    Returns:
        A sorted list of Path objects pointing to .md files.
    """
    root = Path(root).expanduser().resolve()
    if not root.exists():
        raise FileNotFoundError(f"Root path does not exist: {root}")
    if not root.is_dir():
        raise NotADirectoryError(f"Root path is not a directory: {root}")

    # rglob("*.    # rglob("*.md") is case-sensitive on some filesystems; use suffix check for safety
    md_files = [p for p in root.rglob("*") if p.is_file() and p.suffix.lower() == ".md"] #list comprehension
    #print(md_files)
    #print(type(md_files))
   
def extract_png_references(file_path: str) -> List[str]:
    """
    Extracts a list of unique .png filenames (including possible paths) 
    from Obsidian-style Markdown image links in the file.
    
    Supported formats:
    - [[any-file-name.png]]
    - ![[any-file-name.png]]
    - [[any-file-name.png|alt text]]
    - ![[any-file-name.png|thumbnail]]
    - [[folder/subfolder/image with spaces.png]]
    
    Args:
        file_path (str): Path to the text file (e.g., Markdown or Obsidian note).
    
    Returns:
        List[str]: List of unique PNG filenames/path references, in order of first appearance.
    """
    # Regex explanation:
    # (?:!\[\[|\[\[)          -> matches [[ or ![[ (non-capturing)
    # ([^\]\|]+?\.png)        -> captures the filename/path: anything except ] or |, ending with .png (lazy match)
    # (?:\|[^\]]*)?           -> optional | followed by alt text (ignored)
    # \]\]                    -> closing ]]
    pattern = re.compile(r'(?:!\[\[|\[\[)([^\]\|]+?\.png)(?:\|[^\]]*)?\]\]')
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")
    except Exception as e:
        raise IOError(f"Error reading file: {e}")
    
    # Find all matches and extract the filename group
    matches = pattern.findall(content)
    
    # Remove duplicates while preserving order
    seen = set()
    unique_filenames = []
    for filename in matches:
        filename = filename.strip()  # clean any stray spaces
        if filename not in seen:
            unique_filenames.append(filename)
            seen.add(filename)
    
    return unique_filenames




pngs = extract_png_references(single_note)
print(pngs)

files = list_markdown_files(root)
#print(files)
#for f in files:
#    print(f)
