from PyQt5.QtWidgets import QDialog, QLineEdit, QMessageBox, QPushButton, QLabel, QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import QPixmap
from pytube import YouTube

from configs_handler import ConfigsHandler
from client import get_good_tube_api_response
from youtube_parser import YouTubeChannelsParser
from video_player import VideoPlayer

class WindowToRegister(QDialog):
    """Диалоговое окно для ввода ключа апи."""
    def __init__(self) -> None:
        super().__init__()
        self.configs_handler = ConfigsHandler()
        self.init_ui()

    def init_ui(self) -> None:
        """Инициализация интерфейса."""
        self.setStyleSheet(open(self.configs_handler.path_to_styles).read())
        self.setWindowTitle("Registration")
        self.setFixedSize(500, 200)
        self.api_key = 0
        #Подчказка для ввода текста.
        self.prompt = QLabel(self)
        self.prompt.setText("Введите ключ апи, логин и пароль, чтобы смотреть видео:")
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
        self.btn_to_set_api.setFixedSize(180, 30)
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
        
        parametrs = {
            'login': login,
            'password': password,
            'api_key': api_key
        }

        response = get_good_tube_api_response('insert_new_user', parametrs)

        response_code = response['response']
        if response_code == 200:
            parametrs = {
                'login': login,
                'password': password
            }

            response = get_good_tube_api_response('generate_token', parametrs)
            response_code = response['response']

            if response_code == 200:
                token = response['token']

                configs_to_add = [
                    ['User_info', 'token', token],
                    ['User_settings', 'video_num_from_channel', '5']
                ]
                
                self.configs_handler.push_data(configs_to_add)
                self.configs_handler.update()

                message = QMessageBox.information(self, 'Успешно!', 'Регистрация прошла успешно, можете запускать!')

            else:                
                message = QMessageBox.warning(self, 'Ошибка!', 'Что-то пошло не так!')

        elif response_code == 402:
            message = QMessageBox.warning(self, 'Ошибка!', 'Некорректный ключ апи!')
            
        elif response_code == 403:
            message = QMessageBox.warning(self, 'Ошибка!', 'Данный логин уже существует!')


class WindowToAuth(QDialog):
    """Окна входа в аккаунт."""
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.configs_handler = ConfigsHandler()

    def init_ui(self):
        self.setStyleSheet(open(self.configs_handler.path_to_styles).read())
        self.setWindowTitle("Log in")
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
        self.btn_to_auth.setFixedSize(150, 30)
        self.btn_to_auth.clicked.connect(self.auth)
        self.btn_to_auth.move(10, 90)
        self.show()

    def auth(self) -> None:
        """Авторизация."""
        login = self.led_login.text()
        password = self.led_password.text()  

        parametrs = {
            'login': login,
            'password': password
        }

        response = get_good_tube_api_response('generate_token', parametrs)

        response_code = response['response']

        if response_code == 200:
            token = response['token']

            configs_to_add = [
                ['User_info', 'token', token],
                ['User_settings', 'video_num_from_channel', '5']
            ]

            self.configs_handler.push_data(configs_to_add) 
            self.configs_handler.update()           
            message = QMessageBox.information(self, 'Успешно!', 'Вы успешно вошли в аккаунт!')

        else:
            message = QMessageBox.warning(self, 'Ошибка!', 'Неправильный логин или пароль!')

