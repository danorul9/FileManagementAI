from PySide6.QtGui import QPalette
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication

class ThemeManager:
    """Handles theming for the application."""

    @staticmethod
    def apply_dark_theme():
        """Apply a dark theme to the application."""
        palette = QPalette()
        palette.setColor(QPalette.Window, Qt.black)
        palette.setColor(QPalette.WindowText, Qt.white)
        palette.setColor(QPalette.Base, Qt.black)
        palette.setColor(QPalette.AlternateBase, Qt.gray)
        palette.setColor(QPalette.Text, Qt.white)
        palette.setColor(QPalette.Button, Qt.gray)
        palette.setColor(QPalette.ButtonText, Qt.white)
        palette.setColor(QPalette.Highlight, Qt.blue)
        palette.setColor(QPalette.HighlightedText, Qt.black)
        QApplication.instance().setPalette(palette)

    @staticmethod
    def apply_light_theme():
        """Apply a light theme to the application."""
        palette = QPalette()
        palette.setColor(QPalette.Window, Qt.white)
        palette.setColor(QPalette.WindowText, Qt.black)
        palette.setColor(QPalette.Base, Qt.white)
        palette.setColor(QPalette.AlternateBase, Qt.lightGray)
        palette.setColor(QPalette.Text, Qt.black)
        palette.setColor(QPalette.Button, Qt.lightGray)
        palette.setColor(QPalette.ButtonText, Qt.black)
        palette.setColor(QPalette.Highlight, Qt.blue)
        palette.setColor(QPalette.HighlightedText, Qt.white)
        QApplication.instance().setPalette(palette)

    @staticmethod
    def set_theme():
        """Detect system theme and apply the appropriate theme."""
        try:
            import ctypes
            user32 = ctypes.windll.user32
            if user32.GetSysColor(0) == 0:  # 0 is the color for the background
                ThemeManager.apply_light_theme()
            else:
                ThemeManager.apply_dark_theme()

        except Exception as e:
            print(f"Error detecting theme, applying default light theme: {e}")
            ThemeManager.apply_light_theme()
