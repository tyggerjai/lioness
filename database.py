###########
# Database handling for lioness
####
import MySQLdb


class DataBase():
	conn = ''
	def __init__(self, dbname, username, mypass):
		self.conn = MySQLdb.connect(user=username, passwd=mypass, db=dbname )

	def showtables(self):
		return self.query("""SHOW TABLES;""")
		

	def query(self, query):
		self.conn.query(query)
		result = self.conn.use_result()
		return result.fetch_row(0)
