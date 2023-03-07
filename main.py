import CLIbrary, os, platform, sys, shutil
from colorama import Fore, Back, Style
import NBody

version = "1.0.0"
production = True
if "NBody" not in "".join(sys.argv): # Local testing.
	production = False

system = platform.system()
path = os.getenv("PATH")

print("\n" + Back.MAGENTA + Fore.WHITE + " " + version + " " + Back.WHITE + Fore.MAGENTA + " NBody " + Style.RESET_ALL) if production else print("\n" + Back.WHITE + Fore.BLUE + " NBody " + Style.RESET_ALL)
print("N bodies simulation utility written in Python and built with CLIbrary")
print("Developed by " + Style.BRIGHT + Fore.RED + "Andrea Di Antonio" + Style.RESET_ALL + ", more on " + Style.BRIGHT + "https://github.com/diantonioandrea" + Style.RESET_ALL)

# PATHS

if production: # Production.
	homePath = os.path.expanduser("~") + "/"
	installPath = homePath
	
	installPath += "Library/NBody/"

	dataPath = installPath + "data/"
	resourcesPath = installPath + "resources/"

else: # Testing.
	installPath = str(os.getcwd()) + "/"

	dataPath = installPath + "data/"
	reportsPath = installPath + "reports/"
	resourcesPath = installPath + "resources/"

helpPath = resourcesPath + "NBodyHelp.json"

# INSTALLATION

if "install" in sys.argv and production:
	try:
		currentPath = os.getcwd() + "/"
		
		if not os.path.exists(resourcesPath):
			os.makedirs(resourcesPath)

		for file in os.listdir(currentPath + "resources/"):
			shutil.copy(currentPath + "resources/" + file, resourcesPath + file)

		shutil.copy(currentPath + "NBody", installPath + "NBody")

		CLIbrary.output({"type": "verbose", "string": "NBODY INSTALLED SUCCESFULLY TO " + installPath, "before": "\n"})

		if "NBody" not in path:
			CLIbrary.output({"type": "warning", "string": "MAKE SURE TO ADD ITS INSTALLATION DIRECTORY TO PATH TO USE IT ANYWHERE", "after": "\n"})
		
		else:
			print("\nGoodbye.\n")
	
	except:
		CLIbrary.output({"type": "error", "string": "INSTALLATION ERROR", "before": "\n", "after": "\n"})
		sys.exit(-1)

	finally:
		sys.exit(0)

# CHECKS

try:
	# Folders.

	if not os.path.exists(dataPath):
		os.makedirs(dataPath)

	if not os.path.exists(resourcesPath):
		raise(FileNotFoundError)

	# Resources

	resources = [helpPath]
	
	for resource in resources:
		if not os.path.exists(resource):
			raise(FileNotFoundError)
	
except:
	if production:
		CLIbrary.output({"type": "error", "string": "DATA OR RESOURCES ERROR, TRY REINSTALLING NBODY", "after": "\n"})
	
	else:
		CLIbrary.output({"type": "error", "string": "DATA OR RESOURCES ERROR", "before": "\n", "after": "\n"})

	sys.exit(-1)

# LOGIN OR REGISTER

while True:
	user = NBody.user()

	fileHandler = {"path": dataPath + user.name + ".nb", "ignoreMissing": True}
	userData = CLIbrary.aLoad(fileHandler)

	if userData != None:
		if userData.protected:
			if user.login(userData.passwordHash):
				user.protected = True

			else:
				CLIbrary.output({"type": "error", "string": "LOGIN ERROR"})

				if CLIbrary.boolIn({"request": "Exit"}):
					print("\nGoodbye.\n")
					sys.exit(-1)
				else:
					continue
		
		user.registrationDate = userData.registrationDate
		user.bodies = userData.bodies

		try:
			if userData.darkTheme:
				CLIbrary.style.setting_darkMode = True
				user.darkTheme = userData.darkTheme
		
		except:
			user.darkTheme = False

		print("\nWelcome back, " + str(user) + "\nLast login: " + userData.lastLogin.strftime("%A, %B %d, %Y at %H:%M"))
		break

	else:
		if not CLIbrary.boolIn({"request": "User \"" + user.name + "\" does not exist. Would you like to create it?"}):
			if CLIbrary.boolIn({"request": "Exit"}):
				print("\nGoodbye.\n")
				sys.exit(-1)
			continue

		print("\nWelcome, " + str(user))
		break

