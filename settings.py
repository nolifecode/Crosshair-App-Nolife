from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor

class SettingsWindow(QWidget):
    def __init__(self, crosshair):
        super().__init__()
        self.crosshair = crosshair
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(240, 400)
        self.container = QWidget(self)
        self.container.setGeometry(0, 0, 240, 400)
        self.labels = {}
        self.setup_ui()
        self.move(20, 20)

    def setup_ui(self):
        self.main_layout = QVBoxLayout(self.container)
        self.main_layout.setContentsMargins(15, 20, 15, 15)
        self.main_layout.addWidget(QLabel("Nolife.code | Settings"))
        self.main_layout.addSpacing(15)

        controls = [("Transparency", "alpha", 10), ("Offset X", "offset_x", 1),
                    ("Offset Y", "offset_y", 1), ("Rotate", "rotation", 5),
                    ("Size", "c_size", 1)]
        for name, attr, step in controls:
            self.add_control(name, attr, step)
        self.refresh_labels()

        self.main_layout.addSpacing(15)
        self.main_layout.addWidget(QLabel("Crosshair Color"))
        color_layout = QHBoxLayout()
        for c in [Qt.red, Qt.green, Qt.blue, Qt.white, Qt.yellow, Qt.cyan]:
            btn = QPushButton()
            btn.setFixedSize(18, 18)
            btn.setStyleSheet(f"background-color: {QColor(c).name()}; border: 1px solid #333;")
            btn.clicked.connect(lambda checked, col=c: self.crosshair.set_color(col))
            color_layout.addWidget(btn)
        self.main_layout.addLayout(color_layout)

        self.main_layout.addStretch()
        btn_reset = QPushButton("[ RESET SETTINGS ]")
        btn_reset.clicked.connect(self.reset_all)
        self.main_layout.addWidget(btn_reset)

    def add_control(self, name, attr, step):
        row = QHBoxLayout()
        lbl_name = QLabel(name)
        lbl_name.setFixedWidth(80)
        btn_minus = QPushButton("-")
        btn_minus.setFixedSize(22, 22)
        val_display = QLabel("0.0")
        val_display.setAlignment(Qt.AlignCenter)
        val_display.setFixedWidth(40)
        self.labels[attr] = val_display
        btn_plus = QPushButton("+")
        btn_plus.setFixedSize(22, 22)
        btn_minus.clicked.connect(lambda: self.update_val(attr, -step))
        btn_plus.clicked.connect(lambda: self.update_val(attr, step))
        row.addWidget(lbl_name); row.addWidget(btn_minus); row.addWidget(val_display); row.addWidget(btn_plus)
        self.main_layout.addLayout(row)

    def update_val(self, attr, delta):
        if attr == "alpha": self.crosshair.alpha = max(0, min(255, self.crosshair.alpha + delta))
        elif attr == "offset_x": self.crosshair.offset_x += delta; self.crosshair.center_pos()
        elif attr == "offset_y": self.crosshair.offset_y += delta; self.crosshair.center_pos()
        elif attr == "rotation": self.crosshair.rotation += delta
        elif attr == "c_size": self.crosshair.c_size = max(1, self.crosshair.c_size + delta)
        self.crosshair.update(); self.refresh_labels()

    def refresh_labels(self):
        if "alpha" in self.labels: self.labels["alpha"].setText(f"{self.crosshair.alpha/255:.1f}")
        if "offset_x" in self.labels: self.labels["offset_x"].setText(f"{self.crosshair.offset_x}")
        if "offset_y" in self.labels: self.labels["offset_y"].setText(f"{self.crosshair.offset_y}")
        if "rotation" in self.labels: self.labels["rotation"].setText(f"{self.crosshair.rotation}")
        if "c_size" in self.labels: self.labels["c_size"].setText(f"{self.crosshair.c_size}")

    def reset_all(self):
        self.crosshair.reset_defaults()
        self.refresh_labels()
