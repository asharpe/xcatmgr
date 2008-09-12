#!/usr/bin/env python

from xcatmgr.ui.main import Application
import Tkinter as tk
import tkMessageBox

def ask_quit():
	active = app.active()
	if active > 0:
		if tkMessageBox.askokcancel('Quit', "You have %d commands running,\nare you sure you want to quit?" % active):
			app.close()
			master.destroy()
	else:
		master.destroy()

if __name__ == '__main__':
	master = tk.Tk()
	master.protocol('WM_DELETE_WINDOW', ask_quit)

	app = Application(master)
	app.master.title("HPC Cluster")
	app.mainloop()


