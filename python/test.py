# from functools import cached_property
# import sys
# import threading

# import pafy

# import vlc

# from PyQt5.QtCore import pyqtSignal, QEvent, QObject, QRect
# from PyQt5.QtWidgets import QApplication, QDialog, QPushButton, QWidget, QLabel, QVBoxLayout, QScrollArea, QHBoxLayout, QGridLayout
# from  PyQt5.QtGui import QPixmap

# from youtube_parser import YouTubeChannelsParser

# class PlayerManager(QObject):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self.window = QWidget()
#         if sys.platform.startswith("linux"):  # for Linux using the X Server
#             self.player.set_xwindow(self.window.winId())
#         elif sys.platform == "win32":  # for Windows
#             self.player.set_hwnd(self.window.winId())
#         elif sys.platform == "darwin":  # for MacOS
#             self.player.set_nsobject(self.window.winId())
#         self.window.installEventFilter(self)

#     @cached_property
#     def player(self):
#         player = vlc.MediaPlayer()
#         player.event_manager().event_attach(
#             vlc.EventType.MediaPlayerEndReached, self._handle_finished
#         )
#         return player

#     def _handle_finished(self, event):
#         if event.type == vlc.EventType.MediaPlayerEndReached:
#             self.player.stop()

#     def play(self):
#         self.player.play()
#         self.window.show()

#     def set_media(self, url):
#         media = vlc.Media(url)
#         self.player.set_media(media)

#     def eventFilter(self, obj, event):
#         if obj is self.window and event.type() == QEvent.Close:
#             self.player.stop()

#         return super().eventFilter(obj, event)


# class UrlProvider(QObject):
#     finished = pyqtSignal(str)

#     def find_url(self, url):
#         threading.Thread(target=self._find_url, args=(url,), daemon=True).start()

#     def _find_url(self, url):
#         video = pafy.new(url)
#         best = video.getbest()
#         self.finished.emit(best.url)


# class GoodYoutubeGUI(QDialog):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Good Youtube")
#         self.buttons = []
#         youtube_parser = YouTubeChannelsParser("AIzaSyDPRxayW_cIe_8mkhtW-dsknFS46H6opnA")
#         self.video_links_and_info = youtube_parser.parse()
#         self.setFixedHeight(len(self.video_links_and_info) * (180 + 20))
#         youtube_parser.get_videos_prewiew(self.video_links_and_info)
#         self.url_provider.finished.connect(self.handle_url_finished)
#         self.generate_content()

#     @cached_property
#     def player_manager(self):
#         return PlayerManager()

#     @cached_property
#     def url_provider(self):
#         return UrlProvider()

#     def generate_buttons_info(self):
#         buttons_info = {}
#         for link in self.video_links_and_info:
#             button = QPushButton("Открыть видео", self)
#             buttons_info[button] = link

#         return buttons_info

#     def generate_content(self):
#         pos_y = 0 #Порядковый номер каждого блока видео.
#         for button, link in self.generate_buttons_info().items():
#             #Создание пиксмапа превью.
#             path_to_prewiew = f"temp/{pos_y + 1}.jpg"
#             pixmap_img = QPixmap(path_to_prewiew)
#             lbl = QLabel(self)
#             lbl.setPixmap(pixmap_img)
#             lbl.move(0, 200 * pos_y)
#             lbl = QLabel(self)
#             lbl.setText(link[2])
#             lbl.move(320, 200 * pos_y)
#             lbl = QLabel(self)
#             lbl.setText(link[3])
#             lbl.move(320, 20 + 200 * pos_y)
#             lbl = QLabel(self)
#             lbl.setText(self.get_date_in_words(link[4]))
#             lbl.move(320, 40 + 200 * pos_y)
#             button.clicked.connect(lambda checked, link=link[0]: self.open_video(link))
#             button.move(320, 60 + pos_y * 200)
#             pos_y += 1

#     def open_video(self, url):
#         self.url_provider.find_url(url)

#     def handle_url_finished(self, url):
#         self.player_manager.set_media(url)
#         self.player_manager.play()

#     def get_date_in_words(self, date):
#         """Получение из такого 2021-08-27 такое 27 августа 2021 года."""
#         date = date.split('T')[0]
#         date = date.split('-')
#         digits_to_words = {
#             "01": "января",
#             "02": "февраля",
#             "03": "марта",
#             "04": "апреля",
#             "05": "мая",
#             "06": "июня",
#             "07": "июля",
#             "08": "августа",
#             "09": "сентября",
#             "10": "октября",
#             "11": "ноября",
#             "12": "декабря"
#         }
#         result = f"{date[2]} {digits_to_words[date[1]]} {date[0]} года"
#         return result

