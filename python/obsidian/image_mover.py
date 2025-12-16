import re
from typing import List

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



pngs = extract_png_references(r"E:\Capgemini\Capgemini\MainTechnicalVault\IntelliPaat\1 Live Session.md")
print(pngs)
# Possible output:
# [
#   'Pasted image 20250807161258.png',
#   'thethingfromthekitche.png',
#   'diagrams/flow chart.png',
#   'screenshot.png'
# ]