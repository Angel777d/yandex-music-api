# coding=utf-8


from yandex_music import YandexMusicObject




class Genre(YandexMusicObject):
    """Класс, представляющий жанр музыки.

    Attributes:
        id (:obj:`str`): Уникальный идентификатор жанра.
        weight (:obj:`int`): Вес TODO (возможно, чем выше показатель, тем больше нравится пользователю).
        composer_top (:obj:`bool`): TODO.
        title (:obj:`str`): Заголовок жанра.
        titles (:obj:`dict`): Словарь заголовков на разных языках, где ключ - язык.
        images (:obj:`yandex_music.Images`): Объект класса :class:`yandex_music.Images`, представляющий изображение
            жанра.
        show_in_menu (:obj:`bool`): Показывать в меню.
        full_title (:obj:`str`): Полный заголовок.
        url_part (:obj:`str`): Часть ссылки на жанр для открытия в браузере.
        color (:obj:`str`): Цвет фона изображения.
        radio_icon (:obj:`yandex_music.Icon`): Объект класса :class:`yandex_music.Images`, представляющий иконку радио
            жанра.
        sub_genres (:obj:`list` из :obj:`yandex_music.Genre`): Список объектов класса :class:`yandex_music.Genre`,
            представляющие поджанры текущего жанра музыки.
        hide_in_regions (:obj:`list`): В каких регионах скрывать жанр.
        client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client`, представляющий клиент
                Yandex Music.

    Args:
        id_ (:obj:`str`): Уникальный идентификатор жанра.
        weight (:obj:`int`): Вес TODO (возможно, чем выше показатель, тем больше нравится пользователю).
        composer_top (:obj:`bool`): TODO.
        title (:obj:`str`): Заголовок жанра.
        titles (:obj:`dict`): Словарь заголовков на разных языках, где ключ - язык.
        images (:obj:`yandex_music.Images`): Объект класса :class:`yandex_music.Images`, представляющий изображение
            жанра.
        show_in_menu (:obj:`bool`): Показывать в меню.
        full_title (:obj:`str`, optional): Полный заголовок.
        url_part (:obj:`str`, optional): Часть ссылки на жанр для открытия в браузере.
        color (:obj:`str`, optional): Цвет фона изображения.
        radio_icon (:obj:`yandex_music.Icon`, optional): Объект класса :class:`yandex_music.Images`, представляющий
            иконку радио жанра.
        sub_genres (:obj:`list` из :obj:`yandex_music.Genre`, optional): Список объектов класса
            :class:`yandex_music.Genre`, представляющие поджанры текущего жанра музыки.
        hide_in_regions (:obj:`list`, optional): В каких регионах скрывать жанр.
        client (:obj:`yandex_music.Client`, optional): Объект класса :class:`yandex_music.Client`, представляющий клиент
            Yandex Music.
        **kwargs: Произвольные ключевые аргументы полученные от API.
    """

    def __init__(self,
                 id_,
                 weight,
                 composer_top,
                 title,
                 titles,
                 images,
                 show_in_menu,
                 full_title= None,
                 url_part= None,
                 color= None,
                 radio_icon= None,
                 sub_genres= None,
                 hide_in_regions=None,
                 client= None,
                 **kwargs) :
        self.id = id_
        self.weight = weight
        self.composer_top = composer_top
        self.title = title
        self.titles = titles
        self.images = images
        self.show_in_menu = show_in_menu

        self.full_title = full_title
        self.url_part = url_part
        self.color = color
        self.radio_icon = radio_icon
        self.sub_genres = sub_genres
        self.hide_in_regions = hide_in_regions

        self.client = client
        self._id_attrs = (self.id, self.weight, self.composer_top, self.title, self.images, self.show_in_menu)

    @classmethod
    def de_json(cls, data, client):
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client`, представляющий клиент
                Yandex Music.

        Returns:
            :obj:`yandex_music.Genre`: Объект класса :class:`yandex_music.Genre`.
        """
        if not data:
            return None

        data = super(Genre, cls).de_json(data, client)
        from yandex_music import Title, Icon, Images
        data['titles'] = Title.de_dict(data.get('titles'), client)
        data['images'] = Images.de_json(data.get('images'), client)
        data['radio_icon'] = Icon.de_json(data.get('radio_icon'), client)
        data['sub_genres'] = Genre.de_list(data.get('sub_genres'), client)

        return cls(client=client, **data)

    @classmethod
    def de_list(cls, data, client):
        """Десериализация списка объектов.

        Args:
            data (:obj:`list`): Список словарей с полями и значениями десериализуемого объекта.
            client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client`, представляющий клиент
                Yandex Music.

        Returns:
            :obj:`list` из :obj:`yandex_music.Genre`: Список объектов класса :class:`yandex_music.Genre`.
        """
        if not data:
            return []

        genres = list()
        for genre in data:
            genres.append(cls.de_json(genre, client))

        return genres
