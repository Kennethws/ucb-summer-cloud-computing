setup:
	python3 -m venv ~/.virt

install:
	pip install --upgrade pip &&\
	pip install boto3 &&\
	pip install Flask &&\
	pip3 install awsebcli &&\
	pip install pandas &&\
	pip install matplotlib &&\
	pip install tensorflow==1.14 &&\
	pip install keras==2.2.5 &&\
	pip install opencv &&\
	pip install -r requirements.txt &&\
	pip freeze > requirements.txt


	
