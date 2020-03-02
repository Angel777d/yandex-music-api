# coding=utf-8
# coding=utf-8
# coding=utf-8


from yandex_music import YandexMusicObject




class ChartItem(YandexMusicObject):
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
                 track,
                 chart,
                 client= None,
                 **kwargs) :
        self.track = track
        self.chart = chart

        self.client = client
        self._id_attrs = (self.track, self.chart)

    @classmethod
    def de_json(cls, data, client):
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client`, представляющий клиент
                Yandex Music.

        Returns:
            :obj:`yandex_music.ChartItem`: Объект класса :class:`yandex_music.ChartItem`.
        """
        if not data:
            return None

        data = super(ChartItem, cls).de_json(data, client)
        from yandex_music import Chart, Track
        data['track'] = Track.de_json(data.get('track'), client)
        data['chart'] = Chart.de_json(data.get('chart'), client)

        return cls(client=client, **data)

    @classmethod
    def de_list(cls, data, client):
        """Десериализация списка объектов.

        Args:
            data (:obj:`list`): Список словарей с полями и значениями десериализуемого объекта.
            client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client`, представляющий клиент
                Yandex Music.

        Returns:
            :obj:`list` из :obj:`yandex_music.ChartItem`: Список объектов класса :class:`yandex_music.ChartItem`.
        """
        if not data:
            return []

        tracks = list()
        for track in data:
            tracks.append(cls.de_json(track, client))

        return tracks
