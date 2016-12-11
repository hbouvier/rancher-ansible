all: dependencies

pip:
	which pip >/dev/null || (easy_install pip && pip install --upgrade pip)

setuptools:
	pip install setuptools
	pip install --upgrade setuptools --user python

request:
	pip install request

dependencies: pip setuptools request
	pip install -r requirements.txt


