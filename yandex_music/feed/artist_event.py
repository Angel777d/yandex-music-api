# coding=utf-8


from yandex_music import YandexMusicObject




class ArtistEvent(YandexMusicObject):
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
                 artist,
                 tracks,
                 similar_to_artists_from_history,
                 client= None,
                 **kwargs) :
        self.artist = artist
        self.tracks = tracks
        self.similar_to_artists_from_history = similar_to_artists_from_history

        self.client = client
        self._id_attrs = (self.artist, self.tracks, self.similar_to_artists_from_history)

    @classmethod
    def de_json(cls, data, client):
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client`, представляющий клиент
                Yandex Music.

        Returns:
            :obj:`yandex_music.ArtistEvent`: Объект класса :class:`yandex_music.ArtistEvent`.
        """
        if not data:
            return None

        data = super(ArtistEvent, cls).de_json(data, client)
        from yandex_music import Artist, Track
        data['artist'] = Artist.de_json(data.get('artist'), client)
        data['tracks'] = Track.de_list(data.get('tracks'), client)
        data['similar_to_artists_from_history'] = Artist.de_list(data.get('similar_to_artists_from_history'), client)

        return cls(client=client, **data)

    @classmethod
    def de_list(cls, data, client):
        """Десериализация списка объектов.

        Args:
            data (:obj:`list`): Список словарей с полями и значениями десериализуемого объекта.
            client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client`, представляющий клиент
                Yandex Music.

        Returns:
            :obj:`list` из :obj:`yandex_music.ArtistEvent`: Список объектов класса :class:`yandex_music.ArtistEvent`.
        """
        if not data:
            return []

        artist_events = list()
        for artist_event in data:
            artist_events.append(cls.de_json(artist_event, client))

        return artist_events
