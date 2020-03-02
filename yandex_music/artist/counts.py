# coding=utf-8
# coding=utf-8


from yandex_music import YandexMusicObject




class Counts(YandexMusicObject):
    """Класс, представляющий счётчик некоторых значений исполнителя.

    Note:
        Под дополнительными подразумеваются треки и альбомы, в которых артист задействован, но не является его автором.
        Так же в дополнительные альбомы входят сборники.

    Attributes:
        tracks (:obj:`int`): Количество треков.
        direct_albums (:obj:`int`): Количество альбомов.
        also_albums (:obj:`int`): Количество дополнительных треков.
        also_tracks (:obj:`int`): Количество дополнительных альбомов.
        client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client`, представляющий клиент
                Yandex Music.

    Args:
        tracks (:obj:`int`): Количество треков.
        direct_albums (:obj:`int`): Количество альбомов.
        also_albums (:obj:`int`): Количество дополнительных треков.
        also_tracks (:obj:`int`): Количество дополнительных альбомов.
        client (:obj:`yandex_music.Client`, optional): Объект класса :class:`yandex_music.Client`, представляющий клиент
            Yandex Music.
        **kwargs: Произвольные ключевые аргументы полученные от API.
    """

    def __init__(self,
                 tracks,
                 direct_albums,
                 also_albums,
                 also_tracks,
                 client= None,
                 **kwargs) :
        self.tracks = tracks
        self.direct_albums = direct_albums
        self.also_albums = also_albums
        self.also_tracks = also_tracks

        self.client = client
        self._id_attrs = (self.tracks, self.direct_albums, self.also_albums, self.also_tracks)

    @classmethod
    def de_json(cls, data, client):
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client`, представляющий клиент
                Yandex Music.

        Returns:
            :obj:`yandex_music.Counts`: Объект класса :class:`yandex_music.Counts`.
        """
        if not data:
            return None

        data = super(Counts, cls).de_json(data, client)

        return cls(client=client, **data)
