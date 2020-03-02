# coding=utf-8


from yandex_music import YandexMusicObject




class PlayContextsData(YandexMusicObject):
    """Класс, представляющий .

    Attributes:
        client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client`, представляющий клиент
                Yandex Music.

    Args:
        client (:obj:`yandex_music.Client`, optional): Объект класса :class:`yandex_music.Client`, представляющий клиент
            Yandex Music.
        **kwargs: Произвольные ключевые аргументы полученные от API.
    """

    def __init__(self,
                 other_tracks,
                 client= None,
                 **kwargs) :
        self.other_tracks = other_tracks

        self.client = client
        self._id_attrs = (self.other_tracks,)

    @classmethod
    def de_json(cls, data, client):
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client`, представляющий клиент
                Yandex Music.

        Returns:
            :obj:`yandex_music.PlayContextsData`: Объект класса :class:`yandex_music.PlayContextsData`.
        """
        if not data:
            return None

        data = super(PlayContextsData, cls).de_json(data, client)
        from yandex_music import TrackShortOld
        data['other_tracks'] = TrackShortOld.de_list(data.get('other_tracks'), client)

        return cls(client=client, **data)
