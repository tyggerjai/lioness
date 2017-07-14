##############3
# It's all about the people....
# Wed 07 Sep 2016 17:24:37 AEST

class UserManager():
	OPS = list()
	OWNERS = list()
	def __init__(self, dbconn):
		self.dbconn = dbconn
		self.error = 0
	def add_owner(self, op):
		self.OWNERS.append(op)
		self.set_op(op)

	def get_owners(self):
		return self.OWNERS
	
	def set_ops(self, ops):
		for k,v in ops.items():
			self.set_op(v['id'])

	def set_op(self, op):
		self.OPS.append(op)

	def is_op(self, id):
		return (id in self.OPS)

	def checkuser(self, userID):
		self.error = self.dbconn.query("SELECT `userID` FROM `users` WHERE `userID` = %s", [userID,] )
		return self.error

	# We'll get a user structure
	def check_and_add(self, user):
		
		self.error = self.checkuser(user["user"]["id"])

		if not self.error:
			self.error = dbconn.query("INSERT INTO `users`(`userID`,  `name`) VALUES(%s, %s)", [user["user"]["id"], user["user"]["name"]] )
		return self.error	

	#def removeop(self, id):


		