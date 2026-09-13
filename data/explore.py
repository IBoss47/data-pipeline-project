import pandas as pd 

df = pd.read_csv('/Users/iboss/workspace/de-platform-streamify/data/page_view_events.csv', escapechar='\\')
print(df.isna().sum())
print(df.info())
print(df.duplicated().sum())