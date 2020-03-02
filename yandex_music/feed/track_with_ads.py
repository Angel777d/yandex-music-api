# coding=utf-8
# coding=utf-8
# coding=utf-8


from yandex_music import YandexMusicObject




class TrackWithAds(YandexMusicObject):
    """Класс, представляющий трек с рекламой.

    Note:
        Поле `type` встречалось только с значением `track`.

    Attributes:
        type (:obj:`str`): Тип TODO.
        track (:obj:`yandex_music.Track`): Объект класса :class:`yandex_music.Track`, представляющий трек.
        client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client`, представляющий клиент
                Yandex Music.

    Args:
        type_ (:obj:`str`): Тип TODO.
        track (:obj:`yandex_music.Track`): Объект класса :class:`yandex_music.Track`, представляющий трек.
        client (:obj:`yandex_music.Client`, optional): Объект класса :class:`yandex_music.Client`, представляющий клиент
            Yandex Music.
        **kwargs: Произвольные ключевые аргументы полученные от API.
    """

    def __init__(self,
                 type_,
                 track,
                 client= None,
                 **kwargs) :
        self.type = type_
        self.track = track

        self.client = client
        self._id_attrs = (self.type, self.track)

    @classmethod
    def de_json(cls, data, client):
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client`, представляющий клиент
                Yandex Music.

        Returns:
            :obj:`yandex_music.TrackWithAds`: Объект класса :class:`yandex_music.TrackWithAds`.
        """
        if not data:
            return None

        data = super(TrackWithAds, cls).de_json(data, client)
        from yandex_music import Track
        data['track'] = Track.de_json(data.get('track'), client)

        return cls(client=client, **data)

    @classmethod
    def de_list(cls, data, client):
        """Десериализация списка объектов.

        Args:
            data (:obj:`list`): Список словарей с полями и значениями десериализуемого объекта.
            client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client`, представляющий клиент
                Yandex Music.

        Returns:
            :obj:`list` из :obj:`yandex_music.TrackWithAds`: Список объектов класса :class:`yandex_music.TrackWithAds`.
        """
        if not data:
            return []

        tracks_with_ads = list()
        for track_with_ads in data:
            tracks_with_ads.append(cls.de_json(track_with_ads, client))

        return tracks_with_ads
