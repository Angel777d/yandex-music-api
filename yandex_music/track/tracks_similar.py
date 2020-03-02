# coding=utf-8
# coding=utf-8


from yandex_music import YandexMusicObject




class SimilarTracks(YandexMusicObject):
    """Класс, представляющий список похожих треков на другой трек.

    Attributes:
        track (:obj:`yandex_music.Track`): Объект класса :class:`yandex_music.Track` представляющий трек.
        similar_tracks (:obj:`list` из :obj:`yandex_music.Track`): Список объектов класса
            :class:`yandex_music.Track` представляющие похожие треки на `track`.
        client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client`, представляющий клиент
                Yandex Music.

    Args:
        track (:obj:`yandex_music.Track`): Объект класса :class:`yandex_music.Track` представляющий трек.
        similar_tracks (:obj:`list` из :obj:`yandex_music.Track`): Список объектов класса
            :class:`yandex_music.Track` представляющие похожие треки на `track`.
        client (:obj:`yandex_music.Client`, optional): Объект класса :class:`yandex_music.Client`, представляющий клиент
            Yandex Music.
        **kwargs: Произвольные ключевые аргументы полученные от API.
    """

    def __init__(self,
                 track,
                 similar_tracks,
                 client= None,
                 **kwargs) :
        self.track = track
        self.similar_tracks = similar_tracks

        self.client = client
        self._id_attrs = (self.track, self.similar_tracks)

    @classmethod
    def de_json(cls, data, client):
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client`, представляющий клиент
                Yandex Music.

        Returns:
            :obj:`yandex_music.SimilarTracks`: Объект класса :class:`yandex_music.SimilarTracks`.
        """
        if not data:
            return None

        data = super(SimilarTracks, cls).de_json(data, client)
        from yandex_music import Track
        data['track'] = Track.de_json(data.get('track'), client)
        data['similar_tracks'] = Track.de_list(data.get('similar_tracks'), client)

        return cls(client=client, **data)
