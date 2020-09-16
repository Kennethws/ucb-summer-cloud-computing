setup:
	python3 -m venv virt

install:
	pip install --upgrade pip &&\
	pip install boto3 &&\
	pip install -r requirements.txt &&\
		pip freeze > requirements.txt
	


	