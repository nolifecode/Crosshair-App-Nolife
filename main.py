import sys
import os
from PyQt5.QtWidgets import QApplication, QLabel, QWidget
from PyQt5.QtCore import Qt, QSequentialAnimationGroup, QPropertyAnimation, QPauseAnimation, pyqtSignal, QObject
from PyQt5.QtGui import QPixmap, QColor
from pynput import keyboard

from crosshair import Crosshair
from settings import SettingsWindow
from visual import VisualWindow
from menu import MenuWindow
from spotify import SpotifyWindow
from profiles import ProfilesWindow

class HotkeySignal(QObject):
    toggle_menu = pyqtSignal()
    toggle_cross = pyqtSignal()

class OverlayApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.signals = HotkeySignal()
        self.signals.toggle_menu.connect(self.toggle_all)
        self.signals.toggle_cross.connect(self.toggle_c)

        self.listener = keyboard.Listener(on_press=self.on_press)
        self.listener.start()

        self.crosshair = Crosshair()
        self.spotify = SpotifyWindow()
        self.profiles = ProfilesWindow(self.crosshair)
        self.settings = SettingsWindow(self.crosshair)
        self.visual = VisualWindow(self.crosshair)
        
        self.menu = MenuWindow(self.settings, self.visual, self.spotify, self.profiles)

        self.settings.hide()
        self.visual.hide()
        self.menu.hide()
        self.spotify.hide()
        self.profiles.hide()
        
        self.setup_splash()

    def on_press(self, key):
        try:
            if key == keyboard.Key.insert:
                self.signals.toggle_menu.emit()
            elif key == keyboard.Key.f1:
                self.signals.toggle_cross.emit()
        except AttributeError:
            pass

    def setup_splash(self):
        self.splash = QWidget()
        self.splash.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool | Qt.WindowTransparentForInput)
        self.splash.setAttribute(Qt.WA_TranslucentBackground)
        px = QPixmap("loading.png")
        if px.isNull(): 
            px = QPixmap(400, 300)
            px.fill(QColor(5, 5, 5))
        lbl = QLabel(self.splash)
        lbl.setPixmap(px)
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
        self.profiles.setVisible(vis)
        
        if vis and "ON" in self.menu.btn_spotify.text():
            self.spotify.show()
        else:
            self.spotify.hide()

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
