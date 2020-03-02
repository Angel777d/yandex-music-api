# coding=utf-8
# coding=utf-8
# coding=utf-8


from yandex_music import YandexMusicObject




class Value(YandexMusicObject):
    """Класс, представляющий значение(переменную).

    Attributes:
        value (:obj:`str`): Значение.
        name (:obj:`str`): Название.
        client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client`, представляющий клиент
                Yandex Music.

    Args:
        value (:obj:`str`): Значение.
        name (:obj:`str`): Название.
        client (:obj:`yandex_music.Client`, optional): Объект класса :class:`yandex_music.Client`, представляющий клиент
            Yandex Music.
        **kwargs: Произвольные ключевые аргументы полученные от API.
    """

    def __init__(self,
                 value,
                 name,
                 client= None,
                 **kwargs) :
        self.value = value
        self.name = name

        self.client = client
        self._id_attrs = (self.value, self.name)

    @classmethod
    def de_json(cls, data, client):
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client`, представляющий клиент
                Yandex Music.

        Returns:
            :obj:`yandex_music.Value`: Объект класса :class:`yandex_music.Value`.
        """
        if not data:
            return None

        data = super(Value, cls).de_json(data, client)

        return cls(client=client, **data)

    @classmethod
    def de_list(cls, data, client):
        """Десериализация списка объектов.

        Args:
            data (:obj:`list`): Список словарей с полями и значениями десериализуемого объекта.
            client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client`, представляющий клиент
                Yandex Music.

        Returns:
            :obj:`list` из :obj:`yandex_music.Value`: Список объектов класса :class:`yandex_music.Value`.
        """
        if not data:
            return []

        values = list()
        for value in data:
            values.append(cls.de_json(value, client))

        return values
