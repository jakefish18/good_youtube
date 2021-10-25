from functools import cached_property
import sys
import threading
import psycopg2

import pafy

import vlc

from PyQt5.QtCore import pyqtSignal, QEvent, QObject, QRect
from PyQt5.QtWidgets import QApplication, QDialog, QInputDialog, QLineEdit, QMainWindow, QMessageBox, QPushButton, QWidget, QLabel, QVBoxLayout, QScrollArea, QHBoxLayout, QGridLayout, QAction
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
        youtube_parser = YouTubeChannelsParser(api_key, auth_id)
        self.video_links_and_info = youtube_parser.parse()
        self.setFixedHeight(len(self.video_links_and_info) * (180 + 20))
        youtube_parser.get_videos_prewiew(self.video_links_and_info)
        self.url_provider.finished.connect(self.handle_url_finished)
        self.generate_content()

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
        self.player_manager = PlayerManager()
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


class WindowToRegister(QDialog):
    """Диалоговое окно для ввода ключа апи."""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Registration")
        self.setFixedSize(400, 200)
        self.api_key = 0
        #Подчказка для ввода текста.
        self.prompt = QLabel(self)
        self.prompt.setText("Введите ключ апи, логин и пароль, чтобы смортеть видео:")
        self.prompt.move(10, 10)
        #Поле для ввода логина.
        self.led_login = QLineEdit(self)
        self.led_login.setPlaceholderText('Логин...')
        self.led_login.move(10, 30)
        #Поле для ввода пароля.
        self.led_password = QLineEdit(self)
        self.led_password.setPlaceholderText('Пароль...')
        self.led_password.setEchoMode(QLineEdit.Password)
        self.led_password.move(10, 60)
        #Поле для ввода ключа.
        self.led_api_key = QLineEdit(self)
        self.led_api_key.setPlaceholderText('Ключ апи...')
        self.led_api_key.setEchoMode(QLineEdit.Password)
        self.led_api_key.move(10, 90)
        #Кнопка для сохранения ключа.
        self.btn_to_set_api = QPushButton("Зарегистрироваться", self)
        self.btn_to_set_api.clicked.connect(self.set_user)
        self.btn_to_set_api.move(10, 120)
        #Ссылка с гайдом для получения ключа.
        self.url_to_guide = QLabel(self)
        self.url_to_guide.setText("<a href=\"https://www.youtube.com/watch?v=pBrbZGF3HEs\">Как получить ключ апи?</a>")
        self.url_to_guide.setOpenExternalLinks(True)
        self.url_to_guide.move(10, 150)
        self.show()        

    def set_user(self):
        """Получение ключа из поля для запроса."""
        login = self.led_login.text()
        password = self.led_password.text()
        api_key = self.led_api_key.text()

        try:
            connection = psycopg2.connect(
                host="ec2-54-170-163-224.eu-west-1.compute.amazonaws.com",
                user="uvdhbagmtheqly",
                password="898ffb10b3a5fbdf59a98f25e7f03ac3ec8a1933edbdb8fde5b262a936f43ae3",
                database="d7kkv7tv2pire0" 
             )
            with connection.cursor() as cursor:
                # Проверка на наличие в бд
                cursor.execute(f"select * from users where login='{login}'")
                if cursor.fetchall():
                    message = QMessageBox.warning(self, 'Ошибка!', 'Данный логин уже существует!')
                else:
                    cursor.execute(f"INSERT INTO users (login, password, api_key) VALUES ('{login}', '{password}', '{api_key}');")


        except Exception as _ex:
            print("[ERROR] Error while working with PostgreSQL", _ex)
        finally:
            if connection:
                connection.commit()
                connection.close()
                self.destroy()
                print("[INFO] PostgreSQL connection closed")

class WindowToAuth(QDialog):
    """Окна входа в аккаунт."""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Registration")
        self.setFixedSize(400, 130)
        self.api_key = 0
        #Подчказка для ввода текста.
        self.prompt = QLabel(self)
        self.prompt.setText("Введите логин и пароль, чтобы войти в аккаунт:")
        self.prompt.move(10, 10)
        #Поле для ввода логина.
        self.led_login = QLineEdit(self)
        self.led_login.setPlaceholderText('Логин...')
        self.led_login.move(10, 30)
        #Поле для ввода пароля.
        self.led_password = QLineEdit(self)
        self.led_password.setPlaceholderText('Пароль...')
        self.led_password.setEchoMode(QLineEdit.Password)
        self.led_password.move(10, 60)
        #Кнопка для входа.
        self.btn_to_auth = QPushButton("Войти", self)
        self.btn_to_auth.clicked.connect(self.auth)
        self.btn_to_auth.move(10, 90)
        self.show()

    def auth(self):
        """Авторизация."""
        login = self.led_login.text()
        password = self.led_password.text()  

        try:
            connection = psycopg2.connect(
                host="ec2-54-170-163-224.eu-west-1.compute.amazonaws.com",
                user="uvdhbagmtheqly",
                password="898ffb10b3a5fbdf59a98f25e7f03ac3ec8a1933edbdb8fde5b262a936f43ae3",
                database="d7kkv7tv2pire0" 
             )
            with connection.cursor() as cursor:
                #Проверка логина и пароля, что они в одной строке.
                try:
                    cursor.execute(f"select * from users where login='{login}'")
                    row = cursor.fetchall()[0]
                    if row[2] == password:
                        #Флаги входа.
                        global auth, auth_id, auth_api_key
                        auth = True
                        auth_id = row[0]
                        auth_api_key = row[3]

                    else:
                        #Окно с уведомлением о неправильном лгине или пароле.
                        message = QMessageBox.warning(self, "Ошибка!", "Неправильный логин или пароль!")

                except:
                    message = QMessageBox.warning(self, "Ошибка!", "Неправильный логин или пароль!")

        except Exception as _ex:
            print("[ERROR] Error while working with PostgreSQL", _ex)

        finally:
            if connection:
                connection.commit()
                connection.close()
                self.destroy()
                print("[INFO] PostgreSQL connection closed")    

