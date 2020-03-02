# coding=utf-8
# coding=utf-8
# coding=utf-8


from yandex_music import YandexMusicObject




class StationResult(YandexMusicObject):
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
                 station,
                 settings,
                 settings2,
                 ad_params,
                 explanation= None,
                 prerolls= None,
                 client= None,
                 **kwargs) :
        self.station = station
        self.settings = settings
        self.settings2 = settings2
        self.ad_params = ad_params
        self.explanation = explanation
        self.prerolls = prerolls

        self.client = client
        self._id_attrs = (self.station, self.settings, self.settings2, self.ad_params)

    @classmethod
    def de_json(cls, data, client):
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client`, представляющий клиент
                Yandex Music.

        Returns:
            :obj:`yandex_music.StationResult`: Объект класса :class:`yandex_music.StationResult`.
        """
        if not data:
            return None

        data = super(StationResult, cls).de_json(data, client)
        from yandex_music import Station, RotorSettings, AdParams
        data['station'] = Station.de_json(data.get('station'), client)
        data['settings'] = RotorSettings.de_json(data.get('settings'), client)
        data['settings2'] = RotorSettings.de_json(data.get('settings2'), client)
        data['ad_params'] = AdParams.de_json(data.get('ad_params'), client)

        return cls(client=client, **data)

    @classmethod
    def de_list(cls, data, client):
        """Десериализация списка объектов.

        Args:
            data (:obj:`list`): Список словарей с полями и значениями десериализуемого объекта.
            client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client`, представляющий клиент
                Yandex Music.

        Returns:
            :obj:`list` из :obj:`yandex_music.StationResult`: Список объектов класса :class:`yandex_music.StationResult`.
        """
        if not data:
            return []

        station_results = list()
        for station_result in data:
            station_results.append(cls.de_json(station_result, client))

        return station_results
