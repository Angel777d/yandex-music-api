# coding=utf-8
# coding=utf-8


from yandex_music import YandexMusicObject




class PlayCounter(YandexMusicObject):
    """Класс, представляющий счётчик дней.

    Note:
        Присутствует только у плейлиста дня. Счётчик считает количество дней подряд, на протяжении которых был
        прослушан плейлист.

    Attributes:
        value (:obj:`int`): Значение (количество дней).
        description (:obj:`str`): Описание счётчика.
        updated (:obj:`bool`): Обновлён ли сегодня (в этих сутках).
        client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client`, представляющий клиент
                Yandex Music.

    Args:
        value (:obj:`int`): Значение (количество дней).
        description (:obj:`str`): Описание счётчика.
        updated (:obj:`bool`): Обновлён ли сегодня (в этих сутках).
        client (:obj:`yandex_music.Client`, optional): Объект класса :class:`yandex_music.Client`, представляющий клиент
            Yandex Music.
        **kwargs: Произвольные ключевые аргументы полученные от API.
    """

    def __init__(self,
                 value,
                 description,
                 updated,
                 client= None,
                 **kwargs) :
        self.value = value
        self.description = description
        self.updated = updated

        self.client = client
        self._id_attrs = (self.value, self.description, self.updated)

    @classmethod
    def de_json(cls, data, client):
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client`, представляющий клиент
                Yandex Music.

        Returns:
            :obj:`yandex_music.PlayCounter`: Объект класса :class:`yandex_music.PlayCounter`.
        """
        if not data:
            return None

        data = super(PlayCounter, cls).de_json(data, client)

        return cls(client=client, **data)
