FROM python:3.6
RUN apt-get update
#RUN apt-get install -y python3-pip nginx
RUN apt-get install -y openssh-server curl wget nginx
RUN pip3 install pipenv
COPY . /app
WORKDIR /app
#RUN export LC_ALL=C.UTF-8 & export LANG=C.UTF-8
RUN pipenv install
EXPOSE 8000 
CMD pipenv run flask run --host=0.0.0.0 --port=8000
