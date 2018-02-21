import pandas as pd
from cassandra.cluster import Cluster



cluster = Cluster(['10.91.17.54'])
session = cluster.connect('testdb')


query = "SELECT * FROM testtable3"
df = pd.DataFrame(list(session.execute(query)))
print(df)


from flask_jsonpify import jsonpify
df_list = df.values.tolist()
JSONP_data = jsonpify(df_list)
return JSONP_data


# keyspace = cluster.metadata.keyspaces['testdb'].tables
# keyspaces =[]
# for key in keyspace.keys():
#         key = str(key)
#         keyspaces.append(key)
#
# print(keyspaces)
