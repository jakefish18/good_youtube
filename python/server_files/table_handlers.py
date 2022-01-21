import psycopg2
import random

class TableHandler():
    """Общий класс в котором есть подключение к базе данных."""
    def __init__(self):
        """Подключение к базе данных."""
        self.connection = psycopg2.connect(
            host="ec2-54-170-163-224.eu-west-1.compute.amazonaws.com",
            user="uvdhbagmtheqly",
            password="898ffb10b3a5fbdf59a98f25e7f03ac3ec8a1933edbdb8fde5b262a936f43ae3",
            database="d7kkv7tv2pire0" 
        )
    
    def select_execute(self, command: str):
        """Возвращение результата select запроса."""
        with self.connection.cursor() as cursor:
            cursor.execute(command)
            return cursor.fetchall()
    
    def table_update_execute(self, command: str):
        """Выполенение sql комманды и изменение таблицы."""
        with self.connection.cursor() as cursor:
            cursor.execute(command)
            self.connection.commit()

    def close(self):
        """Закрытие соединения с базой данных."""
        self.connection.close()

class UsersHandler(TableHandler):
    """Класс для работы с таблицой users."""
    def __init__(self):
        super().__init__()

    def is_login(self, login: str) -> bool:
        """Проверка на налчие данного логина в таблице users."""
        check = self.select_execute(f"select * from users where login='{login}'")
        #Проверка на наличие подходящих результатов.
        if check:
            return True
                 
        else:
            return False        
    
    def is_account(self, login: str, password: str) -> bool:
        """Проверка пароля пользователя по логину."""
        check = self.select_execute(f"select * from users where login='{login}'")

        #Проверка на наличие подходящих результатов.
        if check and check[0][2] == password:
            return True
        
        else:
            return False

    def update_user_login(self, id: str, new_login: str):
        """Изменение значения логина пользователя."""
        self.table_update_execute(f"UPDATE users SET login='{new_login}' where id='{id}'")
    
    def update_user_api_key(self, id, new_api_key):
        """Изменение значения ключа апи пользователя."""
        self.table_update_execute(f"UPDATE users SET api_key='{new_api_key}' where id='{id}'")

    def insert_new_user(self, login, password, api_key):
        """Добавление нового пользователя в таблицу."""
        if not self.is_login(login):
            self.table_update_execute(f"INSERT INTO users (login, password, api_key) VALUES('{login}', '{password}', '{api_key}')")
            return True
        else:
            return False
        
    def auth_user(self, login: str, password: str) -> bool:
        """Авторизация, проверка на наличие такого логина и пароля."""
        #Проверка на наличие логина.
        if self.is_login(login):

            user_info = self.select_execute(f"select * from users where login='{login}'")[0]

            #Проверка на наличие пароля.
            if user_info[2] == password:
                return True

            else:
                return False

        else:
            return False

    def get_user_id_by_login(self, login: str) -> str:
        """Получение id пользователя по его логину."""
        result = self.select_execute(f"select * from users where login='{login}'")[0]

        return result[0]
    
    
    def get_user_api_key(self, user_id: str) -> str:
        """Получение ключа апи пользователя по его id."""
        result = self.select_execute(f"select * from users where id='{user_id}'")[0]

        return result[3]

class ChannelsHandler(TableHandler):
    """Класс для работы с таблицой channels."""
    def __init__(self):
        super().__init__()
    
    def _is_channel_url_by_id(self, id, channel_url):
        """Проверка на наличие channel_url у id."""
        if self.select_execute(f"select * from channels where channel_url='{channel_url}' and id='{id}'"):
            return True
        else:
            return False

    def get_channel_list(self, id):
        """Получение списка каналов y id."""
        channel_list = self.select_execute(f"select channel_url from channels where id='{id}'")
        channel_list = [url[0] for url in channel_list] # Преобразование из [(url), (url), (url)] в [url, url, url].
        return channel_list
    
    def add_channel(self, id, channel_url):
        """Добавление в таблицу channel_url к id."""
        #Проверка на наличие такого же значения в таблице.
        if not self._is_channel_url_by_id(id, channel_url):
            self.table_update_execute(f"INSERT INTO channels (id, channel_url) VALUES ('{id}', '{channel_url}')")
            return True
        else:
            return False
    
    def del_channel(self, id: str, channel_url: str) -> bool:
        """Удаление из таблицы channel_url по id."""
        if self._is_channel_url_by_id(id, channel_url):
            self.table_update_execute(f"DELETE from channels where id='{id}' and channel_url='{channel_url}'")
            return True

        else:
            return False

class TokensHandler(TableHandler):
    """Класс для управления токенами пользовтелей."""

    def __init__(self):
        super().__init__()
    
    def add_token(self, user_id: str) -> str:
        """Добавление токена в базу данных."""
        token = self._create_token()

        self.table_update_execute(
            f'INSERT INTO tokens (id, token) VALUES (\'{user_id}\', \'{token}\')'
        )

        return token

    def is_token(self, token: str) -> bool:
        """Проверка на наличие переданного токена."""
        result = self.select_execute(f'select * from tokens where token=\'{token}\'')

        return bool(result) # result будет пустым и возвращать False, если нет токена.
    
    def get_user_id(self, token: str) -> str:
        """Получение id по переданному токену."""
        user_id = self.select_execute(f'select * from tokens where token=\'{token}\'')[0][0]

        return user_id

    def _create_token(self):
        """Создание токена пользователя для его заросов."""
        small_letters = 'qwertyuiopasdfghjklzxcvbnm'
        big_letters = 'QWERTYUIOPASDFGHJKLZXCVBNM'
        nums = '1234567890'

        all_chars = small_letters + big_letters + nums

        token = random.sample(all_chars, 25)
        token = "".join(token)
        # Генерация нового случайного токена, если такой токен уже существует, пока не создастся не существующий токен. 
        while self.is_token(token): 
            token = random.sample(all_chars, 25)
            token = "".join(token)

        return token
    