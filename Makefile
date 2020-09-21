setup:
	python3 -m venv ~/.virt

install:
	pip install --upgrade pip &&\
	pip install -r requirements.txt

lint:
	pylint --disable=R,C application.py

test:
	python -m pytest -vv test_application.py
	
all: setup install lint test


	