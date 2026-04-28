from PyQt6.QtCore import Qt, QSettings
from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QVBoxLayout, QHBoxLayout, QTabWidget
from PyQt6.QtGui import QFont

class StateWindow(QWidget):
  def __init__(self, parent=None):
    super().__init__(parent, Qt.WindowType.Window)
    self.setWindowTitle("Statistics")
    self.setFixedSize(700, 500)
    self.settings = QSettings("Mellarii", "ParentControl")
    self.tracker = None  # Will be set by main_window
    
    # Create tab widget
    self.tabs = QTabWidget(self)
    self.tabs.setGeometry(10, 10, 680, 480)
    
    # Tab 1: Time Limit
    self.limit_tab = QWidget()
    self.tabs.addTab(self.limit_tab, "Time Limit")
    
    self.timeLimitLabel = QLabel("Time limit (minutes):", self.limit_tab)
    self.timeLimitLabel.move(15, 15)
    
    self.timeLimit = QLineEdit(self.limit_tab)
    self.timeLimit.setPlaceholderText("Enter time limit (minutes)")
    self.timeLimit.move(15, 40)
    self.timeLimit.resize(200, 30)

    self.UsingTimeText = QLabel("Today you used: ", self.limit_tab)
    self.UsingTimeText.move(15, 85)

    self.timeLimit.setText(self.settings.value("time_limit", ""))
    
    # Tab 2: Site Statistics
    self.stats_tab = QWidget()
    self.tabs.addTab(self.stats_tab, "Site Statistics")
    
    stats_layout = QVBoxLayout(self.stats_tab)
    stats_layout.setContentsMargins(10, 10, 10, 10)
    
    # Header
    header_label = QLabel("Time spent on each site:")
    header_font = QFont()
    header_font.setBold(True)
    header_label.setFont(header_font)
    stats_layout.addWidget(header_label)
    
    # Table
    self.stats_table = QTableWidget(self.stats_tab)
    self.stats_table.setColumnCount(3)
    self.stats_table.setHorizontalHeaderLabels(["Site", "Time", "Visits"])
    self.stats_table.setColumnWidth(0, 300)
    self.stats_table.setColumnWidth(1, 150)
    self.stats_table.setColumnWidth(2, 100)
    stats_layout.addWidget(self.stats_table)
    
    # Buttons layout
    buttons_layout = QHBoxLayout()
    
    self.refresh_btn = QPushButton("Refresh", self.stats_tab)
    self.refresh_btn.clicked.connect(self.refresh_stats)
    buttons_layout.addWidget(self.refresh_btn)
    
    self.clear_stats_btn = QPushButton("Clear Statistics", self.stats_tab)
    self.clear_stats_btn.clicked.connect(self.clear_statistics)
    buttons_layout.addWidget(self.clear_stats_btn)
    
    buttons_layout.addStretch()
    stats_layout.addLayout(buttons_layout)

  def getLimit(self):
    try:
      if self.timeLimit.text():
        return int(self.timeLimit.text()) 
      else: 
        return 0
    except ValueError:
      return 0

  def set_tracker(self, tracker):
    """Set the window tracker instance"""
    self.tracker = tracker
    self.refresh_stats()
  
  def refresh_stats(self):
    """Refresh statistics table"""
    if not self.tracker:
      return
    
    stats = self.tracker.get_sorted_stats()
    self.stats_table.setRowCount(len(stats))
    
    for row, (domain, data) in enumerate(stats):
      # Site name
      site_item = QTableWidgetItem(domain)
      self.stats_table.setItem(row, 0, site_item)
      
      # Time spent (formatted)
      time_str = self.tracker.format_time(data["total_seconds"])
      time_item = QTableWidgetItem(time_str)
      self.stats_table.setItem(row, 1, time_item)
      
      # Visits count
      visits_item = QTableWidgetItem(str(data["visits"]))
      self.stats_table.setItem(row, 2, visits_item)
  
  def clear_statistics(self):
    """Clear all statistics"""
    if self.tracker:
      self.tracker.clear_stats()
      self.refresh_stats()
  
  def closeEvent(self, event):
    self.settings.setValue("time_limit", self.timeLimit.text())
    super().closeEvent(event)