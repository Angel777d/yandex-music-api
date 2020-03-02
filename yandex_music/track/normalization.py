# coding=utf-8


from yandex_music import YandexMusicObject




class Normalization(YandexMusicObject):
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
                 gain,
                 peak,
                 client= None,
                 **kwargs) :
        self.gain = gain
        self.peak = peak

        self.client = client
        self._id_attrs = (self.gain, self.peak)

    @classmethod
    def de_json(cls, data, client):
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client`, представляющий клиент
                Yandex Music.

        Returns:
            :obj:`yandex_music.Normalization`: Объект класса :class:`yandex_music.Normalization`.
        """
        if not data:
            return None

        data = super(Normalization, cls).de_json(data, client)

        return cls(client=client, **data)
