FROM python

RUN pip install \
    flask \
    psycopg2 \
	flask_api

COPY lab1/ /app/

WORKDIR /app

CMD [ "python3", "/app/main.py" ]