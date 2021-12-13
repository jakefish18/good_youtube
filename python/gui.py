from functools import cached_property
import sys
import threading

import keyring
import configparser

from pytube import YouTube

from PyQt5.QtCore import pyqtSignal, QEvent, QObject, QRect
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox, QPushButton, QWidget, QLabel, QVBoxLayout, QScrollArea, QHBoxLayout, QGridLayout
from  PyQt5.QtGui import QPixmap

from youtube_parser import YouTubeChannelsParser
from table_handlers import UsersHandler, ChannelsHandler
from application_windows import WindowToRegister, WindowToAuth, WinAddChannel, WinDelChannel, WinSettings
from video_player import VideoPlayer

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


class UrlProvider(QObject):
    finished = pyqtSignal(str)

    def find_url(self, url):
        threading.Thread(target=self._find_url, args=(url,), daemon=True).start()

    def _find_url(self, url):
        video_url = YouTube(url).streams.get_by_itag(22).url
        print(video_url)
        self.finished.emit(video_url)


class GoodYoutubeGUI(QDialog):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(open("style.css").read())
        self.setWindowTitle("Good Youtube")
        self.buttons = []
        youtube_parser = YouTubeChannelsParser()
        self.video_links_and_info = youtube_parser.parse()
        self.setFixedHeight(len(self.video_links_and_info) * (180 + 20))
        youtube_parser.get_videos_prewiew(self.video_links_and_info)
        self.url_provider.finished.connect(self.handle_url_finished)
        self.generate_content()

    # def player_manager(self):
    #     return PlayerManager()

    @cached_property
    def url_provider(self):
        return UrlProvider()

    def generate_buttons_info(self):
        buttons_info = {}
        for link in self.video_links_and_info:
            button = QPushButton("Открыть видео", self)
            button.setFixedSize(150, 30)
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
        self.video_player = VideoPlayer(url)
        # self.player_manager.set_media(url)
        # self.player_manager.play()

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


class MainMenu(QWidget):
    """Меню в котором кнопка для того, чтобы поставить ключ и запуска основного окна."""
    def __init__(self):
        super().__init__()
        self.setFixedSize(600, 600)
        self.setStyleSheet(open("style.css").read())
        #Кнопка регистрации.
        self.btn_register = QPushButton("Регистрация", self)
        self.btn_register.setFixedSize(150, 30)
        # self.btn_register.setStyleSheet("background: ")
        self.btn_register.clicked.connect(self.open_registration_win)
        self.btn_register.move(449, 1)
        #Кнопка входа.
        self.btn_autorize = QPushButton("Войти", self)
        self.btn_autorize.setFixedSize(150, 30)
        self.btn_autorize.clicked.connect(self.open_auth_win)
        self.btn_autorize.move(294, 1)
        #Кнопка запуска.
        self.btn_run = QPushButton("Запустить", self)
        self.btn_run.setFixedSize(150, 50)
        # self.btn_run.setStyleSheet("border-radius: 3px; background: orange; color: white;")
        self.btn_run.clicked.connect(self.open_main_content)
        self.btn_run.move(225, 250)
        #Кнопка настроек.
        self.btn_settings = QPushButton("Настройки", self)
        self.btn_settings.setFixedSize(150, 50)
        # self.btn_settings.setStyleSheet("border-radius: 3px; background: orange; color: white;")
        self.btn_settings.clicked.connect(self.open_settings_win)
        self.btn_settings.move(225, 305)
        #Кнопка добавления канала.
        self.btn_add_channel = QPushButton("Добавить канал", self)
        self.btn_add_channel.setFixedSize(150, 50)
        # self.btn_add_channel.setStyleSheet("border-radius: 3px; background: orange; color: white;")
        self.btn_add_channel.clicked.connect(self.open_channel_adding_win)
        self.btn_add_channel.move(225, 360)
        #Кнопка удаления канала.
        self.btn_del_channel = QPushButton("Удалить канал", self)
        self.btn_del_channel.setFixedSize(150, 50)
        # self.btn_del_channel.setStyleSheet("border-radius: 3px; background: orange; color: white;")
        self.btn_del_channel.clicked.connect(self.open_channel_deleting_win)
        self.btn_del_channel.move(225, 415)


    def open_registration_win(self):
        """Открытия окна для регистрации."""
        self.win = WindowToRegister()

    def open_auth_win(self):
        """Открытие окна для входа."""
        self.win = WindowToAuth()
    
    def open_main_content(self):
        """Получение ключа и инициализация контента"""
        configs.read('config.ini')
        user_id = configs['User_info']['id']
        auth_api_key = keyring.get_password('good_tube', user_id)
        if auth_api_key:
            self.destroy()
            self.win_goodtube = ScrollWidget(auth_api_key)
            self.win_goodtube.show()
        else:
            message = QMessageBox.warning(self, 'Войдите в аккаунт!', 'Войдите в аккаунт!')

    def open_settings_win(self):
        """Открытие окна с настройками."""
        configs.read('config.ini')
        user_id = configs['User_info']['id']
        auth_api_key = keyring.get_password('good_tube', user_id)
        if auth_api_key == 0:
            message = QMessageBox.warning(self, 'Войдите в аккаунт!', 'Войдите в аккаунт!')
        
        else:
            self.win = WinSettings()

    def open_channel_adding_win(self):
        """Добавление в таблицу со столбцами каналов новый канал."""
        configs.read('config.ini')
        auth_id = configs['User_info']['id']
        auth_api_key = keyring.get_password('good_tube', auth_id)
        if auth_api_key == 0:
            message = QMessageBox.warning(self, 'Войдите в аккаунт!', 'Войдите в аккаунт!')
        
        else:
            self.win = WinAddChannel()
    
    def open_channel_deleting_win(self):
        """Окно для удаления из таблицы со столбцами каналов введенный канал."""
        configs.read('config.ini')
        id = configs['User_info']['id']
        auth_api_key = keyring.get_password('good_tube', id)
        if auth_api_key == 0:
            message = QMessageBox.warning(self, 'Войдите в аккаунт!', 'Войдите в аккаунт!')
        
        else:
            self.win = WinDelChannel()


class ScrollWidget(QWidget):      
    def __init__(self, api_key, parent=None):
        super(ScrollWidget, self).__init__(parent)
        self.initUi(api_key)

    def initUi(self, api_key):
        self.setStyleSheet(open("style.css").read())
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
    users_handler = UsersHandler()
    channels_handler = ChannelsHandler()
    configs = configparser.ConfigParser()
    app = QApplication(sys.argv)
    window = MainMenu()
    window.show()
    sys.exit(app.exec())