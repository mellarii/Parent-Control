import json
import os
import socket
import subprocess

from PyQt6.QtCore import Qt, QSettings
from PyQt6.QtWidgets import  QWidget, QLabel, QLineEdit, QPushButton, QMessageBox

class BlacklistWindow(QWidget):
  def __init__(self, parent=None):
    super().__init__(parent, Qt.WindowType.Window)
    self.setWindowTitle("Blacklist")
    self.setFixedSize(302, 124)

    self.blackFile_path = "blacklist.json"
    self.sites = self.load_data()

    self.input_field = QLineEdit(self)
    self.input_field.setPlaceholderText("Input site to add.")
    self.input_field.setGeometry(20, 20, 260, 30)

    self.watchSites_btn = QPushButton("Wathch blocked sites", self)
    self.watchSites_btn.move(20, 87)

    self.add_btn = QPushButton("Add site",self)
    self.add_btn.move(20, 57)
    self.add_btn.clicked.connect(self.add_site)

    self.delete_btn = QPushButton("Delete site",self)
    self.delete_btn.move(105, 57)
    self.delete_btn.clicked.connect(self.delete_site)

    self.clear_btn = QPushButton("Clear url's", self)
    self.clear_btn.move(190, 57)
    self.clear_btn.clicked.connect(self.clear_all)

  def load_data(self):
    if os.path.exists(self.blackFile_path):
      with open(self.blackFile_path, "r", encoding="utf-8") as f:
        return json.load(f)
    return []

  def save_data(self):
    with open(self.blackFile_path, "w", encoding="utf-8") as f:
      json.dump(self.sites, f, indent=4)

  def get_all_ips(self, domain):
    ips = set()
    try:
      for info in socket.getaddrinfo(domain, 80):
        ip = info[4][0]
        ips.add(ip)
    except socket.gaierror:
      pass
    return list(ips)

  def block_ips(self, ip, site_name):
    rule_name = f"ParentControl_Block_{site_name}_{ip.replace(':','_')}"
    cmd = f'netsh advfirewall firewall add rule name="{rule_name}" dir=out action=block remoteip={ip}'
    subprocess.run(cmd, shell=True)

  def unblock_ips(self, ip, site_name):
    rule_name = f"ParentControl_Block_{site_name}_{ip.replace(':','_')}"
    cmd = f'netsh advfirewall firewall delete rule name="{rule_name}"'
    subprocess.run(cmd, shell=True)

  def _unblock_site(self, site_name):
    rule_name = f"ParentControl_Block_{site_name}_*"
    cmd = f'netsh advfirewall firewall delete rule name="{rule_name}"'
    subprocess.run(cmd, shell=True)

  def _unblock_all_firewall_rules(self):
    cmd = f'netsh advfirewall firewall delete rule name="ParentControl_Block_*"'
    subprocess.run(cmd, shell=True)

  def add_site(self):
    url = self.input_field.text().strip().lower()
    if url:
      if url not in self.sites:
        ips = self.get_all_ips(url)
        if not ips:
          print(f"Sosi{url}")
          return
        for ip in ips:
          self.block_ips(ip,url)

        self.sites.append(url)
        self.save_data()
        self.input_field.clear()
      else:
        QMessageBox.warning(self, "Error", "This site was added earlier")

  def delete_site(self):
    url = self.input_field.text().strip().lower()
    if url in self.sites:
      ips = self.get_all_ips(url)
      for ip in ips:
        self.unblock_ips(ip,url)

      self.sites.remove(url)
      self.save_data()
      self.input_field.clear()
    else:
      QMessageBox.warning(self, "Error", "This site dont be added yet")

  def clear_all(self):
    for site in self.sites:
      ips = self.get_all_ips(site)
      for ip in ips:
        self.unblock_ips(ip,site)
    self._unblock_all_firewall_rules()
    self.sites = []
    with open(self.blackFile_path, "w", encoding="utf-8") as f:
      json.dump([], f)