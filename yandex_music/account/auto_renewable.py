# coding=utf-8


from yandex_music import YandexMusicObject




class AutoRenewable(YandexMusicObject):
    """Класс, представляющий автопродление подписки.

    Attributes:
        expires (:obj:`str`): Дата истечения подписки.
        vendor (:obj:`str`): Продавец.
        vendor_help_url (:obj:`str`): Ссылка на страницу помощи продавца.
        product_id (:obj:`str`): Уникальный идентификатор продукта.
        product (:obj:`yandex_music.Product`): Объект класса :class:`yandex_music.Product` представляющий продукт.
        order_id (:obj:`int`): Уникальный идентификатор заказа.
        finished (:obj:`bool`): Завершенность автопродления.
        client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client`, представляющий клиент
                Yandex Music.

    Args:
        expires (:obj:`str`): Дата истечения подписки.
        vendor (:obj:`str`): Продавец.
        vendor_help_url (:obj:`str`): Ссылка на страницу помощи продавца.
        product_id (:obj:`str`): Уникальный идентификатор продукта.
        finished (:obj:`bool`): Завершенность автопродления.
        product (:obj:`yandex_music.Product`, optional): Объект класса :class:`yandex_music.Product` представляющий
            продукт.
        order_id (:obj:`int`): Уникальный идентификатор заказа.
        client (:obj:`yandex_music.Client`, optional): Объект класса :class:`yandex_music.Client`, представляющий клиент
            Yandex Music.
        **kwargs: Произвольные ключевые аргументы полученные от API.
    """

    def __init__(self,
                 expires,
                 vendor,
                 vendor_help_url,
                 product,
                 finished,
                 product_id= None,
                 order_id= None,
                 client= None,
                 **kwargs) :
        self.expires = expires
        self.vendor = vendor
        self.vendor_help_url = vendor_help_url
        self.product = product
        self.finished = finished

        self.product_id = product_id
        self.order_id = order_id

        self.client = client
        self._id_attrs = (self.expires, self.vendor, self.vendor_help_url, self.product, self.finished)

    @classmethod
    def de_json(cls, data, client):
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client`, представляющий клиент
                Yandex Music.

        Returns:
            :obj:`yandex_music.AutoRenewable`: Объект класса :class:`yandex_music.AutoRenewable`.
        """
        if not data:
            return None

        data = super(AutoRenewable, cls).de_json(data, client)
        from yandex_music import Product
        data['product'] = Product.de_json(data.get('product'), client)

        return cls(client=client, **data)

    @classmethod
    def de_list(cls, data, client):
        """Десериализация списка объектов.

        Args:
            data (:obj:`list`): Список словарей с полями и значениями десериализуемого объекта.
            client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client`, представляющий клиент
                Yandex Music.

        Returns:
            :obj:`list` из :obj:`yandex_music.AutoRenewable`: Список объектов класса
            :class:`yandex_music.AutoRenewable`.
        """
        if not data:
            return []

        auto_renewables = list()
        for auto_renewable in data:
            auto_renewables.append(cls.de_json(auto_renewable, client))

        return auto_renewables
