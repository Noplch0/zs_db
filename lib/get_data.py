import pandas as pd
import tushare as ts
import json

with open("config.json", "r",encoding='utf-8') as f:
    config = json.load(f)
ts_token = config['ts_token']
pro = ts.pro_api(ts_token)


def transdf(df):
    df_t = pd.DataFrame(df.values.T, columns=df.index, index=df.colums)
    return df_t


def get_data(code, interface, name):
    print(name)
    df = pro.query(interface, exchange='', ts_code=code, fields=name)
    return df

