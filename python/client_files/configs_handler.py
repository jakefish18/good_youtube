from configparser import ConfigParser


class ConfigsHandler(ConfigParser):
    """Класс для удобного управления конфигами."""

    def __init__(self):
        """Запись значений из config.ini."""
        super().__init__()

        self.update_variables()

    def push_data(self, data: list) -> None:
        """Добавление данных в config.ini"""
        for elem in data:
            section, option, value = elem
            
            if not self.has_section(section):
                self.add_section(section)

            self[section][option] = value

        with open('config.ini', 'w') as file:
            self.write(file)

    def update_variables(self) -> None:
        """Обновление всех настроек и переменных из config.ini."""
        self.token = self._get_token()
        self.path_to_styles = self._get_path_to_styles()
        self.video_num_from_channel = self._get_video_num_from_channel()

    def _get_video_num_from_channel(self) -> str:
        """Получение количества выбираемых видео с канала."""
        self.read('config.ini')

        try:
            video_num_from_channel = self['User_settings']['video_num_from_channel']
        except:
            video_num_from_channel = "0"

        return video_num_from_channel

    def _get_token(self) -> str:
        """Получение токена из config.ini"""
        self.read('config.ini')
        
        try:
            token = self['User_info']['token']

        except:
            token = ''

        return token
    
    def _get_path_to_styles(self) -> str:
        """Получение пути к css файлам со стилями."""
        self.read('config.ini')

        try:
            path_to_styles = self['User_settings']['path_to_styles']
        
        except:
            path_to_styles = ''

        return path_to_styles