import os

import Agent
import Booking
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
				logout(database, email)
				return
		elif selection == "4" and isAgent:
			recordArrival(database)
		elif selection == "5" and isAgent:
			logout(database, email)
			return
		else:
			pass

def logout(database, email):
	database.put("update users set last_login = sysdate where users.email = '{}'".format(email))
	database.commit()

def searchFlights(database):
	Util.clear()
	print("Search Flights")
	roundTrip = input("Round Trip? (y/n): ").lower() == "y"
	source = Util.findAirportCode(database, input("Source: "))
	destination = Util.findAirportCode(database, input("Destination: "))
	date = input("Departure Date (YYYY-MM-DD): ")
	partySize = int(input("Party Size: "))
	returnDate = None
	if roundTrip:
		returnDate = input("Return Date (YYYY-MM-DD): ")
	sortByCon = input("Sorting by price. Sort by connections instead? (y/n): ").lower() == "y"
	flights = Search.flightQuery(database, roundTrip, returnDate, date, partySize, source, destination, sortByCon)
	if flights == None:
		input("Flight got full because you're too slow")
		return
	print(flights)
	Booking.addBooking(database, flights[0], flights[11], flights[4].strftime('%Y-%m-%d'))
	if not flights[1] == None:
		Booking.addBooking(database, flights[1], flights[12], flights[4].strftime('%Y-%m-%d'))
# need name, email, price
	input("Booked (enter to continue)")

def recordDeparture(database):
	Util.clear()
	print("Record Departure Time")
	flightno = input("Flight Number: ")
	date = input("Departure Date (YYYY-MM-DD): ")
	time = input("Actual Departure Time (hh:mm:ss): ")
	Agent.recordDeparture(database, flightno, date, time)
	input("Updated (enter to continue)")

def recordArrival(database):
	Util.clear()
	print("Record Arrival Time")
	flightno = input("Flight Number: ")
	date = input("Departure Date (YYYY-MM-DD): ")
	time = input("Actual Arrival Time (hh:mm:ss): ")
	Agent.recordArrival(database, flightno, date, time)
	input("Updated (enter to continue)")
