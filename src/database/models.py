from tortoise.models import Model
from .arrayfield import ArrayField
from tortoise import fields

class Sachet(Model):
	__tablename__ = 'sachet'
	id = fields.IntField(pk=True)
	poids = fields.IntField()
	combinaison = ArrayField(int, null=False)
	created_at = fields.DatetimeField(null=True, auto_now_add=False)
	updated_at = fields.DatetimeField(null=True, auto_now=False)

	def __str__(self) -> str:
		return str(dict(
			id = self.id,
			poids = self.poids,
			combinaison = self.combinaison,
			created_at = self.created_at,
			updated_at = self.updated_at,
		))

class Echantionnage(Model):
	__tablename__ = 'echantionnage'
	echantionNumber = fields.IntField(pk=True)
	poidsGenerated = fields.IntField()
	poidsMeasured = fields.IntField()
	created_at = fields.DatetimeField(null=True, auto_now_add=True)
	updated_at = fields.DatetimeField(null=True, auto_now=True)

	def __str__(self) -> str:
		return str(dict(
			echantionNumber=self.echantionNumber,
			poidsGenerated=self.poidsGenerated,
			poidsMeasured=self.poidsMeasured,
			created_at=self.created_at,
			updated_at=self.updated_at,
		))
