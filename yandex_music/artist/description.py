# coding=utf-8


from yandex_music import YandexMusicObject




class Description(YandexMusicObject):
    """Класс, представляющий описание исполнителя из другого источника.

    Note:
        Очень редкий объект, у минимального количества исполнителей.
        Обычно берётся информация из википедии.

    Attributes:
        text (:obj:`str`): Описание исполнителя.
        url (:obj:`str`): Ссылка на источник.
        client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client`, представляющий клиент
                Yandex Music.

    Args:
        text (:obj:`str`): Описание исполнителя.
        url (:obj:`str`): Ссылка на источник.
        client (:obj:`yandex_music.Client`, optional): Объект класса :class:`yandex_music.Client`, представляющий клиент
            Yandex Music.
        **kwargs: Произвольные ключевые аргументы полученные от API.
    """

    def __init__(self,
                 text,
                 uri,
                 client= None,
                 **kwargs) :
        self.text = text
        self.url = uri

        self.client = client
        self._id_attrs = (self.text, self.url)

    @classmethod
    def de_json(cls, data, client):
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client`, представляющий клиент
                Yandex Music.

        Returns:
            :obj:`yandex_music.Description`: Объект класса :class:`yandex_music.Descriptions`.
        """
        if not data:
            return None

        data = super(Description, cls).de_json(data, client)

        return cls(client=client, **data)
