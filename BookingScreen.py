import os
import sys
import Booking
import Util

def bookingScreen(database, email):
	while True:
		Util.clear()
		Booking.bookingQuery(database, email)
		bookings = database.cursor.fetchall()
		print("0 to go back")
		Util.print_table(["Row #", "Ticket no.", "Name", "Date", "Price"],
							[6, 10, 20, 20, 10],
							bookings,
							[0, 3, 1, 6, 2])
#		for idx, booking in enumerate(bookings):
#			print("{0}. Ticket no. = {1} Name = {2} Date = {3} Price = {4}"\
#				.format(idx, booking[2], booking[0], booking[3].strftime("%d-%b-%Y"), booking[1]))
		if len(bookings) == 0:
			print("No bookings.")
			input("")
			return
		selection = int(input("Select booking: "))
		if selection == 0:
			return
		selection = selection - 1
		if selection > len(bookings):
			print("Invalid selection (enter to continue)")
			input("")
			continue
		else:
			Util.clear()
			print("Name = {}".format(bookings[selection][1]))
			print("Price = {}".format(bookings[selection][2]))
			print("Ticket no. = {}".format(bookings[selection][3]))
			print("Flight no. = {}".format(bookings[selection][4]))
			print("Fare Type = {}".format(bookings[selection][5]))
			print("Departure Date = {}".format(bookings[selection][6]))
			print("Seat = {}".format(bookings[selection][7]))
			print("")
			print("1. Delete")
			print("2. Back")
			selectionmenu = int(input(""))
			if selectionmenu == 1:
				Booking.cancelBooking(database, bookings[selection][3], bookings[selection][4], bookings[selection][6])
