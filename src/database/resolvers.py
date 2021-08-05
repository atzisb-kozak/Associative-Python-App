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
	return value.isoformat()

@queries.field('echantionnage')
async def resolve_echantionnage(_, info) -> List[Echantionnage]:
	return await Echantionnage.all()

@queries.field('echantionnageID')
@convert_kwargs_to_snake_case
async def resolve_echantionnageID(*_, echantion_id) -> Echantionnage:
	return await Echantionnage.get_or_none(echantionNumber=echantion_id)

@queries.field('sachet')
async def resolve_sachet(_, info) -> List[Sachet]:
	print(timezone.get_timezone())
	results = await Sachet.all()
	for result in results:
		if (result.combinaison is None):
			continue
		result.combinaison = list(map(int, str(result.combinaison).split(',')))
	return results

@queries.field('sachetID')
@convert_kwargs_to_snake_case
async def resolve_sachetID(*_, sachet_id) -> Sachet:
	result = await Sachet.get_or_none(id=sachet_id)
	if result.combinaison is None:
		return result
	result.combinaison = list(map(int, str(result.combinaison).split(',')))
	return result

@mutations.field('createSachet')
async def resolve_create_sachet(_, info, data) -> Sachet:
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
async def resolve_update_sachet(_,info,sachet_id, data) -> bool:
	sachet = await Sachet.get_or_none(id=sachet_id)
	if sachet is not None:
		sachet.update(poids=data['poids'], combinaison=data['combinaison'])
		return True
	else:
		return False

@mutations.field('deleteSachet')
@convert_kwargs_to_snake_case
async def resolve_delete_sachet(_, info, sachet_id) -> bool:
	sachet = await Sachet.delete(id=sachet_id)
	return sachet is not None