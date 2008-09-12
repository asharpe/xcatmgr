all: bdist_egg

PROJECT = xcatmgr

bdist_egg: clean
	python setup.py bdist_egg

test: clean bdist_egg
	virtualenv $(PROJECT)-test
	cd $(PROJECT)-test; \
		. bin/activate; \
		easy_install ../dist/xcatmgr-0.1.dev-py2.5.egg; \
		xCATmgr.py; \
		deactivate
	rm -rf $(PROJECT)-test


clean:
	rm -rf build dist $(PROJECT).egg-info
