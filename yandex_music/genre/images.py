# coding=utf-8


from yandex_music import YandexMusicObject




class Images(YandexMusicObject):
    """Класс, представляющий изображение жанра.

    Attributes:
        _208x208 (:obj:`str`): Ссылка на изображение размером 208 на 208.
        _300x300 (:obj:`str`): Ссылка на изображение размером 300 на 300.
        client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client`, представляющий клиент
                Yandex Music.

    Args:
        _208x208 (:obj:`str`, optional): Ссылка на изображение размером 208 на 208.
        _300x300 (:obj:`str`, optional): Ссылка на изображение размером 300 на 300.
        client (:obj:`yandex_music.Client`, optional): Объект класса :class:`yandex_music.Client`, представляющий клиент
            Yandex Music.
        **kwargs: Произвольные ключевые аргументы полученные от API.
    """

    def __init__(self,
                 _208x208= None,
                 _300x300= None,
                 client= None,
                 **kwargs) :
        self._208x208 = _208x208
        self._300x300 = _300x300

        self.client = client

    def download_208x208(self, filename) :
        """Загрузка изображения 208x208.

        Args:
            filename (:obj:`str`): Путь для сохранения файла с названием и расширением.
        """
        self.client.request.download(self._208x208, filename)

    def download_300x300(self, filename) :
        """Загрузка изображения 300x300.

        Args:
            filename (:obj:`str`): Путь для сохранения файла с названием и расширением.
        """
        self.client.request.download(self._300x300, filename)

    @classmethod
    def de_json(cls, data, client):
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client`, представляющий клиент
                Yandex Music.

        Returns:
            :obj:`yandex_music.Images`: Объект класса :class:`yandex_music.Images`.
        """
        if not data:
            return None

        data = super(Images, cls).de_json(data, client)

        return cls(client=client, **data)

