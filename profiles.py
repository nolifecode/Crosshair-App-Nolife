import os
import configparser
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel,
    QLineEdit, QScrollArea
)
from PyQt5.QtCore import Qt


class ProfilesWindow(QWidget):
    def __init__(self, crosshair):
        super().__init__()
        self.crosshair = crosshair

        self.path = os.path.join(
            os.path.expanduser("~"),
            "Documents",
            "Nolife-Crosshair"
        )
        self.cfg_file = os.path.join(self.path, "config.ini")
        if not os.path.exists(self.path):
            os.makedirs(self.path)

        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint |
            Qt.Tool
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(200, 300)

        self.container = QWidget(self)
        self.container.setGeometry(0, 0, 200, 300)

        self.setup_ui()
        self.move(20, 440)

    def setup_ui(self):
        self.layout = QVBoxLayout(self.container)
        self.layout.setContentsMargins(12, 12, 12, 12)
        self.layout.setSpacing(6)

        title = QLabel("Nolife.code | Profiles")
        title.setStyleSheet("color: #aaa;")
        self.layout.addWidget(title)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Profile name...")
        self.name_input.setStyleSheet("""
            background: #111;
            color: #888;
            border: 1px solid #333;
            padding: 3px;
        """)
        self.layout.addWidget(self.name_input)

        btn_save = QPushButton("[ SAVE CURRENT ]")
        btn_save.setStyleSheet("""
            QPushButton {
                background: #111;
                color: #aaa;
                border: 1px solid #333;
                padding: 4px;
            }
            QPushButton:hover {
                border-color: #555;
            }
        """)
        btn_save.clicked.connect(self.save_profile)
        self.layout.addWidget(btn_save)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setStyleSheet("background: transparent; border: none;")

        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_layout.setContentsMargins(0, 4, 0, 4)
        self.scroll_layout.setSpacing(3)  # <<< bliżej siebie

        self.scroll.setWidget(self.scroll_content)
        self.layout.addWidget(self.scroll)

        self.refresh_list()

    def save_profile(self):
        name = self.name_input.text().strip() or "Default"

        config = configparser.ConfigParser()
        if os.path.exists(self.cfg_file):
            config.read(self.cfg_file)

        if not config.has_section(name):
            config.add_section(name)

        config.set(name, "preset", str(self.crosshair.preset))
        config.set(name, "color", self.crosshair.color.name())
        config.set(name, "alpha", str(self.crosshair.alpha))
        config.set(name, "rotation", str(self.crosshair.rotation))
        config.set(name, "size", str(self.crosshair.c_size))
        config.set(name, "offset_x", str(self.crosshair.offset_x))
        config.set(name, "offset_y", str(self.crosshair.offset_y))

        with open(self.cfg_file, "w") as f:
            config.write(f)

        self.refresh_list()

    def load_profile(self, name):
        config = configparser.ConfigParser()
        config.read(self.cfg_file)

        if not config.has_section(name):
            return

        self.crosshair.set_preset(config.get(name, "preset"))
        self.crosshair.set_color(config.get(name, "color"))
        self.crosshair.alpha = config.getint(name, "alpha")
        self.crosshair.rotation = config.getint(name, "rotation")
        self.crosshair.c_size = config.getint(name, "size")
        self.crosshair.offset_x = config.getint(name, "offset_x")
        self.crosshair.offset_y = config.getint(name, "offset_y")
        self.crosshair.center_pos()
        self.crosshair.update()

    def refresh_list(self):
        for i in reversed(range(self.scroll_layout.count())):
            w = self.scroll_layout.itemAt(i).widget()
            if w:
                w.setParent(None)

        config = configparser.ConfigParser()
        if not os.path.exists(self.cfg_file):
            return

        config.read(self.cfg_file)
        for section in config.sections():
            btn = QPushButton(f"> {section}")
            btn.setStyleSheet("""
                QPushButton {
                    background: #0f0f0f;
                    color: #888;
                    border: 1px solid #222;
                    padding: 3px;
                    text-align: left;
                }
                QPushButton:hover {
                    color: #ccc;
                    border-color: #444;
                }
            """)
            btn.clicked.connect(lambda _, s=section: self.load_profile(s))
            self.scroll_layout.addWidget(btn)
