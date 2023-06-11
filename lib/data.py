
import requests
import re
from bs4 import BeautifulSoup
import tushare as ts
ts.set_token('099d503dd05ac189ba998bf3404df708bdb38d73171b9b32ec70db26')
pro=ts.pro_api()
df=pro.query('income', ts_code='600519.SH',fields='revenue,n_income_attr_p,basic_eps,oper_exp')#shouru:income jingshouru:n_income_attr_p meigushouyi:basic_eps
df.to_csv('./data/imcome_needed.csv')
df3=pro.query('income', ts_code='600519.SH')
df3.to_csv('./data/imcome.csv')
df2=pro.query('bak_basic', ts_code='600519.SH',fields='npr')#jinglirunlv:npr 
df2.to_csv('./data/basic.csv')
df4=pro.query('fina_indicator', ts_code='600519.SH')
df4.to_csv('./data/fina_indicator.csv')




df5=pro.query('balancesheet', ts_code='600519.SH') #fuzhaiconge:total_liab
df5.to_csv('./data/balancesheet.csv')
df6=pro.query('cashflow', ts_code='600519.SH')#xianjinjingbiandong: n_incr_cash_cash_equ
df6.to_csv('./data/cashflow.csv')
df7=pro.query('express', ts_code='600519.SH')#zongzichan total_assets
df7.to_csv('./data/express.csv')
