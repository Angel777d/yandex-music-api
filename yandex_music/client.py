# coding=utf-8
import functools
import logging
import time
from datetime import datetime

from yandex_music import Album, Artist, ArtistAlbums, ArtistTracks, BriefInfo, Dashboard, DownloadInfo, Experiments, \
	Feed, Genre, Landing, Like, PermissionAlerts, Playlist, PromoCodeStatus, Search, Settings, ShotEvent, SimilarTracks, \
	StationResult, StationTracksResult, Status, Suggestions, Supplement, Track, TracksList, UserSettings, \
	YandexMusicObject, ChartInfo, TagResult
from yandex_music.exceptions import Captcha, InvalidToken
from yandex_music.utils.difference import Difference
from yandex_music.utils.request import Request

CLIENT_ID = '23cabbbdc6cd418abb4b39c32c41195d'
CLIENT_SECRET = '53bc75238f0c4d08a118e51fe9203300'

de_list = {
	'artist': Artist.de_list,
	'album': Album.de_list,
	'track': Track.de_list,
	'playlist': Playlist.de_list,
}

logging.getLogger(__name__).addHandler(logging.NullHandler())


def log(method):
	logger = logging.getLogger(method.__module__)

	@functools.wraps(method)
	def wrapper(*args, **kwargs):
		logger.debug('Entering: %s' % method.__name__)

		result = method(*args, **kwargs)
		logger.debug(result)

		logger.debug('Exiting: %s' % method.__name__)

		return result

	return wrapper


