from flask import request
import flask
from flask_api import status
import psycopg2
import os
import json

DB_NAME = 'ddn1snn0gj8q6a'
DB_HOST = 'ec2-54-76-105-132.eu-west-1.compute.amazonaws.com'
LOGIN = 'ueujuyabujdjip'
PASSWORD = '2ed54beeb0d872556ee17f6088a1729424a44a892ecee12d1c01203e6efb5b86'
    

def persons_to_json(persons):
    listp = []
    for i in persons:
        dictionary = {'id':i[0], 'name':i[1], 'age':i[2], 'address':i[3], 'work':i[4]}
        listp.append(dictionary)
    return json.dumps(listp)

def person_to_json(person):
    dictionary = {'id':person[0], 'name':person[1], 'age':person[2], 'address':person[3], 'work':person[4]}
    return json.dumps(dictionary)

class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.app = flask.Flask(__name__)
        
        self.app.add_url_rule('/api/v1/persons', view_func = self.get_all_persons)
        self.app.add_url_rule('/api/v1/persons', view_func = self.add_new_persons, methods = ['POST'])
        self.app.add_url_rule('/api/v1/persons/<id>', view_func = self.get_person_by_id)
        self.app.add_url_rule('/api/v1/persons/<id>', view_func = self.delete_person_by_id, methods = ['DELETE'])
        self.app.add_url_rule('/api/v1/persons/<id>', view_func = self.patch_person_by_id, methods = ['PATCH'])

        self.connection = psycopg2.connect(dbname = DB_NAME, user = LOGIN, password = PASSWORD, host = DB_HOST)

    def run_server(self):
        return self.app.run(host = self.host, port = self.port)

    def get_all_persons(self):
        cursor = self.connection.cursor()
        cursor.execute('select * from persons')
        func_record = cursor.fetchall()
        cursor.close()

        response = flask.Response(persons_to_json(func_record))
        response.headers['Content-Type'] = 'application/json'
        return response

    def add_new_persons(self):
        request_body = dict(request.json)
        cursor = self.connection.cursor()
        try:
            name = request_body['name']
            age = request_body['age']
            address = request_body['address']
            work = request_body['work']
            cursor.execute('insert into persons (name, age, address, work) values (%s, %s, %s, %s) returning id',
                               (name, age, address, work))
            id = cursor.fetchall()[0][0]
        except:
            cursor.close()
            self.connection.rollback()
            return 'Invalid data', 400
        cursor.close()
        self.connection.commit()

        response = flask.Response('', status.HTTP_201_CREATED)
        response.headers['Location'] = f'/api/v1/persons/{id}'
        return response

    
    def get_person_by_id(self, id):
        
        cursor = self.connection.cursor()
        cursor.execute('select id, name, age, address, work from persons where id = %s', (id,))
        func_record = cursor.fetchall()
        cursor.close()
        if func_record == []:
            return flask.Response(json.dumps({'msg': f'There is no person with id {id}'}), status.HTTP_404_NOT_FOUND,)
        response = flask.Response(person_to_json(func_record[0]), status.HTTP_200_OK)
        response.headers['Content-Type'] = 'application/json'
        return response

    def delete_person_by_id(self, id):

        cursor = self.connection.cursor()
        cursor.execute('delete from persons where id = %s;', (id,))
        cursor.close()
        self.connection.commit()
        return 'Person for ID was removed', 204

    def patch_person_by_id(self, id):

        request_body = dict(request.json)
        cursor = self.connection.cursor()
        cursor.execute('select id, name, age, address, work from persons where id = %s', (id,))
        func_record = cursor.fetchall()
        if func_record == []:
            return flask.Response(json.dumps({'msg': f'There is no person with id {id}'}), status.HTTP_404_NOT_FOUND,)
        if 'name' in request_body:
            name = request_body['name']
        else:
            name = func_record[0][1]
        if 'age' in request_body:
            age = request_body['age']
        else:
            age = func_record[0][2]
        if 'address' in request_body:
            address = request_body['address']
        else:
            address = func_record[0][3]
        if 'work' in request_body:
            work = request_body['work']
        else:
            work = func_record[0][4]
        try:
            cursor.execute('update persons set name = %s, age = %s, address = %s, work = %s WHERE id = %s;',
                               (name, age, address, work, id))
        except:
            self.connection.rollback()
            cursor.close()
            return flask.Response(json.dumps({'msg': 'string', 'errors': {'param1': 'param2'}}), status.HTTP_400_BAD_REQUEST)
        cursor.execute('select id, name, age, address, work from persons where id = %s', (id,))
        func_record = cursor.fetchall()
        cursor.close()
        self.connection.commit()
        response = flask.Response(person_to_json(func_record[0]), status.HTTP_200_OK)
        response.headers['Content-Type'] = 'application/json'
        return response





server_host = '0.0.0.0'
server_port = os.environ.get('PORT', 8080)

server = Server(host=server_host, port=server_port)
server.run_server()
