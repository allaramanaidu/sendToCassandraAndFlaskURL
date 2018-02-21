import pandas as pd
import os
import sys

keyspace , tablename = sys.argv[1:]
dict = {'keyspace':keyspace, 'tablename':tablename}
basePath = os.path.dirname(os.path.abspath(__file__))
df = pd.read_json('t1.json', orient='records')

for index, row in df.iterrows():
    print ("===================")
    dict['record'] = row.to_dict()
    del(dict['record']['index'])
    print (dict)
    print ("===================")
