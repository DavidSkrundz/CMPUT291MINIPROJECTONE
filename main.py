# run: ssh -L 1525:gwynne.cs.ualberta.ca:1521 dskrundz@ohaton.cs.ualberta.ca

import getpass
import sys
import os

import cx_Oracle

import Database
import MainScreen
import Util

def connectScreen():
	database = None
	while True:
		clear()
		print("Connect to database")
		username = input("Username: ")
		password = getpass.getpass("Password: ")
		database = Database.connect(username, password)
		if database:
			break
	introScreen(database)

def introScreen(database):
	while True:
		clear()
		print("Screen 1")
		print("1. Login")
		print("2. Register")
		print("3. Exit")
		selection = input(" ")
		if selection == "1":
			loginScreen(database)
		elif selection == "2":
			registerScreen(database)
		elif selection == "3":
			sys.exit()
		else:
			pass

def loginScreen(database):
	clear()
	print("Login")
	email = input("Email: ")
	password = getpass.getpass("Password: ")
	users = database.get("select u.email, u.pass from users u where u.email = '{}' and u.pass = '{}'".format(email, password))
	if len(users) == 1:
		isAgent = False
		agents = database.get("select * from airline_agents a where a.email = '{}'".format(email))
		if len(agents) == 1:
			isAgent = True
		MainScreen.mainScreen(database, email, isAgent)
	else:
		input("Invalid login")

def registerScreen(database):
	clear()
	print("Register as new user")
	email = input("Email: ")
	# Make sure the email isn't already taken
	emails = database.get("select u.email from users u where u.email = '{}'".format(email))
	if len(emails) > 0:
		input("Email already exists (enter to continue)")
		return
	password = getpass.getpass("Password: ")
	database.put("insert into users values ('{}', '{}', null)".format(email, password))
	database.commit()
	input("User created (enter to continue)")

def main():
	connectScreen()

def clear():
	Util.clear()

if __name__ == "__main__":
	try:
		main()
	except cx_Oracle.DatabaseError as e:
		error, = e.args
		print("Oracle code:", error.code)
		print("Oracle message:", error.message)
	except KeyboardInterrupt:
		sys.exit()
