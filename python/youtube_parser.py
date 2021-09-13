import json
import random
import urllib.request


class YouTubeChannelsParser():
    """Класс парсера каналов в файле ютуба."""
    def __init__(self):
        """Инициализация пути к файлу с url, ключа для доступа в юутб, класс для выкачки данных."""
        self.PATH_TO_URLS = "txt_files/urls_to_channels.txt"
        self.API_KEY = "AIzaSyDPRxayW_cIe_8mkhtW-dsknFS46H6opnA"

    def parse(self):
        """Основная функция парсера, которая возвращает список видео."""
        channel_ids = self.get_channels_ids(self.get_channels_urls())
        video_links_and_info = []
        for channel_id in channel_ids:
            channel_id = channel_id.strip()
            video_links_and_info.extend(self.get_all_video_from_channel(channel_id))
        random.shuffle(video_links_and_info)
        return video_links_and_info

    # def get_video_prewiew(self, video_links_and_info):
    #     """Получение ссылок на превью для скачивания."""
    #     for link in video_links_and_info:
    #         video_id = link.split('=')[1]
    #         url = f"https://www.googleapis.com/youtube/v3/videos?id={video_id}&key={self.API_KEY}"
    #         inp = urllib.request.urlopen(url)
    #         resp = json.load(inp)
    #         img_url = resp["videos"]["snippet"]["thumbnails"]["default"] 
            


    def get_channels_urls(self):
        """Получение пяти последних видео с выбранных каналов в файле."""
        with open(self.PATH_TO_URLS, 'r') as file:
            urls_to_channels = file.readlines()
        return urls_to_channels

    def get_channels_ids(self, urls_to_channels):
        """Получение айдишников канала."""
        channel_ids = []
        for url in urls_to_channels:
            channel_id = url.split('/')[-1] #Формат ссылок такой, что в конце стоит айди канала разделенная "/".
            channel_ids.append(channel_id)
        return channel_ids
    
    def get_all_video_from_channel(self, channel_id):
        """Выкачивание видео с канала."""
        base_video_url = "https://www.youtube.com/watch?v="
        base_search_url = "https://www.googleapis.com/youtube/v3/search?"

        url = base_search_url + f"key={self.API_KEY}&channelId={channel_id}&part=snippet,id&order=date&maxResults=5"

        video_links_and_info = []

        inp = urllib.request.urlopen(url)
        resp = json.load(inp)
        for i in resp['items']:
            if i['id']['kind'] == "youtube#video":
                video_links_and_info.append([base_video_url + i['id']['videoId'],
                                    i['id']['videoId'],
                                    i['snippet']['title'],
                                    i['snippet']['channelTitle'],
                                    i['snippet']['publishTime']])

        return video_links_and_info
