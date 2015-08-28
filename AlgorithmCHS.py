# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import statsmodels.api as sm
import pandas as pd
import numpy as np
from scipy import ndimage
from statsmodels.iolib.table import SimpleTable
#from sklearn.metrics import r2_score
#import ml_metrics as metrics
import time
import csv
ewma = pd.stats.moments.ewma
plt.figure(1)

def read_csvfile(csvfile_name, index_col_name, close_name):
    moex_data = pd.read_csv(csvfile_name,';', index_col=index_col_name, parse_dates=index_col_name, dayfirst=True)  # массив цен в DataFrame
    dataset = moex_data[close_name] #  массив цен закрытия в формате Dataframe
    print type(dataset)
    plt.subplot(211)
    pd.Series.plot(dataset, title='moex_data', style='k--')
    return dataset

#--тест Дикки-Фулера--проверка на стационарность
def Dickey_Fuller(data_Series):
    test = sm.tsa.adfuller(data_Series)
    print 'adf: ', test[0]
    print 'p-value: ', test[1]
    print'Critical values: ', test[4]
    if test[0]> test[4]['5%']:
        print u'Есть единичные корни, ряд не стационарен'
    else:
        print u'Единичных корней нет, ряд стационарен'

#--тест Харки-Бера--определение нормальности распределения (p>0.05)
def Jarque_Bera(data_Series):
    row =  [u'JB', u'p-value', u'skew', u'kurtosis']
    jb_test = sm.stats.stattools.jarque_bera(data_Series)
    a = np.vstack([jb_test])
    itog = SimpleTable(a, row)
    print itog

#  Построение  экспоненциально взвешенной скользящей средней
def exponential_moving_average(data_Series, decay):
    SMA = ewma(data_Series, span = decay)
    SMA_Ser = pd.Series.from_array(SMA)
    #print 'SMA :', SMA
    #plt.subplot(111)
    #pd.Series.plot(SMA_Ser, title='EWMA')
    return SMA_Ser

dataset = read_csvfile('RTSI_100712_101224.csv', index_col_name='<DATE>', close_name='<CLOSE>')

stata = dataset.describe()     #  статистка по ряду
print 'Statistika: ', stata
#dataset.hist()                #  гистограмма
#print 'V = %f' % (stata['std']/stata['mean'])      #коэффициент вариации

decay = 5
#EWMA_Series = exponential_moving_average(dataset, decay)
period=10
SMA = pd.rolling_mean(dataset, window=period, min_periods=1)   # простая скользящая средняя за период
print 'SMA:', SMA
print type(SMA)
#plt.subplot(212)
pd.Series.plot(SMA, title='moex_data', style='k')
Jarque_Bera(SMA)

Dickey_Fuller(SMA)

dataset1diff = SMA.diff(periods=1).dropna()  #  порядок интегрированного ряда нашего ряда
#  print dataset1diff

Dickey_Fuller(dataset1diff)

# проверим мат.ожидание на разных интервалах
m = dataset1diff.index[len(dataset1diff.index)/2+1]
r1 = sm.stats.DescrStatsW(dataset1diff[m:])
r2 = sm.stats.DescrStatsW(dataset1diff[:m])
print 'p-value: ', sm.stats.CompareMeans(r1,r2).ttest_ind()[1]

plt.subplot(212)
pd.Series.plot(dataset1diff, title='Obrabotka')
plt.show()
