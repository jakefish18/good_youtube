import socket


class Client():
    """Подключение к серверу для последующего отправления запросов."""
    
    def __init__(self) -> None:
        self.client = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )

        self.client.connect(('92.255.108.65', 1234))
    
    def send_request(self, message: str) -> None:
        self.client.sendall(message.encode('utf-8'))
    
    def get_response(self) -> str:
        data = self.client.recv(1024)
        data = data.decode('utf-8')

        return data