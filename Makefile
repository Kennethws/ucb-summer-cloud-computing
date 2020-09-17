setup:
	python3 -m venv .virt

install:
	pip install --upgrade pip &&\
	pip install boto3 &&\
<<<<<<< HEAD
	pip install Flask &&\
	pip freeze > requirements.txt &&\
	pip install -r requirements.txt
=======
	pip install -r requirements.txt &&\
		pip freeze > requirements.txt
	
>>>>>>> firstdemo


	