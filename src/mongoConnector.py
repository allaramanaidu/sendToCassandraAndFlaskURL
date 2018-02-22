import pandas as pd
import pymongo
import json
import configparser
import os

config = configparser.ConfigParser()
config.read('config.ini')
host = str(config['mongo']['host'])
port = int(config['mongo']['port'])

def to_mongo(dbname, filepath):
    global host, port
    mongoClient = pymongo.MongoClient(host, port)
    mng_db = mongoClient[dbname]
    collection_name = filepath[:-4]
    db_cm = mng_db[collection_name]
    cdir = os.path.dirname(__file__)
    file_res = os.path.join(cdir, filepath)
    data = pd.read_csv(file_res)
    data_json = json.loads(data.to_json(orient='records'))
    db_cm.remove()
    db_cm.insert(data_json)

def from_mongo(dbName, collection):
    global host, port
    mongoClient = pymongo.MongoClient(host, port)
    mng_db = mongoClient[dbName]
    db = mng_db[collection]
    df = pd.DataFrame(list(db.find({}, {'_id': False})))
    to_json(df)
    #to_csv(df)


def to_json(df):
    jsondata = df.to_json('mongotable2.json', orient='records')
    print jsondata

def to_csv(df):
    df.to_csv('mongotable2.csv')


if __name__ == "__main__":
  filepath = 't3.csv'
  #to_mongo('tvsnext', filepath)
  from_mongo('tvsnext', 't3')
