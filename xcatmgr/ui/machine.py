import Tkinter as tk
from xcatmgr.model.machine import Machine

class MachineUI(tk.Button):
	def __init__(self, master=None, machine=Machine(), disabled=False):
		tk.Button.__init__(self, master, text='%s:%s' % (machine.name, machine.status), command=self.action)
		if disabled:
			self.config(state=tk.DISABLED)
		self.machine = machine

	def updateStatus(self):
		name = "%s:%s" % (self.machine.name, self.machine.status)
		self.config(text=name)
		
	def action(self):
		self.machine.command.run()

