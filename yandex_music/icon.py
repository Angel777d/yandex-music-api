# coding=utf-8


from yandex_music import YandexMusicObject




class Icon(YandexMusicObject):
    """Класс, представляющий иконку.

    Attributes:
        background_color (:obj:`str`): Цвет заднего фона в HEX.
        image_url (:obj:`str`): Ссылка на изображение.
        client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client`, представляющий клиент
                Yandex Music.

    Args:
        background_color (:obj:`str`): Цвет заднего фона в HEX.
        image_url (:obj:`str`): Ссылка на изображение.
        client (:obj:`yandex_music.Client`, optional): Объект класса :class:`yandex_music.Client`, представляющий клиент
            Yandex Music.
        **kwargs: Произвольные ключевые аргументы полученные от API.
    """

    def __init__(self,
                 background_color,
                 image_url,
                 client= None,
                 **kwargs):
        self.background_color = background_color
        self.image_url = image_url

        self.client = client
        self._id_attrs = (self.background_color, self.image_url)

    def download(self, filename, size = '200x200') :
        """Загрузка иконки.

        Args:
            filename (:obj:`str`): Путь для сохранения файла с названием и расширением.
            size (:obj:`str`, optional): Размер иконки.
        """
        self.client.request.download('https://%s' % self.image_url.replace("%%", size), filename)

    @classmethod
    def de_json(cls, data, client):
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client`, представляющий клиент
                Yandex Music.

        Returns:
            :obj:`yandex_music.Icon`: Объект класса :class:`yandex_music.Icon`.
        """
        if not data:
            return None

        data = super(Icon, cls).de_json(data, client)

        return cls(client=client, **data)
