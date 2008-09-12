# this is unix only
from os import kill
from signal import SIGTERM, SIGKILL, SIG_DFL
from subprocess import Popen, PIPE
from copy import deepcopy

from xcatmgr.util import log

class Command:
	DISPLAY='Noop'

	def __init__(self, exe="/bin/true", args=list(), multiprocess=False):
		self.exe = exe
		self.args = args
		self.process = None
		self.processes = []
		self.multiprocess = multiprocess

	def str(self):
		return self.DISPLAY

#	str = property(lambda self: self.DISPLAY)
#	repr = property(lambda self: self.DISPLAY)

	def _kill(self, process):
		kill(process.pid, SIGTERM)
		# this is to reap zombies
		process.wait()

	def active(self):
		active = 0
		if self.multiprocess:
			for process in self.processes:
				try:
					if process.poll() is None:
						active += 1
				except:
					pass
		else:
			if self.process:
				if self.process.poll() is None:
					active += 1

		return active

	running = property(lambda self:self.active() > 0)

	def stop(self):
		if self.multiprocess:
			for process in self.processes:
				self._kill(process)
		else:
			if self.process:
				self._kill(self.process)

	def run(self):
		if not self.multiprocess:
			self.stop()
			self.process = None

		cmd = [self.exe] + self.args
		log.info("running %s" % cmd)
		self.process = Popen(cmd, stdin=PIPE, stdout=PIPE, close_fds=True)

		if self.multiprocess:
			self.processes.append(self.process)


class SshRconsConsole(Command):
	# for some really gay reason, the first argument to the ssh command
	# needs to be quoted!!!
	# the /bin/bash --login -i' is to load the keys for rcons command
	command = 'ssh -t %(mgmt)s.%(mgmt-domain-name)s "echo pausing for %(command-pre-delay)s seconds; sleep %(command-pre-delay)s; screen -xRR -S ssh_rcons_%(node)s /bin/bash --login -i -c \'/opt/xcat/bin/rcons %(node)s\'; echo pausing for %(command-post-delay)s seconds; sleep %(command-post-delay)s"'

	DISPLAY="SSH Rcons"

	def __init__(self, conf, multiprocess=False):
		# the '/bin/bash --login -i' is to load the keys for ssh command
		Command.__init__(self, exe='%(term)s' % conf,
			args=[
				'%(term-command-opt)s' % conf,
				'/bin/bash', '--login', '-i', '-c',
				SshRconsConsole.command % conf
			],
			multiprocess=multiprocess
		)


class SshSshConsole(Command):
	command = 'ssh -t %(mgmt)s.%(mgmt-domain-name)s "echo pausing for %(command-pre-delay)s seconds; sleep %(command-pre-delay)s; screen -xRR -S ssh_ssh_%(node)s /bin/bash --login -i -c \'ssh %(node)s.%(cluster-domain-name)s\'; echo pausing for %(command-post-delay)s seconds; sleep %(command-post-delay)s"'
#	command = 'echo "pausing for %(command-pre-delay)d seconds"; sleep %(command-pre-delay)d; ssh %(node)s.%(domain-name)s; echo "pausing for %(command-post-delay)d seconds"; sleep %(command-post-delay)d'

	DISPLAY="SSH SSH"

	def __init__(self, conf, multiprocess=False):
		Command.__init__(self, exe='%(term)s' % conf,
			args=[
				'%(term-command-opt)s' % conf,
				'/bin/bash', '--login', '-i', '-c',
				SshSshConsole.command % conf
			],
			multiprocess=multiprocess
		)

