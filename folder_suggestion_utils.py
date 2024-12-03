import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from folder_suggestion import suggest_top_folders
import fitz  # PyMuPDF
import shutil  # Importing shutil to move files

def suggest_folders(file_path):
    """Suggest folders based on the selected folder path."""
    if not file_path:
        raise ValueError("No folder selected!")
    suggestions = suggest_top_folders(file_path)
    return suggestions

def display_suggestions(suggestions, master, file_path):
    """Display folder suggestions in a new window."""
    suggestions_window = tk.Toplevel(master)
    suggestions_window.title("Folder Suggestions")
    suggestions_window.geometry("1600x1200")

    filename_components = file_path.split(os.sep)
    filename_label = tk.Label(suggestions_window, text=" > ".join(filename_components))
    filename_label.pack(pady=10)

    table = ttk.Treeview(suggestions_window, columns=("Folder Name", "Confidence Percentage"), show='headings')
    table.heading("Folder Name", text="Folder Name")
    table.heading("Confidence Percentage", text="Confidence Percentage")
    table.pack(pady=10, fill=tk.BOTH, expand=True)
    table.column("Folder Name", width=600)
    table.column("Confidence Percentage", width=150)

    for folder, confidence in suggestions:
        color = get_color_from_confidence(confidence)
        tag_name = f"color_{confidence}"  # Create a unique tag based on confidence
        table.insert("", "end", values=(folder, f"{confidence}%"), tags=(tag_name,))
        table.tag_configure(tag_name, foreground=color)  # Configure the tag with the color

    # Create a frame for buttons
    button_frame = tk.Frame(suggestions_window)
    button_frame.pack(pady=10)

    # Add button to delete file
    def delete_file():
        try:
            os.remove(file_path)
            print(f"Deleted '{file_path}'")
            suggestions_window.destroy()  # Close the suggestions window
        except Exception as e:
            print(f"Error deleting file: {e}")

    delete_button = ttk.Button(button_frame, text="Delete File", command=delete_file)
    delete_button.pack(side=tk.LEFT, padx=5)

    # Add button to move file to "00 Unknown"
    def move_to_unknown_folder():
        unknown_folder = "00 Unknown"
        if not os.path.exists(unknown_folder):
            os.makedirs(unknown_folder)  # Create the folder if it doesn't exist
        try:
            destination_path = os.path.join(unknown_folder, os.path.basename(file_path))
            shutil.move(file_path, destination_path)
            print(f"Moved '{file_path}' to '{destination_path}'")
            suggestions_window.destroy()  # Close the suggestions window
        except Exception as e:
            print(f"Error moving file: {e}")

    move_button = ttk.Button(button_frame, text="Move to '00 Unknown'", command=move_to_unknown_folder)
    move_button.pack(side=tk.LEFT, padx=5)

    preview_label = tk.Label(suggestions_window, text="File Preview:")
    preview_label.pack(pady=10)

    # Check if the file is a valid image or PDF before attempting to open
    if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
        try:
            with Image.open(file_path) as img:
                img.thumbnail((800, 800))  # Increased thumbnail size
                photo = ImageTk.PhotoImage(img)
                preview = tk.Label(suggestions_window, image=photo)
                preview.image = photo
                preview.pack()
        except (FileNotFoundError, IOError, Image.UnidentifiedImageError, AttributeError) as e:
            print(f"Error opening image: {e}")
    elif file_path.lower().endswith('.pdf'):
        try:
            with fitz.open(file_path) as doc:
                page = doc[0]
                pix = page.get_pixmap()
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                img.thumbnail((800, 800))  # Increased thumbnail size
                photo = ImageTk.PhotoImage(img)
                preview = tk.Label(suggestions_window, image=photo)
                preview.image = photo
                preview.pack()
        except (FileNotFoundError, IOError, fitz.EmptyFileError, IndexError) as e:
            print(f"Error opening PDF: {e}")
            preview_text = tk.Text(suggestions_window, height=20, width=100)
            preview_text.pack(pady=10, fill=tk.BOTH, expand=True)
            preview_text.insert(tk.END, "Could not preview PDF.")
            preview_text.config(state=tk.DISABLED)
    else:
        preview_text = tk.Text(suggestions_window, height=20, width=100)
        preview_text.pack(pady=10, fill=tk.BOTH, expand=True)
        preview_text.insert(tk.END, "File type not supported for preview.")
        preview_text.config(state=tk.DISABLED)

    selected_folder = None
    def on_double_click(event):
        nonlocal selected_folder
        item = table.selection()[0]
        selected_folder = table.item(item)['values'][0]
        suggestions_window.destroy()

        # Move the file to the clicked folder
        try:
            destination_path = os.path.join(selected_folder, os.path.basename(file_path))
            if not os.path.exists(selected_folder):
                os.makedirs(selected_folder)  # Create the folder if it doesn't exist
            shutil.move(file_path, destination_path)
            print(f"Moved '{file_path}' to '{destination_path}'")
        except Exception as e:
            print(f"Error moving file: {e}")

    table.bind("<Double-1>", on_double_click)

    suggestions_window.wait_window()
    return selected_folder


def get_color_from_confidence(confidence):
    """Map confidence percentage to color."""
    if confidence >= 80:
        return "green"
    elif confidence >= 50:
        return "yellow"
    else:
        return "red"
