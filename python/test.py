# import sys
# from PyQt5 import Qt

# class ExampleWidget(Qt.QWidget):
#     def __init__(self, parent=None):
#         super(ExampleWidget, self).__init__(parent)
#         self.initUi()

#     def initUi(self):
#         self.mainLayout = Qt.QVBoxLayout()
#         self.label_1 = Qt.QLabel('One')
#         self.label_2 = Qt.QLabel('Two')
#         self.mainLayout.addWidget(self.label_1)
#         self.mainLayout.addWidget(self.label_2)
#         self.setLayout(self.mainLayout)        


# class ScrollWidget(Qt.QWidget):      
#     def __init__(self, parent=None):
#         super(ScrollWidget, self).__init__(parent)
#         self.initUi()

#     def initUi(self):
#         self.layoutV = Qt.QVBoxLayout(self)

#         self.area = Qt.QScrollArea(self)
#         #self.setCentralWidget(self.area)       # setCentralWidget <- QMainWindow
#         self.area.setWidgetResizable(True)
#         self.scrollAreaWidgetContents = Qt.QWidget()
#         self.scrollAreaWidgetContents.setGeometry(Qt.QRect(0, 0, 200, 100))

#         self.layoutH = Qt.QHBoxLayout(self.scrollAreaWidgetContents)
#         self.gridLayout = Qt.QGridLayout()
#         self.layoutH.addLayout(self.gridLayout)

#         self.area.setWidget(self.scrollAreaWidgetContents)
#         self.add_button = Qt.QPushButton("Add Widget")
#         self.layoutV.addWidget(self.area)
#         self.layoutV.addWidget(self.add_button)
#         self.add_button.clicked.connect(self.addWidget)

#         self.widget = ExampleWidget()
#         self.gridLayout.addWidget(self.widget)
#         self.setGeometry(700, 200, 200, 100)        

#     def addWidget(self):
#         #  Как добавить виджет с прокруткой в ​​область?
#         self.widget = ExampleWidget()
#         self.gridLayout.addWidget(self.widget)


# if __name__ == '__main__':
#     app = Qt.QApplication(sys.argv)

#     window = ScrollWidget()
#     window.show()
#     sys.exit(app.exec_())  

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
        self.setFixedSize(1000, 1000)
        self.setWindowTitle("Good Youtube")
        self.buttons = []
        self.video_links_and_info = YouTubeChannelsParser().parse()
        self.PATH_TO_IMG = "video_images/youtubebox.jpg"
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
        for link in self.video_links_and_info:
            button = QPushButton("Открыть видео", self)
            buttons_info[button] = link

        return buttons_info

    def generate_content(self):
        pos_y = 0
        for button, link in self.generate_buttons_info().items():
            lbl = QLabel(self)
            lbl.setPixmap(self.pixmap_img)
            lbl.move(0, 150 * pos_y)
            lbl = QLabel(self)
            lbl.setText(link[2])
            lbl.move(100, 150 * pos_y)
            lbl = QLabel(self)
            lbl.setText(link[3])
            lbl.move(100, 20 + 150 * pos_y)
            lbl = QLabel(self)
            lbl.setText(self.get_date_in_words(link[4]))
            lbl.move(100, 40 + 150 * pos_y)
            button.clicked.connect(lambda checked, link=link[0]: self.open_video(link))
            button.move(100, 60 + pos_y * 150)
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
        #self.setCentralWidget(self.area)       # setCentralWidget <- QMainWindow
        self.area.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 200, 100))

        self.layoutH = QHBoxLayout(self.scrollAreaWidgetContents)
        self.gridLayout = QGridLayout()
        self.layoutH.addLayout(self.gridLayout)

        self.area.setWidget(self.scrollAreaWidgetContents)
        self.add_button = QPushButton("Add Widget")
        self.layoutV.addWidget(self.area)
        self.layoutV.addWidget(self.add_button)
        self.add_button.clicked.connect(self.addWidget)

        self.widget = GoodYoutubeGUI()
        self.gridLayout.addWidget(self.widget)
        self.setGeometry(700, 200, 1000, 1000)        

    def addWidget(self):
        #  Как добавить виджет с прокруткой в ​​область?
        self.widget = GoodYoutubeGUI()
        self.gridLayout.addWidget(self.widget)

    def addWidget(self):
        #  Как добавить виджет с прокруткой в ​​область?
        self.widget = GoodYoutubeGUI()
        self.gridLayout.addWidget(self.widget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ScrollWidget()
    window.show()
    sys.exit(app.exec_())