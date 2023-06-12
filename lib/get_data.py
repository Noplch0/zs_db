import pandas as pd
import requests
import re
from bs4 import BeautifulSoup
import tushare as ts

ts.set_token('099d503dd05ac189ba998bf3404df708bdb38d73171b9b32ec70db26')
pro = ts.pro_api()


def transdf(df):
    df_t = pd.DataFrame(df.values.T, columns=df.index, index=df.colums)
    return df_t


def get_balancesheet(code):
    df1 = pro.query('balancesheet', ts_code=code,
                    fields='ts_code,total_assets,total_cur_liab,total_ncl,fix_assets,total_share')
    df1.to_csv('./data/balancesheet/balancesheet.csv')
    df2 = pro.query('daily_basic', ts_code=code, fields='ts_code,pb')
    df2.to_csv('./data/balancesheet/daily_basic.csv')
    df = pd.concat([df1.iloc[0], df2.iloc[0]])

    return {'code': "'"+df.iloc[0]+"'", 'total_share': df.iloc[1], 'fix_assets': df.iloc[2], 'total_assets': df.iloc[3],
            'total_cur_liab': df.iloc[4],
            'total_ncl ': df.iloc[5], 'total_debt': df.iloc[4] + df.iloc[5], 'pb': df.iloc[7]}


def get_cashflow(code):
    df = pro.query('cashflow', ts_code=code,
                   fields='ts_code,n_cashflow_act,c_inf_fr_operate_a,n_cashflow_inv_act,n_cash_flows_fnc_act')
    df.to_csv('./data/cashflow/cashflow.csv')
    n_df = df.iloc[0]
    return {'code': "'"+n_df.iloc[0]+"'", 'c_inf_fr_operate_a': n_df.iloc[1], 'n_cashflow_act': n_df.iloc[2],
            'n_cashflow_inv_act ': n_df.iloc[3], 'n_cash_flows_fnc_act': n_df.iloc[4]}


def get_income_statement(code):
    df1 = pro.query('daily_basic', ts_code=code, fields='ts_code,total_mv,dv_ratio,')
    df2 = pro.query('income', ts_code=code, fields='total_profit,n_income,basic_eps')
    df = pd.concat([df1.iloc[0], df2.iloc[0]])
    return {'code': "'"+df.iloc[0]+"'", 'dv_ratio': df.iloc[1], 'total_mv ': df.iloc[2], 'basic_eps': df.iloc[3],
            'total_profit': df.iloc[4], 'n_income': df.iloc[5]}


def get_weel_line(code):
    df1 = pro.query('weekly', ts_code=code, fields='ts_code,close,open,high,low,pre_close,change')
    df = df1.iloc[0]
    return {'code': "'"+df.iloc[0]+"'", 'close': df.iloc[1], 'open': df.iloc[2], 'high': df.iloc[3], 'low': df.iloc[4],
            'pre_close': df.iloc[5], 'price_change': df.iloc[6]}

