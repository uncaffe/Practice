"""
This program is a more eye-firendly alternative to the os.walk() method.
It uses recursion to list all files inside each subfolder,
regardless of nesting level, starting from an initial folder.
Works on Windows.
"""

import os

def scanner(startdir, indent=" "):
    entries = os.scandir(startdir)
    files = []
    subdirectories = []

    for item in entries:
        if item.is_dir():
            subdirectories.append(item)
        else:
            files.append(item)

    result = [f"{indent}{os.path.basename(startdir)}:"]

    for file_item in files:
        result.append(f"{indent}  {os.path.basename(file_item)}")

    for dir_item in subdirectories:
        result.extend(scanner(dir_item.path, indent + "  "))

    return result
