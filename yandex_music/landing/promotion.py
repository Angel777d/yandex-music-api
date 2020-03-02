# coding=utf-8


from yandex_music import YandexMusicObject




class Promotion(YandexMusicObject):
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
                 promo_id,
                 title,
                 subtitle,
                 heading,
                 url,
                 url_scheme,
                 text_color,
                 gradient,
                 image,
                 client= None,
                 **kwargs) :
        self.promo_id = promo_id
        self.title = title
        self.subtitle = subtitle
        self.heading = heading
        self.url = url
        self.url_scheme = url_scheme
        self.text_color = text_color
        self.gradient = gradient
        self.image = image

        self.client = client
        self._id_attrs = (self.promo_id, self.title, self.subtitle, self.heading,
                          self.url, self.url_scheme, self.text_color, self.gradient, self.image)

    @classmethod
    def de_json(cls, data, client):
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client`, представляющий клиент
                Yandex Music.

        Returns:
            :obj:`yandex_music.Promotion`: Объект класса :class:`yandex_music.Promotion`.
        """
        if not data:
            return None

        data = super(Promotion, cls).de_json(data, client)

        return cls(client=client, **data)

    @classmethod
    def de_list(cls, data, client):
        """Десериализация списка объектов.

        Args:
            data (:obj:`list`): Список словарей с полями и значениями десериализуемого объекта.
            client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client`, представляющий клиент
                Yandex Music.

        Returns:
            :obj:`list` из :obj:`yandex_music.Promotion`: Список объектов класса :class:`yandex_music.Promotion`.
        """
        if not data:
            return []

        promotions = list()
        for promotion in data:
            promotions.append(cls.de_json(promotion, client))

        return promotions
