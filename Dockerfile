FROM python

RUN pip install \
    flask \
    psycopg2

COPY lab1/ /app/

WORKDIR /app

CMD [ "python3", "/app/main.py" ]