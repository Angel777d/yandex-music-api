# coding=utf-8

from .utils.reserved_names import reserved_names
from abc import ABCMeta
#



ujson = False
try:
	import ujson as json

	ujson = True
except ImportError:
	import json



class YandexMusicObject:
	__metaclass__ = ABCMeta
	_id_attrs = ()

	def __str__(self):
		return str(self.to_dict())

	def __repr__(self):
		return str(self)

	def __getitem__(self, item):
		return self.__dict__[item]

	@classmethod
	def de_json(cls, data, client):
		"""Десериализация объекта.

		Args:
			data (:obj:`dict`): Поля и значения десериализуемого объекта.
			client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client`, представляющий клиент
				Yandex Music.

		Returns:
			:obj:`yandex_music.YandexMusicObject`: Объект класса :class:`yandex_music.YandexMusicObject`.
		"""
		if not data:
			return None

		data = data.copy()

		return data

	def to_json(self):
		return json.dumps(self.to_dict(), ensure_ascii=not ujson)

	def to_dict(self):
		def parse(val):
			if hasattr(val, 'to_dict'):
				return val.to_dict()
			elif isinstance(val, list):
				return [parse(it) for it in val]
			elif isinstance(val, dict):
				return {key: parse(value) for key, value in val.items()}
			else:
				return val

		data = self.__dict__.copy()
		data.pop('client', None)
		data.pop('_id_attrs', None)

		for k, v in data.copy().items():
			if k.lower() in reserved_names:
				data.pop(k)
				data.update({'%s_' % k: v})

		return parse(data)

	def __eq__(self, other):
		if isinstance(other, self.__class__):
			return self._id_attrs == other._id_attrs
		return super(YandexMusicObject, self).__eq__(other)

	def __hash__(self):
		if self._id_attrs:
			frozen_attrs = tuple(frozenset(attr) if isinstance(attr, list) else attr for attr in self._id_attrs)
			return hash((self.__class__, frozen_attrs))
		return super(YandexMusicObject, self).__hash__()
