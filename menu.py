from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QApplication
from PyQt5.QtCore import Qt

class MenuWindow(QWidget):
    def __init__(self, settings, visual, spotify, profiles):
        super().__init__()
        self.settings = settings
        self.visual = visual
        self.spotify = spotify
        self.profiles = profiles
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(200, 320)
        self.container = QWidget(self)
        self.container.setGeometry(0, 0, 200, 320)
        self.setup_ui()
        self.update_theme("#888")
        self.move(QApplication.primaryScreen().geometry().width() - self.width() - 20, 20)

    def setup_ui(self):
        layout = QVBoxLayout(self.container)
        layout.setContentsMargins(15, 20, 15, 10)
        layout.addWidget(QLabel("Nolife.code | Crosshair"))
        layout.addSpacing(10)

        layout.addWidget(QPushButton("> TOGGLE CROSSHAIR [F1]"))
        
        self.btn_spotify = QPushButton("> SPOTIFY WIDGET: ON")
        self.btn_spotify.clicked.connect(self.toggle_spotify_active)
        layout.addWidget(self.btn_spotify)
        
        layout.addStretch()

        layout.addWidget(QLabel("> CHANGE THEME"))
        color_layout = QHBoxLayout()
        for c in ["#FF4444", "#44FF44", "#4444FF", "#FFFF44", "#FF44FF", "#888"]:
            btn = QPushButton()
            btn.setFixedSize(12, 12)
            btn.setStyleSheet(f"background-color: {c}; border: none;")
            btn.clicked.connect(lambda checked, col=c: self.update_theme(col))
            color_layout.addWidget(btn)
        layout.addLayout(color_layout)
        
        layout.addSpacing(10)
        btn_exit = QPushButton("[ EXIT ]")
        btn_exit.setObjectName("ExitBtn")
        btn_exit.clicked.connect(lambda: exit())
        layout.addWidget(btn_exit)

    def toggle_spotify_active(self):
        if self.spotify.isVisible():
            self.spotify.hide()
            self.spotify.timer.stop()
            self.btn_spotify.setText("> SPOTIFY WIDGET: OFF")
        else:
            self.spotify.show()
            self.spotify.timer.start(2000)
            self.btn_spotify.setText("> SPOTIFY WIDGET: ON")

    def update_theme(self, color):
        style = f"""
            QWidget {{ background-color: #0A0A0A; border: 1px solid {color}; }}
            QLabel {{ color: #444; font-family: 'Consolas'; font-size: 10px; border: none; }}
            QPushButton {{ background-color: #111; color: #888; border: 1px solid #222; padding: 5px; font-family: 'Consolas'; font-size: 11px; }}
            QPushButton:hover {{ background-color: #181818; color: {color}; }}
            QLineEdit {{ background-color: #111; color: #888; border: 1px solid #222; font-family: 'Consolas'; font-size: 10px; }}
            QScrollArea {{ background: transparent; }}
            #ExitBtn {{ color: #444; text-align: center; background: transparent; border: none; }}
            #ExitBtn:hover {{ color: #AA0000; }}
        """
        self.container.setStyleSheet(style)
        self.settings.container.setStyleSheet(style)
        self.visual.container.setStyleSheet(style)
        self.spotify.container.setStyleSheet(style)
        self.profiles.container.setStyleSheet(style)
