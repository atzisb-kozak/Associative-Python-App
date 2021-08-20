from typing import List
from ariadne import QueryType, MutationType, ScalarType, convert_kwargs_to_snake_case
from .models import Sachet, Echantionnage
from .payload import SachetPayload, EchantionnagePayload
from tortoise import timezone

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

@mutations.field('createEchantionnage')
@convert_kwargs_to_snake_case
async def resolve_create_echantionnage(*_, echantillon) -> EchantionnagePayload:
	""" Create new Echantionnage data and store into database

	Args:
			echantillon ([type]): Echantionnage's input

	Returns:
			Echantionnage: Data stored into
	"""
	try:
		echantionnage = await Echantionnage.create(
			poidsMeasured = echantillon['poids_measured'],
			poidsGenerated = echantillon['poids_generated'],
		)
		return dict(
			success = True,
			data = echantionnage,
			error = None
		)
	except Exception as error:
		return dict(
			success = False,
			data = None,
			error = error.args
		)

@mutations.field('updateEchantionnage')
@convert_kwargs_to_snake_case
async def resolve_update_echantionnage(*_, echantion_id: int, echantillon) -> EchantionnagePayload:
	""" Get and update existing Echantionnage data stored

	Args:
			echantion_id (int): Echantionnage's data unique ID 
			echantillon ([type]): update data

	Returns:
			bool: result state if operation success or fail
	"""
	try:
		echantion = await Echantionnage.get_or_none(echantionNumber=echantion_id)
		if echantion is not None:
			echantion.update(
				poidsMeasured = echantillon['poids_measured'],
				poidsGenerated = echantillon['poids_generated']
			)
			return dict(
				success = True,
				data = None,
				error = None,
			)
		else:
			return dict(
				success = False,
				data = None,
				error = 'Data doesn\'t exist in database',
			)
	except Exception as error:
		return dict(
			success = False,
			data = None,
			error = error.args
		)

@mutations.field('deleteEchantionnage')
@convert_kwargs_to_snake_case
async def resolve_delete_echantionnage(*_, echantion_id: int) -> EchantionnagePayload:
	""" Deletting existing Echantionnage's data stored in database

	Args:
			echantion_id (int): Echantionnage's data unique ID

	Returns:
			bool: result state if operation success or fail
	"""
	try: 
		echantillon = await Echantionnage.delete(echantionNumber=echantion_id)
		if echantillon is not None:
			return dict(
				success = True,
				data = None,
				error = None
			)
		else:
			return dict(
				success = False,
				data = None,
				error = 'Data doesn\'t exist in database'
			)
	except Exception as error: 
		return dict(
			success = False,
			data = None,
			error = error.args,
		)

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
async def resolve_create_sachet(*_, data) -> SachetPayload:
	"""[summary] Create Sachet data and stored in database

	Args:
		data: Sachet's input data

	Returns:
		Sachet: Sachet's data
	"""
	try:
		data['combinaison'] = ','.join([str(number) for number in data['combinaison']])
		sachet = await Sachet.create(
			poids=data['poids'],
			combinaison=data['combinaison'],
		)
		sachet.combinaison = list(map(int, str(sachet.combinaison).split(',')))
		return dict(
			success = True,
			data = sachet,
			error = None
		)
	except Exception as error:
		return dict(
			success = False,
			data = None,
			error = error.args
		)

@mutations.field('updateSachet')
@convert_kwargs_to_snake_case
async def resolve_update_sachet(*_,sachet_id: int, data) -> SachetPayload:
	"""[summary] Update existing Sachet's data into database

	Args:
		sachet_id (int) : Sachet's data ID number
		data: Sachet's input data

	Returns:
		bool: return state if operation success or failed
	"""
	try:
		sachet = await Sachet.get_or_none(id=sachet_id)
		if sachet is not None:
			sachet.update(poids=data['poids'], combinaison=data['combinaison'])
			return dict(
				success = True,
				data = None,
				error = None
			)
		else:
			return dict(
				success = False,
				data = None,
				error = 'Data doesn\'t exist in database'
			)
	except Exception as error:
		return dict(
			success = False,
			data = None,
			error = error.args
		)

@mutations.field('deleteSachet')
@convert_kwargs_to_snake_case
async def resolve_delete_sachet(_, info, sachet_id) -> SachetPayload:
	"""[summary] Delete existing Sachet data into database

	Args:
		sachet_id (int): Sachet's data ID number
	Returns:
		bool: return state if operation success or failed
	"""
	try:
		sachet = await Sachet.delete(id=sachet_id)
		if sachet is not None:
			return dict(
				success = True,
				data = None,
				error = None,
			)
		else:
			return dict(
				success = False,
				data = None,
				error = 'Data doesn\'t exist in database'
			)
	except Exception as error:
		return dict(
			success = False,
			data = None,
			error = error
		)