# run: ssh -L 1525:gwynne.cs.ualberta.ca:1521 dskrundz@ohaton.cs.ualberta.ca

import sys

from colorama import Fore, Back
import cx_Oracle

import Database
import DBView
import Util

def main():
	# Connect to the database
	database = Database.connect()
	if not database:
		print("Could not connect to database")
		return
	# Present the next view
	DBView.DBView(database)

if __name__ == "__main__":
	try:
		main()
	except cx_Oracle.DatabaseError as e:
		error, = e.args
		print("Oracle code:", error.code)
		print("Oracle message:", error.message)
	except KeyboardInterrupt:
		print(Fore.RESET + Back.RESET)
		sys.exit()