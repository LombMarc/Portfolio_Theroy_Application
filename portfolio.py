import pandas_datareader as pd
import pandas
import numpy as np
import datetime as dt
import scipy as sp

stocks = ['ATL.MI','ENI.MI', 'STM.MI','SRG.MI','IP.MI','FBK.MI']
amnt = [100,100,100,100,100,150]
SUM =sum(amnt)
weight =[]
for w in amnt:
    weight.append((w/SUM))
weight=np.asarray(weight)

def Log_return(stk,Yframe):
    Edt = dt.date.today()
    Sdt = Edt - dt.timedelta(days=365 * Yframe)
    rtrn = []
    for x in stk:
        atl = pd.DataReader(x, data_source='yahoo', start=Sdt, end=Edt)
        Qrtrn = pandas.DataFrame()
        Qrtrn['r'] = atl['Close'].resample('M').ffill().pct_change()
        QRtrn = Qrtrn['r'].to_list()
        QRtrn.sort()
        del QRtrn[0:int(len(QRtrn) * 0.05)]
        del QRtrn[(len(QRtrn) - int(len(QRtrn) * 0.05)):-1]
        Average_return = np.average(QRtrn)
        rtrn.append(Average_return)
    return rtrn
Average_Q_Return = Log_return(stocks,5)

def Covariance(stk,Yframe):
    Stock_MTRX = pandas.DataFrame()
    Edt = dt.date.today()
    Sdt = Edt - dt.timedelta(days=365 * Yframe)
    for x in stk:
        filler = 0
        atl = pd.DataReader(x, data_source='yahoo', start=Sdt, end=Edt)
        Qrtrn = pandas.DataFrame()
        Qrtrn['r'] = atl['Close'].resample('M').ffill().pct_change()
        QRtrn = Qrtrn['r'].to_list()
        QRtrn.sort()
        del QRtrn[0:int(len(QRtrn) * 0.05)]
        del QRtrn[(len(QRtrn) - int(len(QRtrn) * 0.05)):-1]
        Stock_MTRX[x] = np.asarray(QRtrn)
    cova = Stock_MTRX.cov()
    return cova
Covar = Covariance(stocks,5)
st = np.dot(weight.T,np.dot(Covar,weight))**0.5

averg_rtr = []
for i in np.arange(0,len(stocks)):
    averg_rtr.append((stocks[i],Average_Q_Return[i]))

for i in np.arange(0,len(stocks)):
    portfolio_return = Average_Q_Return[i]*weight[i]

print("Stock monthly return average: ",averg_rtr)
print("Covariance matrix of the stock return: ")
print(Covar)
print("Chosen weight: "+ str(weight))
print("Expected portfolio return: ",round(portfolio_return,4)*100,'%')
print("Portfolio's standard deviation: ",round(st,4)*100,'%')
