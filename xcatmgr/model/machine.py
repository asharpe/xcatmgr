from xcatmgr.util import *
from xcatmgr.model.command import Command, SshRconsConsole, SshSshConsole
from xcatmgr.model.rack import Rack

#from xcatmgr.ui.main import config
from copy import deepcopy


class Machine:
	def __init__(self, name="Unknown", status="Unknown", ncpus=0, ram=0, command=Command(), rackindex=-1):
		self.name = name
		self.status = status
		self.interfaces = []
		self.ncpus = ncpus
		self.ram = ram
		self.command = command
		self.rackindex = rackindex

	realrackindex = property(lambda self: self.rackindex - 1)

	def setStatus(self, status):
		self.status = status

	def addInterface(self, interface):
		self.interfaces.append(interface)

	def close(self):
		if self.command.running:
			log.info('%s: stopping command' % self.name)
			self.command.stop()

	def active(self):
		active = self.command.active()
		log.debug('%s: %d active' % (self.name, active))
		return active


class MgmtNode(Machine):
	def __init__(self, name="Machine", status="Unknown", ncpus=0, ram=0):
		Machine.__init__(self, name=name, status=status, ncpus=ncpus, ram=ram)
		self.remote_address = 'mgmt.hpc.jcu.edu.au'
		self.xcat_location = "/opt/xcat"

#		self.command = SshSshConsole
		self.command = SshRconsConsole

		self.racks = []
		# the list machines with unknown positions
		self.unknowns = []
		self._getRacks()

	def close(self):
		for rack in self.racks:
			rack.close()

	def maxRackIndex(self):
		max = 0
		for rack in self.racks:
			max = rack.realindex > max and rack.realindex or max
		return max

	def _getRack(self, index):
		rack = None
		for r in self.racks:
			if r.index == index:
				rack = r
				break

		if not rack:
			rack = Rack(index=index)
			self.racks.append(rack)

		return rack

	def _getRacks(self):
		command = ['%s/bin/nodels' % self.xcat_location, 'all', 'pos']

		if self.remote_address:
			command = ['ssh', self.remote_address] + command

		lines = run_command(command)

		for line in lines:
			log.debug('line: %s' % line)
			m = known_pos_re.match(line)
			if m:
				node, room, rack, unit = m.groups()
				rack, unit = map(int, (rack, unit))
				log.info('node: %s, room: %s, rack: %d, unit: %d' % (node, room, rack, unit))

				rack = self._getRack(rack)

				conf = deepcopy(get_config())
				conf['node'] = node

				command = self.command(conf, multiprocess=True)
				machine = Machine(name=node, status='Unknown', command=command, rackindex=unit)
				rack.addMachine(machine)

			else:
				m = unknown_pos_re.match(line)
				if m:
					node = m.groups()
					log.info('node: %s, location unknown' % node)

					conf = deepcopy(get_config())
					conf['node'] = node

					command = self.command(conf, multiprocess=True)
					machine = Machine(name=node, status='Unknown', command=command)

					self.unknowns.append(machine)
				else:
					log.warn("got a line we don't know how to deal with!")
					log.warn(line)


	def active(self):
		active = 0
		for rack in self.racks:
			active += rack.active()

		log.debug('%s: %d active' % (self.name, active))
		return active



