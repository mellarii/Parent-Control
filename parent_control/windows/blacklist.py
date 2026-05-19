import json
import os
import socket
import subprocess
from urllib.parse import urlparse

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QLineEdit, QPushButton, QMessageBox


DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data")
os.makedirs(DATA_DIR, exist_ok=True)


class BlacklistWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent, Qt.WindowType.Window)
        self.setWindowTitle("Blacklist")
        self.setFixedSize(302, 124)

        self.blackFile_path = os.path.join(DATA_DIR, "blacklist.json")
        self.sites = self.load_data()

        self.input_field = QLineEdit(self)
        self.input_field.setPlaceholderText("Enter site to block")
        self.input_field.setGeometry(20, 20, 260, 30)

        self.watchSites_btn = QPushButton("View blocked sites", self)
        self.watchSites_btn.move(20, 87)
        self.watchSites_btn.clicked.connect(self.show_sites)

        self.add_btn = QPushButton("Add site", self)
        self.add_btn.move(20, 57)
        self.add_btn.clicked.connect(self.add_site)

        self.delete_btn = QPushButton("Delete site", self)
        self.delete_btn.move(105, 57)
        self.delete_btn.clicked.connect(self.delete_site)

        self.clear_btn = QPushButton("Clear all sites", self)
        self.clear_btn.move(190, 57)
        self.clear_btn.clicked.connect(self.clear_all)

    def load_data(self):
        if not os.path.exists(self.blackFile_path):
            return []
        try:
            with open(self.blackFile_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    return data
        except (json.JSONDecodeError, OSError):
            pass
        return []

    def save_data(self):
        with open(self.blackFile_path, "w", encoding="utf-8") as f:
            json.dump(self.sites, f, indent=4, ensure_ascii=False)

    def normalize_site(self, text):
        text = text.strip().lower()
        if not text:
            return ""
        if "://" in text:
            parsed = urlparse(text)
            return parsed.netloc or parsed.path
        return text.split("/")[0]

    def get_all_ips(self, domain):
        ips = set()
        try:
            for info in socket.getaddrinfo(domain, 80, proto=socket.IPPROTO_TCP):
                ips.add(info[4][0])
        except socket.gaierror:
            pass
        return list(ips)

    def run_powershell(self, command):
        result = subprocess.run(
            ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", command],
            capture_output=True,
            text=True
        )
        return result

    def block_ip(self, site_name, ip):
        rule_name = f"ParentControl_Block_{site_name}_{ip.replace(':', '_')}"
        cmd = (
            f'New-NetFirewallRule -DisplayName "{rule_name}" '
            f'-Direction Outbound -Action Block -RemoteAddress "{ip}"'
        )
        result = self.run_powershell(cmd)
        if result.returncode != 0:
            QMessageBox.warning(self, "Firewall error", result.stderr.strip() or "Cannot create rule")

    def delete_rules_by_pattern(self, pattern):
        cmd = (
            f'Get-NetFirewallRule | Where-Object {{ $_.DisplayName -like "{pattern}" }} '
            f'| Remove-NetFirewallRule -Confirm:$false'
        )
        result = self.run_powershell(cmd)
        if result.returncode != 0:
            QMessageBox.warning(self, "Firewall error", result.stderr.strip() or "Cannot delete rule")

    def show_sites(self):
        if not self.sites:
            QMessageBox.information(self, "Blocked sites", "Empty")
            return

        text_lines = []
        for item in self.sites:
            if isinstance(item, dict):
                text_lines.append(item.get("site", ""))
            else:
                text_lines.append(str(item))

        QMessageBox.information(self, "Blocked sites", "\n".join(text_lines))

    def add_site(self):
        site = self.normalize_site(self.input_field.text())
        if not site:
            return

        existing_sites = []
        for item in self.sites:
            if isinstance(item, dict):
                existing_sites.append(item.get("site", ""))
            else:
                existing_sites.append(str(item))

        if site in existing_sites:
            QMessageBox.warning(self, "Error", "This site is already in the list")
            return

        ips = self.get_all_ips(site)
        if not ips:
            QMessageBox.warning(self, "Error", "Cannot resolve this site")
            return

        for ip in ips:
            self.block_ip(site, ip)

        self.sites.append({"site": site, "ips": ips})
        self.save_data()
        self.input_field.clear()

    def delete_site(self):
        site = self.normalize_site(self.input_field.text())
        if not site:
            return

        found = False
        new_sites = []

        for item in self.sites:
            if isinstance(item, dict):
                current_site = item.get("site", "")
            else:
                current_site = str(item)

            if current_site == site:
                found = True
            else:
                new_sites.append(item)

        if not found:
            QMessageBox.warning(self, "Error", "This site hasn't been added yet")
            return

        self.delete_rules_by_pattern(f"ParentControl_Block_{site}_*")
        self.sites = new_sites
        self.save_data()
        self.input_field.clear()

    def clear_all(self):
        self.delete_rules_by_pattern("ParentControl_Block_*")
        self.sites = []
        self.save_data()
        self.input_field.clear()
