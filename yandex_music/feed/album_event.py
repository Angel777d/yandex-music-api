# coding=utf-8
# coding=utf-8
# coding=utf-8


from yandex_music import YandexMusicObject




class AlbumEvent(YandexMusicObject):
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
                 album,
                 tracks,
                 client= None,
                 **kwargs) :
        self.album = album
        self.tracks = tracks

        self.client = client
        self._id_attrs = (self.album, self.tracks)

    @classmethod
    def de_json(cls, data, client):
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client`, представляющий клиент
                Yandex Music.

        Returns:
            :obj:`yandex_music.AlbumEvent`: Объект класса :class:`yandex_music.AlbumEvent`.
        """
        if not data:
            return None

        data = super(AlbumEvent, cls).de_json(data, client)
        from yandex_music import Album, Track
        data['album'] = Album.de_json(data.get('album'), client)
        data['tracks'] = Track.de_list(data.get('tracks'), client)

        return cls(client=client, **data)

    @classmethod
    def de_list(cls, data, client):
        """Десериализация списка объектов.

        Args:
            data (:obj:`list`): Список словарей с полями и значениями десериализуемого объекта.
            client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client`, представляющий клиент
                Yandex Music.

        Returns:
            :obj:`list` из :obj:`yandex_music.AlbumEvent`: Список объектов класса :class:`yandex_music.AlbumEvent`.
        """
        if not data:
            return []

        album_events = list()
        for album_event in data:
            album_events.append(cls.de_json(album_event, client))

        return album_events