print("Type \'help\' if needed\n")

bodies = user.bodies

# Prompt.
cmdHandler = {"request": "[" + str(user) + "@nbody]"}
cmdHandler["style"] = Fore.YELLOW
cmdHandler["allowedCommands"] = ["new", "set", "password"]

cmdHandler["helpPath"] = "resources/NBodyHelp.json"

while True:
	bodies.sort(key = lambda entry: entry.mass, reverse=True)

	fileHandler["data"] = user
	CLIbrary.aDump(fileHandler)

	if len(bodies):
		cmdHandler["allowedCommands"] += ["info", "clear", "reset", "plot"]

		if len(bodies) > 1:
			cmdHandler["allowedCommands"] += ["simulate"]

	command = CLIbrary.cmdIn(cmdHandler)

	cmd = command["command"]
	sdOpts = command["sdOpts"]
	ddOpts = command["ddOpts"]

	# EXIT

	if cmd == "exit": # Exits the program.
		break

	# SET

	if cmd == "set": # Exits the program.
		if "t" in sdOpts: # Theme.
			if sdOpts["t"] == "light":
				CLIbrary.style.setting_darkMode = False
				user.darkTheme = False
				CLIbrary.output({"type": "verbose", "string": "THEME SET TO LIGHT"})
			
			elif sdOpts["t"] == "dark":
				CLIbrary.style.setting_darkMode = True
				user.darkTheme = True
				CLIbrary.output({"type": "verbose", "string": "THEME SET TO DARK"})

			else:
				CLIbrary.output({"type": "error", "string": "UNKNOWN OPTION"})
		
		else:
			CLIbrary.output({"type": "error", "string": "MISSING OPTION"})

	# PASSWORD

	elif cmd == "password": # Toggles the password protection.
		if user.protected:
			if user.login(user.passwordHash):
				CLIbrary.output({"type": "verbose", "string": "PASSWORD DISABLED"})
				user.protected = False
				user.passwordHash = ""
				continue
				
			else:
				CLIbrary.output({"type": "error", "string": "WRONG PASSWORD"})
				continue

		user.register()
		CLIbrary.output({"type": "verbose", "string": "PASSWORD SET"})

	# NEW

	elif cmd == "new": # Creates a new body.
		bodies.append(NBody.body(bodies))
		CLIbrary.output({"type": "verbose", "string": "NEW BODY CREATED", "before": "\n"})

	# INFO

	elif cmd == "info": # Prints infos on current bodies.
		if "all" in ddOpts:
			print("\n".join([str(bodies.index(body) + 1) + ". " + str(body) for body in bodies]))
		
		else:
			print("\n".join([str(bodies.index(body) + 1) + ". " + str(body) for body in bodies if not body.inactive]))

	# CLEAR

	elif cmd == "clear": # Clears the bodies list.
		if CLIbrary.boolIn({"request": "Clear all bodies?"}):
			user.bodies = [] # Don't know why it needs both.
			bodies = []
			CLIbrary.output({"type": "verbose", "string": "BODIES CLEARED", "before": "\n"})

	# RESET

	elif cmd == "reset": # Reset bodies' trajectories.
		if CLIbrary.boolIn({"request": "Reset bodies\' trajectories?"}):
			for body in user.bodies:
				body.reset()

			for body in bodies:
				body.reset()

			CLIbrary.output({"type": "verbose", "string": "BODIES RESET", "before": "\n"})

	# SIMULATION
	
	elif cmd == "simulate": # Starts a simulation.
		if "n" not in sdOpts or "t" not in sdOpts:
			CLIbrary.output({"type": "error", "string": "MISSING OPTION"})
			continue
		
		try:
			NBody.simulate(bodies, float(sdOpts["t"]), int(sdOpts["n"]))
		
		except(ValueError):
			CLIbrary.output({"type": "error", "string": "OPTIONS ERROR"})

	# PLOTTING
	
	elif cmd == "plot": # Plots the computed trajectories.
		if "animated" not in ddOpts:
			NBody.plotTrajectories(bodies)

		else:
			NBody.animateTrajectories(bodies)

print("\nGoodbye, " + str(user) + ".\n")