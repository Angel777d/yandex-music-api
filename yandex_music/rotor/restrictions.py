# coding=utf-8


from yandex_music import YandexMusicObject, Enum, DiscreteScale



de_json = {
    'enum': Enum.de_json,
    'discrete-scale': DiscreteScale.de_json
}


class Restrictions(YandexMusicObject):
    """Класс, представляющий ограничения для настроек станции.

    Attributes:
        language (:obj:`yandex_music.Enum`): Объект класса :class:`yandex_music.Enum`, представляющий перечисление
            значений для языков.
        diversity (:obj:`yandex_music.Enum`): Объект класса :class:`yandex_music.Enum`, представляющий перечисление
            значений для разнообразия (треков).
        mood (:obj:`yandex_music.DiscreteScale`): Объект класса :class:`yandex_music.DiscreteScale`, представляющий
            ограничения для значения настроения.
        energy (:obj:`yandex_music.DiscreteScale`): Объект класса :class:`yandex_music.DiscreteScale`, представляющий
            ограничения для значения энергичности.
        mood_energy (:obj:`yandex_music.Enum`): Объект класса :class:`yandex_music.Enum`, представляющий перечисление
            значений для настроения.
        client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client`, представляющий клиент
                Yandex Music.

    Args:
        language (:obj:`yandex_music.Enum`): Объект класса :class:`yandex_music.Enum`, представляющий перечисление
            значений для языков.
        diversity (:obj:`yandex_music.Enum`): Объект класса :class:`yandex_music.Enum`, представляющий перечисление
            значений для разнообразия (треков).
        mood (:obj:`yandex_music.DiscreteScale`, optional): Объект класса :class:`yandex_music.DiscreteScale`,
            представляющий ограничения для значения настроения.
        energy (:obj:`yandex_music.DiscreteScale`, optional): Объект класса :class:`yandex_music.DiscreteScale`,
            представляющий ограничения для значения энергичности.
        mood_energy (:obj:`yandex_music.Enum`, optional): Объект класса :class:`yandex_music.Enum`, представляющий
            перечисление значений для настроения.
        client (:obj:`yandex_music.Client`, optional): Объект класса :class:`yandex_music.Client`, представляющий клиент
            Yandex Music.
        **kwargs: Произвольные ключевые аргументы полученные от API.
    """

    def __init__(self,
                 language,
                 diversity,
                 mood= None,
                 energy= None,
                 mood_energy= None,
                 client= None,
                 **kwargs) :
        self.language = language
        self.diversity = diversity
        self.mood = mood
        self.energy = energy
        self.mood_energy = mood_energy

        self.client = client
        self._id_attrs = (self.language, self.diversity)

    @classmethod
    def de_json(cls, data, client):
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client`, представляющий клиент
                Yandex Music.

        Returns:
            :obj:`yandex_music.Restrictions`: Объект класса :class:`yandex_music.Restrictions`.
        """
        if not data:
            return None

        data = super(Restrictions, cls).de_json(data, client)

        for key, value in data.items():
            data[key] = de_json.get(value.get('type_'))(value, client)

        return cls(client=client, **data)
