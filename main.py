import sys
import keyboard
from PyQt5.QtWidgets import QApplication, QLabel, QWidget
from PyQt5.QtCore import Qt, QSequentialAnimationGroup, QPropertyAnimation, QPauseAnimation, pyqtSignal, QObject
from PyQt5.QtGui import QPixmap, QColor


from crosshair import Crosshair
from settings import SettingsWindow
from visual import VisualWindow
from menu import MenuWindow

class HotkeySignal(QObject):
    toggle_menu = pyqtSignal()
    toggle_cross = pyqtSignal()

class OverlayApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.signals = HotkeySignal()
        self.signals.toggle_menu.connect(self.toggle_all)
        self.signals.toggle_cross.connect(self.toggle_c)

        keyboard.add_hotkey('insert', lambda: self.signals.toggle_menu.emit())
        keyboard.add_hotkey('f1', lambda: self.signals.toggle_cross.emit())

        self.crosshair = Crosshair()
        self.settings = SettingsWindow(self.crosshair)
        self.visual = VisualWindow(self.crosshair)
        self.menu = MenuWindow(self.settings, self.visual)

        self.settings.hide(); self.visual.hide(); self.menu.hide()
        self.setup_splash()

    def setup_splash(self):
        self.splash = QWidget()
        self.splash.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.splash.setAttribute(Qt.WA_TranslucentBackground)
        px = QPixmap("loading.png")
        if px.isNull(): px = QPixmap(400, 300); px.fill(QColor(5, 5, 5))
        lbl = QLabel(self.splash); lbl.setPixmap(px)
        self.splash.resize(px.width(), px.height())
        sc = self.app.primaryScreen().geometry()
        self.splash.move((sc.width()-px.width())//2, (sc.height()-px.height())//2)

    def toggle_c(self):
        self.crosshair.setVisible(not self.crosshair.isVisible())

    def toggle_all(self):
        vis = not self.menu.isVisible()
        self.menu.setVisible(vis)
        self.settings.setVisible(vis)
        self.visual.setVisible(vis)

    def run(self):
        self.splash.show()
        seq = QSequentialAnimationGroup()
        f_in = QPropertyAnimation(self.splash, b"windowOpacity")
        f_in.setDuration(400); f_in.setStartValue(0); f_in.setEndValue(1)
        seq.addAnimation(f_in)
        seq.addAnimation(QPauseAnimation(1000))
        f_out = QPropertyAnimation(self.splash, b"windowOpacity")
        f_out.setDuration(400); f_out.setStartValue(1); f_out.setEndValue(0)
        seq.addAnimation(f_out)
        seq.finished.connect(lambda: (self.splash.close(), self.crosshair.show()))
        seq.start()
        sys.exit(self.app.exec_())

if __name__ == "__main__":
    OverlayApp().run()
