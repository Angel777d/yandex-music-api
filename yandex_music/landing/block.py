# coding=utf-8


from yandex_music import YandexMusicObject




class Block(YandexMusicObject):
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
                 type_for_from,
                 title,
                 entities,
                 description= None,
                 data= None,
                 client= None,
                 **kwargs) :

        self.id = id_
        self.type = type_
        self.type_for_from = type_for_from
        self.title = title
        self.entities = entities

        self.description = description
        self.data = data

        self.client = client
        self._id_attrs = (self.id, self.type, self.type_for_from, self.title, self.entities)

    def __getitem__(self, item):
        return self.entities[item]

    @classmethod
    def de_json(cls, data, client):
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client`, представляющий клиент
                Yandex Music.

        Returns:
            :obj:`yandex_music.Block`: Объект класса :class:`yandex_music.Block`.
        """
        if not data:
            return None

        data = super(Block, cls).de_json(data, client)
        from yandex_music import BlockEntity, PlayContextsData, PersonalPlaylistsData
        data['entities'] = BlockEntity.de_list(data.get('entities'), client)

        block_type = data.get('type_')
        if block_type == 'personal-playlists':
            data['data'] = PersonalPlaylistsData.de_json(data.get('data'), client)
        elif block_type == 'play-contexts':
            data['data'] = PlayContextsData.de_json(data.get('data'), client)

        return cls(client=client, **data)

    @classmethod
    def de_list(cls, data, client):
        """Десериализация списка объектов.

        Args:
            data (:obj:`list`): Список словарей с полями и значениями десериализуемого объекта.
            client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client`, представляющий клиент
                Yandex Music.

        Returns:
            :obj:`list` из :obj:`yandex_music.Block`: Список объектов класса :class:`yandex_music.Block`.
        """
        if not data:
            return []

        blocks = list()
        for block in data:
            blocks.append(cls.de_json(block, client))

        return blocks