class WinSettings(QDialog):
    """Окно с настройками."""
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.configs_handler = ConfigsHandler()

    def init_ui(self):
        self.setStyleSheet(open(self.configs_handler.path_to_styles).read())
        self.setWindowTitle("Settings")
        self.setFixedSize(400, 200)
        self.lbl_video_settings = QLabel(self)
        self.lbl_video_settings.setText("Настройки видео")
        self.lbl_video_settings.move(10, 10)
        #Поле для ввода настройки видео с одного с канала.
        self.led_video_num_from_channel = QLineEdit(self)
        self.led_video_num_from_channel.setFixedSize(300, 20)
        self.led_video_num_from_channel.setPlaceholderText('Количество видео с одного канала...')
        self.led_video_num_from_channel.move(10, 40)
        #Новый раздел.
        self.lbl_profile_settings = QLabel(self)
        self.lbl_profile_settings.setText("Настройки профиля")
        self.lbl_profile_settings.move(10, 70)
        #Поле для ввода логина.
        self.led_login = QLineEdit(self)
        self.led_login.setFixedSize(300, 20)
        self.led_login.setPlaceholderText('Ваш логин...')
        self.led_login.move(10, 100)
        #Поле для ввода ключа.
        self.led_api_key = QLineEdit(self)
        self.led_api_key.setFixedSize(300, 20)
        self.led_api_key.setPlaceholderText('Ключ апи...')
        self.led_api_key.move(10, 130)
        #Кнопка для обновления данных.
        self.btn_update_settings = QPushButton("Обновить настройки", self)
        self.btn_update_settings.setFixedSize(180, 30)
        self.btn_update_settings.clicked.connect(self.update_settings)
        self.btn_update_settings.move(10, 160)
        self.show()

    def update_settings(self) -> bool:
        """Обновление настроек пользователя."""
        video_num_from_channel = self.led_video_num_from_channel.text()
        login = self.led_login.text()
        api_key = self.led_api_key.text()

        #Проверка введенного значения количества видео с канала на число.
        if video_num_from_channel.isdigit():
            configs_to_add = [
                ['User_settings', 'video_num_from_channel', video_num_from_channel]
            ]
            
            self.configs_handler.push_data(configs_to_add)
            self.configs_handler.update()


        else:
            message = QMessageBox.warning(self, 'Ошибка!', 'Неправильное значение числа  видео из канала!')
            return False

        if login:
            token = self.configs_handler.token

            parametrs = {
                'token': token
            }

            response = get_good_tube_api_response('update_user_login', parametrs)
            response_code = response['response']

            if response_code == 401:
                meessage = QMessageBox.warning(self, 'Ошибка!', 'Авторизуйтесь!')
                return False

            elif response_code == 403:
                message = QMessageBox.warning(self, 'Ошибка', 'Логин уже существует!')          
                return False  

        #Проверка ключа на валидабельность.
        if api_key:
            
            #Если все работает, то продолжаем.
            token = self.configs_handler.token

            parametrs = {
                'token': token
            }

            response = get_good_tube_api_response('update_user_api_key', parametrs)
            
            if response == 402:
                message = QMessageBox.warning(self, 'Ошибка!', 'Неправильное значение ключа апи!')
                return False

        message = QMessageBox.information(self, 'Успешно!', 'Настройки обновлены!')
    

class WinAddChannel(QDialog):
    """Окно для ввода канала."""
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.configs_handler = ConfigsHandler()
        
    def init_ui(self):
        """Инициализация окна."""
        self.setStyleSheet(open(self.configs_handler.path_to_styles).read())
        self.setWindowTitle("Add channel")
        self.setFixedSize(490, 160)
        self.prompt = QLabel(self)
        self.prompt.setText('Введите ссылку канала, видео которого\n вы хотите смотреть. Пример:\nhttps://www.youtube.com/channel/UCMcC_43zGHttf9bY-xJOTwA')
        self.prompt.move(10, 10)
        self.led_channel_url = QLineEdit(self)
        self.led_channel_url.setFixedWidth(445)
        self.led_channel_url.move(10, 75)
        self.btn_add_channel = QPushButton("Добавить канал", self)
        self.btn_add_channel.setFixedSize(150, 30)
        self.btn_add_channel.clicked.connect(self.add_channel)
        self.btn_add_channel.move(10, 110)
        self.show()
    
    def add_channel(self):
        """Добавления данных в таблицу."""
        channel_url = self.led_channel_url.text()
        token = self.configs_handler.token

        parametrs = {
            'channel_url': channel_url,
            'token': token
        }

        response = get_good_tube_api_response('add_channel', parametrs)
        response_code = response['response']

        if response_code == 200:
            message = QMessageBox.information(self, 'Успешно!', 'Канала добавлен!')

        elif response_code == 401:
            message = QMessageBox.warning(self, 'Ошибка!', 'Пройдите авторизацию!')

        elif response_code == 404:
            message = QMessageBox.warning(self, 'Ошибка!', 'Вы уже добавили этот канал!')

        elif response_code == 407:
            message = QMessageBox.warning(self, 'Ошибка!', 'Неправильная ссылка на канал!')

