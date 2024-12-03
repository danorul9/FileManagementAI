import os

def load_file_structure():
    structure = []
    with open("File_structure.txt", 'r') as f:
        for line in f:
            if line.strip() and not line.startswith("#"):
                structure.append(line.strip())
    return structure

def format_filename(filename):
    # Convert to title case and remove underscores and hyphens
    formatted_name = filename.replace('_', ' ').replace('-', ' ')
    return formatted_name.title()
