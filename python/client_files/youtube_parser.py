import json
import random
import os
import requests
import shutil

from html import unescape
from youtube_search import YoutubeSearch

from client import get_good_tube_api_response
from configs_handler import ConfigsHandler


class YouTubeChannelsParser():
    """Класс парсера каналов в файле ютуба."""
    def __init__(self):
        """Инициализация пути к файлу с url, ключа для доступа в юутб, класс для выкачки данных."""

        self.configs_handler = ConfigsHandler()
        token = self.configs_handler.token
        
        parametrs = {
            'token': token
        }

        response = get_good_tube_api_response('get_user_api_key', parametrs=parametrs)

        self.API_KEY = response['api_key']

    def parse(self):
        """Основная функция парсера, которая возвращает список видео."""
        channel_ids = self.get_channels_ids(self.get_channels_urls())
        video_links_and_info = []
        for channel_id in channel_ids:
            channel_id = channel_id.strip()
            video_links_and_info.extend(self.get_all_video_from_channel(channel_id))
        random.shuffle(video_links_and_info) # Рандомное расположение ссылок, чтобы в gui не выводились ссылки с одного канала подряд.
        return video_links_and_info

    def search(self, search_request: str) -> list:
        """Функция поиск и оценки лучшего видео."""
        base_video_url = "https://www.youtube.com/watch?v="

        response = YoutubeSearch(search_request, max_results=10).to_dict()

        best_video_rating = 0
        best_video_info = []

        for element in response:
            video_id = element['id']

            payload = {'id': video_id, 'part': 'contentDetails,statistics,snippet', 'key': self.API_KEY}
            video_request = requests.get('https://www.googleapis.com/youtube/v3/videos', params=payload).text  
            video_info = json.loads(video_request)
            video_info = video_info['items'][0]

            video_channel_title = video_info['snippet']['channelTitle']
            video_title = video_info['snippet']['title']
            video_publish_time = video_info['snippet']['publishedAt']

            video_likes_num = int(video_info['statistics']['likeCount'])
            video_views_num = int(video_info['statistics']['viewCount'])

            video_rating = video_likes_num / video_views_num

            if video_rating > best_video_rating:
                best_video_info = [[base_video_url + video_id, video_id, video_title, video_channel_title, video_publish_time]]
                best_video_rating = video_rating

        return best_video_info

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
        token = self.configs_handler.token
        
        parametrs = {
            'token': token
        }

        response = get_good_tube_api_response('channel_list_by_id', parametrs)
        urls_to_channels = response['channels_list']

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

        video_num_from_channel = self.configs_handler._get_video_num_from_channel() 
        url = base_search_url + f"key={self.API_KEY}&channelId={channel_id}&part=snippet,id&order=date&maxResults={video_num_from_channel}"
        print(url)

        video_links_and_info = []
        inp = requests.get(url)
        resp = json.loads(inp.text)

        for i in resp['items']:
            if i['id']['kind'] == "youtube#video":
                video_links_and_info.append([base_video_url + i['id']['videoId'],
                                    i['id']['videoId'],
                                    unescape(i['snippet']['title']), #Unescape - названия без &amp; &quot; и т.д.
                                    i['snippet']['channelTitle'],
                                    i['snippet']['publishTime']])

        return video_links_and_info

