import os
import tkinter
from tkinter import messagebox, filedialog
from tkinter import ttk
import sv_ttk
from file_renamer_logic import rename_files
from folder_suggestion import suggest_top_folders
from folder_suggestion_utils import suggest_folders, display_suggestions  # Import the new utility functions

class FileRenamerApp:
    def __init__(self, master):
        self.master = master
        master.title("File Renamer")
        self.set_theme()

        self.label = ttk.Label(master, text="Select a folder to rename files:")
        self.label.pack(pady=10)

        self.select_button = ttk.Button(master, text="Select Folder", command=self.select_folder)
        self.select_button.pack(pady=5)

        self.selected_folder_label = ttk.Label(master, text="No folder selected")
        self.selected_folder_label.pack(pady=5)

        self.rename_button = ttk.Button(master, text="Rename Files", command=self.rename_files)
        self.rename_button.pack(pady=5)

        self.suggest_folders_button = ttk.Button(master, text="Suggest Folders", command=self.suggest_folders)
        self.suggest_folders_button.pack(pady=5)

        self.store_structure_button = ttk.Button(master, text="Store File Structure", command=self.store_file_structure)
        self.store_structure_button.pack(pady=5)

        self.revert_button = ttk.Button(master, text="Revert Changes", command=self.revert_changes)
        self.revert_button.pack(pady=5)

        self.folder_path = self.load_last_selected_folder()  # Load last selected folder
        self.renamed_files = {}
        self.file_structure = self.load_file_structure()

        if self.folder_path:
            self.selected_folder_label.config(text=self.folder_path)  # Update label with loaded folder

    def set_theme(self):
        # Set the dark theme using sv_ttk
        sv_ttk.set_theme("dark")

    def load_file_structure(self):
        structure = []
        with open("File_structure.txt", 'r') as f:
            for line in f:
                if line.strip() and not line.startswith("#"):
                    structure.append(line.strip())
        return structure

    def load_last_selected_folder(self):
        try:
            with open("last_selected_folder.txt", 'r') as f:
                return f.read().strip()
        except FileNotFoundError:
            return None

    def select_folder(self):
        self.folder_path = filedialog.askdirectory()
        if not self.folder_path:
            messagebox.showwarning("Warning", "No folder selected!")
        else:
            self.selected_folder_label.config(text=self.folder_path)  # Update label with selected folder
            with open("last_selected_folder.txt", 'w') as f:
                f.write(self.folder_path)  # Save the last selected folder

    def rename_files(self):
        self.renamed_files = rename_files(self.folder_path, self.load_file_structure, self.format_filename, suggest_top_folders)

    def suggest_folders(self):
        if not self.folder_path:
            messagebox.showwarning("Warning", "Please select a folder first!")
            return
        
        # Iterate through each file in the selected folder
        for filename in os.listdir(self.folder_path):
            file_path = os.path.join(self.folder_path, filename)
            if os.path.isfile(file_path):  # Check if it's a file
                suggestions = suggest_folders(file_path)  # Get suggestions for the current file
                display_suggestions(suggestions, self.master, file_path)  # Display suggestions for the current file

    def store_file_structure(self):
        directory = r"D:\00 Files"
        output_file = "file_structure.txt"
        
        with open(output_file, 'w') as f:
            for root, dirs, files in os.walk(directory):
                # Limit to 2 levels deep
                level = root.replace(directory, '').count(os.sep)
                if level < 3:  # Allow all directories up to 2 levels deep
                    for name in dirs:  # Only write directories
                        f.write(os.path.join(root, name) + '\n')
        
        messagebox.showinfo("Success", f"File structure saved to {output_file}")

    def revert_changes(self):
        for original, new in self.renamed_files.items():
            os.rename(new, original)
        self.renamed_files.clear()
        
if __name__ == "__main__":
    root = tkinter.Tk()
    app = FileRenamerApp(root)
    root.mainloop()
