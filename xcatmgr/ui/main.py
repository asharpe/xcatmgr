import Tkinter as tk
import Tix as tx
from xcatmgr.util import EXPAND


config = {
	'xterm' : '/usr/X11R6/bin/xterm',
	'mgmt' : 'mgmt',
	'pre-delay' : 1,
	'post-delay' : 2,
	'domain-name' : 'hpc.jcu.edu.au',
	'cluster-domain-name' : 'cluster',
}



from xcatmgr.util import log
from xcatmgr.model.machine import Machine, MgmtNode
from xcatmgr.model.command import Command, SshRconsConsole, SshSshConsole
from xcatmgr.ui.machine import MachineUI
from xcatmgr.ui.rack import RackUI




class Application(tk.Frame):
	def __init__(self, master=None):
		tk.Frame.__init__(self, master, borderwidth=5)
		self.grid(sticky=EXPAND)

		top = self.winfo_toplevel()
		top.rowconfigure(0, weight=1)
		top.columnconfigure(0, weight=1)

		self.rowconfigure(1, weight=1)
		self.columnconfigure(0, weight=1)

		self.clusters = []
		self.createClusters()

	def active(self):
		active = 0
		for cluster in self.clusters:
			active += cluster.active()

		return active

	def close(self):
		for cluster in self.clusters:
			cluster.close()

	def createClusters(self):
		mgmt = MgmtNode('xcat', status='OK')		
		self.clusters.append(mgmt)

		self._createCluster(mgmt)

	def _createCluster(self, mgmt):
		log.debug('mgmt: %s' % mgmt)

		# find which rack has the most machines to set others to the same height
		max_machines = 0
		for rack in mgmt.racks:
			max_machines = rack.maxMachineIndex() > max_machines and rack.maxMachineIndex() or max_machines

		for rack in mgmt.racks:
			rUi = RackUI(self, rack=rack, size=max_machines)
			rUi.grid(row=1, column=rack.realindex, sticky=EXPAND)

		# make the racks share the width equally
		racks = self.grid_size()[0]
		log.debug('we have %d racks' % racks)
		for index in range(0, racks):
			self.columnconfigure(index, weight=1)

		# create command listbox
		commands = {}
		for command in (SshSshConsole, SshRconsConsole):
			commands[command.DISPLAY] = command

		var = tk.StringVar(self)
		var.set(mgmt.command.DISPLAY)
		commandL = tk.OptionMenu(self, var, *commands.keys())
		commandL.grid(row=0, column=0, columnspan=racks)

		tmp = var.set
		def myset(text):
			log.debug('setting text to %s' % text)
			log.debug('using command: %s' % commands[text])
			mgmt.command = commands[text]
			tmp(text)
		var.set = myset
		
#		commandL = tx.ComboBox(self, selectmode=tk.SINGLE, height=1)
#		commandL.insert(tk.END, 'SSH Rcons')
#		commandL.insert(tk.END, 'SSH SSH')
##		commandL.insert(tk.END, 'Rcons')
##		commandL.insert(tk.END, 'SSH')
#		commandL.grid(row=0, column=0, columnspan=racks)

#		commandL = tk.Listbox(self, selectmode=tk.SINGLE, height=1)
#		commandL.insert(tk.END, 'SSH Rcons')
#		commandL.insert(tk.END, 'SSH SSH')
##		commandL.insert(tk.END, 'Rcons')
##		commandL.insert(tk.END, 'SSH')
#		commandL.grid(row=0, column=0, columnspan=racks)



#class ClusterUI(tk.Frame):
#	def __init__(self, master=None):
#		tk.Frame.__init__(self, master)
#		self.rowconfigure(0, weight=1)
#		self.columnconfigure(0, weight=1)
#		self.grid(sticky=EXPAND)


#		nodeName = 'xcat'
#		hostName = 'xCAT'
#		conf = deepcopy(config)
#		conf['prettyName'] = 'xCAT'
##		conf['host'] = 'xcat'
#		conf['host'] = 'mpinode07'
#
#
#		command = x2200_rcons(conf)
##		command = ssh_console(conf)
#
#		xcat = Machine(name=conf['prettyName'], status='OK', command=command)
#		xcat.status = "broken"
#		xcatUi = MachineUI(self, machine=xcat)
#		xcatUi.grid()
##		xcatUi.updateStatus()


