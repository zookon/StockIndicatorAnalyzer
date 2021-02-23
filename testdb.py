import sqlite3
import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine
import common

def testAllStock():
    sql_cmd = "SELECT * FROM allstock"
    cx = sqlite3.connect(common.db_path_sqlite3)
    result = pd.read_sql(sql=sql_cmd, con=cx)
    print(result)
    print(result.shape[0])

def testStockStatus():
    ticker = 'sh.600614'
    sql_cmd = "SELECT * FROM allstock where code='" + ticker + "'"
    cx = sqlite3.connect(common.db_path_sqlite3)
    result = pd.read_sql(sql=sql_cmd, con=cx)
    print(result)
    print(result.shape[0])

def testStockAdjust():
    ticker = 'sh.603986'
    sql_cmd = "SELECT * FROM stock_adjustfactor where code='" + ticker + "'"
    cx = sqlite3.connect(common.db_path_sqlite3)
    result = pd.read_sql(sql=sql_cmd, con=cx)
    print(result)
    print(result.shape[0])

def testDayK():
    #sql_cmd = "SELECT * FROM stock_day_k"
    sql_cmd = "SELECT * FROM stock_day_k where code='sh.600000' order by date desc limit 0,10"
    #sql_cmd = "SELECT * FROM stock_day_k where date='2020-03-05'"
    #sql_cmd = "SELECT * FROM stock_day_k where code='sh.000001' and date>'2019-01-01'"
    begin = datetime.now()
    cx = create_engine(common.db_path_sqlalchemy)
    begin2 = datetime.now()
    elapse = begin2 - begin
    print(elapse)
    result = pd.read_sql(sql=sql_cmd, con=cx)
    elapse = datetime.now() - begin2
    print(elapse)
    print(result)

def testDayKNoAdjust():
    #sql_cmd = "SELECT * FROM stock_day_k"
    sql_cmd = "SELECT * FROM stock_day_k_noadjust where code='sh.600000' order by date desc limit 0,10"
    #sql_cmd = "SELECT * FROM stock_day_k where date='2020-03-05'"
    #sql_cmd = "SELECT * FROM stock_day_k where code='sh.000001' and date>'2019-01-01'"
    begin = datetime.now()
    cx = create_engine(common.db_path_sqlalchemy)
    begin2 = datetime.now()
    elapse = begin2 - begin
    print(elapse)
    result = pd.read_sql(sql=sql_cmd, con=cx)
    elapse = datetime.now() - begin2
    print(elapse)
    print(result)

def testOneStock():
    ticker = 'sh.688126'
    cx = create_engine(common.db_path_sqlalchemy)
    sql_cmd = "SELECT count(*) FROM stock_day_k where code='" + ticker + "'"
    cursor = cx.execute(sql_cmd)
    result = cursor.fetchone()
    dayk_count = 365
    if result[0] < 365:
        dayk_count = result[0]
    sql_cmd = "SELECT * FROM stock_day_k where code='" + ticker +"' order by date desc limit 0," + str(dayk_count)
    print(sql_cmd)
    begin = datetime.now()
    begin2 = datetime.now()
    elapse = begin2 - begin
    print(elapse)
    result = pd.read_sql(sql=sql_cmd, con=cx)
    elapse = datetime.now() - begin2
    print(elapse)
    print(result)

def testStockSpec():
    cx = create_engine(common.db_path_sqlalchemy)
    #sql_cmd = "SELECT * FROM stock_spec where code='sh.688358'"
    sql_cmd = "SELECT * FROM stock_spec where date=(select max(date) from stock_spec) and amplitude_10 > '0' order by amplitude_10 asc limit 0,50"
    #sql_cmd = "SELECT * FROM stock_spec where date=(select max(date) from stock_spec) order by amplitude_10 asc limit 0,50"
    
    result = pd.read_sql(sql=sql_cmd, con=cx)
    print(result)

def testDate():
    cx = create_engine(common.db_path_sqlalchemy)
    sql_cmd = "select max(date) from stock_spec"
    cursor = cx.execute(sql_cmd)
    result = cursor.fetchone()
    print(result[0])

