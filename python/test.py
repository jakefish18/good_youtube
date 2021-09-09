from functools import cached_property
import sys
import threading

import pafy

import vlc

from PyQt5.QtCore import pyqtSignal, QEvent, QObject
from PyQt5.QtWidgets import QApplication, QDialog, QPushButton, QWidget, QLabel
from  PyQt5.QtGui import QPixmap

from youtube_parser import YouTubeChannelsParser

class PlayerManager(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.window = QWidget()
        if sys.platform.startswith("linux"):  # for Linux using the X Server
            self.player.set_xwindow(self.window.winId())
        elif sys.platform == "win32":  # for Windows
            self.player.set_hwnd(self.window.winId())
        elif sys.platform == "darwin":  # for MacOS
            self.player.set_nsobject(self.window.winId())
        self.window.installEventFilter(self)

    @cached_property
    def player(self):
        player = vlc.MediaPlayer()
        player.event_manager().event_attach(
            vlc.EventType.MediaPlayerEndReached, self._handle_finished
        )
        return player

    def _handle_finished(self, event):
        if event.type == vlc.EventType.MediaPlayerEndReached:
            self.player.stop()

    def play(self):
        self.player.play()
        self.window.show()

    def set_media(self, url):
        media = vlc.Media(url)
        self.player.set_media(media)

    def eventFilter(self, obj, event):
        if obj is self.window and event.type() == QEvent.Close:
            self.player.stop()

        return super().eventFilter(obj, event)


class UrlProvider(QObject):
    finished = pyqtSignal(str)

    def find_url(self, url):
        threading.Thread(target=self._find_url, args=(url,), daemon=True).start()

    def _find_url(self, url):
        video = pafy.new(url)
        best = video.getbest()
        self.finished.emit(best.url)


class GoodYoutubeGUI(QDialog):
    def __init__(self):
        super().__init__()
        self.setFixedSize(800, 800)
        self.setWindowTitle("Good Youtube")
        self.buttons = []
        self.video_links = YouTubeChannelsParser().parse()
        self.PATH_TO_IMG = "video_images/yputubebox.jpg"
        self.pixmap_img = QPixmap(self.PATH_TO_IMG)
        self.url_provider.finished.connect(self.handle_url_finished)
        self.generate_content()

    @cached_property
    def player_manager(self):
        return PlayerManager()

    @cached_property
    def url_provider(self):
        return UrlProvider()

    def generate_buttons_info(self):
        buttons_info = {}
        for link in self.video_links:
            button = QPushButton("Открыть видео", self)
            buttons_info[button] = link

        return buttons_info

    def generate_content(self):
        pos_y = 0
        for button, link in self.generate_buttons_info().items():
            lbl = QLabel(self)
            lbl.setPixmap(self.pixmap_img)
            lbl.move(0, pos_y * 100)
            button.clicked.connect(lambda checked, link=link: self.open_video(link))
            button.move(100, pos_y * 100)
            pos_y += 1

    def open_video(self, url):
        self.url_provider.find_url(url)

    def handle_url_finished(self, url):
        self.player_manager.set_media(url)
        self.player_manager.play()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dlg_main = GoodYoutubeGUI()
    dlg_main.show()
    sys.exit(app.exec_())