import CLIbrary, os, random, platform, sys, shutil, requests, zipfile
from colorama import Fore, Back, Style
import NBody

CLIbrary.data.setting_fileExtension = ".nb"

# ---
# From an answer of Ciro Santilli on https://stackoverflow.com/questions/12791997/how-do-you-do-a-simple-chmod-x-from-within-python
import stat

def get_umask():
    umask = os.umask(0)
    os.umask(umask)

    return umask

def executable(filePath):
    os.chmod(filePath, os.stat(filePath).st_mode | ((stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH) & ~get_umask()))
# ---

name = "NBody"
version = "v1.1.0_dev"
production = True
if name not in "".join(sys.argv): # Local testing.
	production = False

system = platform.system()
path = os.getenv("PATH")

print("\n" + Back.MAGENTA + Fore.WHITE + " " + version + " " + Back.WHITE + Fore.MAGENTA + " " + name + " " + Style.RESET_ALL) if production else print("\n" + Back.WHITE + Fore.BLUE + " " + name + " " + Style.RESET_ALL)
print("N bodies simulation utility written in Python and built with CLIbrary")
print("Developed by " + Style.BRIGHT + Fore.RED + "Andrea Di Antonio" + Style.RESET_ALL + ", more on " + Style.BRIGHT + "https://github.com/diantonioandrea/" + name + Style.RESET_ALL + "\n")

# PATHS

if production: # Production.
	homePath = os.path.expanduser("~") + "/"
	installPath = homePath
	
	if system == "Darwin":
		installPath += "Library/" + name + "/"
	
	elif system == "Linux":
		installPath += ".local/bin/" + name + "/"

	elif system == "Windows":
		installPath += "AppData/Roaming/" + name + "/"

else: # Testing.
	installPath = str(os.getcwd()) + "/"

dataPath = installPath + "data/"
resourcesPath = installPath + "resources/"
helpPath = resourcesPath + name + "Help.json"

# INSTALLATION

if "install" in sys.argv and production:
	try:
		currentPath = os.getcwd() + "/"
		
		if not os.path.exists(resourcesPath):
			os.makedirs(resourcesPath)

		for file in os.listdir(currentPath + "resources/"):
			shutil.copy(currentPath + "resources/" + file, resourcesPath + file)

		if system != "Windows":
			shutil.copy(currentPath + name, installPath + name)

		else:
			shutil.copy(currentPath + name + ".exe", installPath + name + ".exe")

		CLIbrary.output({"type": "verbose", "string": name.upper() + " INSTALLED SUCCESFULLY TO " + installPath, "before": "\n"})

		if name not in path:
			CLIbrary.output({"type": "warning", "string": "MAKE SURE TO ADD ITS INSTALLATION DIRECTORY TO PATH TO USE IT ANYWHERE", "after": "\n"})
		
		else:
			print("\nGoodbye.\n")
	
	except:
		CLIbrary.output({"type": "error", "string": "INSTALLATION ERROR", "before": "\n", "after": "\n"})
		sys.exit(-1)

	finally:
		sys.exit(0)

# UPDATE

if production:
	updateFlag = False

	try:
		latestVersion = requests.get("https://github.com/diantonioandrea/" + name + "/releases/latest").url.split("/")[-1]

		if  version < latestVersion or (latestVersion in version and "_dev" in version):
			CLIbrary.output({"type": "verbose", "string": "UPDATE AVAILABLE: " + version + " \u2192 " + latestVersion, "before": "\n"})

			if CLIbrary.boolIn({"request": "Would you like to download the latest version?"}):
				tempPath = installPath + "temp/"

				if not os.path.exists(tempPath):
					os.makedirs(tempPath)

				filePath = tempPath + name + "-SYSTEM.zip".replace("SYSTEM", system.lower())
				url = "https://github.com/diantonioandrea/" + name + "/releases/download/" + latestVersion + "/" + name + "-SYSTEM.zip".replace("SYSTEM", system.lower())

				file = open(filePath, "wb")
				file.write(requests.get(url).content)
				file.close()

				updatePackage = zipfile.ZipFile(filePath, "r")
				updatePackage.extractall(tempPath)

				for file in os.listdir(tempPath + "resources/"):
					shutil.copy(tempPath + "resources/" + file, resourcesPath + file)

				if system != "Windows":
					shutil.copy(tempPath + name, installPath + name)
					executable(installPath + name)

				else:
					shutil.copy(tempPath + name + ".exe", installPath + name + ".exe")
					executable(installPath + name + ".exe")

				updateFlag = True
				shutil.rmtree(tempPath)
				CLIbrary.output({"type": "verbose", "string": "UPDATED TO: " + latestVersion})
			
			else:
				CLIbrary.output({"type": "verbose", "string": "UPDATE IGNORED"})

	except(requests.exceptions.RequestException):
		CLIbrary.output({"type": "error", "string": "COULDN'T CHECK FOR UPDATES", "before": "\n"})

	except:
		CLIbrary.output({"type": "error", "string": "UPDATE MAY HAVE FAILED", "before": "\n", "after": "\n"})
		sys.exit(-1)

	finally:
		if updateFlag:
			CLIbrary.output({"type": "verbose", "string": "THE PROGRAM HAS BEEN CLOSED TO COMPLETE THE UPDATE", "after": "\n"})
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
		CLIbrary.output({"type": "error", "string": "DATA OR RESOURCES ERROR, TRY REINSTALLING " + name.upper(), "after": "\n"})
	
	else:
		CLIbrary.output({"type": "error", "string": "DATA OR RESOURCES ERROR", "before": "\n", "after": "\n"})

	sys.exit(-1)