class Client(YandexMusicObject):
	"""Класс, представляющий клиент Yandex Music.

	Note:
		При `fetch_account_status = False` многие сокращения перестанут работать в связи с тем, что неоткуда будет взять
		uid аккаунта для отправки запроса. Так же в большинстве методов придётся передавать `uid` явно.

	Attributes:
		logger (:obj:`logging.Logger`): Объект логера.
		token (:obj:`str`): Уникальный ключ для аутентификации.
		base_url (:obj:`str`): Ссылка на API Yandex Music.
		oauth_url (:obj:`str`): Ссылка на OAuth Yandex Music.
		me (:obj:`yandex_music.Status`): Объект класса :class:`yandex_music.Status` представляющего основную
			информацию об аккаунте.

	Args:
		token (:obj:`str`, optional): Уникальный ключ для аутентификации.
		fetch_account_status (:obj:`bool`, optional): Получить ли информацию об аккаунте при инициализации объекта.
		base_url (:obj:`str`, optional): Ссылка на API Yandex Music.
		oauth_url (:obj:`str`, optional): Ссылка на OAuth Yandex Music.
		request (:obj:`yandex_music.utils.request.Request`, optional): Пре-инициализация
			:class:`yandex_music.utils.request.Request`.
	"""

	def __init__(self, token=None, fetch_account_status=True, base_url=None,
				 oauth_url=None, request=None):
		self.logger = logging.getLogger(__name__)
		self.token = token

		if base_url is None:
			base_url = 'https://api.music.yandex.net'
		if oauth_url is None:
			oauth_url = 'https://oauth.yandex.ru'

		self.base_url = base_url
		self.oauth_url = oauth_url

		if request:
			self._request = request
			self._request.set_and_return_client(self)
		else:
			self._request = Request(self)

		self.me = None
		if fetch_account_status:
			self.me = self.account_status()

	@classmethod
	def from_credentials(cls, username, password, x_captcha_answer=None, x_captcha_key=None,
						 captcha_callback=None, *args, **kwargs):
		"""Инициализция клиента по логину и паролю.

		Note:
			Данный метод получает токен каждый раз при вызове. Рекомендуется сгенерировать его самостоятельно, сохранить
			и использовать при следующих инициализациях клиента. Не храните логины и пароли!

		Args:
			username (:obj:`str`): Логин клиента (идентификатор).
			password (:obj:`str`): Пароль клиента (аутентификатор).
			x_captcha_answer (:obj:`str`, optional): Ответ на капчу (цифры с картинки).
			x_captcha_key (:obj:`str`, optional): Уникальный ключ капчи.
			captcha_callback (:obj:`function`, optional): Функция обратного вызова для обработки капчи, должна
				принимать объект класса :class:`yandex_music.exceptions.Captcha` и возвращать проверочный код.
			**kwargs (:obj:`dict`, optional): Аргументы для конструктора клиента.

		Returns:
			:obj:`yandex_music.Client`.

		Raises:
			:class:`yandex_music.YandexMusicError`
		"""

		token = None
		while not token:
			try:
				token = cls(*args, **kwargs).generate_token_by_username_and_password(username, password,
																					 x_captcha_answer=x_captcha_answer,
																					 x_captcha_key=x_captcha_key)
			except Captcha as e:
				if not captcha_callback:
					raise e

				x_captcha_answer = captcha_callback(e.captcha)
				x_captcha_key = e.captcha.x_captcha_key

		return cls(token, *args, **kwargs)

	@classmethod
	def from_token(cls, token, *args, **kwargs):
		"""Инициализция клиента по токену.

		Note:
			Ничем не отличается от `Client(token)`. Так исторически сложилось.

		Args:
			token (:obj:`str`, optional): Уникальный ключ для аутентификации.
			**kwargs (:obj:`dict`, optional): Аргументы для конструктора клиента.

		Returns:
			:obj:`yandex_music.Client`.
		"""

		return cls(token, *args, **kwargs)

	@log
	def generate_token_by_username_and_password(self, username, password, grant_type='password',
												x_captcha_answer=None, x_captcha_key=None,
												timeout=None, *args, **kwargs):
		"""Метод получения OAuth токена по логину и паролю.

		Args:
			username (:obj:`str`): Логин клиента (идентификатор).
			password (:obj:`str`): Пароль клиента (аутентификатор).
			grant_type (:obj:`str`, optional): Тип разрешения OAuth.
			x_captcha_answer (:obj:`str`, optional): Ответ на капчу (цифры с картинки).
			x_captcha_key (:obj:`str`, optional): Уникальный ключ капчи.
			timeout (:obj:`int` | :obj:`float`, optional): Если это значение указано, используется как время ожидания
				ответа от сервера вместо указанного при создании пула.
			**kwargs (:obj:`dict`, optional): Произвольные аргументы (будут переданы в запрос).

		Returns:
			:obj:`str`: OAuth токен.

		Raises:
			:class:`yandex_music.YandexMusicError`
		"""

		url = '%s/token' % self.oauth_url

		data = {
			'grant_type': grant_type,
			'client_id': CLIENT_ID,
			'client_secret': CLIENT_SECRET,
			'username': username,
			'password': password
		}

		if x_captcha_answer and x_captcha_key:
			data.update({'x_captcha_answer': x_captcha_answer, 'x_captcha_key': x_captcha_key})

		result = self._request.post(url, data, timeout=timeout, *args, **kwargs)

		return result.get('access_token')

	@staticmethod
	def _validate_token(token):
		"""Примитивная валидация токена.

		Args:
			token (:obj:`str`): токен для проверки

		Returns:
			:obj:`str`: Токен.

		Raises:
			:class:`yandex_music.exceptions.InvalidToken`: Если токен недействителен.
		"""

		if any(x.isspace() for x in token):
			raise InvalidToken()

		if len(token) != 39:
			raise InvalidToken()

		return token

	@property
	def request(self):
		""":obj:`yandex_music.utils.request.Request`: Объект вспомогательного класса для отправки запросов."""
		return self._request

	@log
	def account_status(self, timeout=None, *args, **kwargs):
		"""Получение статуса аккаунта. Нет обязательных параметров.

		Args:
			timeout (:obj:`int` | :obj:`float`, optional): Если это значение указано, используется как время ожидания
				ответа от сервера вместо указанного при создании пула.
			**kwargs (:obj:`dict`, optional): Произвольные аргументы (будут переданы в запрос).

		Returns:
			:obj:`yandex_music.Status`: Объекта класса :class:`yandex_music.Status` представляющий информацию об
			аккаунте если валиден, иначе :obj:`None`.

		Raises:
			:class:`yandex_music.YandexMusicError`
		"""

		url = '%s/account/status' % self.base_url

		result = self._request.get(url, timeout=timeout, *args, **kwargs)

		return Status.de_json(result, self)

	@log
	def account_settings(self, timeout=None, *args, **kwargs):
		"""Получение настроек текущего пользователя.

		Args:
			timeout (:obj:`int` | :obj:`float`, optional): Если это значение указано, используется как время ожидания
				ответа от сервера вместо указанного при создании пула.
			**kwargs (:obj:`dict`, optional): Произвольные аргументы (будут переданы в запрос).

		Returns:
			:obj:`yandex_music.UserSettings`: Объекта класса :class:`yandex_music.UserSettings` представляющий
			настройки пользователя, иначе :obj:`None`.

		Raises:
			:class:`yandex_music.YandexMusicError`
		"""

		url = '%s/account/settings' % self.base_url

		result = self._request.get(url, timeout=timeout, *args, **kwargs)

		return UserSettings.de_json(result, self)

	@log
	def account_settings_set(self, param=None, value=None,
							 data=None, timeout=None,
							 *args, **kwargs):
		"""Изменение настроек текущего пользователя.

		Note:
			Доступные названия параметров есть поля в классе :class:`yandex_music.UserSettings`, только в CamelCase.

		Args:
			param (:obj:`str`): Название параметра для изменения.
			value (:obj:`str` | :obj:`int` | :obj:`bool`): Значение параметра.
			data (:obj:`dict`): Словарь параметров и значений для множественного изменения.
			timeout (:obj:`int` | :obj:`float`, optional): Если это значение указано, используется как время ожидания
				ответа от сервера вместо указанного при создании пула.
			**kwargs (:obj:`dict`, optional): Произвольные аргументы (будут переданы в запрос).

		Returns:
			:obj:`yandex_music.UserSettings`: Объекта класса :class:`yandex_music.UserSettings` представляющий
			настройки пользователя, иначе :obj:`None`.

		Raises:
			:class:`yandex_music.YandexMusicError`
		"""

		url = '%s/account/settings' % self.base_url

		if not data:
			data = {param: value}

		result = self._request.post(url, data=data, timeout=timeout, *args, **kwargs)

		return UserSettings.de_json(result, self)

	@log
	def settings(self, timeout=None, *args, **kwargs):
		"""Получение предложений по покупке. Нет обязательных параметров.

		Args:
			timeout (:obj:`int` | :obj:`float`, optional): Если это значение указано, используется как время ожидания
				ответа от сервера вместо указанного при создании пула.
			**kwargs (:obj:`dict`, optional): Произвольные аргументы (будут переданы в запрос).

		Returns:
			:obj:`yandex_music.Settings`: Объекта класса :class:`yandex_music.Settings` представляющий информацию о
			предлагаемых продуктах, иначе :obj:`None`.

		Raises:
			:class:`yandex_music.YandexMusicError`
		"""

		url = '%s/settings' % self.base_url

		result = self._request.get(url, timeout=timeout, *args, **kwargs)

		return Settings.de_json(result, self)

	@log
	def permission_alerts(self, timeout=None, *args, **kwargs):
		"""Получение оповещений. Нет обязательных параметров.

		Args:
			timeout (:obj:`int` | :obj:`float`, optional): Если это значение указано, используется как время ожидания
				ответа от сервера вместо указанного при создании пула.
			**kwargs (:obj:`dict`, optional): Произвольные аргументы (будут переданы в запрос).

		Returns:
			:obj:`yandex_music.PermissionAlerts`: Объекта класса :class:`yandex_music.PermissionAlerts`
			представляющий оповещения, иначе :obj:`None`.

		Raises:
			:class:`yandex_music.YandexMusicError`
		"""

		url = '%s/permission-alerts' % self.base_url

		result = self._request.get(url, timeout=timeout, *args, **kwargs)

		return PermissionAlerts.de_json(result, self)

	@log
	def account_experiments(self, timeout=None, *args, **kwargs):
		"""Получение значений экспериментальных функций аккаунта.

		Args:
			timeout (:obj:`int` | :obj:`float`, optional): Если это значение указано, используется как время ожидания
				ответа от сервера вместо указанного при создании пула.
			**kwargs (:obj:`dict`, optional): Произвольные аргументы (будут переданы в запрос).

		Returns:
			:obj:`yandex_music.Experiments`: Объекта класса :class:`yandex_music.Experiments`
			представляющий состояния экспериментальных функций, иначе :obj:`None`.

		Raises:
			:class:`yandex_music.YandexMusicError`
		"""

		url = '%s/account/experiments' % self.base_url

		result = self._request.get(url, timeout=timeout, *args, **kwargs)

		return Experiments.de_json(result, self)

	@log
	def consume_promo_code(self, code, language='en', timeout=None,
						   *args, **kwargs):
		"""Активация промо-кода.

		Args:
			code (:obj:`str`): Промо-код.
			language (:obj:`str`, optional): Язык ответа API в ISO 639-1.
			timeout (:obj:`int` | :obj:`float`, optional): Если это значение указано, используется как время ожидания
				ответа от сервера вместо указанного при создании пула.
			**kwargs (:obj:`dict`, optional): Произвольные аргументы (будут переданы в запрос).

		Returns:
			:obj:`yandex_music.PromoCodeStatus`: Объекта класса :class:`yandex_music.PromoCodeStatus`
			представляющий информацию об активации промо-кода, иначе :obj:`None`.

		Raises:
			:class:`yandex_music.YandexMusicError`
		"""

		url = '%s/account/consume-promo-code' % self.base_url

		result = self._request.post(url, {'code': code, 'language': language}, timeout=timeout, *args, **kwargs)

		return PromoCodeStatus.de_json(result, self)

	@log
	def feed(self, timeout=None, *args, **kwargs):
		"""Получение потока информации (фида) подобранного под пользователя. Содержит умные плейлисты.

		Args:
			timeout (:obj:`int` | :obj:`float`, optional): Если это значение указано, используется как время ожидания
				ответа от сервера вместо указанного при создании пула.
			**kwargs (:obj:`dict`, optional): Произвольные аргументы (будут переданы в запрос).

		Returns:
			:obj:`yandex_music.Feed`: Объекта класса :class:`yandex_music.Feed`
			представляющий умные плейлисты пользователя, иначе :obj:`None`.

		Raises:
			:class:`yandex_music.YandexMusicError`
		"""

		url = '%s/feed' % self.base_url

		result = self._request.get(url, timeout=timeout, *args, **kwargs)

		return Feed.de_json(result, self)

	@log
	def feed_wizard_is_passed(self, timeout=None, *args, **kwargs):
		url = '%s/feed/wizard/is-passed' % self.base_url

		result = self._request.get(url, timeout=timeout, *args, **kwargs)

		return result.get('is_wizard_passed') or False

	@log
	def landing(self, blocks=None, timeout=None,
				*args, **kwargs):
		"""Получение лендинг-страницы содержащий блоки с новыми релизами, чартами, плейлистами с новинками и т.д.

		Note:
			Поддерживаемые типы блоков: `personalplaylists`, `promotions`, `new-releases`, `new-playlists`, `mixes`,
			`chart`, `artists`, `albums`, `playlists`, `play_contexts`.

		Args:
			blocks (:obj:`str` | :obj:`list` из :obj:`str`): Блок или список блоков необходимых для выдачи.
			timeout (:obj:`int` | :obj:`float`, optional): Если это значение указано, используется как время ожидания
				ответа от сервера вместо указанного при создании пула.
			**kwargs (:obj:`dict`, optional): Произвольные аргументы (будут переданы в запрос).

		Returns:
			:obj:`yandex_music.Landing`: Объекта класса :class:`yandex_music.Landing`
			представляющий лендинг-страницу, иначе :obj:`None`.

		Raises:
			:class:`yandex_music.YandexMusicError`
		"""

		url = '%s/landing3' % self.base_url

		result = self._request.get(url, {'blocks': blocks}, timeout=timeout, *args, **kwargs)

		return Landing.de_json(result, self)

	@log
	def chart(self, chart_option='', timeout=None, *args, **kwargs):
		"""Получение чарта.
		Note:
			`chart_option` это постфикс к запросу из поля `menu` чарта.
			Например на сайте можно выбрать глобальный (world) чарт или российский (russia).
		Args:
			chart_option (:obj:`str` optional): Параметры чарта.
			timeout (:obj:`int` | :obj:`float`, optional): Если это значение указано, используется как время ожидания
				ответа от сервера вместо указанного при создании пула.
			**kwargs (:obj:`dict`, optional): Произвольные аргументы (будут переданы в запрос).
		Returns:
			:obj:`yandex_music.ChartInfo`: Чарт.
		Raises:
			:class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
		"""

		url = self.base_url + '/landing3/chart'

		if chart_option:
			url = "%s/%s" % (url, chart_option)

		result = self._request.get(url, timeout=timeout, *args, **kwargs)

		return ChartInfo.de_json(result, self)

	@log
	def genres(self, timeout=None, *args, **kwargs):
		"""Получение жанров музыки.

		Args:
			timeout (:obj:`int` | :obj:`float`, optional): Если это значение указано, используется как время ожидания
				ответа от сервера вместо указанного при создании пула.
			**kwargs (:obj:`dict`, optional): Произвольные аргументы (будут переданы в запрос).

		Returns:
			:obj:`list` из :obj:`yandex_music.Genre`: Список объектов класса :class:`yandex_music.Genre`
			представляющих жанры музыки, иначе :obj:`None`.

		Raises:
			:class:`yandex_music.YandexMusicError`
		"""

		url = '%s/genres' % self.base_url

		result = self._request.get(url, timeout=timeout, *args, **kwargs)

		return Genre.de_list(result, self)

	@log
	def tags(self, tag_id, timeout=None, *args, **kwargs):
		"""Получение тега (подборки).

		Note:
			Теги есть в `MixLink` у `Landing`, а также плейлистов в `.tags`.

			У `MixLink` есть `URL`, но `tag_id` только его последняя часть.
			Например, `/tag/belarus/`. `Tag` - `belarus`.

		Args:
			tag_id (:obj:`str`): Уникальный идентификатор тега.
			timeout (:obj:`int` | :obj:`float`, optional): Если это значение указано, используется как время ожидания
				ответа от сервера вместо указанного при создании пула.
			**kwargs (:obj:`dict`, optional): Произвольные аргументы (будут переданы в запрос).

		Returns:
		   :obj:`yandex_music.TagResult`: Тег с плейлистами.

		Raises:
			:class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
		"""

		url = "%s/tags/%s/playlist-ids" % (self.base_url, tag_id)

		result = self._request.get(url, timeout=timeout, *args, **kwargs)

		return TagResult.de_json(result, self)

	@log
	def tracks_download_info(self, track_id, get_direct_links=False,
							 timeout=None, *args, **kwargs):
		"""Получение информации о доступных вариантах загрузки трека.

		Args:
			track_id (:obj:`str` | :obj:`list` из :obj:`str`): Уникальный идентификатор трека или треков.
			get_direct_links (:obj:`bool`, optional): Получить ли при вызове метода прямую ссылку на загрузку.
			timeout (:obj:`int` | :obj:`float`, optional): Если это значение указано, используется как время ожидания
				ответа от сервера вместо указанного при создании пула.
			**kwargs (:obj:`dict`, optional): Произвольные аргументы (будут переданы в запрос).

		Returns:
			:obj:`list` из :obj:`yandex_music.DownloadInfo`: Список объектов класса :class:`yandex_music.DownloadInfo`
			представляющих варианты загрузки трека, иначе :obj:`None`.

		Raises:
			:class:`yandex_music.YandexMusicError`
		"""

		url = '%s/tracks/%s/download-info' % (self.base_url, track_id)

		result = self._request.get(url, timeout=timeout, *args, **kwargs)

		return DownloadInfo.de_list(result, self, get_direct_links)

	@log
	def track_supplement(self, track_id=None, timeout=None,
						 *args, **kwargs):
		"""Получение дополнительной информации о треке.

		Args:
			track_id (:obj:`str`): Уникальный идентификатор трека.
			timeout (:obj:`int` | :obj:`float`, optional): Если это значение указано, используется как время ожидания
				ответа от сервера вместо указанного при создании пула.
			**kwargs (:obj:`dict`, optional): Произвольные аргументы (будут переданы в запрос).

		Returns:
			:obj:`yandex_music.Supplement`: Объект класса `yandex_music.Supplement` представляющий дополнительную
			информацию о треке.

		Raises:
			:class:`yandex_music.YandexMusicError`
		"""

		url = '%s/tracks/%s/supplement' % (self.base_url, track_id)

		result = self._request.get(url, timeout=timeout, *args, **kwargs)

		return Supplement.de_json(result, self)

	@log
	def tracks_similar(self, track_id=None, timeout=None,
					   *args, **kwargs):
		"""Получение похожих треков.

		Args:
			track_id (:obj:`str`): Уникальный идентификатор трека.
			timeout (:obj:`int` | :obj:`float`, optional): Если это значение указано, используется как время ожидания
				ответа от сервера вместо указанного при создании пула.
			**kwargs (:obj:`dict`, optional): Произвольные аргументы (будут переданы в запрос).

		Returns:
			:obj:`yandex_music.SimilarTracks`: Объект класса `yandex_music.SimilarTracks` представляющий список похожих
			треков на другой трек.

		Raises:
			:class:`yandex_music.YandexMusicError`
		"""

		url = '%s/tracks/%s/similar' % (self.base_url, track_id)

		result = self._request.get(url, timeout=timeout, *args, **kwargs)

		return SimilarTracks.de_json(result, self)

	@log
	def play_audio(self,
				   track_id,
				   from_,
				   album_id,
				   playlist_id=None,
				   from_cache=False,
				   play_id=None,
				   uid=None,
				   timestamp=None,
				   track_length_seconds=0,
				   total_played_seconds=0,
				   end_position_seconds=0,
				   client_now=None,
				   timeout=None,
				   *args, **kwargs):
		"""Метод для отправки текущего состояния прослушиваемого трека.

		Args:
			track_id (:obj:`str` | :obj:`int`): Уникальный идентификатор трека.
			from_ (:obj:`str`): Наименования клиента с которого происходит прослушивание.
			album_id (:obj:`str` | :obj:`int`): Уникальный идентификатор альбома.
			playlist_id (:obj:`str`, optional): Уникальный идентификатор плейлиста, если таковой прослушивается.
			from_cache (:obj:`bool`, optional): Проигрывается ли трек с кеша.
			play_id (:obj:`str`, optional): Уникальный идентификатор проигрывания.
			uid (:obj:`int`, optional): Уникальный идентификатор пользователя.
			timestamp (:obj:`str`, optional): Текущая дата и время в ISO.
			track_length_seconds (:obj:`int`, optional): Продолжительность трека в секундах.
			total_played_seconds (:obj:`int`, optional): Сколько было всего воспроизведено трека в секундах.
			end_position_seconds (:obj:`int`, optional): Окончательное значение воспроизведенных секунд.
			client_now (:obj:`str`, optional): Текущая дата и время клиента в ISO.
			timeout (:obj:`int` | :obj:`float`, optional): Если это значение указано, используется как время ожидания
				ответа от сервера вместо указанного при создании пула.
			**kwargs (:obj:`dict`, optional): Произвольные аргументы (будут переданы в запрос).

		Returns:
			:obj:`bool`: :obj:`True` при успешном выполнении запроса, иначе :obj:`False`.

		Raises:
			:class:`yandex_music.YandexMusicError`
		"""

		if uid is None and self.me is not None:
			uid = self.me.account.uid

		url = '%s/play-audio' % self.base_url

		data = {
			'track-id': track_id,
			'from-cache': from_cache,
			'from': from_,
			'play-id': play_id or '',
			'uid': uid,
			'timestamp': timestamp or '%sZ' % datetime.now().isoformat(),
			'track-length-seconds': track_length_seconds,
			'total-played-seconds': total_played_seconds,
			'end-position-seconds': end_position_seconds,
			'album-id': album_id,
			'playlist-id': playlist_id,
			'client-now': client_now or '%sZ' % datetime.now().isoformat()
		}

		result = self._request.post(url, data, timeout=timeout, *args, **kwargs)

		return result == 'ok'

	def albums_with_tracks(self, album_id=None, timeout=None,
						   *args, **kwargs):
		"""Получение альбома по его уникальному идентификатору вместе с треками.

		Args:
			album_id (:obj:`str` | :obj:`int`): Уникальный идентификатор альбома.
			timeout (:obj:`int` | :obj:`float`, optional): Если это значение указано, используется как время ожидания
				ответа от сервера вместо указанного при создании пула.
			**kwargs (:obj:`dict`, optional): Произвольные аргументы (будут переданы в запрос).

		Returns:
			:obj:`list` из :obj:`yandex_music.Album`: Объект класса :class:`yandex_music.Album` представляющий альбом,
			иначе :obj:`None`.

		Raises:
			:class:`yandex_music.YandexMusicError`
		"""

		url = '%s/albums/%s/with-tracks' % (self.base_url, album_id)

		result = self._request.get(url, timeout=timeout, *args, **kwargs)

		return Album.de_json(result, self)

	@log
	def search(self,
			   text,
			   nocorrect=False,
			   type_='all',
			   page=0,
			   playlist_in_best=True,
			   timeout=None,
			   *args, **kwargs):
		"""Осуществление поиска по запросу и типу, получение результатов.

		Args:
			text (:obj:`str`): Текст запроса.
			nocorrect (:obj:`bool`): Без исправлений ли TODO.
			type_ (:obj:`str`): Среди какого типа искать (трек, плейлист, альбом, исполнитель).
			page (:obj:`int`): Номер страницы.
			playlist_in_best (:obj:`bool`): Выдавать ли плейлисты лучшим вариантом поиска.
			timeout (:obj:`int` | :obj:`float`, optional): Если это значение указано, используется как время ожидания
				ответа от сервера вместо указанного при создании пула.
			**kwargs (:obj:`dict`, optional): Произвольные аргументы (будут переданы в запрос).

		Returns:
			:obj:`yandex_music.Search`: Объекта класса :class:`yandex_music.Search`
			представляющий результаты поиска, иначе :obj:`None`.

		Raises:
			:class:`yandex_music.YandexMusicError`
		"""

		url = '%s/search' % self.base_url

		params = {
			'text': text,
			'nocorrect': nocorrect,
			'type': type_,
			'page': page,
			'playlist-in-best': playlist_in_best,
		}

		result = self._request.get(url, params, timeout=timeout, *args, **kwargs)

		return Search.de_json(result, self)

	@log
	def search_suggest(self, part, timeout=None,
					   *args, **kwargs):
		"""Получение подсказок по введенной части поискового запроса.

		Args:
			part (:obj:`str`): Часть поискового запроса.
			timeout (:obj:`int` | :obj:`float`, optional): Если это значение указано, используется как время ожидания
				ответа от сервера вместо указанного при создании пула.
			**kwargs (:obj:`dict`, optional): Произвольные аргументы (будут переданы в запрос).

		Returns:
			:obj:`yandex_music.Suggestions`: Объекта класса :class:`yandex_music.Suggestions`
			представляющий подсказки для запроса, иначе :obj:`None`.

		Raises:
			:class:`yandex_music.YandexMusicError`
		"""

		url = '%s/search/suggest' % self.base_url

		result = self._request.get(url, {'part': part}, timeout=timeout, *args, **kwargs)

		return Suggestions.de_json(result, self)

	@log
	def users_settings(self, user_id=None, timeout=None,
					   *args, **kwargs):
		"""Получение настроек пользователя.

		Note:
			Для получения настроек пользователя нужно быть авторизованным или владеть `user_id`.

		Args:
			user_id (:obj:`str` | :obj:`int`, optional): Уникальный идентификатор пользователя чьи настройки хотим
				получить.
			timeout (:obj:`int` | :obj:`float`, optional): Если это значение указано, используется как время ожидания
				ответа от сервера вместо указанного при создании пула.
			**kwargs (:obj:`dict`, optional): Произвольные аргументы (будут переданы в запрос).

		Returns:
			:obj:`yandex_music.UserSettings`: Объекта класса :class:`yandex_music.UserSettings` представляющий
			настройки пользователя, иначе :obj:`None`.

		Raises:
			:class:`yandex_music.YandexMusicError`
		"""

		if user_id is None and self.me is not None:
			user_id = self.me.account.uid

		url = '%s/users/%s/settings' % (self.base_url, user_id)

		result = self._request.get(url, timeout=timeout, *args, **kwargs)

		return UserSettings.de_json(result.get('user_settings'), self)

	@log
	def users_playlists(self, kind=None, user_id=None,
						timeout=None, *args, **kwargs):
		"""Получение плейлиста или списка плейлистов по уникальным идентификаторам.

		Args:
			kind (:obj:`str` | :obj:`int` | :obj:`list` из :obj:`str` | :obj:`int`): Уникальный идентификатор плейлиста
				или их список.
			user_id (:obj:`str` | :obj:`int`, optional): Уникальный идентификатор пользователя владеющим плейлистом.
			timeout (:obj:`int` | :obj:`float`, optional): Если это значение указано, используется как время ожидания
				ответа от сервера вместо указанного при создании пула.
			**kwargs (:obj:`dict`, optional): Произвольные аргументы (будут переданы в запрос).

		Returns:
			:obj:`list` из :obj:`yandex_music.Playlist`: Список объектов класса :class:`yandex_music.Playlist`
			представляющих плейлист, иначе :obj:`None`.

		Raises:
			:class:`yandex_music.YandexMusicError`
		"""

		if user_id is None and self.me is not None:
			user_id = self.me.account.uid

		url = '%s/users/%s/playlists' % (self.base_url, user_id)

		data = {
			'kinds': kind
		}

		result = self._request.post(url, data, timeout=timeout, *args, **kwargs)

		return Playlist.de_list(result, self)

	def playlist(self, kind=None, user_id=None, timeout=None, *args, **kwargs):
		"""Получение плейлиста или списка плейлистов по уникальным идентификаторам.

		Args:
			kind (:obj:`str` | :obj:`int` ): Уникальный идентификатор плейлиста.
			user_id (:obj:`str` | :obj:`int`, optional): Уникальный идентификатор пользователя владеющим плейлистом.
			timeout (:obj:`int` | :obj:`float`, optional): Если это значение указано, используется как время ожидания
				ответа от сервера вместо указанного при создании пула.
			**kwargs (:obj:`dict`, optional): Произвольные аргументы (будут переданы в запрос).

		Returns:
			:obj:`list` из :obj:`yandex_music.Playlist`: Список объектов класса :class:`yandex_music.Playlist`
			представляющих плейлист, иначе :obj:`None`.

		Raises:
			:class:`yandex_music.YandexMusicError`
		"""

		if user_id is None and self.me is not None:
			user_id = self.me.account.uid

		url = '%s/users/%s/playlists/%s' % (self.base_url, user_id, kind)
		result = self._request.get(url, timeout=timeout, *args, **kwargs)

		return Playlist.de_json(result, self)

	@log
	def users_playlists_create(self, title, visibility='public', user_id=None,
							   timeout=None, *args, **kwargs):
		"""Создание плейлиста.

		Args:
			title (:obj:`str`): Название.
			visibility (:obj:`str`, optional): Модификатор доступа.
			user_id (:obj:`str` | :obj:`int`, optional): Уникальный идентификатор пользователя владеющим плейлистом.
			timeout (:obj:`int` | :obj:`float`, optional): Если это значение указано, используется как время ожидания
				ответа от сервера вместо указанного при создании пула.
			**kwargs (:obj:`dict`, optional): Произвольные аргументы (будут переданы в запрос).

		Returns:
			:obj:`yandex_music.Playlist`: Объекта класса :class:`yandex_music.Playlist`
			представляющий созданный плейлист, иначе :obj:`None`.

		Raises:
			:class:`yandex_music.YandexMusicError`
		"""

		if user_id is None and self.me is not None:
			user_id = self.me.account.uid

		url = '%s/users/%s/playlists/create' % (self.base_url, user_id)

		data = {
			'title': title,
			'visibility': visibility
		}

		result = self._request.post(url, data, timeout=timeout, *args, **kwargs)

		return Playlist.de_json(result, self)

	@log
	def users_playlists_delete(self, kind=None, user_id=None,
							   timeout=None, *args, **kwargs):
		"""Удаление плейлиста.

		Args:
			kind (:obj:`str` | :obj:`int`): Уникальный идентификатор плейлиста.
			user_id (:obj:`str` | :obj:`int`, optional): Уникальный идентификатор пользователя владеющим плейлистом.
			timeout (:obj:`int` | :obj:`float`, optional): Если это значение указано, используется как время ожидания
				ответа от сервера вместо указанного при создании пула.
			**kwargs (:obj:`dict`, optional): Произвольные аргументы (будут переданы в запрос).

		Returns:
			:obj:`bool`: :obj:`True` при успешном выполнении запроса, иначе :obj:`False`.

		Raises:
			:class:`yandex_music.YandexMusicError`
		"""

		if user_id is None and self.me is not None:
			user_id = self.me.account.uid

		url = '%s/users/%s/playlists/%s/delete' % (self.base_url, user_id, kind)

		result = self._request.post(url, timeout=timeout, *args, **kwargs)

		return result == 'ok'

	@log
	def users_playlists_name(self, kind=None, name=None, user_id=None,
							 timeout=None, *args, **kwargs):
		"""Изменение названия плейлиста.

		Args:
			kind (:obj:`str` | :obj:`int`): Уникальный идентификатор плейлиста.
			name (:obj:`str`): Новое название.
			user_id (:obj:`str` | :obj:`int`, optional): Уникальный идентификатор пользователя владеющим плейлистом.
			timeout (:obj:`int` | :obj:`float`, optional): Если это значение указано, используется как время ожидания
				ответа от сервера вместо указанного при создании пула.
			**kwargs (:obj:`dict`, optional): Произвольные аргументы (будут переданы в запрос).

		Returns:
			:obj:`yandex_music.Playlist`: Объекта класса :class:`yandex_music.Playlist`
			представляющий изменённый плейлист, иначе :obj:`None`.

		Raises:
			:class:`yandex_music.YandexMusicError`
		"""

		if user_id is None and self.me is not None:
			user_id = self.me.account.uid

		url = '%s/users/%s/playlists/%s/name' % (self.base_url, user_id, kind)

		result = self._request.post(url, {'value': name}, timeout=timeout, *args, **kwargs)

		return Playlist.de_json(result, self)

	@log
	def users_playlists_visibility(self, kind=None, visibility=None, user_id=None,
								   timeout=None, *args, **kwargs):
		"""Изменение видимости плейлиста.

		Note:
			Видимость (`visibility`) может быть задана только одним из двух значений: `private`, `public`.

		Args:
			kind (:obj:`str` | :obj:`int`): Уникальный идентификатор плейлиста.
			visibility (:obj:`str`): Новое название.
			user_id (:obj:`str` | :obj:`int`, optional): Уникальный идентификатор пользователя владеющим плейлистом.
			timeout (:obj:`int` | :obj:`float`, optional): Если это значение указано, используется как время ожидания
				ответа от сервера вместо указанного при создании пула.
			**kwargs (:obj:`dict`, optional): Произвольные аргументы (будут переданы в запрос).

		Returns:
			:obj:`yandex_music.Playlist`: Объекта класса :class:`yandex_music.Playlist`
			представляющий изменённый плейлист, иначе :obj:`None`.

		Raises:
			:class:`yandex_music.YandexMusicError`
		"""

		if user_id is None and self.me is not None:
			user_id = self.me.account.uid

		url = '%s/users/%s/playlists/%s/visibility' % (self.base_url, user_id, kind)

		result = self._request.post(url, {'value': visibility}, timeout=timeout, *args, **kwargs)

		return Playlist.de_json(result, self)

	@log
	def users_playlists_change(self, kind, diff, revision=1,
							   user_id=None, timeout=None,
							   *args, **kwargs):
		"""Изменение плейлиста.

		Note:
			Для получения отличий есть вспомогательный класс :class:`yandex_music.utils.difference.Difference`.

			Так же существуют уже готовые методы-обёртки над операциями.

		Args:
			kind (:obj:`str` | :obj:`int`): Уникальный идентификатор плейлиста.
			revision (:obj:`int`): TODO.
			diff (:obj:`str`): JSON представления отличий старого и нового плейлиста.
			user_id (:obj:`str` | :obj:`int`, optional): Уникальный идентификатор пользователя владеющим плейлистом.
			timeout (:obj:`int` | :obj:`float`, optional): Если это значение указано, используется как время ожидания
				ответа от сервера вместо указанного при создании пула.
			**kwargs (:obj:`dict`, optional): Произвольные аргументы (будут переданы в запрос).

		Returns:
			:obj:`yandex_music.Playlist`: Объекта класса :class:`yandex_music.Playlist`
			представляющий изменённый плейлист, иначе :obj:`None`.

		Raises:
			:class:`yandex_music.YandexMusicError`
		"""

		if user_id is None and self.me is not None:
			user_id = self.me.account.uid

		url = '%s/users/%s/playlists/%s/change' % (self.base_url, user_id, kind)

		data = {
			'kind': kind,
			'revision': revision,
			'diff': diff
		}

		result = self._request.post(url, data, timeout=timeout, *args, **kwargs)

		return Playlist.de_json(result, self)

	@log
	def users_playlists_insert_track(self, kind, track_id=None, album_id=None,
									 at=None, revision=None, user_id=None,
									 timeout=None, *args, **kwargs):
		"""Добавление трека в плейлист.

		Note:
			Трек можно вставить с любое место плейлиста задав индекс вставки (аргумент `at`).

		Args:
			kind (:obj:`str` | :obj:`int`): Уникальный идентификатор плейлиста.
			track_id (:obj:`str` | :obj:`int`): Уникальный идентификатор трека.
			album_id (:obj:`str` | :obj:`int`): Уникальный идентификатор альбома.
			at (:obj:`int`): Индекс для вставки.
			revision (:obj:`int`): TODO.
			user_id (:obj:`str` | :obj:`int`, optional): Уникальный идентификатор пользователя владеющим плейлистом.
			timeout (:obj:`int` | :obj:`float`, optional): Если это значение указано, используется как время ожидания
				ответа от сервера вместо указанного при создании пула.
			**kwargs (:obj:`dict`, optional): Произвольные аргументы (будут переданы в запрос).

		Returns:
			:obj:`yandex_music.Playlist`: Объекта класса :class:`yandex_music.Playlist`
			представляющий изменённый плейлист, иначе :obj:`None`.

		Raises:
			:class:`yandex_music.YandexMusicError`
		"""

		if user_id is None and self.me is not None:
			user_id = self.me.account.uid

		diff = Difference().add_insert(at, {'id': track_id, 'album_id': album_id})

		return self.users_playlists_change(kind, diff.to_json(), revision, user_id, timeout, *args, **kwargs)

	@log
	def users_playlists_delete_track(self, kind, from_, to, revision=1,
									 user_id=None, timeout=None,
									 *args, **kwargs):
		"""Удаление треков из плейлиста.

		Note:
			Для удаление необходимо указать границы с какого по какой элемент (трек) удалить.

		Args:
			kind (:obj:`str` | :obj:`int`): Уникальный идентификатор плейлиста.
			from_ (:obj:`int`): С какого индекса.
			to (:obj:`int`): По какой индекс.
			revision (:obj:`int`): TODO.
			user_id (:obj:`str` | :obj:`int`, optional): Уникальный идентификатор пользователя владеющим плейлистом.
			timeout (:obj:`int` | :obj:`float`, optional): Если это значение указано, используется как время ожидания
				ответа от сервера вместо указанного при создании пула.
			**kwargs (:obj:`dict`, optional): Произвольные аргументы (будут переданы в запрос).

		Returns:
			:obj:`yandex_music.Playlist`: Объекта класса :class:`yandex_music.Playlist`
			представляющий изменённый плейлист, иначе :obj:`None`.

		Raises:
			:class:`yandex_music.YandexMusicError`
		"""

		if user_id is None and self.me is not None:
			user_id = self.me.account.uid

		diff = Difference().add_delete(from_, to)

		return self.users_playlists_change(kind, diff.to_json(), revision, user_id, timeout, *args, **kwargs)

	@log
	def rotor_account_status(self, timeout=None, *args, **kwargs):
		"""Получение статуса пользователя с дополнителньыми полями.

		Note:
			Данный статус отличается от обычного наличием дополнительных полей, например, `skips_per_hour`.

		Args:
			timeout (:obj:`int` | :obj:`float`, optional): Если это значение указано, используется как время ожидания
				ответа от сервера вместо указанного при создании пула.
			**kwargs (:obj:`dict`, optional): Произвольные аргументы (будут переданы в запрос).

		Returns:
			:obj:`yandex_music.Status`: Объекта класса :class:`yandex_music.Status`
			представляющий статус пользователя с дополнительными полями от радио, иначе :obj:`None`.

		Raises:
			:class:`yandex_music.YandexMusicError`
		"""

		url = '%s/rotor/account/status' % self.base_url

		result = self._request.get(url, timeout=timeout, *args, **kwargs)

		return Status.de_json(result, self)

	@log
	def rotor_stations_dashboard(self, timeout=None,
								 *args, **kwargs):
		"""Получение рекомендованных станций текущего пользователя.

		Args:
			timeout (:obj:`int` | :obj:`float`, optional): Если это значение указано, используется как время ожидания
				ответа от сервера вместо указанного при создании пула.
			**kwargs (:obj:`dict`, optional): Произвольные аргументы (будут переданы в запрос).

		Returns:
			:obj:`yandex_music.Dashboard`: Объекта класса :class:`yandex_music.Dashboard`
			представляющий рекомендованные станции, иначе :obj:`None`.

		Raises:
			:class:`yandex_music.YandexMusicError`
		"""

		url = '%s/rotor/stations/dashboard' % self.base_url

		result = self._request.get(url, timeout=timeout, *args, **kwargs)

		return Dashboard.de_json(result, self)

	@log
	def rotor_stations_list(self, language='ru', timeout=None,
							*args, **kwargs):
		"""Получение всех радиостанций с настройками пользователя.

		Note:
			Чтобы определить что за тип станции (жанры, настроения, занятие и т.д.) необходимо смотреть в поле
			`id_for_from`.

		Args:
			language (:obj:`str`): Язык, на котором будет информация о станциях.
			timeout (:obj:`int` | :obj:`float`, optional): Если это значение указано, используется как время ожидания
				ответа от сервера вместо указанного при создании пула.
			**kwargs (:obj:`dict`, optional): Произвольные аргументы (будут переданы в запрос).

		Returns:
			:obj:`list` из :obj:`yandex_music.StationResult`: Список объектов класса :class:`yandex_music.StationResult`
			представляющих станцию, иначе :obj:`None`.

		Raises:
			:class:`yandex_music.YandexMusicError`
		"""

		url = '%s/rotor/stations/list' % self.base_url

		result = self._request.get(url, {'language': language}, timeout=timeout, *args, **kwargs)

		return StationResult.de_list(result, self)

	@log
	def rotor_station_feedback(self, station, type_, timestamp=None,
							   from_=None, batch_id=None, total_played_seconds=None,
							   track_id=None, timeout=None,
							   *args, **kwargs):
		"""Отправка ответной реакции на происходящее при прослушивании радио.

		Note:
			Сообщения о начале прослушивания радио, начале и конце трека, его пропуска.

			Известные типы фидбека: `radioStarted`, `trackStarted`, `trackFinished`, `skip`.

			Пример `station`: `user:onyourwave`, `genre:allrock`.

			Пример `from_`: `mobile-radio-user-123456789`.

		Args:
			station (:obj:`str`): Станция.
			type_ (:obj:`str`): Тип отправляемого фидбека.
			timestamp (:obj:`str` | :obj:`float` | :obj:`int`, optional): Текущее время и дата.
			from_ (:obj:`str`, optional): Откуда начато воспроизведение радио.
			batch_id (:obj:`str`, optional): Уникальный идентификатор партии треков. Возвращается при получении треков.
			total_played_seconds (:obj:`int` |:obj:`float`, optional): Сколько было проиграно секунд трека
				перед действием.
			track_id (:obj:`int` | :obj:`str`, optional): Уникальной идентификатор трека.
			timeout (:obj:`int` | :obj:`float`, optional): Если это значение указано, используется как время ожидания
				ответа от сервера вместо указанного при создании пула.
			**kwargs (:obj:`dict`, optional): Произвольные аргументы (будут переданы в запрос).

		Returns:
			:obj:`bool`: :obj:`True` при успешном выполнении запроса, иначе :obj:`False`.

		Raises:
			:class:`yandex_music.YandexMusicError`
		"""

		if timestamp is None:
			timestamp = time.mktime(datetime.now().timetuple())

		url = '%s/rotor/station/%s/feedback' % (self.base_url, station)

		params = {}
		data = {
			'type': type_,
			'timestamp': timestamp
		}

		if batch_id:
			params = {'batch-id': batch_id}

		if track_id:
			data.update({'trackId': track_id})

		if from_:
			data.update({'from': from_})

		if total_played_seconds:
			data.update({'totalPlayedSeconds': total_played_seconds})

		result = self._request.post(url, params=params, json=data, timeout=timeout, *args, **kwargs)

		return result == 'ok'

	@log
	def rotor_station_feedback_radio_started(self, station, from_, batch_id=None,
											 timestamp=None,
											 timeout=None, *args, **kwargs):
		"""Сокращение для::

			client.rotor_station_feedback(station, 'radioStarted', timestamp, from, *args, **kwargs)

		Returns:
			:obj:`bool`: :obj:`True` при успешном выполнении запроса, иначе :obj:`False`.

		Raises:
			:class:`yandex_music.YandexMusicError`
		"""
		return self.rotor_station_feedback(station, 'radioStarted', timestamp, from_=from_, batch_id=batch_id,
										   timeout=timeout, *args, **kwargs)

	@log
	def rotor_station_feedback_track_started(self, station, track_id, batch_id=None,
											 timestamp=None,
											 timeout=None, *args, **kwargs):
		"""Сокращение для::

			client.rotor_station_feedback(station, 'trackStarted', timestamp, track_id, *args, **kwargs)

		Returns:
			:obj:`bool`: :obj:`True` при успешном выполнении запроса, иначе :obj:`False`.

		Raises:
			:class:`yandex_music.YandexMusicError`
		"""
		return self.rotor_station_feedback(station, 'trackStarted', timestamp, track_id=track_id, batch_id=batch_id,
										   timeout=timeout, *args, **kwargs)

	@log
	def rotor_station_feedback_track_finished(self, station, track_id,
											  total_played_seconds, batch_id=None,
											  timestamp=None,
											  timeout=None, *args, **kwargs):
		"""Сокращение для::

			client.rotor_station_feedback(station, 'trackFinished', timestamp, track_id, total_played_seconds,
			*args, **kwargs)

		Returns:
			:obj:`bool`: :obj:`True` при успешном выполнении запроса, иначе :obj:`False`.

		Raises:
			:class:`yandex_music.YandexMusicError`
		"""
		return self.rotor_station_feedback(station, 'trackFinished', timestamp, track_id=track_id,
										   total_played_seconds=total_played_seconds, batch_id=batch_id,
										   timeout=timeout, *args, **kwargs)

	@log
	def rotor_station_feedback_skip(self, station, track_id,
									total_played_seconds, batch_id=None,
									timestamp=None,
									timeout=None, *args, **kwargs):
		"""Сокращение для::

			client.rotor_station_feedback(station, 'skip', timestamp, track_id, total_played_seconds,
			*args, **kwargs)

		Returns:
			:obj:`bool`: :obj:`True` при успешном выполнении запроса, иначе :obj:`False`.

		Raises:
			:class:`yandex_music.YandexMusicError`
		"""
		return self.rotor_station_feedback(station, 'skip', timestamp, track_id=track_id,
										   total_played_seconds=total_played_seconds, batch_id=batch_id,
										   timeout=timeout, *args, **kwargs)

	@log
	def rotor_station_info(self, station, timeout=None,
						   *args, **kwargs):
		"""Получение информации о станции и пользовательских настроек на неё.

		Args:
			station (:obj:`str`): Станция.
			timeout (:obj:`int` | :obj:`float`, optional): Если это значение указано, используется как время ожидания
				ответа от сервера вместо указанного при создании пула.
			**kwargs (:obj:`dict`, optional): Произвольные аргументы (будут переданы в запрос).

		Returns:
			:obj:`list` из :obj:`yandex_music.StationResult`: Список из одного объекта класса
			:class:`yandex_music.StationResult` представляющего информацию о станции, иначе :obj:`None`.

		Raises:
			:class:`yandex_music.YandexMusicError`
		"""

		url = '%s/rotor/station/%s/info' % (self.base_url, station)

		result = self._request.get(url, timeout=timeout, *args, **kwargs)

		return StationResult.de_list(result, self)

	@log
	def rotor_station_settings2(self, station, mood_energy, diversity, language='not-russian',
								timeout=None, *args, **kwargs):
		"""Изменение настроек определённой станции.

		Note:
			Доступные значения для `mood_energy`: `fun`, `active`, `calm`, `sad`, `all`.

			Доступные значения для `diversity`: `favorite`, `popular`, `discover`, `default`.

			Доступные значения для `language`: `not-russian`, `russian`, `any`.

			У станций в `restrictions` есть Enum'ы, а в них `possible_values` - доступные значения для поля.

		Args:
			station (:obj:`str`): Станция.
			mood_energy (:obj:`str`): Настроение.
			diversity (:obj:`str`): Треки.
			language (:obj:`str`): Язык.
			timeout (:obj:`int` | :obj:`float`, optional): Если это значение указано, используется как время ожидания
				ответа от сервера вместо указанного при создании пула.
			**kwargs (:obj:`dict`, optional): Произвольные аргументы (будут переданы в запрос).

		Returns:
			:obj:`bool`: :obj:`True` при успешном выполнении запроса, иначе :obj:`False`.

		Raises:
			:class:`yandex_music.YandexMusicError`
		"""

		url = '%s/rotor/station/%s/settings2' % (self.base_url, station)

		data = {
			'moodEnergy': mood_energy,
			'diversity': diversity
		}

		if language:
			data.update({'language': language})

		result = self._request.post(url, json=data, timeout=timeout, *args, **kwargs)

		return result == 'ok'

	@log
	def rotor_station_tracks(self, station, settings2=None, queue=None,
							 timeout=None, *args, **kwargs):
		"""Получение цепочки треков определённой станции.

		Note:
			Для продолжения цепочки треков необходимо:

			1. Передавать `ID` трека, что был до этого (первый в цепочки).
			2. Отправить фидбек о конче или скипе трека, что был передан в `queue`.
			3. Отправить фидбек о начале следующего трека (второй в цепочки).
			4. Выполнить запрос получения треков. В ответе придёт новые треки или произойдёт сдвиг цепочки на 1 элемент.

			Проход по цепочке до коцна не изучен. Часто встречаются дубликаты.

			Все официальные клиенты выполняют запросы с `settings2 = True`.

		Args:
			station (:obj:`str`): Станция.
			settings2 (:obj:`bool`, optional): Использовать ли второй набор настроек.
			queue (:obj:`str` | :obj:`int` , optional): Уникальной идентификатор трека, который только что был.
			timeout (:obj:`int` | :obj:`float`, optional): Если это значение указано, используется как время ожидания
				ответа от сервера вместо указанного при создании пула.
			**kwargs (:obj:`dict`, optional): Произвольные аргументы (будут переданы в запрос).

		Returns:
			:obj:`yandex_music.StationTracksResult`: Объекта класса :class:`yandex_music.StationTracksResult`
			представляющий последовательность треков станции, иначе :obj:`None`.

		Raises:
			:class:`yandex_music.YandexMusicError`
		"""

		url = '%s/rotor/station/%s/tracks' % (self.base_url, station)

		params = {}
		if settings2:
			params = {'settings2': True}

		if queue:
			params = {'queue': queue}

		result = self._request.get(url, params=params, timeout=timeout, *args, **kwargs)

		return StationTracksResult.de_json(result, self)

	@log
	def artists_brief_info(self, artist_id=None, timeout=None,
						   *args, **kwargs):
		url = '%s/artists/%s/brief-info' % (self.base_url, artist_id)

		result = self._request.get(url, timeout=timeout, *args, **kwargs)

		return BriefInfo.de_json(result, self)

	@log
	def artists_tracks(self, artist_id, page=0, page_size=20,
					   timeout=None, *args, **kwargs):
		"""Получение треков артиста.

		Args:
			artist_id (:obj:`str` | :obj:`int`): Уникальный идентификатор артиста.
			page (:obj:`int`, optional): Номер страницы.
			page_size (:obj:`int`, optional): Количество треков на странице.
			timeout (:obj:`int` | :obj:`float`, optional): Если это значение указано, используется как время ожидания
				ответа от сервера вместо указанного при создании пула.
			**kwargs (:obj:`dict`, optional): Произвольные аргументы (будут переданы в запрос).

		Returns:
			:obj:`yandex_music.ArtistsTracks`: Объекта класса :class:`yandex_music.ArtistsTracks`
			представляющий страницу списка треков артиста, иначе :obj:`None`.

		Raises:
			:class:`yandex_music.YandexMusicError`
		"""

		url = '%s/artists/%s/tracks' % (self.base_url, artist_id)

		params = {
			'page': page,
			'page-size': page_size
		}

		result = self._request.get(url, params, timeout=timeout, *args, **kwargs)

		return ArtistTracks.de_json(result, self)

	@log
	def artists_direct_albums(self, artist_id, page=0, page_size=20,
							  sort_by='year', timeout=None,
							  *args, **kwargs):
		"""Получение альбомов артиста.

		Note:
			Известные значения для `sort_by`: `year`, `rating`.

		Args:
			artist_id (:obj:`str` | :obj:`int`): Уникальный идентификатор артиста.
			page (:obj:`int`, optional): Номер страницы.
			page_size (:obj:`int`, optional): Количество альбомов на странице.
			sort_by (:obj:`str`, optional): Параметр для сортировки.
			timeout (:obj:`int` | :obj:`float`, optional): Если это значение указано, используется как время ожидания
				ответа от сервера вместо указанного при создании пула.
			**kwargs (:obj:`dict`, optional): Произвольные аргументы (будут переданы в запрос).

		Returns:
			:obj:`yandex_music.ArtistAlbums`: Объекта класса :class:`yandex_music.ArtistsTracks`
			представляющий страницу списка альбомов артиста, иначе :obj:`None`.

		Raises:
			:class:`yandex_music.YandexMusicError`
		"""

		url = '%s/artists/%s/direct-albums' % (self.base_url, artist_id)

		params = {
			'sort-by': sort_by,
			'page': page,
			'page-size': page_size
		}

		result = self._request.get(url, params, timeout=timeout, *args, **kwargs)

		return ArtistAlbums.de_json(result, self)

	def _like_action(self, object_type, ids, remove=False,
					 user_id=None, timeout=None, *args, **kwargs):
		if user_id is None and self.me is not None:
			user_id = self.me.account.uid

		action = 'remove' if remove else 'add-multiple'
		url = '%s/users/%s/likes/%ss/%s' % (self.base_url, user_id, object_type, action)

		result = self._request.post(url, {'%s-ids' % object_type: ids}, timeout=timeout, *args, **kwargs)

		if object_type == 'track':
			return 'revision' in result

		return result == 'ok'

	@log
	def users_likes_tracks_add(self, track_ids=None, user_id=None,
							   timeout=None, *args, **kwargs):
		return self._like_action('track', track_ids, False, user_id, timeout, *args, **kwargs)

	@log
	def users_likes_tracks_remove(self, track_ids,
								  user_id=None,
								  timeout=None, *args, **kwargs):
		return self._like_action('track', track_ids, True, user_id, timeout, *args, **kwargs)

	@log
	def users_likes_artists_add(self, artist_ids,
								user_id=None,
								timeout=None, *args, **kwargs):
		return self._like_action('artist', artist_ids, False, user_id, timeout, *args, **kwargs)

	def users_likes_artists_remove(self, artist_ids,
								   user_id=None,
								   timeout=None, *args, **kwargs):
		return self._like_action('artist', artist_ids, True, user_id, timeout, *args, **kwargs)

	@log
	def users_likes_playlists_add(self, playlist_ids,
								  user_id=None,
								  timeout=None, *args, **kwargs):
		return self._like_action('playlist', playlist_ids, False, user_id, timeout, *args, **kwargs)

	@log
	def users_likes_playlists_remove(self, playlist_ids,
									 user_id=None,
									 timeout=None, *args, **kwargs):
		return self._like_action('playlist', playlist_ids, True, user_id, timeout, *args, **kwargs)

	@log
	def users_likes_albums_add(self, album_ids=None, user_id=None,
							   timeout=None, *args, **kwargs):
		return self._like_action('album', album_ids, False, user_id, timeout, *args, **kwargs)

	@log
	def users_likes_albums_remove(self, album_ids,
								  user_id=None,
								  timeout=None, *args, **kwargs):
		return self._like_action('album', album_ids, True, user_id, timeout, *args, **kwargs)

	def _get_list(self, object_type, ids,
				  params=None, timeout=None,
				  *args, **kwargs):
		if params is None:
			params = {}
		params.update({'%s-ids' % object_type: ids})

		url = ('%s/%ss' % (self.base_url, object_type)) + ('/list' if object_type == 'playlist' else '')

		result = self._request.post(url, params, timeout=timeout, *args, **kwargs)

		return de_list.get(object_type)(result, self)

	@log
	def artists(self, artist_ids=None, timeout=None,
				*args, **kwargs):
		return self._get_list('artist', artist_ids, timeout=timeout, *args, **kwargs)

	@log
	def albums(self, album_ids=None, timeout=None,
			   *args, **kwargs):
		return self._get_list('album', album_ids, timeout=timeout, *args, **kwargs)

	@log
	def tracks(self, track_ids, with_positions=True,
			   timeout=None, *args, **kwargs):
		return self._get_list('track', track_ids, {'with-positions': with_positions}, timeout, *args, **kwargs)

	@log
	def playlists_list(self, playlist_ids=None, timeout=None,
					   *args, **kwargs):
		return self._get_list('playlist', playlist_ids, timeout=timeout, *args, **kwargs)

	@log
	def users_playlists_list(self, user_id=None, timeout=None,
							 *args, **kwargs):
		if user_id is None and self.me is not None:
			user_id = self.me.account.uid

		url = '%s/users/%s/playlists/list' % (self.base_url, user_id)

		result = self._request.get(url, timeout=timeout, *args, **kwargs)

		return Playlist.de_list(result, self)

	def _get_likes(self, object_type, user_id=None, params=None,
				   timeout=None, *args, **kwargs):
		if user_id is None and self.me is not None:
			user_id = self.me.account.uid

		url = '%s/users/%s/likes/%ss' % (self.base_url, user_id, object_type)

		result = self._request.get(url, params, timeout=timeout, *args, **kwargs)

		if object_type == 'track':
			return TracksList.de_json(result.get('library'), self)

		return Like.de_list(result, self, object_type)

	@log
	def users_likes_tracks(self, user_id=None, if_modified_since_revision=0,
						   timeout=None, *args, **kwargs):
		return self._get_likes('track', user_id, {'if-modified-since-revision': if_modified_since_revision}, timeout,
							   *args, **kwargs)

	@log
	def users_likes_albums(self, user_id=None, rich=None, timeout=None,
						   *args, **kwargs):
		return self._get_likes('album', user_id, {'rich': rich}, timeout, *args, **kwargs)

	@log
	def users_likes_artists(self, user_id=None, with_timestamps=True,
							timeout=None, *args, **kwargs):
		return self._get_likes('artist', user_id, {'with-timestamps': with_timestamps}, timeout, *args, **kwargs)

	@log
	def users_likes_playlists(self, user_id=None, timeout=None,
							  *args, **kwargs):
		return self._get_likes('playlist', user_id, timeout=timeout, *args, **kwargs)

	@log
	def users_dislikes_tracks(self, user_id=None, if_modified_since_revision=0,
							  timeout=None, *args, **kwargs):
		if user_id is None and self.me is not None:
			user_id = self.me.account.uid

		url = '%s/users/%s/dislikes/tracks' % (self.base_url, user_id)

		result = self._request.get(url, {'if_modified_since_revision': if_modified_since_revision},
								   timeout=timeout, *args, **kwargs)

		return TracksList.de_json(result.get('library'), self)

	def _dislike_action(self, ids, remove=False,
						user_id=None, timeout=None, *args, **kwargs):
		if user_id is None and self.me is not None:
			user_id = self.me.account.uid

		action = 'remove' if remove else 'add-multiple'
		url = '%s/users/%s/dislikes/tracks/%s' % (self.base_url, user_id, action)

		result = self._request.post(url, {'track-ids': ids}, timeout=timeout, *args, **kwargs)

		return 'revision' in result

	@log
	def users_dislikes_tracks_add(self, track_ids,
								  user_id=None,
								  timeout=None, *args, **kwargs):
		return self._dislike_action(track_ids, False, user_id, timeout, *args, **kwargs)

	@log
	def users_dislikes_tracks_remove(self, track_ids,
									 user_id=None,
									 timeout=None, *args, **kwargs):
		return self._dislike_action(track_ids, True, user_id, timeout, *args, **kwargs)

	@log
	def after_track(self, prev_track_id=None, next_track_id=None, context_item=None,
					context='playlist', types='shot', from_='mobile-landing-origin-default',
					timeout=None, *args, **kwargs):
		"""Получение рекламы или шота от Алисы после трека.

		Note:
			При получения шота от Алисы `prev_track_id` можно не указывать.

			Если `context = 'playlist'`, то в `context_item` необходимо передать `{OWNER_PLAYLIST}:{ID_PLAYLIST}`.
			Плейлист с Алисой имеет владельца с `id = 940441070`.

			ID плейлиста можно получить из блоков landing'a. Получить шот чужого плейлиста нельзя.

			Известные значения `context`: `playlist`.

			Известные значения `types`: `shot`, `ad`.

		Args:
			prev_track_id (:obj:`str` | :obj:`int`): Уникальный идентификатор предыдущего трека.
			next_track_id (:obj:`str` | :obj:`int`): Уникальный идентификатор следующего трека.
			context_item (:obj:`str`): Уникальный идентификатор контекста.
			context (:obj:`str`, optional): Место, откуда было вызвано получение.
			types (:obj:`str`, optional): Тип того, что вернуть после трека.
			from_ (:obj:`str`, optional): Место, с которого попали в контекст.
			timeout (:obj:`int` | :obj:`float`, optional): Если это значение указано, используется как время ожидания
				ответа от сервера вместо указанного при создании пула.
			**kwargs (:obj:`dict`, optional): Произвольные аргументы (будут переданы в запрос).

		Returns:
			:obj:`yandex_music.ShotEvent`: Объекта класса :class:`yandex_music.ShotEvent`
			представляющий шоты от Алисы, иначе :obj:`None`.

		Raises:
			:class:`yandex_music.YandexMusicError`
		"""

		url = '%s/after-track' % self.base_url

		params = {
			'from': from_,
			'prevTrackId': prev_track_id,
			'nextTrackId': next_track_id,
			'context': context,
			'contextItem': context_item,
			'types': types,
		}

		result = self._request.get(url, params=params, timeout=timeout, *args, **kwargs)

		# TODO судя по всему эндпоинт ещё возвращает рекламу после треков для пользователей без подписки.
		return ShotEvent.de_json(result.get('shot_event'), self)

	# camelCase псевдонимы

	#: Псевдоним для :attr:`from_credentials`
	fromCredentials = from_credentials
	#: Псевдоним для :attr:`from_token`
	fromToken = from_token
	#: Псевдоним для :attr:`generate_token_by_username_and_password`
	generateTokenByUsernameAndPassword = generate_token_by_username_and_password
	#: Псевдоним для :attr:`account_status`
	accountStatus = account_status
	#: Псевдоним для :attr:`permission_alerts`
	permissionAlerts = permission_alerts
	#: Псевдоним для :attr:`account_experiments`
	accountExperiments = account_experiments
	#: Псевдоним для :attr:`consume_promo_code`
	consumePromoCode = consume_promo_code
	#: Псевдоним для :attr:`feed_wizard_is_passed`
	feedWizardIsPassed = feed_wizard_is_passed
	#: Псевдоним для :attr:`tracks_download_info`
	tracksDownloadInfo = tracks_download_info
	#: Псевдоним для :attr:`track_supplement`
	trackSupplement = track_supplement
	#: Псевдоним для :attr:`tracks_similar`
	tracksSimilar = tracks_similar
	#: Псевдоним для :attr:`play_audio`
	playAudio = play_audio
	#: Псевдоним для :attr:`albums_with_tracks`
	albumsWithTracks = albums_with_tracks
	#: Псевдоним для :attr:`search_suggest`
	searchSuggest = search_suggest
	#: Псевдоним для :attr:`users_playlists`
	usersPlaylists = users_playlists
	#: Псевдоним для :attr:`users_playlists_create`
	usersPlaylistsCreate = users_playlists_create
	#: Псевдоним для :attr:`users_playlists_delete`
	usersPlaylistsDelete = users_playlists_delete
	#: Псевдоним для :attr:`users_playlists_name`
	usersPlaylistsName = users_playlists_name
	#: Псевдоним для :attr:`users_playlists_visibility`
	usersPlaylistsVisibility = users_playlists_visibility
	#: Псевдоним для :attr:`users_playlists_change`
	usersPlaylistsChange = users_playlists_change
	#: Псевдоним для :attr:`users_playlists_insert_track`
	usersPlaylistsInsertTrack = users_playlists_insert_track
	#: Псевдоним для :attr:`users_playlists_delete_track`
	usersPlaylistsDeleteTrack = users_playlists_delete_track
	#: Псевдоним для :attr:`rotor_account_status`
	rotorAccountStatus = rotor_account_status
	#: Псевдоним для :attr:`rotor_stations_dashboard`
	rotorStationsDashboard = rotor_stations_dashboard
	#: Псевдоним для :attr:`rotor_stations_list`
	rotorStationsList = rotor_stations_list
	#: Псевдоним для :attr:`rotor_station_feedback`
	rotorStationFeedback = rotor_station_feedback
	#: Псевдоним для :attr:`rotor_station_feedback_radio_started`
	rotorStationFeedbackRadioStarted = rotor_station_feedback_radio_started
	#: Псевдоним для :attr:`rotor_station_feedback_track_started`
	rotorStationFeedbackTrackStarted = rotor_station_feedback_track_started
	#: Псевдоним для :attr:`rotor_station_feedback_track_finished`
	rotorStationFeedbackTrackFinished = rotor_station_feedback_track_finished
	#: Псевдоним для :attr:`rotor_station_feedback_skip`
	rotorStationFeedbackSkip = rotor_station_feedback_skip
	#: Псевдоним для :attr:`rotor_station_info`
	rotorStationInfo = rotor_station_info
	#: Псевдоним для :attr:`rotor_station_settings2`
	rotorStationSettings2 = rotor_station_settings2
	#: Псевдоним для :attr:`rotor_station_tracks`
	rotorStationTracks = rotor_station_tracks
	#: Псевдоним для :attr:`artists_brief_info`
	artistsBriefInfo = artists_brief_info
	#: Псевдоним для :attr:`artists_tracks`
	artistsTracks = artists_tracks
	#: Псевдоним для :attr:`artists_direct_albums`
	artistsDirectAlbums = artists_direct_albums
	#: Псевдоним для :attr:`users_likes_tracks_add`
	usersLikesTracksAdd = users_likes_tracks_add
	#: Псевдоним для :attr:`users_likes_tracks_remove`
	usersLikesTracksRemove = users_likes_tracks_remove
	#: Псевдоним для :attr:`users_likes_artists_add`
	usersLikesArtistsAdd = users_likes_artists_add
	#: Псевдоним для :attr:`users_likes_artists_remove`
	usersLikesArtistsRemove = users_likes_artists_remove
	#: Псевдоним для :attr:`users_likes_playlists_add`
	usersLikesPlaylistsAdd = users_likes_playlists_add
	#: Псевдоним для :attr:`users_likes_playlists_remove`
	usersLikesPlaylistsRemove = users_likes_playlists_remove
	#: Псевдоним для :attr:`users_likes_albums_add`
	usersLikesAlbumsAdd = users_likes_albums_add
	#: Псевдоним для :attr:`users_likes_albums_remove`
	usersLikesAlbumsRemove = users_likes_albums_remove
	#: Псевдоним для :attr:`playlists_list`
	playlistsList = playlists_list
	#: Псевдоним для :attr:`users_playlists_list`
	usersPlaylistsList = users_playlists_list
	#: Псевдоним для :attr:`users_likes_tracks`
	usersLikesTracks = users_likes_tracks
	#: Псевдоним для :attr:`users_likes_albums`
	usersLikesAlbums = users_likes_albums
	#: Псевдоним для :attr:`users_likes_artists`
	usersLikesArtists = users_likes_artists
	#: Псевдоним для :attr:`users_likes_playlists`
	usersLikesPlaylists = users_likes_playlists
	#: Псевдоним для :attr:`users_dislikes_tracks`
	usersDislikesTracks = users_dislikes_tracks
	#: Псевдоним для :attr:`users_dislikes_tracks_add`
	usersDislikesTracksAdd = users_dislikes_tracks_add
	#: Псевдоним для :attr:`users_dislikes_tracks_remove`
	usersDislikesTracksRemove = users_dislikes_tracks_remove
	#: Псевдоним для :attr:`after_track`
	afterTrack = after_track
