FROM python:3.8
WORKDIR /code
RUN apt-get update && apt-get -y install python3-dev libssl-dev
ENV FLASK_APP app.py
ENV FLASK_RUN_HOST 0.0.0.0
COPY requirements.txt requirements.txt
COPY /mariadb/db/*.sql /docker-entrypoint-initdb.d/
RUN pip install -r requirements.txt
EXPOSE 5000
COPY . .
CMD ["flask", "run"]
