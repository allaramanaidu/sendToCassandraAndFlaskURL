import pandas as pd
import os
import sys
import requests
import json

url = 'http://127.0.0.1:5000/'
headers = {'content-Type': 'application/json'}

keyspace , tablename = sys.argv[1:]
dict = {'keyspace': keyspace, 'tablename': tablename}
basePath = os.path.dirname(os.path.abspath(__file__))
df = pd.read_json('f3.json', orient='records')

for index, row in df.iterrows():
    print("===================")
    dict['record'] = row.to_dict()
    # for k in dict['record'].keys():
    #     k1 = str(k)
    #     if k1 == 'index':
    #         del(dict['record']['index'])
    #print(dict)
    json_data = json.dumps(dict)
    print(json_data)
    server_return = requests.post(url, headers=headers, data=json_data)
    print("==================================")

print(server_return.status_code)