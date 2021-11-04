import json
import random
import urllib.request
import os
import sys
import requests
import shutil
import psycopg2

from html import unescape

class YouTubeChannelsParser():
    """Класс парсера каналов в файле ютуба."""
    def __init__(self, api_key, auth_id):
        """Инициализация пути к файлу с url, ключа для доступа в юутб, класс для выкачки данных."""
        self.API_KEY = api_key
        self.auth_id = auth_id

    def parse(self):
        """Основная функция парсера, которая возвращает список видео."""
        channel_ids = self.get_channels_ids(self.get_channels_urls())
        video_links_and_info = []
        for channel_id in channel_ids:
            channel_id = channel_id.strip()
            video_links_and_info.extend(self.get_all_video_from_channel(channel_id))
        random.shuffle(video_links_and_info)
        return video_links_and_info

    def get_videos_prewiew(self, video_links_and_info):
        """Получение ссылок на превью для скачивания."""
        order = 1
        #Если папка с превьюшками уже есть, она удаляется.
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
        """Получение пяти последних видео с выбранных каналов в файле."""
        urls_to_channels = []
        try:
            connection = psycopg2.connect(
                host="ec2-54-170-163-224.eu-west-1.compute.amazonaws.com",
                user="uvdhbagmtheqly",
                password="898ffb10b3a5fbdf59a98f25e7f03ac3ec8a1933edbdb8fde5b262a936f43ae3",
                database="d7kkv7tv2pire0" 
             )
            #Собрать все ссылки пользователя.
            with connection.cursor() as cursor:
                cursor.execute(f"select channel_url from channels where id='{self.auth_id}'")
                for row in cursor.fetchall():
                    urls_to_channels.append(row[0])

        except Exception as _ex:
            print("[ERROR] Error while working with PostgreSQL", _ex)

        finally:
            if connection:
                connection.commit()
                connection.close()
                print("[INFO] PostgreSQL connection closed")

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
        #Проверка на валедабельность ключа.
        try:
            inp = urllib.request.urlopen(url)
        except:
            return []

        print(inp)
        resp = json.load(inp)
        for i in resp['items']:
            if i['id']['kind'] == "youtube#video":
                video_links_and_info.append([base_video_url + i['id']['videoId'],
                                    i['id']['videoId'],
                                    unescape(i['snippet']['title']), #Unescape - названия без &amp; &quot; и т.д.
                                    i['snippet']['channelTitle'],
                                    i['snippet']['publishTime']])

        return video_links_and_info
