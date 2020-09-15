setup:
	python3 -m venv virt

install:
	pip install --upgrade pip &&\
	pip install boto3 &&\
	pip freeze > requirements.txt &&\
	pip install -r requirements.txt


	