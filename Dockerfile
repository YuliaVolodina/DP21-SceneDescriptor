FROM python:3.6
RUN apt-get update
RUN apt-get install -y openssh-server curl wget nginx python3-pymysql
RUN pip3 install pipenv
COPY . /app
WORKDIR /app
RUN pipenv install
EXPOSE 8000
ENV FLASK_APP /app/autoapp.py
CMD pipenv run flask run --host=0.0.0.0 --port=8000
