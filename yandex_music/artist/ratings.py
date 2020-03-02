# coding=utf-8


from yandex_music import YandexMusicObject




class Ratings(YandexMusicObject):
    """Класс, представляющий рейтинг исполнителя.

    Attributes:
        month (:obj:`int`): Значение ежемесячного рейтинга.
        week (:obj:`int`): Значение еженедельного рейтинга.
        day (:obj:`int`): Значение дневного рейтинга.
        client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client`, представляющий клиент
                Yandex Music.

    Args:
        month (:obj:`int`): Значение ежемесячного рейтинга.
        week (:obj:`int`, optional): Значение еженедельного рейтинга.
        day (:obj:`int`, optional): Значение дневного рейтинга.
        client (:obj:`yandex_music.Client`, optional): Объект класса :class:`yandex_music.Client`, представляющий клиент
            Yandex Music.
        **kwargs: Произвольные ключевые аргументы полученные от API.
    """

    def __init__(self,
                 month,
                 week= None,
                 day= None,
                 client= None,
                 **kwargs) :
        self.week = week
        self.month = month

        self.day = day

        self.client = client
        self._id_attrs = (self.week, self.month)

    @classmethod
    def de_json(cls, data, client):
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client`, представляющий клиент
                Yandex Music.

        Returns:
            :obj:`yandex_music.Ratings`: Объект класса :class:`yandex_music.Ratings`.
        """
        if not data:
            return None

        data = super(Ratings, cls).de_json(data, client)

        return cls(client=client, **data)
