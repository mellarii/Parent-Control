import os
import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
from parent_control.main_window import ParentControlApp


def _get_resource_path(relative_path):
    if getattr(sys, 'frozen', False):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.dirname(__file__), relative_path)


def main():
    app = QApplication(sys.argv)
    icon_path = _get_resource_path(os.path.join("resources", "icon.ico"))
    app.setWindowIcon(QIcon(icon_path))
    window = ParentControlApp()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
