setup:
	python3 -m venv ~/.virt

install:
	sudo yum install mesa-libGL.x86_64
	pip install --upgrade pip &&\
	pip install boto3 &&\
	pip install Flask &&\
	pip install -r requirements.txt &&\
	pip freeze > requirements.txt
