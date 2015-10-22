import cx_Oracle

import LoginView

class Database:
	def __init__(self, connection, cursor):
		self.connection = connection
		self.cursor = cursor
	
	def get(self, querry):
		self.cursor.execute(querry)
		return self.cursor.fetchall()
	
	def commit(self):
		self.connection.commit()
	
	def close(self):
		self.cursor.close()
		self.connection.close()
	
	def newCursor(self):
		return Database(self.connection, self.connection.cursor())

def connect():
	tries = 0
	database = None
	while tries < 3:
		tries += 1
		database = dbLogin(tries > 1)
		if database:
			break
	return database

def dbLogin(previous=False):
	(username, password) = LoginView.getLogin("Connect to database", previous)
	return _connect(username, password)

def _connect(username, password):
	# Build connection string
	host = "localhost"
	port = "1525"
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