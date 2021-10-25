import sys
from PyQt5.QtWidgets import *
import psycopg2

class WinAddChannel(QDialog):
    """Окно для ввода канала."""
    def __init__(self, auth_id):
        """Инициализация окна."""
        super().__init__()
        self.auth_id = auth_id
        self.setWindowTitle("Add channel")
        self.setFixedSize(460, 160)
        self.prompt = QLabel(self)
        self.prompt.setText('Введите ссылку канала, видео которого\n вы хотите смотреть. Пример:\nhttps://www.youtube.com/channel/UCMcC_43zGHttf9bY-xJOTwA')
        self.prompt.move(10, 10)
        self.led_channel_url = QLineEdit(self)
        self.led_channel_url.setFixedWidth(445)
        self.led_channel_url.move(10, 75)
        self.btn_add_channel = QPushButton("Добавить канал", self)
        self.btn_add_channel.clicked.connect(self.add_channel)
        self.btn_add_channel.move(10, 110)
        self.show()
    
    def add_channel(self):
        """Добавления данных в таблицу."""
        channel_url = self.led_channel_url.text()
        try:
            connection = psycopg2.connect(
                host="127.0.0.1",
                user="postgres",
                password="Insaff2006",
                database="postgres" 
             )
             #Добавления ссылки в таблицу.
            with connection.cursor() as cursor:
                cursor.execute(f"select * from channels where channel_url='{channel_url}' and id='{self.auth_id}'")
                if cursor.fetchall():
                    message = QMessageBox(self, 'Ошибка!', 'Этот канал уже добавлен!')
                else:
                    cursor.execute(f"INSERT INTO channels (id, channel_url) VALUES ('{self.auth_id}', '{channel_url}')")


        except Exception as _ex:
            print("[ERROR] Error while working with PostgreSQL", _ex)
        finally:
            if connection:
                connection.commit()
                connection.close()
                self.destroy()
                print("[INFO] PostgreSQL connection closed")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WinAddChannel(1)
    window.show()
    sys.exit(app.exec_())