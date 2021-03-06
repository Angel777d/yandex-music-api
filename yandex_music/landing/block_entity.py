# coding=utf-8


from yandex_music import YandexMusicObject, Promotion, Album, Playlist, MixLink, PlayContext, ChartItem, \
    GeneratedPlaylist



de_json = {
    'personal-playlist': GeneratedPlaylist.de_json,
    'promotion': Promotion.de_json,
    'album': Album.de_json,
    'playlist': Playlist.de_json,
    'chart-item': ChartItem.de_json,
    'play-context': PlayContext.de_json,
    'mix-link': MixLink.de_json
}


class BlockEntity(YandexMusicObject):
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
                 id_,
                 type_,
                 data,
                 client= None,
                 **kwargs) :

        self.id = id_
        self.type = type_
        self.data = data

        self.client = client
        self._id_attrs = (self.id, self.type, self.data)

    @classmethod
    def de_json(cls, data, client):
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client`, представляющий клиент
                Yandex Music.

        Returns:
            :obj:`yandex_music.BlockEntity`: Объект класса :class:`yandex_music.BlockEntity`.
        """
        if not data:
            return None

        data = super(BlockEntity, cls).de_json(data, client)
        data['data'] = de_json.get(data.get('type_'))(data.get('data'), client)

        return cls(client=client, **data)

    @classmethod
    def de_list(cls, data, client):
        """Десериализация списка объектов.

        Args:
            data (:obj:`list`): Список словарей с полями и значениями десериализуемого объекта.
            client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client`, представляющий клиент
                Yandex Music.

        Returns:
            :obj:`list` из :obj:`yandex_music.BlockEntity`: Список объектов класса :class:`yandex_music.BlockEntity`.
        """
        if not data:
            return []

        entities = list()
        for entity in data:
            entities.append(cls.de_json(entity, client))

        return entities
