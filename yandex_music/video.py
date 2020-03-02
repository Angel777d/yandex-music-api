# coding=utf-8
# coding=utf-8
# coding=utf-8
# coding=utf-8
# coding=utf-8


from yandex_music import YandexMusicObject




class Video(YandexMusicObject):
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
                 title,
                 cover= None,
                 embed_url= None,
                 provider= None,
                 provider_video_id= None,
                 youtube_url= None,
                 thumbnail_url= None,
                 duration=None,
                 text=None,
                 html_auto_play_video_player=None,
                 regions=None,
                 client= None,
                 **kwargs):
        self.title = title

        # Видео из brief info
        self.cover = cover
        self.embed_url = embed_url
        self.provider = provider
        self.provider_video_id = provider_video_id

        # Видео из результатов поиска
        self.youtube_url = youtube_url
        self.thumbnail_url = thumbnail_url
        self.duration = duration
        self.text = text
        self.html_auto_play_video_player = html_auto_play_video_player
        self.regions = regions

        self.client = client
        self._id_attrs = (self.provider_video_id, self.youtube_url, self.title)

    @classmethod
    def de_json(cls, data, client):
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client`, представляющий клиент
                Yandex Music.

        Returns:
            :obj:`yandex_music.Video`: Объект класса :class:`yandex_music.Video`.
        """
        if not data:
            return None

        data = super(Video, cls).de_json(data, client)

        return cls(client=client, **data)

    @classmethod
    def de_list(cls, data, client):
        """Десериализация списка объектов.

        Args:
            data (:obj:`list`): Список словарей с полями и значениями десериализуемого объекта.
            client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client`, представляющий клиент
                Yandex Music.

        Returns:
            :obj:`list` из :obj:`yandex_music.Video`: Список объектов класса :class:`yandex_music.Video`.
        """
        if not data:
            return []

        videos = list()
        for video in data:
            videos.append(cls.de_json(video, client))

        return videos
