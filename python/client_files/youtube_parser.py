import configparser
import json
import random
import urllib.request
import os
import requests
import shutil
import keyring

from html import unescape

from client import Client


class YouTubeChannelsParser():
    """Класс парсера каналов в файле ютуба."""
    def __init__(self):
        """Инициализация пути к файлу с url, ключа для доступа в юутб, класс для выкачки данных."""
        self.configs = configparser.ConfigParser()
        self.configs.read('config.ini')

        self.user_id = self.configs['User_info']['id']
        self.login = self.configs['User_info']['login']
        self.password = keyring.get_password('good_tube', self.user_id)

        self.client = Client()
        print('Ready')
        self.API_KEY = self._get_user_api_key()

    def _get_user_api_key(self):
        """Запрос на сервер для получения ключа для запросов."""

        request = self.client.generate_request('get', 'user_api_key', (self.user_id, self.login, self.password))
        self.client.send_request(request)
        response = self.client.get_response()

        return response

    def parse(self):
        """Основная функция парсера, которая возвращает список видео."""
        channel_ids = self.get_channels_ids(self.get_channels_urls())
        video_links_and_info = []
        for channel_id in channel_ids:
            channel_id = channel_id.strip()
            video_links_and_info.extend(self.get_all_video_from_channel(channel_id))
        random.shuffle(video_links_and_info) # Рандомное расположение ссылок, чтобы в gui не выводились ссылки с одного канала подряд.
        return video_links_and_info

    def get_videos_prewiew(self, video_links_and_info):
        """Получение ссылок на превью для скачивания."""
        order = 1
        # Если папка с превьюшками уже есть, она удаляется.
        try:
            os.mkdir('temp') 
        except FileExistsError:
            shutil.rmtree('temp')
            os.mkdir('temp')

        for link in video_links_and_info:
            video_id = link[1]
            img_url = f"https://img.youtube.com/vi/{video_id}/mqdefault.jpg"
            img_data = requests.get(img_url, allow_redirects=True)

            with open(f'temp/{order}.jpg', 'wb') as handler:
                handler.write(img_data.content)
            order += 1

    def get_channels_urls(self):
        """Получение списка каналов у пользователя под auth_id."""

        request = self.client.generate_request('get', 'channel_list_by_id', (self.user_id, self.login, self.password))
        self.client.send_request(request)
        urls_to_channels = self.client.get_response()

        urls_to_channels = eval(urls_to_channels)

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

        video_num_from_channel = self.configs['User_settings']['video_num_from_channel'] 
        url = base_search_url + f"key={self.API_KEY}&channelId={channel_id}&part=snippet,id&order=date&maxResults={video_num_from_channel}"
        print(url)
        video_links_and_info = []
        inp = urllib.request.urlopen(url)

        resp = json.load(inp)
        for i in resp['items']:
            if i['id']['kind'] == "youtube#video":
                video_links_and_info.append([base_video_url + i['id']['videoId'],
                                    i['id']['videoId'],
                                    unescape(i['snippet']['title']), #Unescape - названия без &amp; &quot; и т.д.
                                    i['snippet']['channelTitle'],
                                    i['snippet']['publishTime']])

        return video_links_and_info



