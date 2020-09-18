setup:
	python3 -m venv ~/.virt

install:
	pip install --upgrade pip &&\
	pip install boto3 &&\
	pip install Flask &&\
	pip3 install awsebcli &&\
	pip install -r requirements.txt &&\
	pip freeze > requirements.txt


	