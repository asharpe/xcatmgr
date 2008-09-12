import Tkinter as tk
from xcatmgr.ui.machine import MachineUI
from xcatmgr.util import EXPAND, log

class RackUI(tk.Frame):
	def __init__(self, master=None, rack=None, size=0):
		tk.Frame.__init__(self, master, relief=tk.RIDGE, borderwidth=5)
		self.columnconfigure(0, weight=1)

		self.size = size
		self.rack = rack
		self.__createWidgets()

	def __createWidgets(self):
		label = tk.Label(self, text='Rack %d' % self.rack.index)
		label.grid(row=0, column=0, sticky=tk.N+tk.E+tk.W)

		done = []
		for machine in self.rack.machines:
			mUi = MachineUI(self, machine)
			mUi.grid(row=machine.rackindex, column=0, sticky=EXPAND)
			done.append(machine.rackindex)

		for index in range(1, self.size + 1):
			if index not in done:
				mUi = MachineUI(self, disabled=True)
				mUi.grid(row=index, column=0, sticky=EXPAND)
			self.rowconfigure(index, weight=1)
			


