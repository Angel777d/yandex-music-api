# coding=utf-8


from yandex_music import Album, Artist, Playlist, YandexMusicObject

de_list = {
	'album': Album.de_json,
	'playlist': Playlist.de_json,
}


class Like(YandexMusicObject):
	"""Класс, представляющий объект с отметкой "мне нравится".

	None:
		В поле `type` содержится одно из трёх значений: `artist`, `playlist`, `album`. Обозначает поле, в котором
		содержится информация.

	Attributes:
		type (:obj:`str`): Тип объекта с отметкой.
		id (:obj:`str`): Уникальный идентификатор отметки.
		timestamp (:obj:`str`): Дата и время добавления отметки.
		album (:obj:`yandex_music.Album`): Объект класса :class:`yandex_music.Album`, представляющий понравившейся
			альбом.
		artist (:obj:`yandex_music.Artist`): Объект класса :class:`yandex_music.Artist`, представляющий понравившегося
			артиста.
		playlist (:obj:`yandex_music.Playlist`): Объект класса :class:`yandex_music.Playlist`, представляющий
			понравившейся плейлист.
		client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client`, представляющий клиент
				Yandex Music.

	Args:
		type (:obj:`str`): Тип объекта с отметкой.
		id (:obj:`str`, optional): Уникальный идентификатор отметки.
		timestamp (:obj:`str`, optional): Дата и время добавления отметки.
		album (:obj:`yandex_music.Album`, optional): Объект класса :class:`yandex_music.Album`, представляющий
			понравившейся альбом
		artist (:obj:`yandex_music.Artist`, optional): Объект класса :class:`yandex_music.Artist`, представляющий
			понравившегося артиста.
		playlist (:obj:`yandex_music.Playlist`, optional): Объект класса :class:`yandex_music.Playlist`, представляющий
			понравившейся плейлист.
		client (:obj:`yandex_music.Client`, optional): Объект класса :class:`yandex_music.Client`, представляющий клиент
			Yandex Music.
		**kwargs: Произвольные ключевые аргументы полученные от API.
	"""

	def __init__(self,
	             type_,
	             id_=None,
	             timestamp= None,
	             album= None,
	             artist= None,
	             playlist= None,
	             client= None,
	             **kwargs):
		self.id = id_
		self.type = type_

		self.album = album
		self.artist = artist
		self.playlist = playlist
		self.timestamp = timestamp

		self.client = client
		self._id_attrs = (self.id, self.type, self.timestamp, self.album, self.artist, self.playlist)

	@classmethod
	def de_json(cls, data, client, type_=None):
		"""Десериализация объекта.

		Args:
			data (:obj:`dict`): Поля и значения десериализуемого объекта.
			type_ (:obj:`str`, optional): Тип объекта с отметкой "мне нравится".
			client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client`, представляющий клиент
				Yandex Music.

		Returns:
			:obj:`yandex_music.Like`: Объект класса :class:`yandex_music.Like`.
		"""
		if not data:
			return None

		data = super(Like, cls).de_json(data, client)

		if type_ == 'artist':
			if 'artist' not in data:
				temp_data = data.copy()
				data.clear()
				data[type_] = Artist.de_json(temp_data, client)
			else:
				data[type_] = Artist.de_json(data.get('artist'), client)
		else:
			data[type_] = de_list[type_](data.get(type_), client)

		data['type_'] = type_

		return cls(client=client, **data)

	@classmethod
	def de_list(cls, data, client, type_=None):
		"""Десериализация списка объектов.

		Args:
			data (:obj:`list`): Список словарей с полями и значениями десериализуемого объекта.
			type_ (:obj:`str`, optional): Тип объекта с отметкой "мне нравится".
			client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client`, представляющий клиент
				Yandex Music.

		Returns:
			:obj:`list` из :obj:`yandex_music.Like`: Список объектов класса :class:`yandex_music.Like`.
		"""
		if not data:
			return []

		likes = list()
		for like in data:
			likes.append(cls.de_json(like, client, type_))

		return likes
