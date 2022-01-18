import socket


class Client():
    """Подключение к серверу для последующего отправления запросов."""
    
    def __init__(self) -> None:
        self.client = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )

        self.client.connect(('92.255.108.65', 12345))
    
    def send_request(self, message: str) -> None:
        self.client.sendall(message.encode('utf-8'))
    
    def get_response(self) -> str:
        data = self.client.recv(1024)
        data = data.decode('utf-8')

        return data

    def generate_request(self, request_type: str, request_task: str, request_parametrs: tuple) -> str:
        """Создание запроса по переданным параметрам."""
        request_parametrs = '/'.join(request_parametrs)
        request = f"{request_type} {request_task} {request_parametrs}"

        return request