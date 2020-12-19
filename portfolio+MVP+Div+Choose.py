import pandas_datareader as pd
import pandas
import numpy as np
import datetime as dt

stocks = ['ATL.MI','ENI.MI', 'STM.MI','SRG.MI','IP.MI','FBK.MI']
amnt = [1000,50,300,5,100,150]

'''
i=True
stocks=[]
amnt=[]
while i==True:
    inpt=input("Insert Stock Code (UPPER CASE): ")
    if len(inpt)>=1:
        stocks.append(str(inpt))
    else:
        i=False        
    inp=input("Insert quantities: ")
    if len(inp)>=1:
        amnt.append(int(inp))
    else:
        i=False
'''

kinp=input("Choose Target Expected Return: ")
if len(kinp)<1:
    k=0.0036
        
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

 
mu=[]
for i in averg_rtr:
    mu.append(i[1])
mut=np.transpose(mu)
e=[]
for j in range(len(stocks)):
    e.append(1)
et=np.transpose(e)
Vinv=np.linalg.inv(Covar)
a=np.dot(np.dot(mut,Vinv),mu)
b=np.dot(np.dot(et,Vinv),mu)
c=np.dot(np.dot(et, Vinv), e)

l1=(k*c-b)/(a*c-b**2)
l2=(a-b*k)/(a*c-b**2)

x1=np.dot(np.dot(l1,Vinv), mu)
x2=np.dot(np.dot(l2, Vinv), e)
x=x1+x2
xt=np.transpose(x)
xret=np.dot(mut, xt)
xvar=np.dot(np.dot(x,Covar), xt)**0.5


H=0
for n in weight:
    H=H+n**2
oon=1/(int(len(stocks)))
Hmod=(H-oon)/(1-oon)

ewp=[]
for l in range(len(stocks)):
    ewp.append(float(oon))
ewreturn=np.dot(mut, ewp)
ewpt=np.transpose(ewp)
ewstd=(np.dot(np.dot(ewpt, Covar), ewp))**0.5 

ewpH=0
for o in ewp: 
    ewpH=ewpH+o**2
Hmodewp=(ewpH-oon)/(1-oon)
    


print("Stock monthly return average: ",averg_rtr)
print("Covariance matrix of the stock return: ")
print(Covar)
print("Chosen weight: "+ str(weight))
print("Expected portfolio return: ",round(portfolio_return,4)*100,'%')
print("Portfolio's standard deviation: ",round(st,4)*100,'%')
print("")
print("")
print("Minimum Variance Portfolio, given target expected return: ", k)
print("Composition: ", x)
print("Expected Return: ",round(xret,5)*100, " %")
print("Standard Deviation: ", round(xvar,5)*100, " %")
print("")
print("")
print("Diversification Analysis")
print("   Modified Herfindal Index: ", Hmod)
print("   Equally Weighted Portfolio:")
print("    - Composition", ewpt)
print("    - Average Return: ", round(ewreturn,4)*100, " %")
print("    - Standard Deviation: ", round(ewstd,4)*100, " %")
