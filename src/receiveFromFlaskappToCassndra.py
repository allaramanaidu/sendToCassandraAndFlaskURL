#! /usr/bin/env python3
# -*- coding: utf-8 -*-
from flask import Flask, Response, request
from cassandra.cluster import Cluster
import ast

cluster = Cluster(['10.91.17.54'])
session = cluster.connect()

header = []
values = []
previousTable = ''

app = Flask(__name__)
@app.route('/',  methods=['POST'])
def get_data():
    global session, previousTable, header, values
    dict = ast.literal_eval(request.data)
    for k in dict['record'].keys():
        k1 = str(k)
        if k1 == 'index':
            del(dict['record']['index'])
    print(dict)
    keyspace = dict['keyspace']
    tablename = dict['tablename']
    values = []

    if (tablename != previousTable):
        header = []
        previousTable = tablename
        session.execute("CREATE KEYSPACE IF NOT EXISTS "+keyspace+" WITH REPLICATION = {'class': 'SimpleStrategy', 'replication_factor': '3'}")
        session.set_keyspace(keyspace)

        for columnName, val in dict['record'].iteritems():
            header.append(columnName)

        for columName in range(0, len(header)):
            if columName == 0:
                #session.execute("""CREATE TABLE IF NOT EXISTS tvs(""" +header[i] +""" text,PRIMARY KEY (""" +header[0] +"""))""")
                session.execute("""CREATE TABLE IF NOT EXISTS """+tablename+"""(""" + header[columName] + """ text,PRIMARY KEY ("""+header[columName]+"""))""")
            else:
                session.execute("""ALTER TABLE """+tablename+""" ADD """+ header[columName] +""" text""")
        print("****************Table created successfully!!!!")

    for columnName, val in dict['record'].iteritems():
        values.append(str(val))


    query = """INSERT INTO """+tablename+"""("""

    for i in range(0, len(header)):
        query += header[i] + ""","""
    query = query[:-1]
    query += """)""" + """ VALUES"""

    for row in range(len(values)):
        if (row != 0):
            insertQuery = ''
            data = tuple(values)
            insertQuery = query
            insertQuery += str(data)
            session.execute(insertQuery)
    print("*******************Data inserted")
    return Response('We recieved something…')

if __name__ == '__main__':
    app.run('0.0.0.0', 5000, debug=True)
