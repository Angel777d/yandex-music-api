# coding=utf-8


from yandex_music import YandexMusicObject




class Link(YandexMusicObject):
    """Класс, представляющий ссылку на официальную страницу исполнителя.

    Note:
        Известные типы страниц: `official` - официальный сайт и `social` - социальная сеть.

    Attributes:
        title (:obj:`str`): Название страницы.
        href (:obj:`str`): URL страницы.
        type_ (:obj:`str`): Тип страницы.
        social_network (:obj:`str`): Название социальной сети.
        client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client`, представляющий клиент
                Yandex Music.

    Args:
        title (:obj:`str`): Название страницы.
        href (:obj:`str`): URL страницы.
        type_ (:obj:`str`): Тип страницы.
        social_network (:obj:`str`, optional): Название социальной сети.
        client (:obj:`yandex_music.Client`, optional): Объект класса :class:`yandex_music.Client`, представляющий клиент
            Yandex Music.
    """

    def __init__(self,
                 title,
                 href,
                 type_,
                 social_network= None,
                 client= None,
                 **kwargs) :
        self.title = title
        self.href = href
        self.type = type_

        self.social_network = social_network

        self.client = client
        self._id_attrs = (self.title, self.href, self.type)

    @classmethod
    def de_json(cls, data, client):
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client`, представляющий клиент
                Yandex Music.

        Returns:
            :obj:`yandex_music.Link`: Объект класса :class:`yandex_music.Link`.
        """
        if not data:
            return None

        data = super(Link, cls).de_json(data, client)

        return cls(client=client, **data)

    @classmethod
    def de_list(cls, data, client):
        """Десериализация списка объектов.

        Args:
            data (:obj:`list`): Список словарей с полями и значениями десериализуемого объекта.
            client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client`, представляющий клиент
                Yandex Music.

        Returns:
            :obj:`list` из :obj:`yandex_music.Link`: Список объектов класса :class:`yandex_music.Link`.
        """
        if not data:
            return []

        links = list()
        for link in data:
            links.append(cls.de_json(link, client))

        return links
