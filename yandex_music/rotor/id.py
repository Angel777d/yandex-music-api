# coding=utf-8
# coding=utf-8


from yandex_music import YandexMusicObject




class Id(YandexMusicObject):
    """Класс, представляющий уникальный идентификатор станции.

    Note:
        Известные типы станций: `user`, `genre`.

    Attributes:
        type (:obj:`str`): Тип станции.
        tag (:obj:`str`): Тег станции.
        client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client`, представляющий клиент
                Yandex Music.

    Args:
        type_ (:obj:`str`): Тип станции.
        tag (:obj:`str`): Тег станции.
        client (:obj:`yandex_music.Client`, optional): Объект класса :class:`yandex_music.Client`, представляющий клиент
            Yandex Music.
        **kwargs: Произвольные ключевые аргументы полученные от API.
    """

    def __init__(self,
                 type_,
                 tag,
                 client= None,
                 **kwargs) :
        self.type = type_
        self.tag = tag

        self.client = client
        self._id_attrs = (self.type, self.tag)

    @classmethod
    def de_json(cls, data, client):
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client`, представляющий клиент
                Yandex Music.

        Returns:
            :obj:`yandex_music.Id`: Объект класса :class:`yandex_music.Id`.
        """
        if not data:
            return None

        data = super(Id, cls).de_json(data, client)

        return cls(client=client, **data)
