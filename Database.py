import cx_Oracle

class Database:
	def __init__(self, connection, cursor):
		self.connection = connection
		self.cursor = cursor
	
	def get(self, query):
		self.cursor.execute(query)
		return self.cursor.fetchall()
	
	def put(self, query):
		self.cursor.execute(query)
	
	def commit(self):
		self.connection.commit()
	
	def close(self):
		self.cursor.close()
		self.connection.close()
	
	def newCursor(self):
		return Database(self.connection, self.connection.cursor())

def connect(username, password):
	# Build connection string
	host = "localhost"
#	host = "gwynne.cs.ualberta.ca"
	port = "1525"
#	port = "1521"
	sid = "CRS"
	dsn = cx_Oracle.makedsn(host, port, sid)
	cursor = None
	try:
		connection = cx_Oracle.connect(username, password, dsn)
		if not connection:
			return None
		cursor = connection.cursor()
	except cx_Oracle.DatabaseError as e:
		error, = e.args
		print("Oracle code:", error.code)
		print("Oracle message:", error.message)
		return None
	return Database(connection, cursor)