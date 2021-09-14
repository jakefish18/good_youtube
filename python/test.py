import sys
from PyQt5.QtWidgets import QApplication, QDialog, QLabel
from  PyQt5.QtGui import QPixmap

class GoodYoutubeGUI(QDialog):
    def __init__(self):
        super().__init__()
        self.setFixedSize(1000, 1000)
        self.setWindowTitle("Good Youtube")
        self.PATH_TO_IMG = "temp/1.jpg"
        self.pixmap_img = QPixmap(self.PATH_TO_IMG)
        self.generate_content()

    def generate_content(self):
        lbl = QLabel(self)
        lbl.setPixmap(self.pixmap_img)
        lbl.move(0, 150)
 
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GoodYoutubeGUI()
    window.show()
    sys.exit(app.exec_())