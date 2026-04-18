from PyQt6.QtCore import Qt, QSettings
from PyQt6.QtWidgets import  QWidget, QLabel, QLineEdit, QApplication, QPushButton

class SettingsWindow(QWidget):
  def __init__(self, parent=None):
    super().__init__(parent, Qt.WindowType.Window)
    self.setWindowTitle("Settings")
    self.setFixedSize(480, 270)
    self.settings = QSettings("Mellarii", "ParentControl")
    
    self.parentLabel = QLabel("Parent: ", self)
    self.parentLabel.move(15, 15)
    self.parentName = QLineEdit(self)
    self.parentName.setPlaceholderText(" Name ")
    self.parentName.move(57, 10)
    self.parentName.resize(120, 30)

    self.childLabel = QLabel("Child: ", self)
    self.childLabel.move(15, 39)
    self.childName = QLineEdit(self)
    self.childName.setPlaceholderText(" Name ")
    self.childName.move(57, 34)
    self.childName.resize(120, 30)

    self.parentName.setText(self.settings.value("parent_name", ""))
    self.childName.setText(self.settings.value("child_name", ""))

    self.pinkTheme_btn = QPushButton("Pink Theme", self)
    self.pinkTheme_btn.move(15, 69)
    self.pinkTheme_btn.clicked.connect(lambda: self.apply_theme("pink"))
    self.whiteTheme_btn = QPushButton("White Theme", self)
    self.whiteTheme_btn.move(15, 99)
    self.whiteTheme_btn.clicked.connect(lambda: self.apply_theme("white"))
    self.whiteTheme_btn = QPushButton("Dark Theme", self)
    self.whiteTheme_btn.move(15, 129)
    self.whiteTheme_btn.clicked.connect(lambda: self.apply_theme("default"))

  def closeEvent(self, event):
    self.settings.setValue("parent_name", self.parentName.text())
    self.settings.setValue("child_name", self.childName.text())
    super().closeEvent(event)

  def apply_theme(self, theme_name: str):
    app = QApplication.instance()

    if (not app):
      return

    if theme_name == "pink":
      pink_qss = """
      QWidget {
        background-color: #e86bc1;
        color: #ffffff;
      } 
      QLineEdit, QPushButton {
        background: #c761a8;
        border-color: #b34791;
        border-style: solid;
        border-width: 2px;
        border-radius: 6px;
        padding: 5px;
      }
      QPushButton:hover {
        background-color: #91467b;
      }
      QLabel {
        color: #ffffff;
      }
      """
      app.setStyleSheet(pink_qss)
    elif theme_name == "white": 
      white_qss = """
      QWidget {
        background-color: #ffffff;
        color: #000000;
      } 
      QLineEdit, QPushButton {
        background: #f0f0f0;
        border-color: #c7c7c7;
        border-style: solid;
        border-width: 2px;
        border-radius: 6px;
        padding: 5px;
      }
      QPushButton:hover {
        background-color: #ababab ;
      }
      QLabel {
        color: #000000;
      }
      """
      app.setStyleSheet(white_qss)
    elif theme_name == "default":
      app.setStyleSheet("")
      self.settings.setValue("theme", "default")
      return