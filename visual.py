from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtCore import Qt

class VisualWindow(QWidget):
    def __init__(self, crosshair):
        super().__init__()
        self.crosshair = crosshair
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(200, 360)
        self.container = QWidget(self)
        self.container.setGeometry(0, 0, 200, 360)
        self.setup_ui()
        self.move(270, 20)

    def setup_ui(self):
        layout = QVBoxLayout(self.container)
        layout.setContentsMargins(15, 20, 15, 15)
        layout.addWidget(QLabel("Nolife.code | Visual"))
        layout.addSpacing(15)

        presets = [("DOT", "dot"), ("CROSS (X)", "cross"), ("PLUS (+)", "plus"),
                   ("BOX", "box"), ("T-SHAPE", "t_shape")]

        for name, p_type in presets:
            btn = QPushButton(f"> {name}")
            btn.clicked.connect(lambda checked, t=p_type: self.crosshair.set_preset(t))
            layout.addWidget(btn)
        layout.addStretch()
