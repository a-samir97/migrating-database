FROM python:3.8-alpine
WORKDIR /code
RUN apk add --no-cache gcc musl-dev linux-headers mariadb-dev build-base python3-dev gcc
ENV FLASK_APP app.py
ENV FLASK_RUN_HOST 0.0.0.0
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 5000
COPY . .
CMD ["flask", "run"]
