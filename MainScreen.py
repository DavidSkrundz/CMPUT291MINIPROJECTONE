import os

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
				pass
			else:
				return
		elif selection == "4" and isAgent:
			pass
		elif selection == "5" and isAgent:
			return
		else:
			pass

def clear():
	os.system("clear")