def testSearchTime():
    begin = datetime.now()
    ticker = 'sh.688126'
    cx = create_engine(common.db_path_sqlalchemy)
    sql_cmd = "SELECT count(*) FROM stock_day_k where code='" + ticker + "'"
    cursor = cx.execute(sql_cmd)
    result = cursor.fetchone()
    # dayk_count = 365
    # if result[0] < 365:
    #     dayk_count = result[0]

    elapse = datetime.now() - begin
    print(result[0], elapse)

def testStockhs300Spec():
    cx = create_engine(common.db_path_sqlalchemy)
    #sql_cmd = "SELECT * FROM stock_spec where code='sh.688358'"
    sql_cmd = "SELECT * FROM stock_hs300_spec where date=(select max(date) from stock_hs300_spec) order by trendgap_y desc limit 0,50"
    #sql_cmd = "SELECT * FROM stock_spec where date=(select max(date) from stock_spec) order by amplitude_10 asc limit 0,50"
    
    result = pd.read_sql(sql=sql_cmd, con=cx)
    print(result)

def testStockQualification():
    cx = create_engine(common.db_path_sqlalchemy)
    #sql_cmd = "SELECT * FROM stock_spec where code='sh.688358'"
    sql_cmd = "SELECT * FROM stock_qualification where code = 'sh.600000' and date=(select max(date) from stock_qualification)"
    #sql_cmd = "SELECT * FROM stock_spec where date=(select max(date) from stock_spec) order by amplitude_10 asc limit 0,50"
    
    result = pd.read_sql(sql=sql_cmd, con=cx)
    print(result)

def testStockQualification2():
    cx = create_engine(common.db_path_sqlalchemy)
    sql_cmd = "SELECT * FROM stock_qualification where ma5_5 = '2' and date=(select max(date) from stock_qualification) and (code like 'sh.6%' or code like 'sz.00%' or code like 'sz.300%')"
    #sql_cmd = "SELECT * FROM stock_spec where date=(select max(date) from stock_spec) order by amplitude_10 asc limit 0,50"
    
    result = pd.read_sql(sql=sql_cmd, con=cx)
    print(result)

def testDayK22():
    ticker = 'sh.000001'
    sql_cmd = "SELECT * FROM stock_day_k where code='" + ticker + "'"
    #sql_cmd = "SELECT * FROM stock_day_k where code='sh.000001' order by date asc limit 0,10"
    cx = create_engine(common.db_path_sqlalchemy)
    result = pd.read_sql(sql=sql_cmd, con=cx)
    print(result)
    #print(result.values.tolist())

def testFactor():
    current_date = "2020-07-22"
    sql_cmd = "SELECT * FROM stock_adjustfactor where date>='" + current_date + "'"
    db = create_engine(common.db_path_sqlalchemy)
    factor = pd.read_sql(sql=sql_cmd, con=db)
    print(factor)
    for i in range(factor.shape[0]):
        ticker = factor.loc[i, 'code']
        print(ticker)
        sql_cmd = "SELECT * FROM stock_day_k_noadjust where code='" + ticker+"' order by date desc limit 0,300"
        daily = pd.read_sql(sql=sql_cmd, con=db)
        print(daily.head(50))
        sql_cmd = "SELECT * FROM stock_adjustfactor where code='" + ticker + "' order by date desc"
        adjustfactor = pd.read_sql(sql=sql_cmd, con=db)
        print(adjustfactor)
        common.calculateDayKWithAdjustFactor(daily, adjustfactor)
        print(daily.head(50))
        break

import baostock as bs
def testGetFactor():
    bs.login()
    data_list=[]
    k_rs = bs.query_adjust_factor(code="sh.600161", start_date="2010-01-01", end_date="")
    while (k_rs.error_code == '0') & k_rs.next():
        data_list.append(k_rs.get_row_data())
    print(data_list)
    bs.logout()

testAllStock()
#testStockStatus()
testDayK()
#testDayKNoAdjust()
#testStockAdjust()
#testOneStock()
#testStockSpec()
#testDate()
#testSearchTime()
#testStockhs300Spec()
#testStockQualification()
testStockQualification2()
#testFactor()
#testGetFactor()