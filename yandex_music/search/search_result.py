# coding=utf-8
# coding=utf-8


from yandex_music import YandexMusicObject, Artist, Album, Track, Playlist, Video




de_json_result = {
    'track': Track.de_list,
    'artist': Artist.de_list,
    'album': Album.de_list,
    'playlist': Playlist.de_list,
    'video': Video.de_list,
}


class SearchResult(YandexMusicObject):
    """Класс, представляющий результаты поиска.

    Note:
        Значения поля `type`: `track`, `artist`, `playlist`, `album`, `video`.

    Attributes:
        type (:obj:`str`):  Тип результата.
        total (:obj:`int`): Количество результатов.
        per_page (:obj:`int`): Максимальное количество результатов на странице.
        order (:obj:`int`): Позиция блока.
        results (:obj:`list` из :obj:`yandex_music.Track` | :obj:`yandex_music.Artist` | :obj:`yandex_music.Album` \
            | :obj:`yandex_music.Playlist` | :obj:`yandex_music.Video`): Результаты поиска.
        client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client`, представляющий клиент
                Yandex Music.

    Args:
        type_ (:obj:`str`):  Тип результата.
        total (:obj:`int`): Количество результатов.
        per_page (:obj:`int`): Максимальное количество результатов на странице.
        order (:obj:`int`): Позиция блока.
        results (:obj:`list` из :obj:`yandex_music.Track` | :obj:`yandex_music.Artist` | :obj:`yandex_music.Album` \
            | :obj:`yandex_music.Playlist` | :obj:`yandex_music.Video`): Результаты поиска.
        client (:obj:`yandex_music.Client`, optional): Объект класса :class:`yandex_music.Client`, представляющий клиент
            Yandex Music.
        **kwargs: Произвольные ключевые аргументы полученные от API.
    """

    def __init__(self,
                 type_,
                 total,
                 per_page,
                 order,
                 results,
                 client= None,
                 **kwargs) :
        self.type = type_
        self.total = total
        self.per_page = per_page
        self.order = order
        self.results = results

        self.client = client
        self._id_attrs = (self.total, self.per_page, self.order, self.results)

    @classmethod
    def de_json(cls, data, client, type_ = None):
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            type_ (:obj:`str`, optional): Тип результата.
            client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client`, представляющий клиент
                Yandex Music.

        Returns:
            :obj:`yandex_music.SearchResult`: Объект класса :class:`yandex_music.SearchResult`.
        """
        if not data:
            return None

        data = super(SearchResult, cls).de_json(data, client)
        data['type_'] = type_
        data['results'] = de_json_result.get(type_)(data.get('results'), client)

        return cls(client=client, **data)
