# coding=utf-8

from yandex_music import YandexMusicObject, Playlist, ChartInfoMenu


class ChartInfo(YandexMusicObject):
	"""Класс, представляющий чарт.

	Attributes:
		id (:obj:`str`): Уникальный идентификатор блока.
		type (:obj:`str`): Тип блока.
		type_for_from (:obj:`str`): Откуда получен блок (как к нему пришли).
		title (:obj:`str`): Заголовок.
		menu (:obj:`yandex_music.ChartInfoMenu` | :obj:`None`): Меню TODO.
		chart (:obj:`yandex_music.Playlist` | :obj:`None`): Плейлист.
		chart_description (:obj:`str`): Описание.
		client (:obj:`yandex_music.Client`): Клиент Yandex Music.

	Args:
		id_ (:obj:`str`): Уникальный идентификатор блока.
		type_ (:obj:`str`): Тип блока.
		type_for_from (:obj:`str`): Откуда получен блок (как к нему пришли).
		title (:obj:`str`): Заголовок.
		menu (:obj:`yandex_music.ChartInfoMenu`, optional): Меню TODO.
		chart (:obj:`yandex_music.Playlist`, optional): Плейлист.
		chart_description (:obj:`str`, optional): Описание.
		client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
	"""

	def __init__(self, id_, type_, type_for_from, title, menu, chart, chart_description, client):
		self.id = id_
		self.type = type_
		self.type_for_from = type_for_from
		self.title = title

		self.menu = menu
		self.chart = chart
		self.chart_description = chart_description

		self.client = client
		self._id_attrs = (id_,)

	@classmethod
	def de_json(cls, data, client):
		"""Десериализация объекта.

		Args:
			data (:obj:`dict`): Поля и значения десериализуемого объекта.
			client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

		Returns:
			:obj:`yandex_music.ChartInfo`: Чарт.
		"""
		if not data:
			return None

		data = super(ChartInfo, cls).de_json(data, client)
		data['chart'] = Playlist.de_json(data.get('chart'), client)
		data['menu'] = ChartInfoMenu.de_json(data.get('menu'), client)

		return cls(client=client, **data)
