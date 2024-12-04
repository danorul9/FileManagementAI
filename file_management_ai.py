import os
from PySide6.QtWidgets import QApplication, QMessageBox, QFileDialog, QVBoxLayout, QHBoxLayout, QFrame, QWidget, QLabel, QPushButton
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM
# mmodules
from theme_manager import ThemeManager
from layout_manager import LayoutManager

class FileManagementAiApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("File Management AI")
        # Apply theme on initialization
        ThemeManager.set_theme() 
        # Initialize the UI layout
        self.init_ui()    
        
    def init_ui(self):
        """Set up the user interface layout."""
        self.setLayout(LayoutManager.create_layout(self))

    def load_file_structure(self):
        structure = []
        with open("File_structure.txt", 'r') as f:
            for line in f:
                if line.strip() and not line.startswith("#"):
                    structure.append(line.strip())
        return structure

    def select_folder(self):
        self.folder_path = QFileDialog.getExistingDirectory(self, "Select Folder")
        if not self.folder_path:
            QMessageBox.warning(self, "Warning", "No folder selected!")
        else:
            self.folder_path_label.setText(self.folder_path)
            self.folder_path = self.folder_path.replace("\\", "/")  # Convert to Unix-style path

    def rename_files(self):
        if not self.folder_path:
            QMessageBox.warning(self, "Warning", "Please select a folder first!")
            return

        for filename in os.listdir(self.folder_path):
            original_path = os.path.join(self.folder_path, filename)
            if os.path.isfile(original_path):
                new_name = self.format_filename(filename)
                new_path = os.path.join(self.folder_path, new_name)
                os.rename(original_path, new_path)
                self.renamed_files[original_path] = new_path
    

    def ai_rename_files(self):
        if not self.folder_path:
            QMessageBox.warning(self, "Warning", "Please select a folder first!")
            return
    
        # Batch 10 files renames for langchain ollam callo to be implemented later
    
    def store_file_structure(self):
        directory = r"D:\00 Files"
        output_file = "file_structure.txt"
        
        with open(output_file, 'w') as f:
            for root, dirs, files in os.walk(directory):
                # Limit to 2 levels deep
                level = root.replace(directory, '').count(os.sep)
                if level == 1:  # Store Level 2 folders only
                    for name in dirs:  # Only write directories
                        f.write(os.path.join(root, name) + '\n')
        
        QMessageBox.information(self, "Success", f"File structure saved to {output_file}")

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
    app = QApplication([]) 
    window = FileManagementAiApp()
    window.show()
    app.exec()
