#libraries
import openpyxl
import numpy as np
from pandas import read_excel
import pandas as pd
import pymc3 as pm
import arviz as az

#xlsx reader
def Exlreader(name):
    np.set_printoptions(suppress=True)
    data = read_excel(name)
    data = pd.DataFrame.to_numpy(data)
    return data

#Reading the chart
file_name = 'stdnew.xlsx'
data = Exlreader(file_name)

#Experienment set
n = []
sfy = []
nmax = []
for i in range(len(data)):
    n.append(data[i][0])
    sfy.append(data[i][1])
    nmax.append(data[i][2])

#Estimation Model    
model =  pm.Model()

#MCMC
with model as bm:

    A1 = pm.Normal('A1', mu=0, sd=10)
    A2 = pm.Normal('A2', mu=0, sd=10)
    A3 = pm.Normal('A3', mu=0, sd=10)
    er = pm.HalfNormal('er', sd=1)

    est = A1 + A2*(np.log10(sfy))+A3*(np.log10(nmax))
     
    result = pm.Normal('result', mu=est, sd=er, observed=np.log10(n))
    
summ = pm.sample(draws=200000,model=bm,cores=1)
pm.traceplot(summ)
print(pm.summary(summ).round(3))
