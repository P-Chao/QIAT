#coding=utf-8
import tushare as ts
import pandas as pd
import numpy as np
import math

def singleton(cls):
    def wrapper(code_list, starttime, endtime):
        if cls._instance is None:
            cls._instance = cls(code_list, starttime, endtime)
        return cls._instance
    return wrapper

@singleton
#DataRepository = singleton(DataRepository)
class DataRepository(object):
    _instance = None
    def __init__(self, code_list, starttime, endtime):
        self.all_data = {}
        for code in code_list:
            df = ts.get_k_data(code, starttime, endtime)
            df['ma5'] = df['close'].rolling(5).mean()
            df['ma10'] = df['close'].rolling(10).mean()
            df = df.dropna(how='any')
            self.all_data[code] = df

    def get_onecode_df(selfself, code):
        return self.all_data[code]


