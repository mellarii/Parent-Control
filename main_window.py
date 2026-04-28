from PyQt6.QtCore import (Qt, QTimer)
from PyQt6.QtWidgets import  (QWidget, QLabel, QPushButton, QMessageBox)

from StateWindow import StateWindow 
from BlacklistWindow import BlacklistWindow
from SettingsWindow import SettingsWindow

class ParentControlApp(QWidget):
  def __init__(self):
    super().__init__()
    self.time_seconds = 0

    self.state_win = StateWindow(self)
    self.blacklist_win = BlacklistWindow(self)
    self.settings_win = SettingsWindow(self)

    self.init_ui()
    self.init_timer()

  def init_ui(self):
    lenght = 390 
    self.setWindowTitle("Parent Control")  
    self.resize(lenght,540)

    self.main_text = QLabel("Start protecting", self)
    self.main_text.resize(400,100)
    self.main_text.move(160, 200)

    self.timerMain = QLabel("00:00", self) 
    self.timerMain.move(0,270)
    self.timerMain.resize(400, 100)
    self.timerMain.setAlignment(Qt.AlignmentFlag.AlignCenter)

    self.start_btn = QPushButton("Start", self)
    self.start_btn.move(160, 270)
    self.settings_btn = QPushButton("Settings", self)
    self.settings_btn.move(15, 15)
    self.state_btn = QPushButton("Device activity statistics", self)
    self.state_btn.move(15, 465)
    self.blacklist_btn = QPushButton("Manage blocked sites", self)
    self.blacklist_btn.move(15, 500)

    self.start_btn.clicked.connect(self.startLogic)
    self.settings_btn.clicked.connect(self.settings_win.show)
    self.state_btn.clicked.connect(self.state_win.show)
    self.blacklist_btn.clicked.connect(self.blacklist_win.show)
    

  def init_timer(self):
    self.clock = QTimer()
    self.clock.timeout.connect(self.tick) 
        
  def tick(self):
    self.time_seconds += 1
    minutes = self.time_seconds //60
    seconds = self.time_seconds % 60
    self.timerMain.setText(f"{minutes:02}:{seconds:02}")

    limit = self.state_win.getLimit()
    if limit > 0 and minutes >= limit:
      self.clock.stop()
      QMessageBox.warning(self, "Warning", "Time limit exceeded")
    

  def startLogic(self):
    if self.clock.isActive(): 
      self.clock.stop()
      self.start_btn.setText("Resume")
    else:
      self.clock.start(1000)
      self.start_btn.setText("Running...")
