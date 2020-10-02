setup:
	python3 -m venv ~/.virt

install:
	yum install mesa-libGL.x86_64
	pip install --upgrade pip &&\
	pip install boto3 &&\
	pip install keras &&\
	pip install tensorflow &&\
	pip install Flask &&\
	pip install opencv-python &&\
	pip install -r requirements.txt &&\
	pip freeze > requirements.txt
