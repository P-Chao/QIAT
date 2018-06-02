#coding=utf-8
#from trade import Trade
from demo.dm_data import DataRepository
import tushare as ts
import pandas as pd
import numpy as np
import math

class Strategy(object):
    def __init__(self, code_list, init_cash, start_time, end_time):
        self.start_time = start_time
        self.end_time = end_time
        self.data_repository = DataRepository(code_list , self.start_time, self.end_time)
        #self.data_repository = DataRepository.get_instance(code_list, \
        #                                                   self.start_time, \
        #                                                   self.end_time)
        self.code_list = code_list
        self.benchmark_code = 'sh'

        self.cash = init_cash
        self.limited_cash = init_cash/len(code_list)
        self.position_list = {}
        for code in self.code_list:
            self.position_list[code] = 0

        self.trade = 0

        d = list(pd.period_range(start=start_time, end = end_time, freq='B'))
        self.date_range = list(map(str,d))
        self.res_df = pd.DataFrame()
        self.res_df['date'] = self.date_range
        self.capital_market_value = []

    def run_simulation(self):
        for date in self.date_range:
            for code in self.code_list:
                sell_signal, sell_open_price = self.get_sell_signal(code, date)
                direction = -1
                if sell_signal == 1:
                    amount = self.get_sell_amount(code)
                    if amount > 0:
                        commission = self.cal_cost_function(sell_open_price, amount)
                        #update cash
                        self.cash += sell_open_price*amount
                        self.cash -= commission
                        #update hold
                        self.position_list[code] -= amount
                        #add trade log
                        self.trade = 0

            for code in self.code_list:
                buy_signal, buy_open_price = self.get_buy_signal(code,date)
                direction = 1
                if buy_signal == 1:
                    amount = self.get_buy_amount(code, buy_open_price)
                    if amount > 0:
                        commission = self.cal_cost_function(buy_open_price, amount)
                        #update cash
                        self.cash -= buy_open_price*amount
                        self.cash -= commission
                        #update hold
                        self.position_list[code] += amount
                        #add trade
                        self.trade = 0

            self.capital_market_value.append(self.get_market_value(date))

        # dates goes by
        self.res_df['capital_market_value'] = pd.Series(self.capital_market_value)
        self.res_df['profolio_daily_return'] = round((self.res_df['capital_market_value']/\
                                        self.res_df['capital_market_value'].shift(1)-1),4)
        self.res_df['benchmark'] = self.get_benchmark_index()
        self.res_df['benchmark'].fillna(method='bfill', inplace=True)
        self.res_df['benchmark'].fillna(method='ffill', inplace=True)
        self.res_df.to_csv('./datares.csv')

    def get_benchmark_index(self):
        df = ts.get_k_data(self.benchmark_code, start=self.start_time, end=self.end_time)
        benchmark_list = []
        for date in self.date_range:
            if df[df['date'] == date].empty:
                benchmark_list.append(np.nan)
            else:
                benchmark_list.append(float(df[df['date']==date]['close']))
        return benchmark_list

    def get_market_value(self, date):
        market_value = 0
        for code in self.position_list:
            df = self.data_repository.get_onecode_df(code)
            if self.position_list[code] != 0:
                close_price = df[df['date'] <= date].tail(1)['close']
                market_value += self.position_list[code]*float(close_price)
        return round(market_value+self.cash, 2)

    def get_sell_signal(self, code, date):
        df = self.data_repository.get_onecode_df(code)
        sell_signal = 0
        sell_open_price = 0


        if df[df['date'] == date].empty:
            return sell_signal, sell_open_price
        df = df[df['date'] <= date].tail(3)
        if len(df) == 3 and df.iloc[0]['ma5'] > df.iloc[0]['ma10'] and df.iloc[1]['ma5'] < df.iloc[1]['ma10']:
            sell_signal = 1
            sell_open_price = df.iloc[1]['open']
        return sell_signal, sell_open_price


        #以后还要加入判断止盈的方法


    def get_buy_signal(self, code, date):
        df = self.data_repository.get_onecode_df(code)
        buy_signal = 0
        buy_open_price = 0
        if df[df['date'] == date].empty:
            return buy_signal, buy_open_price
        df = df[df['date'] <= date].tail(3)
        if len(df) == 3 and df.iloc[0]['ma5'] < df.iloc[0]['ma10'] and df.iloc[1]['ma5'] > df.iloc[1]['ma10']:
            buy_signal = 1
            buy_open_price = df.iloc[1]['open']
        return buy_signal, buy_open_price

    def get_sell_amount(self, code):
        return self.position_list[code]


    def get_buy_amount(self, code, price):
        if self.position_list[code] == 0:
            amount = math.floor(self.limited_cash/(price*100))*100
            return amount
        else:
            return 0

    def cal_cost_function(self, price, amount):
        commission = price*amount*0.0003
        #最低5元手续费
        if commission > 5:
            return commission
        else:
            return 5


