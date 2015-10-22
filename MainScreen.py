import os

import Agent
import BookingScreen
import Search
import Util

def mainScreen(database, email, isAgent):
	while True:
		Util.clear()
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
			searchFlights(database)
		elif selection == "2":
			BookingScreen.bookingScreen(database, email)
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

def searchFlights(database):
	Util.clear()
	print("Search Flights")
	roundTrip = input("Round Trip? (y/n): ").lower() == "y"
	source = Util.findAirportCode(database, input("Source: "))
	destination = Util.findAirportCode(database, input("Destination: "))
	date = input("Departure Date (YYYY-MM-DD): ")
	partySize = 1
	returnDate = None
	if roundTrip:
		partySize = input("Party Size: ")
		returnDate = input("Return Date (YYYY-MM-DD): ")
	flights = Search.flightQuery(database, roundTrip, returnDate, date, partySize, source, destination)
	# TODO:

def recordDeparture(database):
	Util.clear()
	print("Record Departure Time")
	flightno = input("Flight Number: ")
	date = input("Departure Date (YYYY-MM-DD): ")
	time = input("Actual Departure Time (hh-mm-ss): ")
	Agent.recordDeparture(database, flightno, date, time)
	input("Updated (enter to continue)")

def recordArrival(database):
	Util.clear()
	print("Record Arrival Time")
	flightno = input("Flight Number: ")
	date = input("Departure Date (YYYY-MM-DD): ")
	time = input("Actual Arrival Time (hh-mm-ss): ")
	Agent.recordArrival(database, flightno, date, time)
	input("Updated (enter to continue)")
