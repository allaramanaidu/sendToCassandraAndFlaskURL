import pandas as pd
from pandas import read_csv
from sqlalchemy import create_engine
import sys

credentials = {"username": "root", "password": "tvs#123$", "host": "localhost", "port": 3306}
engine = create_engine("mysql://" + credentials["username"] + ":" + credentials["password"] + "@" + credentials["host"])

def to_mysql(filename, db_name):
    global credentials, engine
    tableName = filename[:-4]
    engine.execute("CREATE DATABASE IF NOT EXISTS "+ db_name)  # create db
    engine.execute("USE "+db_name)
    data = read_csv(filename)
    data.to_sql(tableName, engine, if_exists='append')

def from_mysql_to_csv(db_name):
    global engine
    engine.execute('USE '+ db_name)
    tables = engine.execute('SHOW TABLES')
    available_tables = tables.fetchall()
    for i in range(len(available_tables)):
       to_Json(available_tables[i][0], 'select * from ' + available_tables[i][0])
       #to_Csv(available_tables[i][0], 'select * from ' + available_tables[i][0])

def to_Json(filename, query):
    global credentials, engine, dataframe
    df = pd.read_sql(query, con=engine)
    #df.to_json(orient='records')[1:-1].replace('},{', '} {')
    df.to_json(filename+'.json', orient='records')



def to_Csv(filename, query):
    global credentials, engine
    df = pd.read_sql(query, con=engine)
    df.to_csv(filename+'.csv', header= False)
    #with open(db_name+'.csv', 'a') as f:
    #    df.to_csv(f, header=False)


if __name__=='__main__':
    dbname = sys.argv[1:]
    dbname = str(dbname[0])
    #to_mysql('SampleCSVFile_119kb.csv', 'flask')
    from_mysql_to_csv(dbname) ## schema name == 'testDb'
