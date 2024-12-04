from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QFrame, QLabel, QPushButton

class LayoutManager:
    @staticmethod
    def create_layout(app):

        # Folder selection section
        app.folder_label = QLabel("Select a folder to manage files:")
        app.select_folder_button = QPushButton("01 Select Folder")
        app.select_folder_button.clicked.connect(app.select_folder)
        app.folder_path_label = QLabel('') # Text field for folder path
        app.folder_path_label.setFrameStyle(QFrame.Panel | QFrame.Sunken)  # For better appearance

        # Folder selection layout
        folder_title_layout = QHBoxLayout()
        folder_title_layout.addWidget(app.folder_label)
        folder_layout = QHBoxLayout()
        folder_layout.addWidget(app.select_folder_button)
        folder_layout.addWidget(app.folder_path_label)
        folder_layout.setContentsMargins(10, 10, 10, 10)  # Add padding
        folder_layout.setSpacing(10)  # Space between widgets

        # Renaming section
        app.rename_button = QPushButton("01 Rename Files")
        app.rename_button.clicked.connect(app.rename_files)

        app.ai_rename_button = QPushButton("02 AI Rename Files")
        app.ai_rename_button.clicked.connect(app.ai_rename_files)

        app.revert_button = QPushButton("03 Revert Changes")
        app.revert_button.clicked.connect(app.revert_changes)

         # Horizontal layout for renaming buttons
        rename_layout = QHBoxLayout()
        rename_layout.addWidget(app.rename_button)
        rename_layout.addWidget(app.ai_rename_button)
        rename_layout.addWidget(app.revert_button)
        rename_layout.setSpacing(20)  # Space between buttons

        # Organizing section
        app.store_structure_button = QPushButton("01 Store File Structure")
        app.store_structure_button.clicked.connect(app.store_file_structure)

        app.suggest_folders_button = QPushButton("02 Suggest Folders")
        app.suggest_folders_button.clicked.connect(app.suggest_top_folders)

        # Horizontal layout for organizing buttons
        organizing_layout = QHBoxLayout()
        organizing_layout.addWidget(app.store_structure_button)
        organizing_layout.addWidget(app.suggest_folders_button)
        organizing_layout.setSpacing(20)  # Space between buttons
      
         # Main layout
        main_layout = QVBoxLayout()
        main_layout.addLayout(folder_title_layout)  # Add folder selection section
        main_layout.addSpacing(20)  # Add some space between sections
        main_layout.addLayout(folder_layout)  # Add folder selection section
        main_layout.addSpacing(20)  # Add some space between sections
        main_layout.addLayout(rename_layout)  # Add renaming section
        main_layout.addSpacing(20)  # Add some space between sections
        main_layout.addLayout(organizing_layout)  # Add renaming section
        main_layout.setContentsMargins(20, 20, 20, 20)  # Add padding around the entire layout

        # Set the layout to the window
        app.setLayout(main_layout)
        app.setWindowTitle("File Management App")
        app.resize(400, 200)

        app.folder_path = ""
        app.renamed_files = {}
        app.file_structure = app.load_file_structure()