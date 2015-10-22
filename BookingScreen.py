import os

def bookingScreen(database, email):
	while True:
		clear()
		bookingQuery(database, email)
		bookings = database.cursor.fetchall()
		for idx, booking in enumerate(bookings):
			print("{0}. Ticket no. = {1} Name = {2} Date = {3} Price = {4}"\
				  .format(idx, booking[0], booking[1], booking[2].strftime("%d-%b-%Y"), booking[3]))
		selection = input("")