class WinAddChannel(QDialog):
    """Окно для ввода канала."""
    def __init__(self, auth_id):
        """Инициализация окна."""
        super().__init__()
        self.auth_id = auth_id
        self.setWindowTitle("Add channel")
        self.setFixedSize(460, 160)
        self.prompt = QLabel(self)
        self.prompt.setText('Введите ссылку канала, видео которого\n вы хотите смотреть. Пример:\nhttps://www.youtube.com/channel/UCMcC_43zGHttf9bY-xJOTwA')
        self.prompt.move(10, 10)
        self.led_channel_url = QLineEdit(self)
        self.led_channel_url.setFixedWidth(445)
        self.led_channel_url.move(10, 75)
        self.btn_add_channel = QPushButton("Добавить канал", self)
        self.btn_add_channel.clicked.connect(self.add_channel)
        self.btn_add_channel.move(10, 110)
        self.show()
    
    def add_channel(self):
        """Добавления данных в таблицу."""
        channel_url = self.led_channel_url.text()
        try:
            connection = psycopg2.connect(
                host="ec2-54-170-163-224.eu-west-1.compute.amazonaws.com",
                user="uvdhbagmtheqly",
                password="898ffb10b3a5fbdf59a98f25e7f03ac3ec8a1933edbdb8fde5b262a936f43ae3",
                database="d7kkv7tv2pire0" 
             )
             #Добавления ссылки в таблицу.
            with connection.cursor() as cursor:
                cursor.execute(f"select * from channels where channel_url='{channel_url}' and id='{self.auth_id}'")
                if cursor.fetchall():
                    message = QMessageBox(self, 'Ошибка!', 'Этот канал уже добавлен!')
                else:
                    cursor.execute(f"INSERT INTO channels (id, channel_url) VALUES ('{self.auth_id}', '{channel_url}')")


        except Exception as _ex:
            print("[ERROR] Error while working with PostgreSQL", _ex)
        finally:
            if connection:
                connection.commit()
                connection.close()
                self.destroy()
                print("[INFO] PostgreSQL connection closed")

class MainMenu(QWidget):
    """Меню в котором кнопка для того, чтобы поставить ключ и запуска основного окна."""
    def __init__(self):
        global auth, auth_id, auth_api_key
        auth_id = None
        auth_api_key = 0
        auth = False 
        super().__init__()
        self.setFixedSize(600, 600)
        #Кнопка регистрации.
        self.btn_register = QPushButton("Регистрация", self)
        self.btn_register.setFixedSize(150, 30)
        self.btn_register.clicked.connect(self.open_registration_win)
        self.btn_register.move(450, 0)
        #Кнопка входа.
        self.btn_autorize = QPushButton("Войти", self)
        self.btn_autorize.setFixedSize(150, 30)
        self.btn_autorize.clicked.connect(self.open_auth_win)
        self.btn_autorize.move(299, 0)
        #Кнопка запуска.
        self.btn_run = QPushButton("Запустить", self)
        self.btn_run.setFixedSize(150, 50)
        self.btn_run.clicked.connect(self.open_main_content)
        self.btn_run.move(225, 250)
        #Кнопка добавления канала.
        self.btn_add_channel = QPushButton("Добавить канал", self)
        self.btn_add_channel.setFixedSize(150, 50)
        self.btn_add_channel.clicked.connect(self.open_channel_adding_win)
        self.btn_add_channel.move(225, 300)

    def open_registration_win(self):
        """Открытия окна для регистрации."""
        self.win = WindowToRegister()

    def open_auth_win(self):
        """Открытие окна для входа."""
        self.win = WindowToAuth()
    
    def open_main_content(self):
        """Получение ключа и инициализация контента"""
        if auth_api_key == 0:
            message = QMessageBox.warning(self, 'Войдите в аккаунт!', 'Войдите в аккаунт!')
        else:
            self.destroy()
            self.win_goodtube = ScrollWidget(auth_api_key)
            self.win_goodtube.show()
        
    def open_channel_adding_win(self):
        """Добавление в таблицу с массивом каналов новый канал."""
        if auth_api_key == 0:
            message = QMessageBox.warning(self, 'Войдите в аккаунт!', 'Войдите в аккаунт!')
        
        else:
            self.win = WinAddChannel(auth_id)

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