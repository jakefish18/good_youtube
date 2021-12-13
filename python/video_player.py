import sys

from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, \
    QSlider, QStyle, QSizePolicy, QApplication
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtGui import QPalette
from PyQt5.QtCore import Qt, QUrl, QEvent

class VideoPlayer(QWidget):
    def __init__(self, video_url):
        super().__init__()

        self.video_url = video_url

        self.setWindowTitle("PyQt5 Media Player")
        self.setGeometry(350, 100, 700, 500)
        self.installEventFilter(self)

        p =self.palette()
        p.setColor(QPalette.Window, Qt.black)
        self.setPalette(p)

        self.init_ui()
        
        self.show()
 
 
    def init_ui(self):
 
        #Медиаплеер.
        self.media_player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.media_player.setMedia(QMediaContent(QUrl(self.video_url)))

        #Вывод видео.
 
        videowidget = QVideoWidget()
 
        #Кнопка для запуска и паузы.
        self.playBtn = QPushButton()
        self.playBtn.setEnabled(True)
        self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playBtn.clicked.connect(self.play_video)
 
 
 
        #Перемотка видео.
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0,0)
        self.slider.sliderMoved.connect(self.set_position)
 
 
 
        #Место кнопок управления.
        self.label = QLabel()
        self.label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
 
 
        #Лэйаут кнопок управления.
        hboxLayout = QHBoxLayout()
        hboxLayout.setContentsMargins(0,0,0,0)
 
        hboxLayout.addWidget(self.playBtn)
        hboxLayout.addWidget(self.slider)
 
 
 
        #Лэйаут меню управления и плеера.
        vboxLayout = QVBoxLayout()
        vboxLayout.addWidget(videowidget)
        vboxLayout.addLayout(hboxLayout)
        vboxLayout.addWidget(self.label)
 
 
        self.setLayout(vboxLayout)
 
        self.media_player.setVideoOutput(videowidget)
 
 
        #Подключение функций по нажатию кнопок
 
        self.media_player.stateChanged.connect(self.mediastate_changed)
        self.media_player.positionChanged.connect(self.position_changed)
        self.media_player.durationChanged.connect(self.duration_changed)
 
    def play_video(self):
        if self.media_player.state() == QMediaPlayer.PlayingState:
            self.media_player.pause()
 
        else:
            self.media_player.play()
 
 
    def mediastate_changed(self, state):
        if self.media_player.state() == QMediaPlayer.PlayingState:
            self.playBtn.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPause)
 
            )
 
        else:
            self.playBtn.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPlay)
 
            )
 
    def position_changed(self, position):
        self.slider.setValue(position)
 
 
    def duration_changed(self, duration):
        self.slider.setRange(0, duration)
 
 
    def set_position(self, position):
        self.media_player.setPosition(position)
 
 
    def handle_errors(self):
        self.playBtn.setEnabled(False)
        self.label.setText("Error: " + self.media_player.errorString())
    
    def eventFilter(self, obj, event):
        if event.type() == QEvent.Close:
            self.media_player.stop()

        return super().eventFilter(obj, event)

app = QApplication(sys.argv)

h = VideoPlayer("https://r1---sn-045oxu-045k.googlevideo.com/videoplayback?expire=1639419325&ei=XTm3YZ7cK5av7QTyvJX4CQ&ip=81.30.199.142&id=o-ADTeDnDMU0umLiE1IkzTQDP8RFOlljOho4OQTUMelh3L&itag=22&source=youtube&requiressl=yes&mh=xa&mm=31%2C29&mn=sn-045oxu-045k%2Csn-ixh7rn76&ms=au%2Crdu&mv=m&mvi=1&pl=24&initcwndbps=1876250&vprv=1&mime=video%2Fmp4&cnr=14&ratebypass=yes&dur=1442.446&lmt=1638183301035338&mt=1639397349&fvip=1&fexp=24001373%2C24007246&c=ANDROID&txp=4432434&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cvprv%2Cmime%2Ccnr%2Cratebypass%2Cdur%2Clmt&sig=AOq0QJ8wRQIgBqhfIpclqk7IDrwv3A_LL1gEGFk26f-DlC2U_n5dfcMCIQC-xjne77Yg-UmicZKxHIgcFcR6B00FscB1v11o4YMqBw%3D%3D&lsparams=mh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Cinitcwndbps&lsig=AG3C_xAwRQIgfWQbCpxiXNgnn-spmAW5-hd477n2mA97e_eThs7ExMkCIQDhCx0XDpKRIgX_wlMJebF3P2gTkFPj6bdNT7iaUoo_MQ%3D%3D")
print('finished')
v = VideoPlayer("https://r3---sn-045oxu-045k.googlevideo.com/videoplayback?expire=1639419311&ei=Tzm3YeSQLsuIpAT3iop4&ip=81.30.199.142&id=o-AMpuYjilV2X0d1rAOL-r8hoOZJZ_Uwjh4mO5ozX_eTXS&itag=22&source=youtube&requiressl=yes&mh=Kv&mm=31%2C29&mn=sn-045oxu-045k%2Csn-ixh7rn76&ms=au%2Crdu&mv=m&mvi=3&pl=24&initcwndbps=1876250&vprv=1&mime=video%2Fmp4&cnr=14&ratebypass=yes&dur=788.549&lmt=1638626415154576&mt=1639397349&fvip=5&fexp=24001373%2C24007246&c=ANDROID&txp=5535432&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cvprv%2Cmime%2Ccnr%2Cratebypass%2Cdur%2Clmt&sig=AOq0QJ8wRgIhANDoW2DyaOb1vltkhr36OQRCEtFsKDgJF9-wAnbdvh2HAiEAzwlbVL5n4SAfPozISsg3wLtrqa9wrtcw-0oyyEXZmy4%3D&lsparams=mh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Cinitcwndbps&lsig=AG3C_xAwRQIhANhGgJfh8ZmXNkRgs0qIGxin2d0N6XVVOyGZIpwPpvh3AiBzA6Yl9aFQC7N7XRE4cxvPd6vG3y5Y2C8nfxsM64JjDQ%3D%3D")

sys.exit(app.exec())