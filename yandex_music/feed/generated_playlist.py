# coding=utf-8
# coding=utf-8
# coding=utf-8


from yandex_music import YandexMusicObject




class GeneratedPlaylist(YandexMusicObject):
    """Класс, представляющий автоматически сгенерированный плейлист.

    Note:
        Известные значения `type`: `playlistOfTheDay`, `origin`, `recentTracks`, `neverHeard`, `podcasts`,
        `missedLikes`.

    Attributes:
        type (:obj:`str`): Тип сгенерированного плейлиста.
        ready (:obj:`bool`): Готовность плейлиста.
        notify (:obj:`bool`): Уведомлён ли пользователь об обновлении содержания.
        data (:obj:`yandex_music.Playlist`): Объект класса :class:`yandex_music.Playlist`, представляющий \
            сгенерированный плейлист.
        client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client`, представляющий клиент
                Yandex Music.

    Args:
        type_ (:obj:`str`): Тип сгенерированного плейлиста.
        ready (:obj:`bool`): Готовность плейлиста.
        notify (:obj:`bool`): Уведомлён ли пользователь об обновлении содержания.
        data (:obj:`yandex_music.Playlist`, optional): Объект класса :class:`yandex_music.Playlist`, представляющий \
            сгенерированный плейлист.
        client (:obj:`yandex_music.Client`, optional): Объект класса :class:`yandex_music.Client`, представляющий клиент
            Yandex Music.
        **kwargs: Произвольные ключевые аргументы полученные от API.
    """

    def __init__(self,
                 type_,
                 ready,
                 notify,
                 data,
                 client= None,
                 **kwargs) :
        self.type = type_
        self.ready = ready
        self.notify = notify
        self.data = data

        self.client = client
        self._id_attrs = (self.type, self.ready, self.notify, self.data)

    @classmethod
    def de_json(cls, data, client):
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client`, представляющий клиент
                Yandex Music.

        Returns:
            :obj:`yandex_music.GeneratedPlaylist`: Объект класса :class:`yandex_music.GeneratedPlaylist`.
        """
        if not data:
            return None

        data = super(GeneratedPlaylist, cls).de_json(data, client)
        from yandex_music import Playlist
        data['data'] = Playlist.de_json(data.get('data'), client)

        return cls(client=client, **data)

    @classmethod
    def de_list(cls, data, client):
        """Десериализация списка объектов.

        Args:
            data (:obj:`list`): Список словарей с полями и значениями десериализуемого объекта.
            client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client`, представляющий клиент
                Yandex Music.

        Returns:
            :obj:`list` из :obj:`yandex_music.GeneratedPlaylist`: Список объектов класса
            :class:`yandex_music.GeneratedPlaylist`.
        """
        if not data:
            return []

        generated_playlists = list()
        for generated_playlist in data:
            generated_playlists.append(cls.de_json(generated_playlist, client))

        return generated_playlists
