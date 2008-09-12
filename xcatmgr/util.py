import sys, re
import logging as log
import Tkinter as tk

known_pos_re = re.compile(r"^([^:]+):\s+Room:\s+([^,]+),\s+Rack:\s+([^,]+),\s+Unit:\s+(.*)$")
unknown_pos_re = re.compile(r"^([^:]+):\s+NO POSITION DEFINED!$")
status_re = re.compile(r"^([^:]+):\s+(.*)$")

EXPAND = tk.N + tk.S + tk.E + tk.W

log.basicConfig(level=log.DEBUG,
	format='%(asctime)s %(levelname)-8s %(message)s',
)


def run_command(command):
	version = sys.version.split()[0].split(".")

	if map(int, version) >= [2, 4]:
		from subprocess import Popen, PIPE
		if type(command) == type(""):
			stdout = Popen([command], stdout=PIPE).communicate()[0]
			return [l.strip() for l in stdout.splitlines()]
		else:
			stdout = Popen(command, stdout=PIPE).communicate()[0]
			return [l.strip() for l in stdout.splitlines()]

	else:
		if type(command) == type(""):
			return [l.strip() for l in os.popen2(command)[1].readlines()]
		else:
			return [l.strip() for l in os.popen2(" ".join(command))[1].readlines()]