class WinDelChannel(QDialog):
    """Класс окна для удаления канала пользователя из таблицы."""
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.configs_handler = ConfigsHandler()

    def init_ui(self):
        self.setStyleSheet(open(self.configs_handler.path_to_styles).read())
        self.setWindowTitle("Del channel")
        self.setFixedSize(490, 160)
        self.prompt = QLabel(self)
        self.prompt.setText("Введите ссылку канала, \nкоторую вы добавляли, чтобы удалить её. Пример:\nhttps://www.youtube.com/channel/UCMcC_43zGHttf9bY-xJOTwA")
        self.prompt.move(10, 10)
        self.led_channel_url = QLineEdit(self)
        self.led_channel_url.setFixedWidth(445)
        self.led_channel_url.move(10, 75)
        self.btn_del_channel = QPushButton("Удалить канал", self)
        self.btn_del_channel.setFixedSize(150, 30)
        self.btn_del_channel.clicked.connect(self.del_channel)
        self.btn_del_channel.move(10, 110)
        self.show()
    
    def del_channel(self):
        """Удаление канала, который лежит в self.led_channel_url."""
        channel_url = self.led_channel_url.text()
        token = self.configs_handler.token

        parametrs = {
            'channel_url': channel_url,
            'token': token
        }

        response = get_good_tube_api_response('del_channel', parametrs)
        response_code = response['response']

        #Вывод сообщения по результату действия.
        if response_code == 200:
            message = QMessageBox.information(self, 'Успешно!', 'Канал удален успешно!')
        
        elif response_code == 401:
            message = QMessageBox.warning(self, 'Ошибка!', 'Авторизуйтесь!')

        elif response_code == 405:
            message = QMessageBox.warning(self, 'Ошибка!', 'Канала нет в вашем списке!')

class WinSearchVideo(QDialog):
    """Класс виджета для поиска видео."""
    
    def __init__(self) -> None:
        super().__init__()

        self.buttons = {}

        self.youtube_parser = YouTubeChannelsParser()
        self.configs_handler = ConfigsHandler()

        self.setStyleSheet(open(self.configs_handler.path_to_styles).read())
        self.init_UI()
        self.show()

    def init_UI(self) -> None:
        """Инициализация интерфейса окна."""
        self.layout_global = QVBoxLayout()
        self.layout_search = QHBoxLayout()

        #Поле для ввода запроса поиска.
        self.led_search = QLineEdit()
        self.led_search.setPlaceholderText('Поиск')

        self.layout_search.addWidget(self.led_search)

        #Кнопка поиска введенного запроса.
        self.btn_search = QPushButton('Поиск')
        self.btn_search.clicked.connect(self._search)

        self.layout_search.addWidget(self.btn_search)

        self.layout_global.addLayout(self.layout_search)
        self.layout_global.addStretch()
        self.setLayout(self.layout_global)

    def _search(self) -> list:
        """Поиск видео по запросу."""
        search_request = self.led_search.text()

        video_info = self.youtube_parser.search(search_request)

        self.youtube_parser.get_videos_prewiew(video_info)

        self.layout_video = QHBoxLayout()

        # Добавление превью видео.
        self.pixmap_prewiew = QPixmap('temp/1.jpg')
        self.lbl_prewiew = QLabel()
        self.lbl_prewiew.setPixmap(self.pixmap_prewiew)
        
        self.layout_video.addWidget(self.lbl_prewiew)

        self.layout_video_text_info = QVBoxLayout()

        # Добавление названия видео.
        video_title = video_info[0][2]
        self.lbl_video_title = QLabel()
        self.lbl_video_title.setText(video_title)
        
        self.layout_video_text_info.addWidget(self.lbl_video_title)

        # Добавление названия канала.
        channel_title = video_info[0][3]
        self.lbl_channel_title = QLabel()
        self.lbl_channel_title.setText(channel_title)

        self.layout_video_text_info.addWidget(self.lbl_channel_title)

        # Добавление даты загрузки.
        publish_date = video_info[0][4]
        publish_date = self._get_date_in_words(publish_date)
        self.lbl_publish_date = QLabel()
        self.lbl_publish_date.setText(publish_date)

        self.layout_video_text_info.addWidget(self.lbl_publish_date)

        #Добавление кнопки запуска видео.
        run_button = QPushButton("Открыть видео")
        run_button.clicked.connect(lambda checked, url=video_info[0][0]: self._open_video(url))
        
        self.layout_video_text_info.addWidget(run_button)

        self.layout_video.addLayout(self.layout_video_text_info)
        
        self.layout_global.addLayout(self.layout_video)

        self.update()
    
    def _open_video(self, url):
        """Открытие видео по ссылке."""
        video_url = YouTube(url).streams.get_by_itag(22).url
        self.video_player = VideoPlayer(video_url)

    def _get_date_in_words(self, date):
        """Получение из такого 2021-08-27: такое 27 августа 2021 года."""
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
