# coding=utf-8


from yandex_music import YandexMusicObject




class Station(YandexMusicObject):
    """Класс, представляющий станцию.

    Note:
        `id_for_from` обозначает предка станции, например, жанр, настроение или занятие.
        Неизвестно когда используется `id_for_from`, а когда `parent_id`.

    Attributes:
        id (:obj:`yandex_music.Id`): Объект класса :class:`yandex_music.Id`, представляющий уникальный идентификатор
            станции.
        name (:obj:`str`): Название станции.
        icon (:obj:`yandex_music.Icon`): Объект класса :class:`yandex_music.Icon`, представляющий иконку станции.
        mts_icon (:obj:`yandex_music.Icon`): Объект класса :class:`yandex_music.Icon`, представляющий иконку TODO.
        geocell_icon (:obj:`yandex_music.Icon`): Объект класса :class:`yandex_music.Icon`, представляющий иконку TODO.
        id_for_from (:obj:`str`): Категория (тип) станции.
        restrictions (:obj:`yandex_music.Restrictions`): Объект класса :class:`yandex_music.Restrictions`,
            представляющий ограничения для настроек станции старого формата.
        restrictions2 (:obj:`yandex_music.Restrictions`): Объект класса :class:`yandex_music.Restrictions`,
            представляющий ограничения для настроек станции.
        parent_id (:obj:`yandex_music.Id`): Объект класса :class:`yandex_music.Id`, представляющий уникальный
            идентификатор станции, являющейся предком текущей.
        client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client`, представляющий клиент
                Yandex Music.

    Args:
        id_ (:obj:`yandex_music.Id`): Объект класса :class:`yandex_music.Id`, представляющий уникальный идентификатор
            станции.
        name (:obj:`str`): Название станции.
        icon (:obj:`yandex_music.Icon`): Объект класса :class:`yandex_music.Icon`, представляющий иконку станции.
        mts_icon (:obj:`yandex_music.Icon`): Объект класса :class:`yandex_music.Icon`, представляющий иконку TODO.
        geocell_icon (:obj:`yandex_music.Icon`): Объект класса :class:`yandex_music.Icon`, представляющий иконку TODO.
        id_for_from (:obj:`str`): Категория (тип) станции.
        restrictions (:obj:`yandex_music.Restrictions`): Объект класса :class:`yandex_music.Restrictions`,
            представляющий ограничения для настроек станции старого формата.
        restrictions2 (:obj:`yandex_music.Restrictions`): Объект класса :class:`yandex_music.Restrictions`,
            представляющий ограничения для настроек станции.
        parent_id (:obj:`yandex_music.Id`, optional): Объект класса :class:`yandex_music.Id`, представляющий уникальный
            идентификатор станции, являющейся предком текущей.
        client (:obj:`yandex_music.Client`, optional): Объект класса :class:`yandex_music.Client`, представляющий клиент
            Yandex Music.
        **kwargs: Произвольные ключевые аргументы полученные от API.
    """

    def __init__(self,
                 id_,
                 name,
                 icon,
                 mts_icon,
                 geocell_icon,
                 id_for_from,
                 restrictions,
                 restrictions2,
                 parent_id= None,
                 client= None,
                 **kwargs) :
        self.id = id_
        self.name = name
        self.icon = icon
        self.mts_icon = mts_icon
        self.geocell_icon = geocell_icon
        self.id_for_from = id_for_from
        self.restrictions = restrictions
        self.restrictions2 = restrictions2

        self.parent_id = parent_id

        self.client = client
        self._id_attrs = (self.id, self.name, self.icon, self.mts_icon, self.geocell_icon,
                          self.id_for_from, self.restrictions, self.restrictions2)

    @classmethod
    def de_json(cls, data, client):
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client`, представляющий клиент
                Yandex Music.

        Returns:
            :obj:`yandex_music.Station`: Объект класса :class:`yandex_music.Station`.
        """
        if not data:
            return None

        data = super(Station, cls).de_json(data, client)
        from yandex_music import Id, Icon, Restrictions
        data['id_'] = Id.de_json(data.get('id_'), client)
        data['parent_id'] = Id.de_json(data.get('parent_id'), client)
        data['icon'] = Icon.de_json(data.get('icon'), client)
        data['mts_icon'] = Icon.de_json(data.get('mts_icon'), client)
        data['geocell_icon'] = Icon.de_json(data.get('geocell_icon'), client)
        data['restrictions'] = Restrictions.de_json(data.get('restrictions'), client)
        data['restrictions2'] = Restrictions.de_json(data.get('restrictions2'), client)

        return cls(client=client, **data)
