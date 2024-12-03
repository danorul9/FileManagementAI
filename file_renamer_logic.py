import os
import re
from tkinter import messagebox

def rename_files(folder_path, load_file_structure, format_filename, suggest_top_folders):
    renamed_files = {}
    if not folder_path:
        messagebox.showwarning("Warning", "Please select a folder first!")
        return renamed_files

    for filename in os.listdir(folder_path):
        original_path = os.path.join(folder_path, filename)
        if os.path.isfile(original_path):
            new_name = format_filename(filename)
            new_path = os.path.join(folder_path, new_name)
            os.rename(original_path, new_path)
            renamed_files[original_path] = new_path

    return renamed_files

def format_filename(filename):
    # Convert to title case, remove underscores and hyphens, and remove multiple spaces
    formatted_name = filename.replace('_', ' ').replace('-', ' ')
    formatted_name = re.sub(r'\s+', ' ', formatted_name).strip()  # Remove multiple spaces
    
    # Title case with exceptions for specific words
    words = formatted_name.split()
    for i in range(len(words)):
        if words[i].lower() in {"to", "and", "of", "in", "the", "a", "an", "for"} and i != 0:
            words[i] = words[i].lower()
        else:
            words[i] = words[i].capitalize()
    
    return ' '.join(words)
