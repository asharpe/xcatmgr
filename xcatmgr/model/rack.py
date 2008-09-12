from xcatmgr.util import log

class Rack:
	def __init__(self, index=-1, room="Machine Room"):
		self.index = index
		self.room = room
		self.machines = []

	def addMachine(self, machine):
		self.machines.append(machine)

	def size(self):
		return self.machines.length

	size = property(size)
	realindex = property(lambda self:self.index - 1)

	def close(self):
		for machine in self.machines:
			machine.close()

	def maxMachineIndex(self):
		max = 0
		for machine in self.machines:
			max = machine.rackindex > max and machine.rackindex or max

		return max

	def active(self):
		active = 0
		for machine in self.machines:
			active += machine.active()

		log.debug('rack %d: %d active' % (self.index, active))
		return active

