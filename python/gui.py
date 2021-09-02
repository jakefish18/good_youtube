import sys
import webbrowser

from PyQt5.QtWidgets import QApplication, QDialog, QLabel, QHBoxLayout, QPushButton
from PyQt5.QtGui import QPixmap
from functools import partial

from youtube_parser import YouTubeChannelsParser


class GoodYoutubeGUI(QDialog):
    """Класс графического интерфейса приложения."""
    def __init__(self):
        """Предопределние нужных переменных.ю"""
        super().__init__()
        self.setFixedSize(800, 800)
        self.setWindowTitle("Good Youtube")
        self.video_links = YouTubeChannelsParser().parse()
        self.PATH_TO_IMG = "video_images/youtubebox.jpg"
        self.pixmap_img = QPixmap(self.PATH_TO_IMG)
        self.icons = []
        self.buttons = []
        self.generate_content()

    def generate_buttons_info(self):
        """Уставновка картинок в приложение."""
        buttons_info = {}
        for link in self.video_links:
            button = QPushButton('Открыть видео', self)
            buttons_info[button] = link
        
        return buttons_info

    def generate_content(self):
        """Генерация контента."""
        pos_y = 0
        for button, link in self.generate_buttons_info().items():
            lbl = QLabel(self)
            lbl.setPixmap(self.pixmap_img)
            lbl.move(0, pos_y * 100)
            button.clicked.connect(self.open_page(link))
            button.move(100, pos_y * 100)
            pos_y += 1

    def open_page(self, link):
        return lambda: webbrowser.open(link)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    dlg_main = GoodYoutubeGUI()
    dlg_main.show()
    sys.exit(app.exec_())
