from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import Qt

class Crosshair(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool | Qt.WindowTransparentForInput)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.resize(200, 200)
        self.preset = "cross"
        self.reset_defaults()

    def reset_defaults(self):
        self.color = QColor(255, 255, 255)
        self.alpha = 255
        self.rotation = 0
        self.c_size = 5
        self.offset_x = 0
        self.offset_y = 0
        self.center_pos()
        self.update()

    def set_preset(self, p):
        self.preset = p
        self.update()

    def set_color(self, col):
        self.color = QColor(col)
        self.update()

    def center_pos(self):
        sc = QApplication.primaryScreen().geometry()
        self.move((sc.width()-self.width())//2 + self.offset_x,
                  (sc.height()-self.height())//2 + self.offset_y)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, False)
        c = QColor(self.color)
        c.setAlpha(self.alpha)
        painter.setPen(QPen(c, 1))
        painter.translate(self.width()/2, self.height()/2)
        painter.rotate(self.rotation)
        s = self.c_size

        if self.preset == "dot":
            painter.drawPoint(0, 0)
        elif self.preset == "cross":
            painter.drawLine(-s, -s, s, s)
            painter.drawLine(-s, s, s, -s)
        elif self.preset == "plus":
            painter.drawLine(-s, 0, s, 0)
            painter.drawLine(0, -s, 0, s)
        elif self.preset == "box":
            painter.drawRect(-s, -s, s*2, s*2)
        elif self.preset == "t_shape":
            painter.drawLine(-s, 0, s, 0)
            painter.drawLine(0, 0, 0, s)
