from .models import Sachet, Echantionnage

class SachetPayload():
	success: bool
	data: Sachet
	error: str

class EchantionnagePayload():
	success: bool
	data: Echantionnage
	error: str