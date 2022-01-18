from re import S
import urllib.request
import keyring
import configparser

from PyQt5.QtWidgets import QDialog, QLineEdit, QMessageBox, QPushButton, QLabel

# from python.server_files.table_handlers import UsersHandler, ChannelsHandler
from client import Client

# users_handler = UsersHandler()
# channels_handler = ChannelsHandler()
client = Client()
configs = configparser.ConfigParser()

class WindowToRegister(QDialog):
    """Диалоговое окно для ввода ключа апи."""
    def __init__(self):
        super().__init__()
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

        #Проверка ключа апи на валидабелность на тестовом запросе..
        try:
            url = f"https://www.googleapis.com/youtube/v3/search?key={api_key}&channelId=UCMcC_43zGHttf9bY-xJOTwA&part=snippet,id&order=date&maxResults=5"
            test = urllib.request.urlopen(url)
        
        except:
            message = QMessageBox.warning(self, 'Ошибка!', 'Не правильный ключ апи!')
            return 1

        request = client.generate_request('push', 'insert_new_user', (login, password, api_key))
        client.send_request(request)
        response = int(client.get_response())

        if response:
            request = client.generate_request('get', 'user_id_by_login', (login, ))
            client.send_request(request)
            response = client.get_response()

            id = int(response)

            keyring.set_password('good_tube', str(id), password) #Добавление пароля в пароли системы.

            configs.add_section('User_info')
            configs.set('User_info', 'id', str(id))
            configs.set('User_info', 'login', login)
            configs.add_section('User_settings')
            configs.set('User_settings', 'video_num_from_channel', '5')

            with open('config.ini', 'w') as file:
                configs.write(file)
            
            message = QMessageBox.information(self, 'Успешно!', 'Регистрация прошла успешно!')
            return 2

        else:
            message = QMessageBox.warning(self, 'Ошибка!', 'Данный логин уже существует!')
            return 3


class WindowToAuth(QDialog):
    """Окна входа в аккаунт."""
    def __init__(self):
        super().__init__()
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

    def auth(self):
        """Авторизация."""
        login = self.led_login.text()
        password = self.led_password.text()  

        request = f'get auth_user {login}_{password}'
        request = client.generate_request('get', 'auth_user', (login, password))
        client.send_request(request)
        auth_info = eval(client.get_response())
        
        if auth_info:
            auth_id, auth_api_key = auth_info
            auth_id = str(auth_id)

            keyring.set_password('good_tube', auth_id, password)

            configs.add_section('User_info')
            configs.set('User_info', 'id', str(auth_id))
            configs.set('User_info', 'login', login)
            configs.add_section('User_settings')
            configs.set('User_settings', 'video_num_from_channel', '5')

            with open('config.ini', 'w') as file:
                configs.write(file)
            
            message = QMessageBox.information(self, 'Успешно!', 'Вы успешно вошли в аккаунт!')
            return 0

        else:
            message = QMessageBox.warning(self, 'Ошибка!', 'Неправильный логин или пароль!')
            return 1

class WinSettings(QDialog):
    """Окно с настройками."""
    def __init__(self):
        super().__init__()
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

    def update_settings(self):
        """Обновление настроек пользователя."""
        video_num_from_channel = self.led_video_num_from_channel.text()
        login = self.led_login.text()
        api_key = self.led_api_key.text()

        #Проверка введенного значения количества видео с канала на число.
        if video_num_from_channel.isdigit():
            configs.read('config.ini')
            configs['User_settings']['video_num_from_channel'] = video_num_from_channel

        else:
            message = QMessageBox.warning(self, 'Ошибка!', 'Неправильное значение числа  видео из канала!')
            return 1

        if login:
            request = client.generate_request('get', 'is_login', (login, ))
            client.send_request(request)
            response = int(client.get_response())

            user_id = configs['User_info']['id']
            password = keyring.get_password('good_tube', user_id)

            request = client.generate_request('update', 'user_login', (user_id, login, password))
            client.send_request(request)
            response = client.get_response()

            if response == '1':
                configs['User_info']['login'] = login

            else:
                meessage = QMessageBox.warning(self, 'Ошибка!', 'Что-то пошло не так!')
                return 4

        #Проверка ключа на валидабельность.
        if api_key:
            
            try: 
                url = f"https://www.googleapis.com/youtube/v3/search?key={api_key}&channelId=UCMcC_43zGHttf9bY-xJOTwA&part=snippet,id&order=date&maxResults=5"
                test = urllib.request.urlopen(url)
                #Если все работает, то продолжаем.
                configs.read('config.ini')

                user_id = configs['User_info']['id']
                login = configs['User_info']['login']
                
                password = keyring.get_password('good_tube', user_id)

                request = client.generate_request('update', 'user_api_key', (user_id, login, password, api_key))
                client.send_request(request)
                response = client.get_response()
                
                if response != '1':
                    QMessageBox.warning(self, 'Ошибка!', 'Что-то пошло не так!')
                    return 5
                # users_handler.update_user_api_key(user_id, api_key)

            except:
                message = QMessageBox.warning(self, 'Ошибка!', 'Неправильное значение ключа апи!')
                return 3
        
        with open("config.ini", 'w') as file:
            configs.write(file)

        message = QMessageBox.information(self, 'Успешно!', 'Настройки обновлены!')
    

class WinAddChannel(QDialog):
    """Окно для ввода канала."""
    def __init__(self):
        """Инициализация окна."""
        super().__init__()
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
        raise NotImplementedError()
        # channel_url = self.led_channel_url.text()
        # configs.read('config.ini')
        # user_id = configs['User_info']['id']
        # # api_key = keyring.get_password('good_tube', user_id)
        # #Проверка на правильность channel_id при помощи тестового запроса.
        # try:
        #     channel_id = channel_url.split('/')[-1] #Получение id в ссылке.
        #     url = f"https://www.googleapis.com/youtube/v3/search?key={api_key}&channelId={channel_id}&part=snippet,id&order=date&maxResults=5"
        #     test = urllib.request.urlopen(url)
        # except:
        #     message = QMessageBox.warning(self, 'Ошибка!', 'Неправильная ссылка!')
        #     return 1
    
        # # if channels_handler.add_channel(user_id, channel_url):
        #     # message = QMessageBox.information(self, 'Успешно!', 'Канала добавлен!')
        # # else:
        #     # message = QMessageBox.warning(self, 'Ошибка!', 'Вы уже добавили этот канал!')


class WinDelChannel(QDialog):
    """Класс окна для удаления канала пользователя из таблицы."""
    def __init__(self):
        super().__init__()
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
        return NotImplementedError()
        # """Удаление канала, который лежит в self.led_channel_url."""
        # configs.read('config.ini')
        # user_id = configs['User_info']['id']
        # channel_url = self.led_channel_url.text()

        # #Вывод сообщения по результату действия.
        # if channels_handler.del_channel(id, channel_url):
        #     message = QMessageBox.information(self, 'Успешно!', 'Канал удален успешно!')
        
        # else:
        #     message = QMessageBox.warning(self, 'Ошибка!', 'Канала нет в вашем списке!')
