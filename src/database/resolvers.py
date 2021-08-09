from typing import List
from ariadne import QueryType, MutationType, ScalarType, convert_kwargs_to_snake_case
from .models import Sachet, Echantionnage
from tortoise import timezone
from datetime import datetime
import json

datetime_scalar = ScalarType("DateTime")
queries = QueryType()
mutations = MutationType()

@datetime_scalar.serializer
def serialize_datetime(value: str) -> str:
	"""Change DateTime brut format into ISO string format to display

	Args:
		value (str): DateTime brut value 

	Returns:
		str: DateTime ISO Format string value
	"""
	return value.isoformat()

@queries.field('echantionnage')
async def resolve_echantionnage(_, info) -> List[Echantionnage]:
	"""Fetch all Echantionnage's data stored in database

	Returns:
		List[Echantionnage]: data list
	"""
	return await Echantionnage.all()

@queries.field('echantionnageID')
@convert_kwargs_to_snake_case
async def resolve_echantionnageID(*_, echantion_id: int) -> Echantionnage:
	"""Fetch specific Echantionnage's data with unique ID

	Args:
		echantion_id (int): Echantionnage's data ID number 

	Returns:
		Echantionnage: Echantionnage's data matched with ID 
	"""
	return await Echantionnage.get_or_none(echantionNumber=echantion_id)

@queries.field('sachet')
async def resolve_sachet(_, info) -> List[Sachet]:
	"""Fetch all Sachet's data from the database

	Returns:
		List[Sachet]: Data list
	"""
	print(timezone.get_timezone())
	results = await Sachet.all()
	for result in results:
		if (result.combinaison is None):
			continue
		result.combinaison = list(map(int, str(result.combinaison).split(',')))
	return results

@queries.field('sachetID')
@convert_kwargs_to_snake_case
async def resolve_sachetID(*_, sachet_id: int) -> Sachet:
	"""Fetch specific Sachet's data with unique ID

	Args:
		sachet_id (int): Sachet's data ID number

	Returns:
		Sachet: Sachet's data matched with ID 
	"""
	result = await Sachet.get_or_none(id=sachet_id)
	if result.combinaison is None:
		return result
	result.combinaison = list(map(int, str(result.combinaison).split(',')))
	return result

@mutations.field('createSachet')
async def resolve_create_sachet(*_, data) -> Sachet:
	"""[summary] Create Sachet data and stored in database

	Args:
		data: Sachet's input data

	Returns:
		Sachet: Sachet's data
	"""
	data['combinaison'] = ','.join([str(number) for number in data['combinaison']])
	sachet = await Sachet.create(
		poids=data['poids'],
		combinaison=data['combinaison'],
		created_at=datetime.now(tz=None),
		updated_at=datetime.now(tz=None),
	)
	sachet.combinaison = list(map(int, str(sachet.combinaison).split(',')))
	return sachet

@mutations.field('updateSachet')
@convert_kwargs_to_snake_case
async def resolve_update_sachet(*_,sachet_id: int, data) -> bool:
	"""[summary] Update existing Sachet's data into database

	Args:
		sachet_id (int) : Sachet's data ID number
		data: Sachet's input data

	Returns:
		bool: return state if operation success or failed
	"""
	sachet = await Sachet.get_or_none(id=sachet_id)
	if sachet is not None:
		sachet.update(poids=data['poids'], combinaison=data['combinaison'])
		return True
	else:
		return False

@mutations.field('deleteSachet')
@convert_kwargs_to_snake_case
async def resolve_delete_sachet(_, info, sachet_id) -> bool:
	"""[summary] Delete existing Sachet data into database

	Args:
		sachet_id (int): Sachet's data ID number
	Returns:
		bool: return state if operation success or failed
	"""
	sachet = await Sachet.delete(id=sachet_id)
	return sachet is not None