import os
import pandas as pd
import numpy as np
import optionpricing as op
from WindPy import *
w.start()

def get_windcode(id):
    if  id[0] == 'I':
        code = id+'.CFE' #future
    elif id in ['510050','510510','510360','510300']:
        code = id+'.SH'  #ETF
    elif len(id) == 8:
        code = id+'.SH'  #option
    elif id[0] == '6':
        code = id+'.SH'       #stock
    else:
        code = id+'.SZ'
    return code


def get_Greeks(ETF50_close, Greek, windcode, position, close, date):
    # _,ETF50 = w.wsd("510050.SH", "close", Date, Date, "",usedf=True)
    # _,ETF50 = w.wss("510050.SH", "close","tradeDate="+Date+";priceAdj=U;cycle=D",usedf=True)
    # ETF50_close = ETF50['CLOSE'][0]
    if Greek == 'delta':
        if len(windcode) == 11:
            _, Data = w.wss(windcode, "delta", "tradeDate=" + Date, usedf=True)
            Delta = Data['DELTA'][0] * ETF50_close * 10000 * 0.01 * position
        elif windcode[1] in ['H', 'F']:
            Delta = 300 * close * 0.01 * position
        elif windcode[1] == 'C':
            Delta = 200 * close * 0.01 * position
        else:
            Delta = close * 0.01 * position
        return (Delta)
    elif Greek == 'gamma':
        if len(windcode) == 11:
            _, Data = w.wss(windcode, "gamma", "tradeDate=" + Date, usedf=True)
            Gamma = Data['GAMMA'][0] * (ETF50_close * 0.01) ** 2 * 10000 * position
        else:
            Gamma = 0
        return (Gamma)
    elif Greek == 'vega':
        if len(windcode) == 11:
            _, Data = w.wss(windcode, "vega", "tradeDate=" + Date, usedf=True)
            Vega = Data['VEGA'][0] * 10000 * position
        else:
            Vega = 0
        return (Vega)
    elif Greek == 'theta':
        if len(windcode) == 11:
            _, Data = w.wss(windcode, "theta", "tradeDate=" + Date, usedf=True)
            Theta = Data['THETA'][0] * 10000 / 365 * position
        else:
            Theta = 0
        return (Theta)


def get_RiskView(df):
    df2 = df[['证券代码', '证券名称', '持仓量', '持仓方向', 'Strategy']]
    df2['position'] = df2.持仓方向.apply(lambda x: 1 if x == '多仓' else -1)
    df2['Position'] = df2['持仓量'] * df2['position']
    df2 = df2.drop(columns=['持仓量', '持仓方向', 'position'])
    # df3 = df2.groupby(['Strategy','证券名称','证券代码']).sum()
    df2['windcode'] = list(map(lambda x: get_windcode(x), df2['证券代码']))
    windcode_list = list(set(df2['windcode'].tolist()))
    _, Close = w.wss(windcode_list, "close", "tradeDate=" + Date + ";priceAdj=U;cycle=D", usedf=True)
    df2['close'] = list(map(lambda x: Close['CLOSE'][x], df2['windcode']))
    _, ETF50 = w.wss("510050.SH", "close", "tradeDate=" + Date + ";priceAdj=U;cycle=D", usedf=True)
    ETF50_close = ETF50['CLOSE'][0]
    df2['delta'] = list(
        map(lambda a, b, c,: get_Greeks(ETF50_close, 'delta', a, b, c, Date), df2['windcode'], df2['Position'],
            df2['close']))
    df2['gamma'] = list(
        map(lambda a, b, c,: get_Greeks(ETF50_close, 'gamma', a, b, c, Date), df2['windcode'], df2['Position'],
            df2['close']))
    df2['vega'] = list(
        map(lambda a, b, c,: get_Greeks(ETF50_close, 'vega', a, b, c, Date), df2['windcode'], df2['Position'],
            df2['close']))
    df2['theta'] = list(
        map(lambda a, b, c,: get_Greeks(ETF50_close, 'theta', a, b, c, Date), df2['windcode'], df2['Position'],
            df2['close']))

    df3 = df2[['Strategy', 'delta', 'gamma', 'vega', 'theta']]
    df3 = df3.groupby(['Strategy']).sum()

    return (df2, df3)



def get_impliedvolatility(windcode,Date):
    if len(windcode)==11:
        _, Data = w.wss(windcode, "us_impliedvol", "tradeDate=" + Date, usedf=True)
        iv = Data['us_impliedvol'][0]
    else:
        iv = 0
    return (iv)






#输入为get_RiskView中的第一个输出
def greeks_scenorio(df):
    pass





if __name__ == '__main__':
    os.chdir('D:\\TTpython\\Daily_Review\\Fdd_Review')
    Date = '2019-09-12'
    result = 'risk-'+Date+'.xlsx'
    path = 'D:\\TTpython\\Daily_Review\\Fdd_Review\\Fdd_Risk\\'
    #今收
    df_today = pd.read_excel(path+result,sheet_name='今收')
    df0_a, df0_b = get_RiskView(df_today)

    with pd.ExcelWriter("D:\\TTpython\\Daily_Review\\Fdd_Review\\金衍风险报告"+Date+".xlsx") as writer:
        df0_a.to_excel(writer, sheet_name='明细')
        df0_b.to_excel(writer,sheet_name = '汇总')