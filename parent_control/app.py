import os
import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
from parent_control.main_window import ParentControlApp


def main():
    app = QApplication(sys.argv)
    icon_path = os.path.join(os.path.dirname(__file__), "resources", "icon.ico")
    app.setWindowIcon(QIcon(icon_path))
    window = ParentControlApp()
    window.show()
    sys.exit(app.exec())
