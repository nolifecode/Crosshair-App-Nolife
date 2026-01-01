from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QApplication
from PyQt5.QtCore import Qt


class MenuWindow(QWidget):
    def __init__(self, settings, visual):
        super().__init__()
        self.settings = settings
        self.visual = visual
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(200, 280)
        self.container = QWidget(self)
        self.container.setGeometry(0, 0, 200, 280)
        self.setup_ui()
        self.update_theme("#888")
        self.move(QApplication.primaryScreen().geometry().width() - self.width() - 20, 20)

    def setup_ui(self):
        layout = QVBoxLayout(self.container)
        layout.setContentsMargins(15, 20, 15, 10)
        layout.addWidget(QLabel("Nolife.code | Crosshair"))
        layout.addSpacing(20)

        self.btn_cross = QPushButton("> SHOW CROSSHAIR [F1]")
        self.btn_menu = QPushButton("> SHOW MENU [INS]")
        layout.addWidget(self.btn_cross)
        layout.addWidget(self.btn_menu)
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

        self.btn_exit = QPushButton("[ EXIT ]")
        self.btn_exit.setObjectName("ExitBtn")
        self.btn_exit.clicked.connect(lambda: exit())
        layout.addWidget(self.btn_exit)

    def update_theme(self, color):
        style = f"""
            QWidget {{ background-color: #0A0A0A; border: 1px solid {color}; }}
            QLabel {{ color: #444; font-family: 'Consolas'; font-size: 10px; border: none; }}
            QPushButton {{ background-color: #111; color: #888; border: 1px solid #222; padding: 5px; font-family: 'Consolas'; font-size: 11px; }}
            QPushButton:hover {{ background-color: #181818; color: {color}; }}
            #ExitBtn {{ color: #444; text-align: center; background: transparent; border: none; }}
            #ExitBtn:hover {{ color: #AA0000; }}
        """
        self.container.setStyleSheet(style)
        self.settings.container.setStyleSheet(style)
        self.visual.container.setStyleSheet(style)
