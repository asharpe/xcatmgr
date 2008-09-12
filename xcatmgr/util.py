import sys, re, os.path
import logging as log
import Tkinter as tk
from ConfigParser import ConfigParser

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


def get_config():
	CONFIG_PATH = os.path.expanduser('~/.xcatmgr.ini')

# this is for using the variable %(HOME)s inside the config
#	c = ConfigParser({ 'HOME' : os.path.expanduser('~') })
	c = ConfigParser()

	f = file(CONFIG_PATH, 'r')
	c.readfp(f)
	f.close()

	if not c.has_section('config'):
		raise IOError('[config] section not found in configuration file (%s)' % CONFIG_PATH)
#		raise IOError('configuration file not found (%s)' % CONFIG_PATH)

	return dict(c.items('config'))

	
