import os
import Booking

def bookingScreen(database, email):
	while True:
		clear()
		bookingQuery(database, email)
		bookings = database.cursor.fetchall()
		for idx, booking in enumerate(bookings):
			print("{0}. Ticket no. = {1} Name = {2} Date = {3} Price = {4}"\
				.format(idx, booking[2], booking[0], booking[3].strftime("%d-%b-%Y"), booking[1]))
		selection = input("Select booking:")
		if int(selection) > len(bookings):
			print("Invalid selection.")
			continue
		else:
			clear()
			print("Name = {}".format(bookings[selection][0]))
			print("Price = {}".format(bookings[selection][1]))
			print("Ticket no. = {}".format(bookings[selection][2]))
			print("Flight no. = {}".format(bookings[selection][3]))
			print("Fare Type = {}".format(bookings[selection][4]))
			print("Departure Date = {}".format(bookings[selection][5]))
			print("Seat = {}".format(bookings[selection][6]))
			print("")
			print("1. Delete")
			print("2. Back")
			selection = input("")
			if selection == 1:
				Booking.cancelBooking(database, bookings[selection][2])
				
			