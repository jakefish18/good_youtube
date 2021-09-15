from functools import cached_property
import sys
import threading

import pafy

import vlc

from PyQt5.QtCore import pyqtSignal, QEvent, QObject, QRect
from PyQt5.QtWidgets import QApplication, QDialog, QPushButton, QWidget, QLabel, QVBoxLayout, QScrollArea, QHBoxLayout, QGridLayout
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
        self.setWindowTitle("Good Youtube")
        self.buttons = []
        youtube_parser = YouTubeChannelsParser()
        self.video_links_and_info = youtube_parser.parse()
        self.setFixedHeight(len(self.video_links_and_info) * (180 + 20))
        youtube_parser.get_videos_prewiew(self.video_links_and_info)
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
        for link in self.video_links_and_info:
            button = QPushButton("Открыть видео", self)
            buttons_info[button] = link

        return buttons_info

    def generate_content(self):
        pos_y = 0 #Порядковый номер каждого блока видео.
        for button, link in self.generate_buttons_info().items():
            #Создание пиксмапа превью.
            path_to_prewiew = f"temp/{pos_y + 1}.jpg"
            pixmap_img = QPixmap(path_to_prewiew)
            lbl = QLabel(self)
            lbl.setPixmap(pixmap_img)
            lbl.move(0, 200 * pos_y)
            lbl = QLabel(self)
            lbl.setText(link[2])
            lbl.move(320, 200 * pos_y)
            lbl = QLabel(self)
            lbl.setText(link[3])
            lbl.move(320, 20 + 200 * pos_y)
            lbl = QLabel(self)
            lbl.setText(self.get_date_in_words(link[4]))
            lbl.move(320, 40 + 200 * pos_y)
            button.clicked.connect(lambda checked, link=link[0]: self.open_video(link))
            button.move(320, 60 + pos_y * 200)
            pos_y += 1

    def open_video(self, url):
        self.url_provider.find_url(url)

    def handle_url_finished(self, url):
        self.player_manager.set_media(url)
        self.player_manager.play()

    def get_date_in_words(self, date):
        """Получение из такого 2021-08-27 такое 27 августа 2021 года."""
        date = date.split('T')[0]
        date = date.split('-')
        digits_to_words = {
            "01": "января",
            "02": "февраля",
            "03": "марта",
            "04": "апреля",
            "05": "мая",
            "06": "июня",
            "07": "июля",
            "08": "августа",
            "09": "сентября",
            "10": "октября",
            "11": "ноября",
            "12": "декабря"
        }
        result = f"{date[2]} {digits_to_words[date[1]]} {date[0]} года"
        return result

class ScrollWidget(QWidget):      
    def __init__(self, parent=None):
        super(ScrollWidget, self).__init__(parent)
        self.initUi()

    def initUi(self):
        self.layoutV = QVBoxLayout(self)

        self.area = QScrollArea(self)
        self.area.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 200, 100))

        self.layoutH = QHBoxLayout(self.scrollAreaWidgetContents)
        self.gridLayout = QGridLayout()
        self.layoutH.addLayout(self.gridLayout)

        self.area.setWidget(self.scrollAreaWidgetContents)
        self.layoutV.addWidget(self.area)

        self.widget = GoodYoutubeGUI()
        self.gridLayout.addWidget(self.widget)
        window_height = len(self.widget.video_links_and_info) * 320
        self.setGeometry(700, 200, 1000, window_height)        


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ScrollWidget()
    window.show()
    sys.exit(app.exec_())