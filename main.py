# run: ssh -L 1525:gwynne.cs.ualberta.ca:1521 dskrundz@ohaton.cs.ualberta.ca

import getpass
import sys
import os

import cx_Oracle

import Database

def connectScreen():
	database = None
	while True:
		print("Connect to database")
		username = input("Username: ")
		password = getpass.getpass("Password: ")
		database = Database.connect(username, password)
		if database:
			break
	mainScreen(database)

def mainScreen(database):
	while True:
		print("Screen 1")
		print("1. Login")
		print("2. Register")
		print("3. Exit")
		selection = input("")
		if selection == "1":
			loginScreen(database)
		elif selection == "2":
			registerScreen(database)
		elif selection == "3":
			sys.exit()
		else:
			pass

def loginScreen(database):
	pass

def registerScreen(database):
	pass

def main():
	connectScreen()

def clear():
	os.system("clear")

if __name__ == "__main__":
	try:
		main()
	except cx_Oracle.DatabaseError as e:
		error, = e.args
		print("Oracle code:", error.code)
		print("Oracle message:", error.message)
	except KeyboardInterrupt:
		sys.exit()