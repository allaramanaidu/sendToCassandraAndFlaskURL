import pandas as pd
from flask import Flask, request
from cassandra.cluster import Cluster
import json

cluster = Cluster(['10.91.17.54'])
session = cluster.connect()

app = Flask(__name__)

@app.route("/")
def getAllDbs():
    keyspace = cluster.metadata.keyspaces
    keyspaces = []
    for key in keyspace.keys():
        key = str(key)
        keyspaces.append(key)
    return json.dumps({'Available keyspaces': keyspaces, 'URL for getting tables in keyspace': 'https:/localhost:7000/keyspacename'})

@app.route("/<keyspace>")
def getTableNames(keyspace):
    table = cluster.metadata.keyspaces[keyspace].tables
    tables = []
    for key in table.keys():
        key = str(key)
        tables.append(key)
    return json.dumps({'Available tables': tables, 'URL for getting collections in db': 'https:/localhost:7000/keysapce/table name'})

@app.route("/<keyspace>/<tablename>")
def getDataFromTable(keyspace, tablename):
    query = "SELECT * FROM "+keyspace+"."+tablename
    df = pd.DataFrame(list(session.execute(query)))
    tableVal = df.to_json(orient='records')
    return tableVal

if __name__ == '__main__':
    app.run('0.0.0.0', 5000, debug=True)
    # app.run(debug=True)