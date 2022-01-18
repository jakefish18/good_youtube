from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, QSlider, QStyle, QSizePolicy
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
