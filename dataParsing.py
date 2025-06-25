import json
import pandas as pd

with open('data/playlist.json') as f:
    data = json.load(f)

df = pd.DataFrame(data)
# print(df.head(10))
df.to_csv('data/playlist.csv', index=False)