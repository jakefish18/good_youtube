from PyQt5.QtWidgets import QDialog, QLineEdit, QMessageBox, QPushButton, QLabel

from configs_handler import ConfigsHandler
from client import get_good_tube_api_response


class WindowToRegister(QDialog):
    """Диалоговое окно для ввода ключа апи."""
    def __init__(self) -> None:
        super().__init__()
        self.configs_handler = ConfigsHandler()
        self.init_ui()

    def init_ui(self) -> None:
        """Инициализация интерфейса."""
        self.setStyleSheet(open("style.css").read())
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
        self.setStyleSheet(open("style.css").read())
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
        self.setStyleSheet(open("style.css").read())
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


        else:
            message = QMessageBox.warning(self, 'Ошибка!', 'Неправильное значение числа  видео из канала!')
            return False

        if login:
            token = self.configs_handler.get_token()

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
            token = self.configs_handler.get_token()

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
        self.config_handler = ConfigsHandler()
        
    def init_ui(self):
        """Инициализация окна."""
        self.setStyleSheet(open("style.css").read())
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
        token = self.config_handler.get_token()

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
        self.setStyleSheet(open("style.css").read())
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
        token = self.configs_handler.get_token()

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