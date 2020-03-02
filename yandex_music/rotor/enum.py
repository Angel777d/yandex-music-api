# coding=utf-8


from yandex_music import YandexMusicObject




class Enum(YandexMusicObject):
    """Класс, представляющий перечисления.

    Attributes:
        type (:obj:`str`): Тип перечисления.
        name (:obj:`str`): Название перечисления.
        possible_values (:obj:`list` из :obj:`yandex_Music.Value`): Список из :obj:`yandex_Music.Value`, представляющий
            доступные значения.
        client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client`, представляющий клиент
                Yandex Music.

    Args:
        type_ (:obj:`str`): Тип перечисления.
        name (:obj:`str`): Название перечисления.
        possible_values (:obj:`list` из :obj:`yandex_Music.Value`): Список из :obj:`yandex_Music.Value`, представляющий
            доступные значения.
        client (:obj:`yandex_music.Client`, optional): Объект класса :class:`yandex_music.Client`, представляющий клиент
            Yandex Music.
        **kwargs: Произвольные ключевые аргументы полученные от API.
    """

    def __init__(self,
                 type_,
                 name,
                 possible_values,
                 client= None,
                 **kwargs) :
        self.type = type_
        self.name = name
        self.possible_values = possible_values

        self.client = client
        self._id_attrs = (self.type, self.name, self.possible_values)

    @classmethod
    def de_json(cls, data, client):
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client`, представляющий клиент
                Yandex Music.

        Returns:
            :obj:`yandex_music.Enum`: Объект класса :class:`yandex_music.Enum`.
        """
        if not data:
            return None

        data = super(Enum, cls).de_json(data, client)
        from yandex_music import Value
        data['possible_values'] = Value.de_list(data.get('possible_values'), client)

        return cls(client=client, **data)
