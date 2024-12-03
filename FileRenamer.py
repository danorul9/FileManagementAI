import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM

class FileRenamerApp:
    def __init__(self, master):
        self.master = master
        master.title("File Renamer")
        self.set_theme()

        self.label = ttk.Label(master, text="Select a folder to rename files:")
        self.label.pack(pady=10)

        self.select_button = ttk.Button(master, text="Select Folder", command=self.select_folder)
        self.select_button.pack(pady=5)

        self.rename_button = ttk.Button(master, text="Rename Files", command=self.rename_files)
        self.rename_button.pack(pady=5)

        self.store_structure_button = ttk.Button(master, text="Store File Structure", command=self.store_file_structure)
        self.store_structure_button.pack(pady=5)

        self.revert_button = ttk.Button(master, text="Revert Changes", command=self.revert_changes)
        self.revert_button.pack(pady=5)

        self.folder_path = ""
        self.renamed_files = {}
        self.file_structure = self.load_file_structure()

    def set_theme(self):
        # Check system theme and set colors accordingly
        try:
            import ctypes
            user32 = ctypes.windll.user32
            if user32.GetSysColor(0) == 0:  # 0 is the color for the background
                self.master.tk_setPalette(background='white', foreground='black')
            else:
                self.master.tk_setPalette(background='black', foreground='white')
        except Exception as e:
            print(f"Error detecting theme: {e}")

    def load_file_structure(self):
        structure = []
        with open("File_structure.txt", 'r') as f:
            for line in f:
                if line.strip() and not line.startswith("#"):
                    structure.append(line.strip())
        return structure

    def select_folder(self):
        self.folder_path = filedialog.askdirectory()
        if not self.folder_path:
            messagebox.showwarning("Warning", "No folder selected!")

    def rename_files(self):
        if not self.folder_path:
            messagebox.showwarning("Warning", "Please select a folder first!")
            return

        for filename in os.listdir(self.folder_path):
            original_path = os.path.join(self.folder_path, filename)
            if os.path.isfile(original_path):
                new_name = self.format_filename(filename)
                new_path = os.path.join(self.folder_path, new_name)
                os.rename(original_path, new_path)
                self.renamed_files[original_path] = new_path

        # After renaming, suggest top folders for each renamed file
        for original_path in self.renamed_files.keys():
            original_filename = os.path.basename(original_path)
            suggestions = self.suggest_top_folders(original_filename)
            suggestion_text = "\n".join([f"{folder} - {confidence}%" for folder, confidence in suggestions])
            messagebox.showinfo("Folder Suggestions", f"Suggested Folders for '{original_filename}':\n{suggestion_text}")

    def store_file_structure(self):
        directory = r"D:\00 Files"
        output_file = "file_structure.txt"
        
        with open(output_file, 'w') as f:
            for root, dirs, files in os.walk(directory):
                # Limit to 2 levels deep
                level = root.replace(directory, '').count(os.sep)
                if level < 2:  # Change from 3 to 2
                    for name in dirs:  # Only write directories
                        f.write(os.path.join(root, name) + '\n')
        
        messagebox.showinfo("Success", f"File structure saved to {output_file}")

    def format_filename(self, filename):
        # Convert to title case and remove underscores and hyphens
        formatted_name = filename.replace('_', ' ').replace('-', ' ')
        return formatted_name.title()

    def suggest_top_folders(self, filename):
        # Use Ollama to suggest top folders based on the filename
        prompt = ChatPromptTemplate.from_template(
            "Given the filename '{filename}', suggest the top 3 folders to move it to, along with confidence percentages."
        )
        model = OllamaLLM(model="llama3.2:latest")
        chain = prompt | model
        
        response = chain.invoke({"filename": filename})
        
        # Parse the response to extract folder suggestions and confidence
        suggestions = self.parse_suggestions(response)
        return suggestions

    def parse_suggestions(self, response):
        # This function should parse the response from the model to extract folder suggestions and confidence
        # For now, let's assume the response is a list of tuples (folder, confidence)
        # Example response: "Folder1 - 90%, Folder2 - 80%, Folder3 - 70%"
        suggestions = []
        for line in response.split(','):
            folder_info = line.strip().split(' - ')
            if len(folder_info) == 2:
                folder, confidence = folder_info
                suggestions.append((folder.strip(), int(confidence.strip().replace('%', ''))))
        return suggestions[:3]  # Return top 3 suggestions

    def revert_changes(self):
        for original, new in self.renamed_files.items():
            os.rename(new, original)
        self.renamed_files.clear()

if __name__ == "__main__":
    root = tk.Tk()
    app = FileRenamerApp(root)
    root.mainloop()
