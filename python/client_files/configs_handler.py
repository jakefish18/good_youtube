from configparser import ConfigParser


class ConfigsHandler(ConfigParser):
    """Класс для удобного управления конфигами."""

    def push_data(self, data: list) -> None:
        """Добавление данных в config.ini"""
        for elem in data:
            section, option, value = elem
            
            if not self.has_section(section):
                self.add_section(section)

            self[section][option] = value

        with open('config.ini', 'w') as file:
            self.write(file)

    def get_video_num_from_channel(self) -> str:
        """Получение количества выбираемых видео с канала."""
        self.read('cofig.ini')

        video_num_from_channel = self['User_settings']['video_num_from_channel']

        return video_num_from_channel

    def get_token(self) -> str:
        """Получение токена из config.ini"""
        self.read('config.ini')
        try:
            token = self['User_info']['token']

        except:
            token = ''

        return token