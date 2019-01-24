#!/usr/bin/python
#  Description: MARCS SETUP MODULE: HYDROLOGY + PRECIPITATION
#  Experiment: SINGLE CATCHMENT
#  31.05.2018
#  Code Owner: Elena Shevnina, Finnish Meteorological Institute
#  ph. +358449185446
#  e-mail:eshevnina@gmail.com

import sys
import numpy as np
from scipy.stats import moment
import pandas as pd

# to define a WORKING DIRECTORY
WD = './'

# to convert string argument to digit
def to_digit(x):
    try:
        if x.isdigit():
            return int(x)
        return float(x)
    except ValueError:
        return False


# Input argument: the name of file with the yearly time series of discharge and site's metadata in format of GRDC database
# see details https://www.bafg.de/GRDC/EN/01_GRDC/13_dtbse/database_node.html
fn=str(sys.argv[1])

with open(fn, 'r') as f:
     arr = f.readlines()


# to get the GRDC ID, the observational period and a catchment area 
grdc = arr[8][25:-2]
area = float(arr[14][27:-2])
nlines = int(arr[24][24:-2]) + 48

# to read the yearly time series of water discharge data, yearly time scale
year = []
d = []
for i in range(48, nlines):
    data = arr[i].split(';')
    year.append(int(data[0]))
    d.append(float(data[3]))

q = []
ty = 365*24*60*60

# to convert annual water discharges (m3s-1) to the annual runoff rate (mm yr-1)
for i in range (0, len(d)):
    if d[i] == -999.0: 
        q.append(np.nan)
    else:
        q.append((d[i]*ty)/(area*1000))


rr = pd.Series(q, index=year)


# to set-up the reference period manually 
# additional option to define a reference period is using the floating point/period algoritms (Shevnina et al., 2017)
y_beg = 1950
y_end = 1990

# to calculate three non-central moments estimates for the annaul runoff rate 
# for the reference period
m1 = np.nanmean(rr.loc[y_beg:y_end].values)
m2 = moment(rr.loc[y_beg:y_end].values, moment=2, nan_policy='omit') + m1 * m1
m3 = moment(rr.loc[y_beg:y_end].values, moment=3,nan_policy='omit') + 3 * m2 * m1 - 2 * m1 * m1 * m1

# to read the yearly time seris of annual precipitation amount (mm yr-1) for the reference period
# these time series were extracted from gridded dataset of NOAA/OAR/ESRL PSD, Boulder, Colorado, USA,
# the web site at http://www.esrl.noaa.gov/psd/

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

# to calculate mean value of the annual precipitation amount for the reference period
pre = np.mean(pre_obs.loc[y_beg:y_end].values)

# to save the model set-up output file
fileout = 'Modelsetup_reference.txt'
with open(fileout, 'a') as f:
     f.write("%s %s %s %s %s\n" % (grdc, m1, m2, m3, pre))

