#! /usr/bin/env python3
# -*- coding: utf-8 -*-
from flask import Flask, Response, request
from cassandra.cluster import Cluster
import ast

cluster = Cluster(['10.91.17.54'])
session = cluster.connect()

app = Flask(__name__)

row = 1
@app.route('/', methods=['POST'])
def get_data():
    global session, row
    dict = ast.literal_eval(request.data)
    print(dict)
    keyspace = dict['keyspace']
    tablename = dict['tablename']
    header = []
    values = []

    if row == 1:
        session.execute("CREATE KEYSPACE IF NOT EXISTS "+keyspace+" WITH REPLICATION = {'class': 'SimpleStrategy', 'replication_factor': '3'}")
        session.set_keyspace(keyspace)

        for k, v in dict['record'].iteritems():
            header.append(k)
        for i in range(0, len(header)):
            if i == 0:
                #session.execute("""CREATE TABLE IF NOT EXISTS tvs(""" +header[i] +""" text,PRIMARY KEY (""" +header[0] +"""))""")
                session.execute("""CREATE TABLE IF NOT EXISTS """+tablename+"""(""" + header[i] + """ text,PRIMARY KEY ("""+header[i]+"""))""")
            else:
                session.execute("""ALTER TABLE """+tablename+""" ADD """+ header[i] +""" text""")
        print("****************Table created successfully!!!! with row:", row)

    row = row + 1
    for k, v in dict['record'].iteritems():
        if row > 2:
            header.append(k)
        values.append(str(v))
    print("values:", values)

    query = """INSERT INTO """+tablename+"""("""

    for i in range(0, len(header)):
        query += header[i] + ""","""
    query = query[:-1]
    query += """)""" + """ VALUES"""

    for r in range(len(values)):
        if (r != 0):
            qu = ''
            t = tuple(values)
            #print (t)
            qu = query
            qu += str(t)
            #print (qu)
            session.execute(qu)
            print("*******************Data inserted!!!!!!!!!!!!!!!")
    return Response('We recieved something…')

if __name__ == '__main__':
    app.run('0.0.0.0', 5000, debug=True)
