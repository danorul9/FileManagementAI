import sys
from PySide6.QtWidgets import QApplication
from FileManagementAiApp import file_maangement_ai

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FileManagementAiApp()
    window.show()
    sys.exit(app.exec())
