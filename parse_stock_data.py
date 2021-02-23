import baostock as bs
import pandas as pd
from sqlalchemy import create_engine
import common

def refresh_all_stock(current_date = "2020-03-27"):
    db_conn = create_engine(common.db_path_sqlalchemy)
    bs.login()
    rs = bs.query_all_stock(day=current_date)

    data_list = []
    while (rs.error_code == '0') & rs.next():
        data_list.append(rs.get_row_data())
    db_conn.execute(r'''
    INSERT OR REPLACE INTO allstock VALUES (?, ?, ?)
    ''', data_list)

    bs.logout()

def refresh_all_stock_adjust(start_date="2020-03-27",current_date = "2020-03-30"):
    bs.login()

    db_conn = create_engine(common.db_path_sqlalchemy)
    stock_rs = bs.query_all_stock(day=current_date)
    stock_df = stock_rs.get_data()
    rs_list = []
    for code in stock_df["code"]:
        if code.startswith("sh.6") | code.startswith("sz.00") | code.startswith("sz.300"):
            print('query_stock_factor code:'+code)
            rs_factor = bs.query_adjust_factor(code=code, start_date=start_date, end_date=current_date)
            while (rs_factor.error_code == '0') & rs_factor.next():
                rs_list.append(rs_factor.get_row_data())
    factor_list = []
    for d in rs_list:
        code = d[0]
        print("refresh all factor for " + code)
        rs_factor = bs.query_adjust_factor(code=code, start_date='2006-01-01', end_date=current_date)
        while (rs_factor.error_code == '0') & rs_factor.next():
                factor_list.append(rs_factor.get_row_data())
    if len(factor_list) > 0:
        db_conn.execute(r'''
                INSERT OR REPLACE INTO stock_adjustfactor VALUES (?, ?, ?, ?, ?)
                ''', factor_list)
    bs.logout()

def refresh_stock_day_k(code="sh.000001",start_date="2020-03-27",current_date = "2020-03-30"):
    bs.login()

    data_list = []
    k_rs = bs.query_history_k_data_plus(code,
        "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,peTTM,pbMRQ,psTTM,pcfNcfTTM,isST",
        start_date=start_date, end_date='', 
        frequency="d", adjustflag="3")
    while (k_rs.error_code == '0') & k_rs.next():
        data_list.append(k_rs.get_row_data())
    print('query_history_k_data_plus code:'+code)
    print(len(data_list))
    bs.logout()
    db_conn = create_engine(common.db_path_sqlalchemy)

    db_conn.execute(r'''
    INSERT OR REPLACE INTO stock_day_k VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    ''', data_list)

def refresh_all_stock_day_k_noadjust(start_date="2020-03-27",current_date = "2020-03-30"):
    bs.login()

    stock_rs = bs.query_all_stock(day=current_date)
    stock_df = stock_rs.get_data()
    data_list = []
    for code in stock_df["code"]:
        k_rs = bs.query_history_k_data_plus(code,
            "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,peTTM,pbMRQ,psTTM,pcfNcfTTM,isST",
            start_date=start_date, end_date='', 
            frequency="d", adjustflag="3")
        while (k_rs.error_code == '0') & k_rs.next():
            data_list.append(k_rs.get_row_data())
        print('query_history_k_data_plus no adjust code:'+code)
    bs.logout()
    db_conn = create_engine(common.db_path_sqlalchemy)

    db_conn.execute(r'''
    INSERT OR REPLACE INTO stock_day_k_noadjust VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    ''', data_list)

