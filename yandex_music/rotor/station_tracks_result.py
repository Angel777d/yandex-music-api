# coding=utf-8


from yandex_music import YandexMusicObject




class StationTracksResult(YandexMusicObject):
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
                 sequence,
                 batch_id,
                 pumpkin,
                 client= None,
                 **kwargs) :
        self.id = id_
        self.sequence = sequence
        self.batch_id = batch_id
        self.pumpkin = pumpkin

        self.client = client
        self._id_attrs = (self.id, self.sequence, self.batch_id, self.pumpkin)

    @classmethod
    def de_json(cls, data, client):
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client`, представляющий клиент
                Yandex Music.

        Returns:
            :obj:`yandex_music.StationTracksResult`: Объект класса :class:`yandex_music.StationTracksResult`.
        """
        if not data:
            return None

        data = super(StationTracksResult, cls).de_json(data, client)
        from yandex_music import Id, Sequence
        data['id_'] = Id.de_json(data.get('id_'), client)
        data['sequence'] = Sequence.de_list(data.get('sequence'), client)

        return cls(client=client, **data)
