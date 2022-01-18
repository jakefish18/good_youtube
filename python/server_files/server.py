import socket
import threading
from urllib import request
from table_handlers import UsersHandler, ChannelsHandler
from Socket import Socket


class RequestAnalyzer():
    """Class for analyze user requests"""
    def __init__(self):
        self.users_handler = UsersHandler()
        self.channels_handler = ChannelsHandler()

    def analyzer(self, request):
        """Data distribution by types."""

        if not request:
            return 'empty'

        request_type, request_task, request_parametrs = request.split()
        
        print(request_type, request_task, request_parametrs)

        if request_type == 'get':
            result = self.get_request_analyzer(request_task, request_parametrs)

        elif request_type == 'push':
            result = self.push_request_analyzer(request_task, request_parametrs)
        
        elif request_type == 'update':
            result = self.update_request_analyzer(request_task, request_parametrs)

        else:
            result = 'empty'

        return result

    def get_request_analyzer(self, request_task, request_parametrs):
        """GET Request proccesing."""
        if request_task == 'channel_list_by_id':
            #Request to get all use channels.
            id, login, password = request_parametrs.split('/')
            print(id, login, password)
            
            if self.users_handler.is_account(login, password):
                channel_list = self.channels_handler.get_channel_list_by_id(id)

                return str(channel_list)

            else:
                return 'Wrong data'
        
        elif request_task == 'user_id_by_login':
            #Request to id by login.
            login = request_parametrs


            if self.users_handler.is_login(login):
                id = self.users_handler.get_user_id_by_login(login)
                return str(id)

            else:
                id = -1
                return '-1'
        
        elif request_task == 'auth_user':
            #Request to get is there transmitted account.
            login, password = request_parametrs.split('/')

            auth_check = self.users_handler.auth_user(login, password)

            return str(auth_check)
        
        elif request_task == 'is_login':
            #Request to get is there transmitted login.
            login = request_parametrs

            check_login = self.users_handler.is_login(login)

            return self._bool_to_string(check_login)
        
        elif request_task == 'user_api_key':
            #Request to get user api key.
            user_id, login, password = request_parametrs.split('/')

            if self.users_handler.is_account(login, password):
                api_key = self.users_handler.get_user_api_key(user_id)
                print(api_key)
                return api_key

            else:
                return '0'

    def push_request_analyzer(self, request_task, request_parametrs):
        """Push requests proccessing"""
        if request_task == 'insert_new_user':
            #Adding new user.
            print(request_task, request_parametrs)
            login, password, api_key = request_parametrs.split('/')

            result = self.users_handler.insert_new_user(login, password, api_key)

            if result:
                return '1'
            
            else:
                return '0'
        
        elif request_task == 'add_chanel':
            #Adding new channel to user channel list.
            user_id, login, password, channel_url = request_parametrs.split('/')

            if self.users_handler.is_account(login, password):
                self.channels_handler.del_channel(user_id, channel_url)
                return '1'
            
            else:
                return '0'

        elif request_task == 'del_channel':
            #Delete channel from user channel list.
            user_id, login, password, channel_url = request_parametrs.split('/')

            if self.users_handler.is_account(login, password):
                self.channels_handler.del_channel(user_id, channel_url)
                return '1'
            
            else:
                return '0'

    def update_request_analyzer(self, request_task, request_parametrs):
        """Update requests proccessing"""
        if request_task == 'user_login':
            #Updating user login.
            user_id, login, password = request_parametrs.split('/')

            if self.users_handler.is_account(login, password):
                self.users_handler.update_user_login(user_id, login)
                return '1'

            else:
                return '0'

            self.users_handler.update_user_login(user_id, login)
        
        elif request_task == 'user_api_key':
            #Updating user api_key.
            user_id, login, password, api_key = request_task.split('/')

            if self.users_handler.is_account(login, password):
                self.users_handler.update_user_api_key(user_id, api_key)
                return '1'

            else:
                return '0'

    def _bool_to_string(self, data):
        """Transformation from bool to string."""
        if data:
            return '1'
        
        else:
            return '0'
    
    def _list_to_string(self, data):
        """Transformation from bool to string."""
        result = ''

        for word in data:
            result += f'{word} '

        return result.rstrip() 


class Server(Socket):
    def __init__(self):
        self.request_analyzer = RequestAnalyzer()

        super(Server, self).__init__()
        self.bind(("92.255.108.65", 12345))

        self.listen(5)
        print("Server is listening")

        self.users = []
    
    def send_data(self, user, data):
        user.send(data.encode('UTF-8'))

    def listen_socket(self, user):
        print("Listening user")

        while True:
            data = user.recv(2048)

            call_back = self.request_analyzer.analyzer(data.decode('utf-8'))
            
            self.send_data(user, call_back)

    def start_server(self):
        while True:
            user_socket, adress = self.accept()
            
            listen_accepted_user = threading.Thread(target=self.listen_socket, args=(user_socket,))
            listen_accepted_user.start()


if __name__ == '__main__':
    server = Server()
    server.start_server()