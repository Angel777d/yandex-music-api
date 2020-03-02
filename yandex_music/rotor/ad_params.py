# coding=utf-8
# coding=utf-8


from yandex_music import YandexMusicObject




class AdParams(YandexMusicObject):
    """Класс, представляющий параметры рекламного объявления.

    Note:
        Известные дополнительные параметры(`other_params`): `user:{ID}`.

    Attributes:
        partner_id (:obj:`str` | :obj:`int`): Уникальный идентификатор заказчика рекламы.
        category_id (:obj:`str` | :obj:`int`): Уникальный идентификатор категории рекламы.
        page_ref (:obj:`str`): Ссылка на ссылающуюся страницу.
        target_ref (:obj:`str`): Ссылка на целевую страницу.
        other_params (:obj:`str`): Другие параметры.
        ad_volume (:obj:`int`): Громкость воспроизводимой рекламы.
        genre_id (:obj:`str`): Уникальный идентификатор жанра.
        genre_name (:obj:`str`): Название жанра.
        client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client`, представляющий клиент
                Yandex Music.

    Args:
        partner_id (:obj:`str` | :obj:`int`): Уникальный идентификатор заказчика рекламы.
        category_id (:obj:`str` | :obj:`int`): Уникальный идентификатор категории рекламы.
        page_ref (:obj:`str`): Ссылка на ссылающуюся страницу.
        target_ref (:obj:`str`): Ссылка на целевую страницу.
        other_params (:obj:`str`): Другие параметры.
        ad_volume (:obj:`int`): Громкость воспроизводимой рекламы.
        genre_id (:obj:`str`, optional): Уникальный идентификатор жанра.
        genre_name (:obj:`str`, optional): Название жанра.
        client (:obj:`yandex_music.Client`, optional): Объект класса :class:`yandex_music.Client`, представляющий клиент
            Yandex Music.
        **kwargs: Произвольные ключевые аргументы полученные от API.
    """

    def __init__(self,
                 partner_id,
                 category_id,
                 page_ref,
                 target_ref,
                 other_params,
                 ad_volume,
                 genre_id= None,
                 genre_name= None,
                 client= None,
                 **kwargs) :
        self.partner_id = partner_id
        self.category_id = category_id
        self.page_ref = page_ref
        self.target_ref = target_ref
        self.other_params = other_params
        self.ad_volume = ad_volume

        self.genre_id = genre_id
        self.genre_name = genre_name

        self.client = client
        self._id_attrs = (self.partner_id, self.category_id, self.page_ref,
                          self.target_ref, self.other_params, self.ad_volume)

    @classmethod
    def de_json(cls, data, client):
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client`, представляющий клиент
                Yandex Music.

        Returns:
            :obj:`yandex_music.AdParams`: Объект класса :class:`yandex_music.AdParams`.
        """
        if not data:
            return None

        data = super(AdParams, cls).de_json(data, client)

        return cls(client=client, **data)
