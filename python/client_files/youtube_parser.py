import json
import random
import os
import requests
import shutil

from html import unescape
from youtube_search import YoutubeSearch

from configs_handler import ConfigsHandler

class YouTubParser():
    """Класс парсера каналов в файле ютуба."""
    def __init__(self, api_key) -> None:
        """Инициализация пути к файлу с url, ключа для доступа в юутб, класс для выкачки данных."""
        self.configs_handler = ConfigsHandler()
        self.API_KEY = api_key

    def parse(self, channel_urls: list) -> list:
        """Основная функция парсера, которая возвращает список видео."""
        channel_ids = self._get_channels_ids(channel_urls)
        video_links_and_info = []
        
        for channel_id in channel_ids:
            channel_id = channel_id.strip()
            video_links_and_info.extend(self._get_all_video_from_channel(channel_id))

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

    def get_videos_preview(self, video_links_and_info: list):
        """
        Скачивание превью со списка переданных каналов и
        запись в папку с превьюшками. 
        """

        try:
            os.mkdir('temp') # Если папка с превьюшками уже есть, она удаляется. 

        except FileExistsError:
            shutil.rmtree('temp')
            os.mkdir('temp')

        for link in video_links_and_info:
            video_id = link[1]
            video_preview_url = f"https://img.youtube.com/vi/{video_id}/mqdefault.jpg"
            video_preview_data = requests.get(video_preview_url, allow_redirects=True)

            with open(f'temp/{video_id}.jpg', 'wb') as handler:
                handler.write(video_preview_data.content)

    def _get_channels_ids(self, urls_to_channels: list) -> list:
        """Получение айдишников канала."""
        channel_ids = []

        for url in urls_to_channels:
            channel_id = url.split('/')[-1] #Формат ссылок такой, что в конце стоит айди канала разделенная "/".
            channel_ids.append(channel_id)
        
        return channel_ids
    
    def _get_all_video_from_channel(self, channel_id: str) -> list:
        """
        Получение информации о видео по его id черезе YouTube API:
        1. ссылка на страницу с видео
        2. id видео
        3. название видео
        4. название канала
        5. дата загрузки видео в формате YYYY-MM-DD
        """

        base_video_url = "https://www.youtube.com/watch?v="
        base_search_url = "https://www.googleapis.com/youtube/v3/search?"

        video_num_from_channel = self.configs_handler._get_video_num_from_channel() 
        url = base_search_url + f"key={self.API_KEY}&channelId={channel_id}&part=snippet,id&order=date&maxResults={video_num_from_channel}"

        video_links_and_info = []
        inp = requests.get(url)
        resp = json.loads(inp.text)

        print(resp)
        for i in resp['items']:
            if i['id']['kind'] == "youtube#video":
                video_links_and_info.append([base_video_url + i['id']['videoId'],
                                    i['id']['videoId'],
                                    unescape(i['snippet']['title']), #Unescape - названия без &amp; &quot; и т.д.
                                    i['snippet']['channelTitle'],
                                    i['snippet']['publishTime']])

        return video_links_and_info

