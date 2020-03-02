# coding=utf-8


from yandex_music import YandexMusicObject


class UserSettings(YandexMusicObject):
	"""Класс, представляющий настройки пользователя.

	Note:
		Доступные значения для поля `theme`: `white`, `black`.

		Доступные значения для полей `user_music_visibility` и `user_social_visibility`: `private`, `public`.

	Notes:
		`promos_disabled`, `ads_disabled`, `rbt_disabled` устарели и не работают.

		`last_fm_scrobbling_enabled`, `facebook_scrobbling_enabled` выглядят устаревшими.

	Attributes:
		uid (:obj:`int`): Уникальный идентификатор пользователя.
		last_fm_scrobbling_enabled (:obj:`bool`): Скробблинг lastfm.
		shuffle_enabled (:obj:`bool`): Переключать треки в случайном порядке.
		volume_percents (:obj:`int`): Громкость звука в процентах.
		modified (:obj:`str`): Дата изменения настроек.
		facebook_scrobbling_enabled (:obj:`bool`): Скробблинг facebook.
		add_new_track_on_playlist_top (:obj:`bool`): Добавлять новые треки в начало плейлиста.
		user_music_visibility (:obj:`str`): Публичный доступ к моей фонотеке.
		user_social_visibility (:obj:`str`): Показывать соцсети на странице.
		rbt_disabled (:obj:`bool`): TODO (неиспользуемая фича).
		theme (:obj:`str`): Тема оформления.
		promos_disabled (:obj:`bool`): Не показывать рекламируемый контент).
		auto_play_radio (:obj:`bool`): Бесконечный поток музыки.
		ads_disabled (:obj:`bool`): Не показывать рекламу.
		disk_enabled (:obj:`bool`): TODO.
		show_disk_tracks_in_library (:obj:`bool`): Показывать локальные треки в библиотеке.
		client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client`, представляющий клиент
				Yandex Music.

	Args:
		uid (:obj:`int`): Уникальный идентификатор пользователя.
		last_fm_scrobbling_enabled (:obj:`bool`): Скробблинг lastfm.
		shuffle_enabled (:obj:`bool`): Переключать треки в случайном порядке.
		volume_percents (:obj:`int`): Громкость звука в процентах.
		modified (:obj:`str`): Дата изменения настроек.
		facebook_scrobbling_enabled (:obj:`bool`): Скробблинг facebook.
		add_new_track_on_playlist_top (:obj:`bool`): Добавлять новые треки в начало плейлиста.
		user_music_visibility (:obj:`str`): Публичный доступ к моей фонотеке.
		user_social_visibility (:obj:`str`): Показывать соцсети на странице.
		rbt_disabled (:obj:`bool`): TODO (неиспользуемая фича).
		theme (:obj:`str`): Тема оформления.
		promos_disabled (:obj:`bool`): Не показывать рекламируемый контент).
		auto_play_radio (:obj:`bool`): Бесконечный поток музыки.
		ads_disabled (:obj:`bool`, optional): Не показывать рекламу.
		disk_enabled (:obj:`bool`, optional): TODO.
		show_disk_tracks_in_library (:obj:`bool`, optional): Показывать локальные треки в библиотеке.
		client (:obj:`yandex_music.Client`, optional): Объект класса :class:`yandex_music.Client`, представляющий клиент
			Yandex Music.
		**kwargs: Произвольные ключевые аргументы полученные от API.
	"""

	def __init__(self,
	             uid,
	             last_fm_scrobbling_enabled,
	             shuffle_enabled,
	             volume_percents,
	             modified,
	             facebook_scrobbling_enabled,
	             add_new_track_on_playlist_top,
	             user_music_visibility,
	             user_social_visibility,
	             rbt_disabled,
	             theme,
	             promos_disabled,
	             auto_play_radio,
	             ads_disabled=None,
	             disk_enabled=None,
	             show_disk_tracks_in_library=None,
	             client=None,
	             **kwargs):
		self.uid = uid
		self.last_fm_scrobbling_enabled = last_fm_scrobbling_enabled
		self.shuffle_enabled = shuffle_enabled
		self.volume_percents = volume_percents
		self.modified = modified
		self.facebook_scrobbling_enabled = facebook_scrobbling_enabled
		self.add_new_track_on_playlist_top = add_new_track_on_playlist_top
		self.user_music_visibility = user_music_visibility
		self.user_social_visibility = user_social_visibility
		self.rbt_disabled = rbt_disabled
		self.theme = theme
		self.promos_disabled = promos_disabled
		self.auto_play_radio = auto_play_radio

		self.ads_disabled = ads_disabled
		self.disk_enabled = disk_enabled
		self.show_disk_tracks_in_library = show_disk_tracks_in_library

		self.client = client
		self._id_attrs = (self.uid, self.last_fm_scrobbling_enabled, self.shuffle_enabled, self.volume_percents,
		                  self.modified, self.facebook_scrobbling_enabled, self.add_new_track_on_playlist_top,
		                  self.user_music_visibility, self.user_social_visibility, self.rbt_disabled, self.theme,
		                  self.promos_disabled, self.auto_play_radio, self.ads_disabled, self.disk_enabled,
		                  self.show_disk_tracks_in_library)

	@classmethod
	def de_json(cls, data, client):
		"""Десериализация объекта.

		Args:
			data (:obj:`dict`): Поля и значения десериализуемого объекта.
			client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client`, представляющий клиент
				Yandex Music.

		Returns:
			:obj:`yandex_music.UserSettings`: Объект класса :class:`yandex_music.UserSettings`.
		"""
		if not data:
			return None

		data = super(UserSettings, cls).de_json(data, client)

		return cls(client=client, **data)
