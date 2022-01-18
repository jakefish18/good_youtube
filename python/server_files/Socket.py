import socket


class Socket(socket.socket):
    """Общий класс сокета для сервера и клиента."""
    def __init__(self):
        super(Socket, self).__init__(
            socket.AF_INET,
            socket.SOCK_STREAM
        )
    
    def send_data(self):
        raise NotImplementedError()
    
    def listen_socket(self):
        raise NotImplementedError()