from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QApplication
from PyQt5.QtCore import Qt, QTimer
import win32gui
import win32process
import psutil

class SpotifyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(240, 80)
        
        self.container = QWidget(self)
        self.container.setGeometry(0, 0, 240, 80)
        
        layout = QVBoxLayout(self.container)
        layout.setContentsMargins(15, 10, 15, 10)
        
        title_lbl = QLabel("Nolife.code | Spotify")
        layout.addWidget(title_lbl)
        
        self.song_label = QLabel("Waiting for Spotify...")
        self.song_label.setStyleSheet("color: #888; font-size: 11px; border: none;")
        self.song_label.setWordWrap(True)
        layout.addWidget(self.song_label)
        
        # Pozycja: lewy dolny róg
        sc = QApplication.primaryScreen().geometry()
        self.move(20, sc.height() - self.height() - 40)
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_info)
        self.timer.start(8000)

    def get_spotify_track(self):
        def callback(hwnd, hwnds):
            if win32gui.IsWindowVisible(hwnd):
                _, pid = win32process.GetWindowThreadProcessId(hwnd)
                try:
                    proc = psutil.Process(pid)
                    if proc.name().lower() == "spotify.exe":
                        txt = win32gui.GetWindowText(hwnd)
                        if txt and txt not in ["Spotify Free", "Spotify Premium", "Spotify"]:
                            hwnds.append(txt)
                except: pass
            return True
        
        titles = []
        win32gui.EnumWindows(callback, titles)
        return titles[0] if titles else "Spotify is closed"

    def update_info(self):
        track = self.get_spotify_track()
        if self.song_label.text() != track:
            self.song_label.setText(track)
