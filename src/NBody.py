import CLIbrary, numpy, bcrypt, time, random
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation
from colorama import Fore, Back, Style
from datetime import datetime

# USERS

class user:
	def __init__(self):
		self.name = CLIbrary.strIn({"request": "\nUser", "space": False, "blockedAnswers": [""]})

		self.registrationDate = datetime.now()
		self.lastLogin = self.registrationDate

		self.protected = False
		self.passwordHash = ""

		self.darkTheme = False

		self.bodies = []
	
	def __str__(self):
		return self.name

	def login(self, passwordHash):
		password = CLIbrary.strIn({"request": "Password", "space": False, "fixedLength": 8})
		self.passwordHash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

		return bcrypt.checkpw(password.encode(), passwordHash)

	def register(self):
		self.passwordHash = bcrypt.hashpw(CLIbrary.strIn({"request": "Password", "space": False, "verification": True, "fixedLength": 8}).encode(), bcrypt.gensalt())
		self.protected = True

# BODIES

def norm(vector: numpy.array) -> float:
	return numpy.sqrt(sum([v**2 for v in vector]))

def getPosition(position: numpy.array) -> list: # Needed due to Python's referencing system.
	return [coordinate for coordinate in position]

class body:
	def __init__(self, others: list):
		while True:
			self.name = CLIbrary.strIn({"request": "Body's name", "space": False, "blockedAnswers": [""]})
			self.name = self.name[0].upper() + self.name[1:]

			if self.name not in [other.name for other in others]:
				break

			else:
				CLIbrary.output({"type": "error", "string": "NAME UNAVAILABLE"})

		while True:
			self.mass = float(CLIbrary.numIn({"request": "\n" + self.name + "'s mass"}))
			self.radius = float(CLIbrary.numIn({"request": self.name + "'s radius"}))

			if self.mass > 0 and self.radius > 0:
				break
			
			else:
				CLIbrary.output({"type": "error", "string": "PHYSICS ERROR"})

		x = CLIbrary.numIn({"request": "\n" + self.name + "'s starting X"})
		y = CLIbrary.numIn({"request": self.name + "'s starting Y"})
		z = CLIbrary.numIn({"request": self.name + "'s starting Z"})

		vx = CLIbrary.numIn({"request": "\n" + self.name + "'s starting V_X"})
		vy = CLIbrary.numIn({"request": self.name + "'s starting V_Y"})
		vz = CLIbrary.numIn({"request": self.name + "'s starting V_Z"})

		self.position = numpy.array([float(x), float(y), float(z)])
		self.speed = numpy.array([float(vx), float(vy), float(vz)])

		self.lifespan = 0.0

		self.force = numpy.array([0.0] * 3)

		self.merged = []
		self.history = [getPosition(self.position)]
		self.inactive = False

	def __str__(self) -> str:
		string = Fore.RED + self.name.upper() + Style.RESET_ALL if self.merged else self.name.upper()
		if self.merged:
			string += "\n\tMerged with: " + ", ".join(mergedBody.name for mergedBody in self.merged)
		string += "\n\tLifespan: " + str(round(self.lifespan, 2))
		string += "\n\n\tMass: " + str(round(self.mass, 2))
		string += "\n\tRadius: " + str(round(self.radius, 2))
		string += "\n\n\tPosition: [" + ", ".join([str(round(self.position[index], 2)) for index in range(3)]) + "]: " + str(round(norm(self.position), 2))
		string += "\n\tSpeed: [" + ", ".join([str(round(self.speed[index], 2)) for index in range(3)]) + "]: " + str(round(norm(self.speed), 2))

		return string

	def reset(self) -> None:
		self.history = [getPosition(self.position)]

	def merge(self, other: "body") -> None:
		if not self.inactive:
			self.merged.append(other)

			self.position = (self.mass * self.position + other.mass * other.position) / (self.mass + other.mass)
			self.speed = (self.mass * self.speed + other.mass * other.speed) / (self.mass + other.mass)

			self.mass += other.mass
			self.radius += other.radius

			other.inactive = True

	def newton(self, other: "body") -> None:
		if not (self.inactive or other.inactive):
			if norm(self.position - other.position) <= (self.radius + other.radius) / 2:
				self.merge(other)

			else:
				self.force += (self.mass * other.mass) / (norm(self.position - other.position) ** 3) * (other.position - self.position)
				other.force += - self.force

	def move(self, step: float) -> None:
		if not self.inactive:
			self.speed += self.force / self.mass * step
			self.position += self.speed * step

			self.lifespan += step

			self.history.append(getPosition(self.position))
			self.force = 0