def refresh_all_stock_day_k(start_date="2020-03-27",current_date = "2020-03-30"):
    bs.login()

    stock_rs = bs.query_all_stock(day=current_date)
    stock_df = stock_rs.get_data()
    data_list = []
    for code in stock_df["code"]:
        k_rs = bs.query_history_k_data_plus(code,
            "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,peTTM,pbMRQ,psTTM,pcfNcfTTM,isST",
            start_date=start_date, end_date='', 
            frequency="d", adjustflag="2")
        while (k_rs.error_code == '0') & k_rs.next():
            data_list.append(k_rs.get_row_data())
        print('query_history_k_data_fore code:'+code)
    bs.logout()
    db_conn = create_engine(common.db_path_sqlalchemy)

    db_conn.execute(r'''
    INSERT OR REPLACE INTO stock_day_k VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    ''', data_list)

    sql_cmd = "SELECT * FROM stock_adjustfactor where date>='" + start_date + "'"
    factor = pd.read_sql(sql=sql_cmd, con=db_conn)
    for i in range(factor.shape[0]):
        ticker = factor.loc[i, 'code']
        print("adjust the dayK fore" + ticker)
        sql_cmd = "SELECT * FROM stock_day_k_noadjust where code='" + ticker+"' order by date desc limit 0,300"
        daily = pd.read_sql(sql=sql_cmd, con=db_conn)
        sql_cmd = "SELECT * FROM stock_adjustfactor where code='" + ticker + "' order by date desc"
        adjustfactor = pd.read_sql(sql=sql_cmd, con=db_conn)
        common.calculateDayKWithAdjustFactor(daily, adjustfactor)
        data = daily.values.tolist()
        sql_cmd = "DELETE from stock_day_k where code='" + ticker + "'"
        db_conn.execute(sql_cmd)
        db_conn.execute(r'''
            INSERT OR REPLACE INTO stock_day_k VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            ''', data)

def refresh_all_stock_day_k_no_adjust_first_time(start_date="2020-03-27", end_date="2020-05-08", current_date = "2020-05-08"):
    bs.login()

    stock_rs = bs.query_all_stock(day=current_date)
    stock_df = stock_rs.get_data()
    db_conn = create_engine(common.db_path_sqlalchemy)
    data_list = []
    number = 0
    for code in stock_df["code"]:
        k_rs = bs.query_history_k_data_plus(code,
            "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,peTTM,pbMRQ,psTTM,pcfNcfTTM,isST",
            start_date=start_date, end_date=end_date, 
            frequency="d", adjustflag="3")
        while (k_rs.error_code == '0') & k_rs.next():
            data_list.append(k_rs.get_row_data())
        print('query_history_k_data_plus code:'+code)
        number += 1
        if number == 50:
            if len(data_list) > 0: 
                db_conn.execute(r'''
                    INSERT OR REPLACE INTO stock_day_k_noadjust VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                    ''', data_list)
            data_list = []
            number = 0
    
    if number != 50:
        if len(data_list) > 0: 
            db_conn.execute(r'''
                    INSERT OR REPLACE INTO stock_day_k_noadjust VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                    ''', data_list)
        data_list = []
        number = 0

    bs.logout()
    
def refresh_all_stock_day_k_first_time(start_date="2020-03-27", end_date="2020-05-08", current_date = "2020-05-08"):
    bs.login()

    stock_rs = bs.query_all_stock(day=current_date)
    stock_df = stock_rs.get_data()
    db = create_engine(common.db_path_sqlalchemy)
    number = 0
    data_list = []
    for ticker in stock_df["code"]:
        print("adjust " + ticker)
        sql_cmd = "SELECT * FROM stock_day_k_noadjust where code='" + ticker+"' order by date desc limit 0,300"
        daily = pd.read_sql(sql=sql_cmd, con=db)
        if ticker.startswith("sh.6") | ticker.startswith("sz.00") | ticker.startswith("sz.300"):
            sql_cmd = "SELECT * FROM stock_adjustfactor where code='" + ticker + "' order by date desc"
            factor = pd.read_sql(sql=sql_cmd, con=db)
            common.calculateDayKWithAdjustFactor(daily, factor)
        
        data = daily.values.tolist()
        for d in data:
            data_list.append(d)
        number += 1
        if number == 100:
            if len(data_list) > 0: 
                db.execute(r'''
                        INSERT OR REPLACE INTO stock_day_k VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                        ''', data_list)
            data_list = []
            number = 0
    
    if number != 100:
        if len(data_list) > 0: 
            db.execute(r'''
                    INSERT OR REPLACE INTO stock_day_k VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                    ''', data_list)
        data_list = []
        number = 0
        

    bs.logout()
    

if __name__=='__main__':
    #refresh_all_stock("2020-04-20")
    #refresh_stock_day_k("sh.000001", "2020-04-20", "2020-04-27")
    #refresh_all_stock_day_k()
    refresh_all_stock_day_k_first_time("2015-01-01", "2010-01-01")