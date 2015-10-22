import os

import Agent

def mainScreen(database, email, isAgent):
	while True:
		clear()
		print("Main Screen")
		print("1. Search")
		print("2. List Bookings")
		if isAgent:
			print("3. Record departure")
			print("4. Record arrival")
			print("5. Logout")
		else:
			print("3. Logout")
		selection = input(" ")
		if selection == "1":
			pass
		elif selection == "2":
			pass
		elif selection == "3":
			if isAgent:
				recordDeparture(database)
			else:
				return
		elif selection == "4" and isAgent:
			recordArrival(database)
		elif selection == "5" and isAgent:
			return
		else:
			pass

def recordDeparture(database):
	clear()
	print("Record Departure Time")
	flightno = input("Flight Number: ")
	date = input("Departure Date (YYYY-MM-DD): ")
	time = input("Time (hh-mm-ss): ")
	Agent.recordDeparture(database, flightno, date, time)

def recordArrival(database):
	clear()
	print("Record Arrival Time")
	flightno = input("Flight Number: ")
	date = input("Departure Date (YYYY-MM-DD): ")
	time = input("Time (hh-mm-ss): ")
	Agent.recordArrival(database, flightno, date, time)

def clear():
	os.system("clear")