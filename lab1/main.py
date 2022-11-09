from flask import Flask, request
import psycopg2
import os

DB_NAME = 'ddn1snn0gj8q6a'
DB_HOST = 'ec2-54-76-105-132.eu-west-1.compute.amazonaws.com'
LOGIN = 'ueujuyabujdjip'
PASSWORD = '2ed54beeb0d872556ee17f6088a1729424a44a892ecee12d1c01203e6efb5b86'

class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.app = Flask(__name__)
        
##        self.app.add_url_rule('/', view_func = self.get_home)
        self.app.add_url_rule('/api/v1/persons', view_func = self.get_all_persons)
        self.app.add_url_rule('/api/v1/persons', view_func = self.add_new_persons, methods = ['POST'])
        self.app.add_url_rule('/api/v1/persons/<id>', view_func = self.get_person_by_id)
        self.app.add_url_rule('/api/v1/persons/<id>', view_func = self.delete_person_by_id, methods = ['DELETE'])
        self.app.add_url_rule('/api/v1/persons/<id>', view_func = self.patch_person_by_id, methods = ['PATCH'])

    def run_server(self):
        return self.app.run(host = self.host, port = self.port)

##    def get_home(self):
##        return 'Home page'

    def get_all_persons(self):
        connection = psycopg2.connect(dbname = DB_NAME, user = LOGIN, password = PASSWORD, host = DB_HOST)
        cursor = connection.cursor()
        cursor.execute('select * from persons')
        func_record = cursor.fetchall()
        cursor.close()
        return func_record

    def add_new_persons(self):
        request_body = dict(request.json)
        name = request_body['name']
        age = request_body['age']
        address = request_body['address']
        work = request_body['work']
        return f'Success added {name}', 200
    
    def get_person_by_id(self, id):
        return 'get ' + id

    def delete_person_by_id(self, id):
        return 'delete ' + id

    def patch_person_by_id(self, id):
        return 'patch ' + id





server_host = '0.0.0.0'
server_port = os.environ.get('PORT', 8080)

server = Server(host=server_host, port=server_port)
server.run_server()
