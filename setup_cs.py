import os
from pathlib import Path

# Create the resource path text file

resources_dir_text = "Resources_Path.txt"

with open(resources_dir_text, 'a') as writer:
    pass

# Read the directory

entry_list = []

with open(resources_dir_text, 'r') as reader:
    entry_list.append(reader.read())

# Create the necessary folders

if entry_list[0]:
    resources_dir = Path(str(entry_list[0]).replace('"', ''))
    print(f"Resources Directory: {resources_dir}")

    if not resources_dir.exists():
        os.mkdir(resources_dir)
