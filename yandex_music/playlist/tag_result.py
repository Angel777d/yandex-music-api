# coding=utf-8
from yandex_music import YandexMusicObject


class TagResult(YandexMusicObject):
	"""Класс, представляющий тег и его плейлисты.

	Attributes:
		tag (:obj:`yandex_music.Tag`): Тег.
		ids (:obj:`list` из :obj:`yandex_music.PlaylistId`): Уникальные идентификаторы плейлистов тега.
		client (:obj:`yandex_music.Client`): Клиент Yandex Music.

	Args:
		tag (:obj:`yandex_music.Tag`): Тег.
		ids (:obj:`list` из :obj:`yandex_music.PlaylistId`): Уникальные идентификаторы плейлистов тега.
		client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
		**kwargs: Произвольные ключевые аргументы полученные от API.
	"""

	def __init__(self, tag, ids, client=None, **kwargs):
		self.tag = tag
		self.ids = ids

		self.client = client
		self._id_attrs = (self.tag, self.ids)

		# YandexMusicObject.handle_unknown_kwargs(self, **kwargs)

	@classmethod
	def de_json(cls, data, client):
		"""Десериализация объекта.

		Args:
			data (:obj:`dict`): Поля и значения десериализуемого объекта.
			client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

		Returns:
			:obj:`yandex_music.TagResult`: Тег и его плейлисты.
		"""
		if not data:
			return None

		data = super(TagResult, cls).de_json(data, client)
		from yandex_music import Tag, PlaylistId
		data['tag'] = Tag.de_json(data.get('tag'), client)
		data['ids'] = PlaylistId.de_list(data.get('ids'), client)

		return cls(client=client, **data)
