import getpass

from colorama.ansi import Back

import Util

def getLogin(title, previous=False):
	# Clear the screen
	Util.clearScreen()
	# Get the screen size
	(width, height) = Util.getTerminalSize()
	x = int(width / 8)
	y = int(height / 2 - 2)
	print(Back.CYAN + Util.moveCursorString((x * 4) - int(len(title) / 2), y - 4) + title)
	if previous:
		print(Back.RED + Util.moveCursorString(x * 4 - 6, y + 8) + "Login Failed")
	# Get the username
	username = input(Back.RESET + Util.moveCursorString(x, y) + "Username: " + Back.GREEN)
	# Get the password
	password = getpass.getpass(Back.RESET + Util.moveCursorString(x, y + 4) + "Password: ")
#	password = ""
#	print(Back.RESET + Util.moveCursorString(x, y + 4) + "Password: " + Back.RED, end="", flush=True)
#	while True:
#		char = str(Util.getCharacter())
#		if char == "\r":
#			break
#		if char == '\x08' or char == '\x7f':
#			print('\x08 \x08', end="", flush=True)
#		else:
#			print("•", end="", flush=True)
#		if char == '\x11':
#			raise KeyboardInterrupt()
#		password = password + char
	Util.clearScreen()
	return (username, password)