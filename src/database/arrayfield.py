from enum import Enum
from typing import Any, List, Type, Union

from tortoise.exceptions import ConfigurationError
from tortoise.fields.base import Field


class ArrayField(Field):  # type: ignore
	"""
	Array field.

	This field can store array of integer or string or Enums of these.
	Only postgres db supported.
	"""
	indexable = False

	def __init__(self, elem_type: Type, **kwargs: Any) -> None:
		if not issubclass(elem_type, (int, str)):
			raise ConfigurationError("ArrayField only supports integer or string or Enums of these!")
		super().__init__(**kwargs)
		self.elem_type = elem_type

	def to_db_value(self, value: List[Union[int, str, Enum]], instance) -> List[Union[int, str]]:
		if value and issubclass(self.elem_type, Enum):
			return [v.value for v in value]
		return value

	def to_python_value(self, value: List[Union[int, str]]) -> List[Union[int, str, Enum]]:
		if value and issubclass(self.elem_type, Enum):
			return [self.elem_type(v) for v in value]
		return value

	@property
	def SQL_TYPE(self) -> str:  # type: ignore
		if issubclass(self.elem_type, int):
			return "INTEGER ARRAY"
		if issubclass(self.elem_type, str):
			return "TEXT ARRAY"