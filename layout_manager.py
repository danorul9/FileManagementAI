from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QGroupBox, QLabel, QPushButton, QFrame

class LayoutManager:
    @staticmethod
    def create_layout(app):

        # Folder selection section
        app.folder_label = QLabel("Select a folder to manage files:")
        app.select_folder_button = QPushButton("01 Select Folder")
        app.select_folder_button.clicked.connect(app.select_folder)
        app.folder_path_label = QLabel('')  # Text field for folder path
        app.folder_path_label.setFrameStyle(QFrame.Panel | QFrame.Sunken)  # For better appearance

        # Folder selection layout
        folder_layout = QVBoxLayout()
        folder_layout.addWidget(app.folder_label)
        folder_controls_layout = QHBoxLayout()
        folder_controls_layout.addWidget(app.select_folder_button)
        folder_controls_layout.addWidget(app.folder_path_label)
        folder_layout.addLayout(folder_controls_layout)

        # Add a group box for folder selection
        folder_group_box = QGroupBox("01 Folder Selection")
        folder_group_box.setLayout(folder_layout)

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

        # Add a group box for renaming
        rename_group_box = QGroupBox("02 Renaming")
        rename_group_box.setLayout(rename_layout)

        # Organizing section
        app.store_structure_button = QPushButton("01 Store Folder Structure")
        app.store_structure_button.clicked.connect(app.store_file_structure)

        app.suggest_folders_button = QPushButton("02 Suggest Folders")
        app.suggest_folders_button.clicked.connect(app.suggest_top_folders)

        # Horizontal layout for organizing buttons
        organizing_layout = QHBoxLayout()
        organizing_layout.addWidget(app.store_structure_button)
        organizing_layout.addWidget(app.suggest_folders_button)

        # Add a group box for organizing
        organizing_group_box = QGroupBox("03 Organising")
        organizing_group_box.setLayout(organizing_layout)

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(folder_group_box)  # Add folder selection group
        main_layout.addWidget(rename_group_box)  # Add renaming group
        main_layout.addWidget(organizing_group_box)  # Add organizing group
        main_layout.setContentsMargins(20, 20, 20, 20)  # Add padding around the entire layout

        # Set the layout to the window
        app.setLayout(main_layout)
        app.setWindowTitle("File Management App")
        app.resize(400, 300)

        app.folder_path = ""
        app.renamed_files = {}
        app.file_structure = app.load_file_structure()
