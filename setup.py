from setuptools import setup, find_packages

setup(
	name='xcatmgr',
	version='0.1',
	description='xCAT management UI',
	author='Andrew Sharpe',
	author_email='hpc@jcu.edu.au',
	url='http://www.hpc.jcu.edu.au/',
	packages=find_packages(),
	scripts=['xCATmgr.py'],
	long_description="""\
	xcatmgr is a utility to help manage clusters managed by xCAT (http://xcat.sourceforge.net).	It is a simple Tkinter application that uses xcat commands (not tab files) to display a representation of an xCAT managed cluster and allows you to perform simple operations on nodes
	""",
	classifiers=[
		"License :: OSI Approved :: GNU General Public License (GPL)",
		"Programming Language :: Python",
		"Development Status :: 4 - Beta",
		"Intended Audience :: Administrators",
		"Topic :: Internet",
	],
	keywords='xcat networking cluster hpc',
	license='GPL',
	install_requires=[
		'setuptools',
	],
)

