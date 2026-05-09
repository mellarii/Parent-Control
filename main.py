import sys

from PyQt6.QtWidgets import QApplication
from main_window import ParentControlApp

def main():
  app = QApplication(sys.argv)
  window = ParentControlApp()
  window.show()
  sys.exit(app.exec())
  app.setWindowIcon(QIcon("icon.ico"))

if __name__ == "__main__":
    main()