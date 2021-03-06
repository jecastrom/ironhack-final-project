import pandas as pd
import requests


# URL of our endpoint
URL = "https://2krjwwbp8d.execute-api.us-east-1.amazonaws.com/prod/hello"


# read the testfile
df = pd.read_csv('data/data_7000.csv', sep=',')
# Cleaning data dropping any row with any null value
df.dropna(axis=0, how='any', inplace=True)
data = df.copy()
# write a single row from the testfile into the api
#export = data.loc[2].to_json()
#response = requests.post(URL, data = export)
# print(response)
# write all the rows from the testfile to the api as put request
for i in data.index:
    try:
        # convert the row to json
        export = data.loc[i].to_json()

        # send it to the api
        response = requests.post(URL, data=export)

        # print the returncode
        print(export)
        print(response)
    except:
        print(data.loc[i])
