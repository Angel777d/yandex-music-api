# coding=utf-8
# coding=utf-8


from yandex_music import YandexMusicObject




class Landing(YandexMusicObject):
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
                 pumpkin,
                 content_id,
                 blocks,
                 client= None,
                 **kwargs) :

        self.pumpkin = pumpkin
        self.content_id = content_id
        self.blocks = blocks

        self.client = client
        self._id_attrs = (self.content_id, self.blocks)

    def __getitem__(self, item):
        return self.blocks[item]

    @classmethod
    def de_json(cls, data, client):
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client`, представляющий клиент
                Yandex Music.

        Returns:
            :obj:`yandex_music.Landing`: Объект класса :class:`yandex_music.Landing`.
        """
        if not data:
            return None

        data = super(Landing, cls).de_json(data, client)
        from yandex_music import Block
        data['blocks'] = Block.de_list(data.get('blocks'), client)

        return cls(client=client, **data)
