# coding=utf-8


from yandex_music import YandexMusicObject


class ShotData(YandexMusicObject):
	"""Класс, представляющий основную информацию о шоте.

	Attributes:
		cover_uri (:obj:`str`): Ссылка на обложку шота (иконка Алисы).
		mds_url (:obj:`str`): Ссылка на аудиоверсию шота в озвучке от Алисы.
		shot_text (:obj:`str`): Текстовая версия шота.
		shot_type (:obj:`yandex_music.ShotType`): Объект класса :class:`yandex_music.ShotType` представляющий тип
			шота.
		client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client`, представляющий клиент
				Yandex Music.

	Args:
		cover_uri (:obj:`str`): Ссылка на обложку шота (иконка Алисы).
		mds_url (:obj:`str`): Ссылка на аудиоверсию шота в озвучке от Алисы.
		shot_text (:obj:`str`): Текстовая версия шота.
		shot_type (:obj:`yandex_music.ShotType`): Объект класса :class:`yandex_music.ShotType` представляющий тип
			шота.
		client (:obj:`yandex_music.Client`, optional): Объект класса :class:`yandex_music.Client`, представляющий клиент
			Yandex Music.
		**kwargs: Произвольные ключевые аргументы полученные от API.
	"""

	def __init__(self,
				 cover_uri,
				 mds_url,
				 shot_text,
				 shot_type,
				 client=None,
				 **kwargs):
		self.cover_uri = cover_uri
		self.mds_url = mds_url
		self.shot_text = shot_text
		self.shot_type = shot_type

		self.client = client
		self._id_attrs = (self.cover_uri, self.mds_url, self.shot_text, self.shot_type)

	def download_cover(self, filename, size='200x200'):
		"""Загрузка обложки.

		Args:
			filename (:obj:`str`): Путь для сохранения файла с названием и расширением.
			size (:obj:`str`, optional): Размер обложки.
		"""
		self.client.request.download('https://%s' % self.cover_uri.replace("%%", size), filename)

	def download_mds(self, filename):
		"""Загрузка аудиоверсии шота.

		Args:
			filename (:obj:`str`): Путь для сохранения файла с названием и расширением.
		"""
		self.client.request.download(self.mds_url, filename)

	@classmethod
	def de_json(cls, data, client):
		"""Десериализация объекта.

		Args:
			data (:obj:`dict`): Поля и значения десериализуемого объекта.
			client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client`, представляющий клиент
				Yandex Music.

		Returns:
			:obj:`yandex_music.ShotData`: Объект класса :class:`yandex_music.ShotData`.
		"""
		if not data:
			return None

		data = super(ShotData, cls).de_json(data, client)
		from yandex_music import ShotType
		data['shot_type'] = ShotType.de_json(data.get('shot_type'), client)

		return cls(client=client, **data)

	# camelCase псевдонимы

	#: Псевдоним для :attr:`download_cover`
	downloadCover = download_cover
	#: Псевдоним для :attr:`download_mds`
	downloadMds = download_mds
