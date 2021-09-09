import pafy
import vlc

class VideoPlayer():
    """Медиа плеер для открытия видео в потоке."""
    def __init__(self, video_url):
        self.video_url = video_url
    
    def play_video(self):
        """Запуск видео вместе с потоком."""

        video = pafy.new(self.video_url)
        best = video.getbest()
        media = vlc.MediaPlayer(best.url)
        media.play()
        while media.get_state() != vlc.State.Ended:
                continue

        media.stop()


if __name__ == '__main__':
    player = VideoPlayer("https://www.youtube.com/watch?v=zPA2Een1EQA")
    player.play_video()
    print(1)
    while True:
        print(1)

