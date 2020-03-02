# coding=utf-8
# coding=utf-8


from yandex_music import YandexMusicObject




class RotorSettings(YandexMusicObject):
    """Класс, представляющий настройки станции.

    Note:
        Поля `energy`, `mood` используются в старых настройках (`settings1`).

        Значения `mood_energy`: `fun`, `active`, `calm`, `sad`, `all`.

        Значения `diversity`: `favorite`, `popular`, `discover`, `default`.

        Значения `language`: `not-russian`, `russian`, `any`.

    Attributes:
        language (:obj:`str`): Язык.
        diversity (:obj:`str`): Разнообразие (треки).
        mood (:obj:`int`): Настроение (старое).
        energy (:obj:`int`): Энергичное.
        mood_energy (:obj:`str`): Настроение.
        client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client`, представляющий клиент
                Yandex Music.

    Args:
        language (:obj:`str`): Язык.
        diversity (:obj:`str`): Разнообразие (треки).
        mood (:obj:`int`, optional): Настроение (старое).
        energy (:obj:`int`, optional): Энергичное.
        mood_energy (:obj:`str`, optional): Настроение.
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
            :obj:`yandex_music.RotorSettings`: Объект класса :class:`yandex_music.RotorSettings`.
        """
        if not data:
            return None

        data = super(RotorSettings, cls).de_json(data, client)

        return cls(client=client, **data)
