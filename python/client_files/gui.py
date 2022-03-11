import sys
import threading

from pytube import YouTube

from PyQt5.QtCore import pyqtSignal, QObject, QPropertyAnimation, QEasingCurve, QSize, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QMessageBox, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QFrame
from PyQt5.QtGui import QIcon, QPixmap

from configs_handler import ConfigsHandler
from qt_designer_interfaces.main_window import Ui_MainWindow
from qt_designer_interfaces.welcome_window import Ui_welcome_window
from qt_designer_interfaces.logon import Ui_form_logon
from qt_designer_interfaces.login import Ui_form_login
from qt_designer_interfaces.message_window import Ui_Message
from client import RequestsHandler
from youtube_parser import YouTubParser
from video_player import VideoPlayer


class AppLogic():
    """
    Логика приложения: открытие окон вначале, 
    закрытие одного окна и открытие другого.
    """

    def __init__(self) -> None:
        self.configs_handler = ConfigsHandler()
        self.request_handler = RequestsHandler()

        self.response_messages = { # Коды возвращаемого json с API.
            200: "Успешно!",
            401: "Неправильный токен. Перезайдите в аккаунт!",
            402: "Неправильный ключ API",
            403: "Логин уже занят",
            404: "Канал уже существует в вашем списке",
            405: "Канал не существует в вашем списке",
            406: "Аккаунт не существует",
            407: "Неправильная ссылка на канал",
            408: "Короткий логин",
            409: "Короткйи пароль"
        }

        #Открытие окна.
        win_num = self._define_window() 
        self._open_first_window(win_num)

    def _define_window(self) -> int:
        """
        Выбор окна при запуска по наличию токена от аккаунта.
        Функия возвращает 1 -> открытие окна главного контента,
        функция возвращает 2 -> открытие окна выбора входа или регистрации. 
        """

        token = self.configs_handler.token

        return 1 if token else 2

    def _open_first_window(self, win_num: int) -> None:
        """Открытие окна по номеру."""    
        if win_num == 1:
            self._open_main_window()

        elif win_num == 2:
            self._open_welcome_window()
    
    def _open_main_window(self) -> None:
        """Открытие главного окна."""
        user_api_key = self._get_user_api_key()
        print(user_api_key)
        self.youtube_parser = YouTubParser(user_api_key) # Инициализация класса парсера YouTube.

        self.ui_main_window = Ui_MainWindow()
        self.main_window = QMainWindow()
        self.ui_main_window.setupUi(self.main_window)
        self._show_login_to_user()

        # self.ui_main_window.btn_search.clicked.connect(sel) TODO: search function
        self.ui_main_window.btn_menu.clicked.connect(self._slide_menu)
        self.ui_main_window.btn_update_settings.clicked.connect(self._update_settings)
        self.ui_main_window.btn_add_channel.clicked.connect(self._add_channel)
        self.ui_main_window.btn_del_channel.clicked.connect(self._del_channel)

        self._generate_videos()
        
        self.main_window.show()

    def _show_login_to_user(self) -> None:
        """Вставка логина пользователя в правый верхний угол окна."""
        token = self.configs_handler.token
        response = self.request_handler.get_user_login(token)
        response_code = response['response']

        if response_code == 200:
            login = response['login']
            self.ui_main_window.lbl_account_info.setText(login)

        else:
            self._show_message(self.response_messages[response_code])

    def _generate_videos(self) -> None:
        """
        Генерирование видео с выбранных каналов пользователя.
        """

        # Инициализация данных о видео.
        video_links_and_info = self._get_video_links_and_info() 
        self.youtube_parser.get_videos_preview(video_links_and_info)

        video_column_num = 0
        video_row_num = 0

        for video_link_and_info in video_links_and_info:
            
            video_layout = QHBoxLayout() # Макет блока видео. Слева распологается превью видео, справа информация о видео.

            video_link, video_id, video_title, channel_title, publish_time = video_link_and_info

            # Создание превью видео и добавление в макет.
            path_to_video_preview = f"temp/{video_id}.jpg"
            pxm_prewiew = QPixmap(path_to_video_preview)
            lbl_video_preview = QLabel()
            lbl_video_preview.setMinimumSize(320, 180)
            lbl_video_preview.setPixmap(pxm_prewiew)

            video_layout.addWidget(lbl_video_preview)

            video_text_info_layout = QVBoxLayout()

            # Обрезание названия видео, если оно больше 85 символов и добавление троеточия в конце.
            video_title = video_title[:82] + '...' if len(video_title) > 85 else video_title

            lbl_video_title = QLabel()
            lbl_video_title.setWordWrap(True)
            lbl_video_title.setText(video_title)
            lbl_video_title.setMaximumWidth(200)

            video_text_info_layout.addWidget(lbl_video_title)

            lbl_channel_title = QLabel()
            lbl_channel_title.setWordWrap(True)
            lbl_channel_title.setText(channel_title)
            lbl_channel_title.setMaximumWidth(200)                          
        
            video_text_info_layout.addWidget(lbl_channel_title)

            normal_date = self._get_normal_date(publish_time)
            lbl_published_date = QLabel()
            lbl_published_date.setWordWrap(True)
            lbl_published_date.setText(normal_date)
            lbl_published_date.setMaximumWidth(200)

            video_text_info_layout.addWidget(lbl_published_date)

            btn_open_video = QPushButton("Открыть видео")
            print(video_link)
            btn_open_video.clicked.connect(lambda video_link=video_link: self._open_video(video_link))

            video_text_info_layout.addWidget(btn_open_video)

            video_layout.addLayout(video_text_info_layout)

            self._add_video_layout(video_layout, video_row_num, video_column_num)
            
            video_column_num += 1 # Увеличивание столбца видео после каждого добавления.
            video_row_num += video_column_num // 3 # Увеличивание номера ряда, если номер столбца достиг 3, т.к. в одном ряду 3 элемента
            video_column_num %= 3 # Если номер столбца был равен 3, то он обновляется обратно в 0
            
    def _add_video_layout(self, video_layout: QHBoxLayout, row_num: int, column_num: int) -> None:
            """
            Добавление макета с видео на главное окно.
            """
            self.frame = QFrame(self.ui_main_window.scrollAreaWidgetContents)
            self.frame.setMaximumSize(QSize(520, 200))
            self.frame.setMinimumSize(QSize(520, 200))
            self.frame.setLayout(video_layout)
            self.frame.setContentsMargins(0, 0, 0, 0)

            self.ui_main_window.gridLayout_2.addWidget(self.frame, row_num, column_num, 1, 1)
            

    def _get_normal_date(self, date):
        """Получение из такого 2021-08-27 в такое 27 августа 2021 года."""
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

    def _get_video_links_and_info(self) -> list:
        """Получение списка каналов пользователя"""
        user_channels_url = self._get_user_channels_url()
        video_links_and_info = self.youtube_parser.parse(user_channels_url)

        return video_links_and_info

    def _get_user_channels_url(self) -> list:
        token = self.configs_handler.token
        
        response = self.request_handler.get_user_channels_url(token) # Запрос на API на получение списка каналов пользователя.
        response_code = response['response']

        if response_code == 200:
            user_channels_url = response['channels_list']           

        else:
            user_channels_url = []

        return user_channels_url 

    def _get_user_api_key(self) -> str:
        """Получение ключа YouTube API пользователя."""
        token = self.configs_handler.token

        response = self.request_handler.get_user_api_key(token) # Запрос на API на получение ключа YouTube API пользователя.
        response_code = response['response']

        if response_code == 200:
            user_api_key = response['api_key']

        else:
            user_api_key = ""
        
        return user_api_key
    
    def _open_video(self, video_page_url: str) -> None:
        """Открытие видео по ссылке."""
        video_page_url = "https://www.youtube.com/watch?v=TX81PMeAwwU"
        video_url = YouTube(video_page_url).streams.get_by_itag(85).url
        self.player = VideoPlayer(video_url)

    def _slide_menu(self) -> None:
        """Выдвижени или закрытие меню в зависимости от его прошлого состояния."""
        width = self.ui_main_window.frame_left_menu_container.width()
        if width == 0: # Увеличение меню, если он закрыт.
            new_width = 260
            self.ui_main_window.btn_menu.setIcon(QIcon('icons/стрелка влево.png'))
            print(new_width)
        else: # Уменьшение меню, если он открыт.
            new_width = 0
            self.ui_main_window.btn_menu.setIcon(QIcon('icons/меню.png'))

        # Анимация закрытия или открытия.
        self.animation = QPropertyAnimation(self.ui_main_window.frame_left_menu_container, b'maximumWidth')
        self.animation.setDuration(250)
        self.animation.setStartValue(width)
        self.animation.setEndValue(new_width)
        self.animation.setEasingCurve(QEasingCurve.InOutQuart)
        self.animation.start()

    def _update_settings(self) -> None:
        """Обновление настроек пользователя."""
        login = self.ui_main_window.led_login.text()
        api_key = self.ui_main_window.led_api_key.text()
        token = self.configs_handler.token

        response = self.request_handler.update_settings(login, api_key, token)
        response_code = response['response']

        self._show_message(self.response_messages[response_code])

    def _add_channel(self) -> None:
        """Добавление канала в список каналов."""
        channel_url = self.ui_main_window.led_add_channel.text()
        token = self.configs_handler.token        

        response = self.request_handler.add_channel(channel_url, token)
        response_code = response['response']

        self._show_message(self.response_messages[response_code])

    def _del_channel(self) -> None:
        """Удаление канала со списка каналов."""
        channel_url = self.ui_main_window.led_del_channel.text()
        token = self.configs_handler.token

        response = self.request_handler.del_channel(channel_url, token)
        response_code = response['response']

        self._show_message(self.response_messages[response_code])

    def _open_welcome_window(self) -> None:
        """Открытие приветственного окна."""
        self.ui_welcome_window = Ui_welcome_window()
        self.welcome_window = QDialog()
        self.ui_welcome_window.setupUi(self.welcome_window)
        
        self.ui_welcome_window.btn_login.clicked.connect(self._open_login_window)
        self.ui_welcome_window.btn_logon.clicked.connect(self._open_logon_window)

        self.welcome_window.show()

    def _open_logon_window(self) -> None:
        """Открытие окна для регистрации."""
        self.ui_logon_window = Ui_form_logon()
        self.logon_window = QDialog()
        self.ui_logon_window.setupUi(self.logon_window)

        self.ui_logon_window.btn_logon.clicked.connect(self._logon)

        self.logon_window.show()
    
    def _logon(self) -> None:
        """Обработка регистрации."""
        login = self.ui_logon_window.led_login.text()
        password = self.ui_logon_window.led_password.text()
        api_key = self.ui_logon_window.led_api_key.text()
        
        response = self.request_handler.logon(login, password, api_key)
        response_code = response['response']

        if response_code == 200:
            token = response['token']

            configs_to_add = [
                ['User_info', 'token', token],
                ['User_settings', 'video_num_from_channel', '5'],
                ['User_settings', 'path_to_styles', 'styles/style.css']
            ]
            
            self.configs_handler.push_data(configs_to_add)
            self.configs_handler.update()

            self._switch_to_main_window()
        
        else:
            self._show_message(self.response_messages[response_code])

        

    def _open_login_window(self) -> None:
        """Открытие окна для входа."""
        self.ui_login_window = Ui_form_login()
        self.login_window = QDialog()
        self.ui_login_window.setupUi(self.login_window)
        
        self.ui_login_window.btn_login.clicked.connect(self._login)
        
        self.login_window.show()
    
    def _login(self) -> None:
        """Обработка входа."""
        login = self.ui_login_window.led_login.text()
        password = self.ui_login_window.led_password.text()

        response = self.request_handler.login(login, password)
        response_code = response['response']

        if response_code == 200:
            token = response['token']

            configs_to_add = [
                ['User_info', 'token', token],
                ['User_settings', 'video_num_from_channel', '5'],
                ['User_settings', 'path_to_styles', 'styles/style.css']
            ]

            self.configs_handler.push_data(configs_to_add) 
            self.configs_handler.update_variables()           

            self._switch_to_main_window()

        else:
            self._show_message(self.response_messages[response_code])

    def _show_message(self, message: str) -> None:
        """Открытие окна с введенным сообщением."""
        self.ui_message_window = Ui_Message()
        self.message_window = QDialog()
        self.ui_message_window.setupUi(self.message_window)
        self.ui_message_window.lbl_message_text.setText(message)
        self.ui_message_window.btn_exit.clicked.connect(self.message_window.close)
        self.message_window.show()

    def _switch_to_main_window(self) -> None:
        """Закрытие всех окон и открытие главного окна."""
        app.closeAllWindows()
        self._open_main_window()
    
    def _switch_to_welcome_window(self) -> None:
        """
        Закрытие всех окон и переход на приветственное окно
        выбор входа или регистрации.
        """
        app.closeAllWindows()
        self._open_welcome_window()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app_logic = AppLogic()
    sys.exit(app.exec())