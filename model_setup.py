#!/usr/bin/python
#  Description: MARCS SETUP MODULE: HYDROLOGY + PRECIPITATION
#  Experiment: SINGLE CATCHMENT
#  31.05.2018
#  Current Code Owner: Elena Shevnina, Finnish Meteorological Institute
#  ph. +358449185446
#  e-mail:eshevnina@gmail.com

import sys
import numpy as np
from scipy.stats import moment
import pandas as pd

# WORKING DIRECTORY
WD = './'

# Convert string argument to digit
def to_digit(x):
    try:
        if x.isdigit():
            return int(x)
        return float(x)
    except ValueError:
        return False


#Input file contains yearly time series of discharge and site's metedata
#fn = 'pvm_6730501.txt'
fn=str(sys.argv[1])

with open(fn, 'r') as f:
     arr = f.readlines()


# getting metadata
grdc = arr[8][25:-2]
area = float(arr[14][27:-2])
nlines = int(arr[24][24:-2]) + 48

# read discharge data
year = []
d = []
for i in range(48, nlines):
    data = arr[i].split(';')
    year.append(int(data[0]))
    d.append(float(data[3]))

q = []
ty = 365*24*60*60

for i in range (0, len(d)):
    if d[i] == -999.0: 
        q.append(np.nan)
    else:
        q.append((d[i]*ty)/(area*1000))


rr = pd.Series(q, index=year)


#to define the reference period with the "floating window" technique, n=15
#res_df=np.zeros(8,dtype=float)
#columns = ['year','spr','spr_pv','fsr','stt','stt_pv','kst','kst_pv']
#invar = rr
#for i in range (0,len(invar)-29):
#    index=invar.index[i+14]
#    spr=stats.spearmanr(invar.values[i:i+14],invar.values[i+15:i+29],nan_policy='omit') #test for the trends
#    fsr=np.nanvar(invar.values[i:i+14])/np.nanvar(invar.values[i+15:i+29]) #test for difference in variance
#    stt=stats.ttest_ind(invar.values[i:i+14],invar.values[i+15:i+29],nan_policy='omit') #test for difference in mean
#    kst=stats.ks_2samp(invar.values[i:i+14],invar.values[i+15:i+29])  #test for similarity
#    df=np.array([index,spr[0],spr[1],fsr,stt[0],stt[1],kst[0],kst[1]]) #result of calculation
#    res_df=np.vstack((res_df,df))


#non-central statistical moments for the reference period
y_beg = 1950
y_end = 1990

m1 = np.nanmean(rr.loc[y_beg:y_end].values)
m2 = moment(rr.loc[y_beg:y_end].values, moment=2, nan_policy='omit') + m1 * m1
m3 = moment(rr.loc[y_beg:y_end].values, moment=3,nan_policy='omit') + 3 * m2 * m1 - 2 * m1 * m1 * m1

#precipitation fro the reference period
filename = grdc +'_pre_obs.txt'
pre_otmp = []
with open(filename,'r') as f:
     pre_otmp = f.read().splitlines()

f.close()

t1=[]
t2=[]
t3=[]
t4=[]
for i in range (0, len(pre_otmp)):
    tmp = pre_otmp[i].split(' ')
    t1.append(float(tmp[1]))
    t2.append(float(tmp[2]))
    t3.append(int(tmp[3]))
    t4.append(float(tmp[4]))

pre_obs=pd.Series(t4, index=t3)
del t1, t2, t3, t4, tmp, pre_otmp

pre = np.mean(pre_obs.loc[y_beg:y_end].values)


fileout = 'Modelsetup_reference.txt'
with open(fileout, 'a') as f:
     f.write("%s %s %s %s %s\n" % (grdc, m1, m2, m3, pre))

