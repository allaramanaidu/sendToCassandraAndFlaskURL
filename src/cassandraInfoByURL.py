import pandas as pd
from flask import Flask, request
from cassandra.cluster import Cluster
import json

cluster = Cluster(['10.91.17.54'])
session = cluster.connect()

app = Flask(__name__)

@app.route("/")
def getAllDbs():
    """
    this function will listout the available keyspaces in  cassandra

    :param None: None
    :type None: None

    :rtype: json(all the keyspaces)

    """
    keyspace = cluster.metadata.keyspaces
    keyspaces = []
    for key in keyspace.keys():
        key = str(key)
        keyspaces.append(key)
    return json.dumps({'Available keyspaces': keyspaces, 'URL for getting tables in keyspace': 'https:/localhost:5000/keyspace name'})

@app.route("/<keyspace>")
def getTableNames(keyspace):
    """
    this function will listout the available keyspaces in  cassandra

    :param keyspace: keyspace name
    :type keyspace : str

    :rtype: json(All the tables in keyspace)

    """
    table = cluster.metadata.keyspaces[keyspace].tables
    tables = []
    for key in table.keys():
        key = str(key)
        tables.append(key)
    return json.dumps({'Available tables': tables, 'URL for getting data in table': 'https:/localhost:5000/keysapce name/table name'})

@app.route("/<keyspace>/<tablename>")
def getDataFromTable(keyspace, tablename):
    """
    this function will listout the available keyspaces in  cassandra

    :param keyspace: keyspace name
    :type keyspace : str
    :param tablename: table name
    :type tablename: str

    :rtype: json(All the rows in specified table)

    """
    query = "SELECT * FROM "+keyspace+"."+tablename
    df = pd.DataFrame(list(session.execute(query)))
    tableVal = df.to_json(orient='records')
    return tableVal

if __name__ == '__main__':
    app.run('0.0.0.0', 5000, debug=True)
    # app.run(debug=True)