# SIMULATION

def simulate(bodies: list, step: float, steps: int) -> None:
	start = time.time()

	for _ in range(steps):
		simulationBodies = [body for body in bodies if not body.inactive]
		
		# Evaluates Newton's force.
		for j in range(len(simulationBodies)):
			for k in range(j + 1, len(simulationBodies)):
				simulationBodies[j].newton(simulationBodies[k])

		# Moves bodies.
		for body in simulationBodies:
			body.move(step)

	CLIbrary.output({"type": "verbose", "string": "DONE IN " + str(round(time.time() - start, 2)) + " SECONDS"})

# GRAPHICS

def getTrajectories(bodies: list) -> list:
	def step(x: float) -> int: # Less points.
		return int(numpy.ceil(x / (2000 / numpy.pi) / numpy.arctan(x * numpy.pi / 2000)))
	
	trajectories = [[point for point in body.history] for body in bodies]
	return [[trajectory[index] for index in range(0, len(trajectory), step(len(trajectory)))] for trajectory in trajectories]

def plotTrajectories(bodies: list) -> None:
	fig = plt.figure()
	ax = fig.add_subplot(111, projection = '3d')

	limit = max([max([max([abs(position[index]) for index in range(3)]) for position in body.history]) for body in bodies])

	ax.set_xlim(-limit, limit)
	ax.set_ylim(-limit, limit)
	ax.set_zlim(-limit, limit)

	trajectories = getTrajectories(bodies)
	for trajectory in trajectories:
		x = [position[0] for position in trajectory]
		y = [position[1] for position in trajectory]
		z = [position[2] for position in trajectory]
		
		colour = [random.randint(0, 128) / 256 for _ in range(3)]

		ax.plot(x, y, z, color=colour)

		if len(trajectory) > 1:
			ax.scatter(x[-1], y[-1], z[-1], marker="o" if not bodies[trajectories.index(trajectory)].inactive else ".", color=colour, label=bodies[trajectories.index(trajectory)].name)
	
	ax.legend()
	plt.show()

def animateTrajectories(bodies: list) -> None:
	def updateTrajectories(index: int, rawTrajectories: list, trajectories, dots):
		for trajectory, rawTrajectory, dot in zip(trajectories, rawTrajectories, dots):
			xData = [position[0] for position in rawTrajectory[:index]]
			yData = [position[1] for position in rawTrajectory[:index]]
			zData = [position[2] for position in rawTrajectory[:index]]

			try:
				dot._offsets3d = ([xData[-1]], [yData[-1]], [zData[-1]])
			
			except(IndexError):
				pass

			trajectory.set_data(xData, yData)
			trajectory.set_3d_properties(zData)

	fig = plt.figure()
	ax = fig.add_subplot(111, projection = '3d')

	limit = max([max([max([abs(position[index]) for index in range(3)]) for position in body.history]) for body in bodies])

	ax.set_xlim(-limit, limit)
	ax.set_ylim(-limit, limit)
	ax.set_zlim(-limit, limit)

	rawTrajectories = getTrajectories(bodies)

	colours = [[random.randint(0, 128) / 256 for _ in range(3)] for _ in rawTrajectories]
	labels = [body.name for body in bodies]
	
	trajectories = [ax.plot([], [], [], color=colours[index])[0] for index in range(len(rawTrajectories))]
	dots = [ax.scatter([], [], [], label=labels[index], color=colours[index], marker="o" if not bodies[index].inactive else ".") for index in range(len(rawTrajectories))]

	ani = animation.FuncAnimation(fig, updateTrajectories, len(rawTrajectories[0]), fargs=(rawTrajectories, trajectories, dots), interval=24, repeat=False)

	ax.legend()
	plt.show()