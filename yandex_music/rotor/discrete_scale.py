# coding=utf-8


from yandex_music import YandexMusicObject




class DiscreteScale(YandexMusicObject):
    """Класс, представляющий дискретное значение.

    Note:
        Известные значения поля `type`: `discrete-scale`.

    Attributes:
        type (:obj:`str`): Тип.
        name (:obj:`str`): Название.
        min (:obj:`yandex_music.Value`): Объект класса :class:`yandex_music.Value`, представляющий минимальное значение.
        max (:obj:`yandex_music.Value`): Объект класса :class:`yandex_music.Value`, представляющий максимальное
            значение.
        client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client`, представляющий клиент
                Yandex Music.

    Args:
        type_ (:obj:`str`): Тип.
        name (:obj:`str`): Название.
        min_ (:obj:`yandex_music.Value`): Объект класса :class:`yandex_music.Value`, представляющий минимальное
            значение.
        max_ (:obj:`yandex_music.Value`): Объект класса :class:`yandex_music.Value`, представляющий максимальное
            значение.
        client (:obj:`yandex_music.Client`, optional): Объект класса :class:`yandex_music.Client`, представляющий клиент
            Yandex Music.
        **kwargs: Произвольные ключевые аргументы полученные от API.
    """

    def __init__(self,
                 type_,
                 name,
                 min_,
                 max_,
                 client= None,
                 **kwargs) :
        self.type = type_
        self.name = name
        self.min = min_
        self.max = max_

        self.client = client
        self._id_attrs = (self.type, self.name, self.min, self.max)

    @classmethod
    def de_json(cls, data, client):
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client`, представляющий клиент
                Yandex Music.

        Returns:
            :obj:`yandex_music.DiscreteScale`: Объект класса :class:`yandex_music.DiscreteScale`.
        """
        if not data:
            return None

        data = super(DiscreteScale, cls).de_json(data, client)
        from yandex_music import Value
        data['min_'] = Value.de_json(data.get('min_'), client)
        data['max_'] = Value.de_json(data.get('max_'), client)

        return cls(client=client, **data)
