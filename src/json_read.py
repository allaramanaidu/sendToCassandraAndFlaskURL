import pandas as pd

# json_read
df = pd.read_json('t1.json', orient='records')
print(df)

