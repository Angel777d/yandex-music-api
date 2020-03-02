# coding=utf-8


from yandex_music import YandexMusicObject




class Vinyl(YandexMusicObject):
    """Класс, представляющий виниловую пластинку.

    Attributes:
        url (:obj:`str`): Ссылка на пластинку в магазине.
        title (:obj:`str`): Заголовок.
        year (:obj:`int`): Год выпуска.
        price (:obj:`int`): Цена.
        media (:obj:`str`): Средство распространения.
        picture (:obj:`str`): Ссылка на обложку.
        client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client`, представляющий клиент
                Yandex Music.

    Args:
        url (:obj:`str`): Ссылка на пластинку в магазине.
        title (:obj:`str`): Заголовок.
        year (:obj:`int`): Год выпуска.
        price (:obj:`int`): Цена.
        media (:obj:`str`): Средство распространения.
        picture (:obj:`str`, optional): Ссылка на обложку.
        client (:obj:`yandex_music.Client`, optional): Объект класса :class:`yandex_music.Client`, представляющий клиент
            Yandex Music.
        **kwargs: Произвольные ключевые аргументы полученные от API.
    """

    def __init__(self,
                 url,
                 title,
                 year,
                 price,
                 media,
                 picture= None,
                 client= None,
                 **kwargs) :
        self.url = url
        self.picture = picture
        self.title = title
        self.year = year
        self.price = price
        self.media = media

        self.client = client
        self._id_attrs = (self.title, self.price, self.year, self.url, self.price, self.media)

    @classmethod
    def de_json(cls, data, client):
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client`, представляющий клиент
                Yandex Music.

        Returns:
            :obj:`yandex_music.Vinyl`: Объект класса :class:`yandex_music.Vinyl`.
        """
        if not data:
            return None

        data = super(Vinyl, cls).de_json(data, client)

        return cls(client=client, **data)

    @classmethod
    def de_list(cls, data, client):
        """Десериализация списка объектов.

        Args:
            data (:obj:`list`): Список словарей с полями и значениями десериализуемого объекта.
            client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client`, представляющий клиент
                Yandex Music.

        Returns:
            :obj:`list` из :obj:`yandex_music.Vinyl`: Список объектов класса :class:`yandex_music.Vinyl`.
        """
        if not data:
            return []

        vinyls = list()
        for vinyl in data:
            vinyls.append(cls.de_json(vinyl, client))

        return vinyls
