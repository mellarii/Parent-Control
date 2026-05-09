import ctypes
import json
import os
import re
import time
from datetime import datetime
from threading import Thread
from urllib.parse import urlparse


class WindowTracker:
    """Tracks active window and time spent on websites"""
    
    def __init__(self):
        self.stats_file = "site_stats.json"
        self.running = False
        self.current_domain = None
        self.stats = self.load_stats()
        self.thread = None
        
    def load_stats(self):
        """Load site statistics from JSON"""
        if not os.path.exists(self.stats_file):
            return {}
        try:
            with open(self.stats_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, dict):
                    return data
        except (json.JSONDecodeError, OSError):
            pass
        return {}
    
    def save_stats(self):
        """Save site statistics to JSON"""
        with open(self.stats_file, "w", encoding="utf-8") as f:
            json.dump(self.stats, f, indent=4, ensure_ascii=False)
    
    def get_foreground_window_title(self):
        """Get the title of the active window"""
        try:
            hwnd = ctypes.windll.user32.GetForegroundWindow()
            length = ctypes.windll.user32.GetWindowTextLengthW(hwnd)
            buf = ctypes.create_unicode_buffer(length + 1)
            ctypes.windll.user32.GetWindowTextW(hwnd, buf, length + 1)
            return buf.value
        except Exception:
            return ""
    
    def extract_domain_from_title(self, title):
        """Extract domain name from browser window title"""
        if not title:
            return None
        
        if "firefox" not in title.lower() and "chrome" not in title.lower() and "edge" not in title.lower():
            return None
        
        title = title.lower()
        title = title.replace(" — mozilla firefox", "").replace(" — google chrome", "").replace(" — microsoft edge", "")
        title = title.replace("mozilla firefox", "").replace("google chrome", "").replace("microsoft edge", "")
        title = title.strip()
        
        if not title:
            return None
        
        url_pattern = r'(?:https?://)?(?:www\.)?([a-zA-Z0-9](?:[a-zA-Z0-9\-]*[a-zA-Z0-9])?(?:\.[a-zA-Z]{2,})+)'
        match = re.search(url_pattern, title)
        
        if match:
            domain = match.group(1).lower()
            if domain.startswith("www."):
                domain = domain[4:]
            return domain
        
        words = title.split()
        if words:
            first_word = words[0].strip('[]()«»"\'').lower()
            common_words = ["the", "a", "an", "and", "or", "page", "tab", "new", "home", "search"]
            if first_word and first_word not in common_words and len(first_word) > 1:
                first_word = re.sub(r'[^a-z0-9\-]', '', first_word)
                if first_word:
                    return first_word
        
        return None
    
    def update_stats(self, domain, seconds=1):
        """Update statistics for a domain"""
        if domain not in self.stats:
            self.stats[domain] = {
                "total_seconds": 0,
                "visits": 0,
                "last_visit": None
            }
        
        self.stats[domain]["total_seconds"] += seconds
        self.stats[domain]["last_visit"] = datetime.now().isoformat()
    
    def track(self):
        """Main tracking loop"""
        last_domain = None
        check_interval = 1  
        
        while self.running:
            try:
                title = self.get_foreground_window_title()
                domain = self.extract_domain_from_title(title)
                
                if domain and domain != last_domain:
                    if last_domain:
                        self.stats[last_domain]["visits"] += 1
                        self.save_stats()
                    last_domain = domain
                    self.current_domain = domain
                
                if domain:
                    self.update_stats(domain, check_interval)
                
                time.sleep(check_interval)
                
            except Exception as e:
                print(f"Tracking error: {e}")
                time.sleep(check_interval)
    
    def start(self):
        """Start tracking in background thread"""
        if not self.running:
            self.running = True
            self.thread = Thread(target=self.track, daemon=True)
            self.thread.start()
    
    def stop(self):
        """Stop tracking"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=2)
        self.save_stats()
    
    def get_stats(self):
        """Get current statistics"""
        return self.stats
    
    def get_sorted_stats(self):
        """Get statistics sorted by total time (descending)"""
        sorted_stats = sorted(
            self.stats.items(),
            key=lambda x: x[1]["total_seconds"],
            reverse=True
        )
        return sorted_stats
    
    def clear_stats(self):
        """Clear all statistics"""
        self.stats = {}
        self.save_stats()
    
    def format_time(self, seconds):
        """Format seconds to HH:MM:SS"""
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