# LOGIN OR REGISTER

while True:
	user = NBody.user()

	fileHandler = {"path": dataPath + user.name, "ignoreMissing": True}
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

# Prompt.
cmdHandler = {"request": "[" + str(user) + "@" + name + "]"}
cmdHandler["style"] = Fore.YELLOW
cmdHandler["helpPath"] = helpPath

while True:
	bodies = user.bodies
	bodies.sort(key = lambda entry: entry.mass, reverse=True)

	fileHandler["data"] = user
	CLIbrary.aDump(fileHandler)

	cmdHandler["allowedCommands"] = ["new", "set", "password", "delete"]

	if len(bodies):
		cmdHandler["allowedCommands"] += ["info", "clear", "reset", "remove", "plot"]

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

	# DELETE
		
	elif cmd == "delete": # Deletes the profile.
		deletionCode = str(random.randint(10**3, 10**4-1))

		if CLIbrary.strIn({"request": "Given that this action is irreversible, insert \"" + deletionCode + "\" to delete your profile"}) == deletionCode:
			os.remove(dataPath + user.name + ".nb")

			CLIbrary.output({"type": "verbose", "string": "PROFILE DELETED"})
			break

		CLIbrary.output({"type": "error", "string": "WRONG VERIFICATION CODE"})
		continue

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
			user.bodies = []
			CLIbrary.output({"type": "verbose", "string": "BODIES CLEARED", "before": "\n"})

	# RESET

	elif cmd == "reset": # Reset bodies' trajectories.
		if CLIbrary.boolIn({"request": "Reset bodies\' trajectories?"}):
			for body in user.bodies:
				body.reset()

			CLIbrary.output({"type": "verbose", "string": "BODIES RESET", "before": "\n"})

	# REMOVE

	elif cmd == "remove": # Removes a body by its name.
		if "n" not in sdOpts:
			CLIbrary.output({"type": "error", "string": "MISSING OPTION"})
			continue

		targetBody = [body for body in bodies if body.name.lower() == sdOpts["n"]]

		if len(targetBody):
			targetBody = targetBody.pop()
			user.bodies.remove(targetBody)
			CLIbrary.output({"type": "verbose", "string": "BODY REMOVED"})

		else:
			CLIbrary.output({"type": "error", "string": "BODY NOT FOUND"})

	# SIMULATION
	
	elif cmd == "simulate": # Starts a simulation.
		if "n" not in sdOpts or "t" not in sdOpts:
			CLIbrary.output({"type": "error", "string": "MISSING OPTION(S)"})
			continue
		
		try:
			NBody.simulate(bodies, float(sdOpts["t"]), int(sdOpts["n"]))
		
		except(ValueError):
			CLIbrary.output({"type": "error", "string": "OPTIONS ERROR"})

	# PLOTTING
	
	elif cmd == "plot": # Plots the computed trajectories.
		if max([len(body.history) for body in bodies]) < 2 and min([len(body.history) for body in bodies]) < 2:
			CLIbrary.output({"type": "error", "string": "NOT ENOUGH POINTS"})
			continue

		if "animated" not in ddOpts:
			NBody.plotTrajectories(bodies)

		else:
			NBody.animateTrajectories(bodies)

print("\nGoodbye, " + str(user) + ".\n")