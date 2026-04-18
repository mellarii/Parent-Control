from PyQt6.QtCore import Qt, QSettings
from PyQt6.QtWidgets import  QWidget, QLabel, QLineEdit, QPushButton

class StateWindow(QWidget):
  def __init__(self, parent=None):
    super().__init__(parent, Qt.WindowType.Window)
    self.setWindowTitle("Statistics")
    self.setFixedSize(480, 270)
    self.settings = QSettings("Mellarii", "ParentControl")
    
    self.timeLimit = QLineEdit(self)
    self.timeLimit.setPlaceholderText("Enter time limit (minutes)")
    self.timeLimit.move(15, 15)
    
    self.UsingTimeText = QLabel("Today you use: ", self)
    self.UsingTimeText.move(15, 55)

    self.timeLimit.setText(self.settings.value("time_limit", ""))

  def getLimit(self):
    try:
      if self.timeLimit.text():
        return int(self.timeLimit.text()) 
      else: 
        return 0
    except ValueError:
      return 0

  def closeEvent(self, event):
    self.settings.setValue("time_limit", self.timeLimit.text())
    super().closeEvent(event)