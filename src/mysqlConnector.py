import pandas as pd
from pandas import read_csv
from sqlalchemy import create_engine
import sys
import configparser
import logger


loggerObject = logger.logger_class(__name__)

config = configparser.ConfigParser()
config.read('config.ini')
username = str(config["mysql"]["username"])
password = str(config["mysql"]["password"])
host = str(config.read["mysql"]["host"])
port = int(config.read["mysql"]["port"]))

engine = create_engine("mysql://" + username + ":" + password + "@" + host)
def to_mysql(filename, db_name):
    """
    :param filename:
    :param db_name:
    :return:
    """
    try:
        loggerObject.logger.info("******** to_mysql starts")
        global engine
        tableName = filename[:-4]
        engine.execute("CREATE DATABASE IF NOT EXISTS "+ db_name)  # create db
        engine.execute("USE "+db_name)
        data = read_csv(filename)
        data.to_sql(tableName, engine, if_exists='append')
    except Exception as e:
        loggerObject.logger.info(e, exc_info = True)
    loggerObject.logger.info("********** to_mysql ends")

def from_mysql(db_name):
    """
    :param db_name:
    :return:
    """
    try:
        loggerObject.logger.info("*************** from_mysql starts")
        global engine
        engine.execute('USE '+ db_name)
        tables = engine.execute('SHOW TABLES')
        available_tables = tables.fetchall()
        for i in range(len(available_tables)):
           to_Json(available_tables[i][0], 'select * from ' + available_tables[i][0])
           #to_Csv(available_tables[i][0], 'select * from ' + available_tables[i][0])
    except Exception as e:
        loggerObject.logger.info(e, exc_info = True)
    loggerObject.logger.info("************* from_mysql ends")

def to_Json(filename, query):
    """
    :param filename:
    :param query:
    :return:
    """
    try:
        loggerObject.logger.info("********* to_Json starts")
        global engine
        df = pd.read_sql(query, con=engine)
        #df.to_json(orient='records')[1:-1].replace('},{', '} {')
        df.to_json(filename+'.json', orient='records')
    except Exception as e:
        loggerObject.logger.info(e, exc_info  = True)
    loggerObject.logger.info("******** to_Json ends")

def to_Csv(filename, query):
    """
    :param filename:
    :param query:
    :return:
    """
    try:
        loggerObject.logger.info("********* to_Csv starts")
        df = pd.read_sql(query, con=engine)
        df.to_csv(filename+'.csv', header= False)
        #with open(db_name+'.csv', 'a') as f:
        #    df.to_csv(f, header=False)
    except Exception as e:
        loggerObject.logger.info(e, exc_info  = True)
    loggerObject.logger.info("********* to_Csv ends")


if __name__=='__main__':
    dbname = sys.argv[1:]
    dbname = str(dbname[0])
    #to_mysql('t1.csv', 'flask')
    from_mysql(dbname)
