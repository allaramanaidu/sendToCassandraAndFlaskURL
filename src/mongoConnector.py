import pandas as pd
import pymongo
import json
import configparser
import os
import logger


loggerObject = logger.logger_class(__name__)

config = configparser.ConfigParser()
config.read('config.ini')
host = str(config['mongo']['host'])
port = int(config['mongo']['port'])

def to_mongo(dbname, filepath):
    try:
        loggerObject.logger.info("************ to_mongo starts")
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
    except Exception as e:
        loggerObject.logger.info(e, exc_info = True)

    loggerObject.logger.info("***************** to_mongo ends")

def from_mongo(dbName, collection):
    try:
        loggerObject.logger.info('******* from_mongo starts')
        global host, port
        mongoClient = pymongo.MongoClient(host, port)
        mng_db = mongoClient[dbName]
        db = mng_db[collection]
        df = pd.DataFrame(list(db.find({}, {'_id': False})))
        to_json(df)
        #to_csv(df)
    except Exception as e:
        loggerObject.logger.info(e, exc_info = True)
    loggerObject.logger.info('******* from_mongo ends')


def to_json(df):
    try:
        loggerObject.logger.info("******** to_json starts")
        jsondata = df.to_json('mongotable2.json', orient='records')
        print jsondata
    except Exception as e:
        loggerObject.logger.info(e, exc_info = True )
    loggerObject.logger.info("*********** to_json ends")

def to_csv(df):
    try:
        loggerObject.logger.info('********** to_csv starts')
        df.to_csv('mongotable2.csv')
    except Exception as e:
            loggerObject.logger.info(e, exc_info = True)
    loggerObject.logger.info('********* to_csv ends')


if __name__ == "__main__":
  filepath = 'sample.csv'
  #to_mongo('tvsnext', filepath)
  from_mongo('tvsnext', 't3')
