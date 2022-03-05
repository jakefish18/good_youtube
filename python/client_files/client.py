from urllib import response
import requests
import json    


class RequestsHandler():
    """
    Обработка заросов на бекенд и возвращение ответов
    для входа в аккаунт, для регистрации и др.
    """

    def logon(self, login: str, password: str, api_key: str) -> dict:
        """
        Регистрация пользователя.
        Коды возвращаемого словаря:
        200 -> ОК
        402 -> Неправильный ключ API
        403 -> Логин уже существует
        иначе -> Неизвестная ошибка
        """
        
        request_parametrs = {
            'login': login,
            'password': password,
            'api_key': api_key
        }

        response = self._get_good_tube_api_response('insert_new_user', request_parametrs)

        response_code = response['response']
        if response_code == 200:

            request_parametrs = {
                'login': login,
                'password': password
            }

            response = self._get_good_tube_api_response('generate_token', request_parametrs)
            
            return response

        else:
            return response

    def login(self, login: str, password: str) -> dict:
        """
        Обработка запроса на вход.
        Коды возвращаемого словаря:
        200 -> ОК
        406 -> аккаунт не существует
        """
        request_parameters = {
            'login': login,
            'password': password
        }

        response = self._get_good_tube_api_response('generate_token', request_parameters)

        return response
    
    def update_settings(self, login: str, api_key: str, token: str) -> dict:
        """
        Обновление логина или api_key.
        Коды возвращаемого словаря:
        200 -> ОК
        401 -> клиент не авторизован
        402 -> неправильный ключ API
        403 -> логин уже существует
        """
        if login:

            request_parameters = {
                'login': login,
                'token': token
            }

            response = self._get_good_tube_api_response('update_user_login', request_parameters)
            response_code = response['response']

            if response_code != 200:
                return response

        if api_key:
            
            request_parameters = {
                'api_key': api_key,
                'token': token
            }

            response = self._get_good_tube_api_response('update_user_api_key', request_parameters)
            response_code = response['response']

            if response_code != 200:
                return response
        
        return {'response': 200}
    
    def add_channel(self, channel_url: str, token: str):
        """
        Добавление в список каналов пользователя новый канал.
        Коды возвращаемого словаря:
        200 -> ОК
        401 -> клиент не авторизован
        404 -> канал уже был добавлен
        407 -> неправильная ссылка на канал
        """
        request_parameters = {
            'channel_url': channel_url,
            'token': token
        }

        response = self._get_good_tube_api_response('add_channel', request_parameters)
        
        return response
    
    def del_channel(self, channel_url: str, token: str):
        """
        Удаление канала из списка канала пользовтеля.
        Коды возвращаемого словаря:
        200 -> OK
        401 -> клиент не авторизован
        405 -> канал не был добавлен
        """
        request_parameters = {
            'channel_url': channel_url,
            'token': token
        }

        response = self._get_good_tube_api_response('del_channel', request_parameters)

        return response
    
    def get_user_channels_url(self, token: str) -> list:
        """
        Получение списка канала пользователя
        Коды возвращаемого словаря:
        200 -> OK
        401 -> клиент не авторизован
        """
        request_parametrs = {
            'token': token
        }

        response = self._get_good_tube_api_response('channel_list_by_id', request_parametrs)

        return response

    def get_user_api_key(self, token: str) -> str:
        """
        Получения ключа YouTube API пользователя
        Коды возвращаемого словаря:
        200 -> OK
        401 -> клиент не авторизован
        """

        request_parametrs = {
            'token': token
        }

        response = self._get_good_tube_api_response('get_user_api_key', request_parametrs)

        return response

    def _get_good_tube_api_response(self, task: str, parameters: dict) -> dict:    
        """Отправка запроса на API и возвращение результата."""
        base_url = "http://92.255.108.65:12345"
        request = f"{base_url}/{task}"

        print(request, parameters)
        response = requests.get(request, params=parameters)
        
        data = json.loads(response.text)

        return data