# class ScrollWidget(QWidget):      
#     def __init__(self, parent=None):
#         super(ScrollWidget, self).__init__(parent)
#         self.initUi()

#     def initUi(self):
#         self.layoutV = QVBoxLayout(self)

#         self.area = QScrollArea(self)
#         self.area.setWidgetResizable(True)
#         self.scrollAreaWidgetContents = QWidget()
#         self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 200, 100))

#         self.layoutH = QHBoxLayout(self.scrollAreaWidgetContents)
#         self.gridLayout = QGridLayout()
#         self.layoutH.addLayout(self.gridLayout)

#         self.area.setWidget(self.scrollAreaWidgetContents)
#         self.layoutV.addWidget(self.area)

#         self.widget = GoodYoutubeGUI()
#         self.gridLayout.addWidget(self.widget)
#         window_height = len(self.widget.video_links_and_info) * 320
#         self.setGeometry(700, 200, 1000, window_height)        


# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = ScrollWidget()
#     window.show()
#     sys.exit(app.exec_())

from functools import cached_property
import sys
import threading

import pafy

import vlc

from PyQt5.QtCore import pyqtSignal, QEvent, QObject, QRect
from PyQt5.QtWidgets import QApplication, QDialog, QLineEdit, QMainWindow, QMessageBox, QPushButton, QWidget, QLabel, QVBoxLayout, QScrollArea, QHBoxLayout, QGridLayout, QAction
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
    def __init__(self, api_key):
        super().__init__()
        self.setWindowTitle("Good Youtube")
        self.buttons = []
        youtube_parser = YouTubeChannelsParser(api_key)
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


class WindowToSetKey(QDialog):
    """Диалоговое окно для ввода ключа апи."""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Key Editor")
        self.setFixedSize(350, 110)
        self.api_key = 0
        #Подчказка для ввода текста.
        self.prompt = QLabel(self)
        self.prompt.setText("Введите ключ апи, чтобы смортеть видео:")
        self.prompt.move(10, 10)
        #Поле для ввода ключа.
        self.led_api_key = QLineEdit(self)
        self.led_api_key.move(10, 30)
        #Кнопка для сохранения ключа.
        self.btn_to_set_api = QPushButton("Поставить ключ", self)
        self.btn_to_set_api.clicked.connect(self.get_api_key)
        self.btn_to_set_api.move(10, 60)
        #Ссылка с гайдом для получения ключа.
        self.url_to_guide = QLabel(self)
        self.url_to_guide.setText("<a href=\"https://www.youtube.com/watch?v=pBrbZGF3HEs\">Как получить ключ апи?</a>")
        self.url_to_guide.setOpenExternalLinks(True)
        self.url_to_guide.move(10, 90)
        self.show()        

    def get_api_key(self):
        """Получение ключа из поля для запроса."""
        self.api_key = self.led_api_key.text()
        print(self.api_key)
        #Запись в файл ключа.
        with open("txt_files/api_key.txt", 'w') as file:
            file.write(self.api_key)

        self.destroy()
    

class MainMenu(QWidget):
    """Меню в котором кнопка для того, чтобы поставить ключ и запуска основного окна."""
    def __init__(self):
        super().__init__()
        self.setFixedSize(600, 600)
        self.btn_to_start = QPushButton("Запустить", self)
        self.btn_to_start.setFixedSize(300, 100)
        self.btn_to_start.clicked.connect(self.open_main_content)
        self.btn_to_start.move(150, 200)
        self.btn_to_set_key = QPushButton("Поставить ключ", self)
        self.btn_to_set_key.setFixedSize(300, 100)
        self.btn_to_set_key.clicked.connect(self.open_set_key_win)
        self.btn_to_set_key.move(150, 300)
    
    def open_set_key_win(self):
        """Открытия окна для ввода ключа апи."""
        self.win = WindowToSetKey()
    
    def open_main_content(self):
        """Получение ключа и инициализация контента"""
        with open("txt_files/api_key.txt", 'r') as file:
            api_key = file.readline()

        if api_key == "пустой":
            message = QMessageBox.warning(self, 'Поставьте ключ апи!', 'Поставьте ключ апи')
        else:
            self.destroy()
            self.win_goodtube = ScrollWidget(api_key)
            self.win_goodtube.show()

class ScrollWidget(QWidget):      
    def __init__(self, api_key, parent=None):
        super(ScrollWidget, self).__init__(parent)
        self.initUi(api_key)

    def initUi(self, api_key):
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

        self.widget = GoodYoutubeGUI(api_key)
        self.gridLayout.addWidget(self.widget)
        window_height = len(self.widget.video_links_and_info) * 320
        self.setGeometry(700, 200, 1000, window_height)        


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainMenu()
    window.show()
    sys.exit(app.exec_())