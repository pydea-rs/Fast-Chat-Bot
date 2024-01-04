from random import randrange
from db_interface import DatabaseInterface

class Anon:
	Onlines = {}

	@staticmethod
	def Get(message):
		user = message.from_user
		
		if not user.id in Anon.Onlines:
			Anon.Onlines[user.id] = Anon(user)
			DatabaseInterface.Get().add_anon(Anon.Onlines[user.id])
		return Anon.Onlines[user.id]

	def __init__(self, user):
		self.user_id = user.id
		self.companion = None
		self.id = len(Anon.Onlines)
		self.alias = f'anon#{self.id}'

	def next(self):
		alones = list(
			filter(lambda anon: not Anon.Onlines[anon].companion and anon != self.user_id, Anon.Onlines)
		)
		alones_num = len(alones)
		if not alones_num:
			return
		lucky1 = randrange(alones_num)
		self.companion = Anon.Onlines[alones[lucky1]]
		self.companion.companion = self
