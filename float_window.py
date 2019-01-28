#!/usr/bin/python

import numpy as np
import pandas as pd
from scipy.stats import moment
from scipy import stats
import math as ma
import matplotlib.pyplot as plt

WD = '/home/shevnina/Manuscripts/2019/UnivGeosc/support_data/'

# Convert string argument to digit
def to_digit(x):
    try:
        if x.isdigit():
            return int(x)
        return float(x)
    except ValueError:
        return False

####################### READING YEARLY TIME SERIES ######################################
# Water discharge observations on a gauging site
fn = WD+'pvm_6730501.txt'
arr = []

with open(fn, encoding="utf8", errors='ignore') as f:
     arr = f.readlines()

grdc = arr[8][25:-2]
area = float(arr[14][27:-2])
nlines = int(arr[24][24:-1]) + 48

# to read water discharge (m3s-1) data
year = []
d = []
for i in range(48, nlines):
    data = arr[i].split(';')
    year.append(int(data[0]))
    d.append(float(data[3]))

q = []
ty = 365*24*60*60

# to convert a water discharge (m3s-1) to a runoff rate (mm yr-1)
for i in range (0, len(d)):
    if d[i] == -999.0:
        q.append(np.nan)
    else:
        q.append((d[i]*ty)/(area*1000))

numb = int(len(q))
rr = pd.Series(q, index=year)

# to read the yearly time series of annual precipitation amount (mm yr-1)
WCl = '/home/shevnina/Manuscripts/2019/UnivGeosc/support_data/tst/GCM/' 
filename = WCl +'6730501_pre_obs.txt'
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


################# function to define a year to split observational period into two time interval #####
# Floating window/point algoritms to define training and control periods for model cross-validation (Shevnina et. al, 2017; Kovalenko, 1993)
# variables
n = 15 # length of floating window
m = 2  # collums for output statistics
alpha = 0.05 # level of statistical significance
res_df=np.zeros(m,dtype=int) 

t = [] # array of t-values 2 sided Student test: https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.ttest_ind.html
p = [] # array of p-values to test difference in two mean values
years = []
# to define periods by floating window
lim = int(len(rr.values)-2*n-1) # to limit iterations
for i in range (0, lim):
      index=rr.index[i+n-1]
      t,p = stats.ttest_ind(rr.values[i:(i+n-1)],rr.values[i+n:i+lim], nan_policy='omit')
#      print("i " + str(i) + " t " + str(t) + " p " + str(p) + " year " + str(index))
      if p < alpha:
         years.append(rr.index[i]) 

# to define periods by floating point
lim = int(len(rr.values)) # to limit iterations
for i in range (0, lim-2*n-1):
    index=rr.index[i+n]
    t,p = stats.ttest_ind(rr.values[0:(i+n)],rr.values[(i+n+1):lim],nan_policy='omit')        
#   print("i " + str(i) + " t " + str(t) + " p " + str(p) + " year " + str(index))
    if p < alpha:
       years.append(rr.index[i])

########################### end of the function  ##############################################

############# cross validation function #######################################################
# to choose the year to split the observational period into the training and control periods
# what to do if there are no values in the array? change the level of statistical significance
split_year = max(years)
# arguments: rr [Pandas], split_year [int]....
#ytr_beg = rr.index[0]
#ytr_end = split_year

# ycon_beg = split_year+1
# ycon_end = rr.index[numb-1]

# to non-central statistical moments of runoff for the training period
# cv is a coefficient of variation (CV) based on the moments (Rogdestvensky, 1988)
# cs is moment skweness coefficient (Kovalenko et al. 2006, p.249)
m1 = np.nanmean(rr.loc[rr.index[0]:split_year].values)
m2 = moment(rr.loc[rr.index[0]:split_year].values, moment=2, nan_policy='omit') + m1 * m1
m3 = moment(rr.loc[rr.index[0]:split_year].values, moment=3,nan_policy='omit') + 3 * m2 * m1 - 2 * m1 * m1 * m1
cv_tr = estimate_cv(m1,m2)
cs_tr = estimate_cs(m1,m2,cv_con)

# to calulate mean values of precipitation for the trainig and controling periods
pre_tr = np.nanmean(pre_obs.loc[rr.index[0]:split_year].values) # training 
pre_con = np.nanmean(pre_obs.loc[split_year+1:rr.index[numb-1]].values) # controling 

# to simulate three parameters of the Pearson System for the control period (a_con, b0_con, b1_con)
a_tr, b0_tr, b1_tr = basic_param_pearson(m1, m2, m3) # basic parameterization
c_tr, gn_tr, gcn_tr =  basic_param_fpk(a_tr, b0_tr, b1_tr, pre_tr) 
a_con, b0_con, b1_con = simulate_param_pearson3(gcn_tr, gn_tr, c_tr, pre_con) # constant parameters
# to simulate CV and CS for the Pearson type 3 distribution for the control period
cv_con, cs_con = simulate_skw(a_con, b0_con, b1_con)

# to compare the empirical Pt3 distribution for the control period 
# with the Pt3 distribution simulated form CS for the control period

# by the Kolmogorov-Smirnov test on two samples

# ks, p_ks = stats.kstest(rr.loc[split_year+1:rr.index[numb-1]].values, 'person3')

# r1 = pearson3.rvs(cs_tr,size=len(rr.loc[split_year+1:rr.index[numb-1]].values))
# r2 = pearson3.rvs(cs_con,size=len(rr.loc[split_year+1:rr.index[numb-1]].values))
# ks, p_ks = stats.ks_2samp(r1,r2)

######### extracted from model_core.py: PARAMETERIZATION: GENERAL SCHEME, CONSTANT PARAMETERS ##
# Equations 23-25 (Shevnina and Silaev, 2018) and (Kovalenko et al., 2006 p. 247-249)
def basic_param_pearson(m1, m2, m3):
    low_index = 2 * (m2 - m1 ** 2)
    a_local = (5 * m1 * m2 - 4 * m1 ** 3 - m3) / low_index
    b0_local = (m2 * m1 ** 2 - 2 * m2 ** 2 + m1 * m3) / low_index
    b1_local = (3 * m1 * m2 - 2 * m1 ** 3 - m3) / low_index
    return a_local, b0_local, b1_local  # three parameters of the Pearson System (Adnreev et al., 2005) 

# Equations 26-28 (Shevnina and Silaev, 2018) and (Kovalenko et. al 2006).
def basic_param_fpk(a_local, b0_local, b1_local, npre_local):
    low_index = (a_local - b1_local / 2)
    gcn = npre_local * b1_local / low_index
    gn = -2 * npre_local * b0_local / low_index
    c = npre_local / low_index
    return c, gn, gcn                      # three paramaters of the FPK (Pugachev et al., 1974)

# Equations 22-24 (Shevnina and Silaev, 2018)
def simulate_param_pearson3(gcn_p, gn_p, c_p, npre_proj):
    a_p = (gcn_p + 2 * npre_proj) / (2 * c_p)
    b0_p = - gn_p / (2 * c_p)
    b1_p = gcn_p / c_p
    return a_p, b0_p, b1_p                # three parameters of the Pearson System (simulated) 

# Equations 25-27 (Shevnina and Silaev, 2018)
def simulate_skw(a_p, b0_p, b1_p):
    m1_p = a_p - b1_p
    m2_p = a_p * m1_p - 2 * m1_p * b1_p - b0_p
    m3_p = m2_p * a_p - 2 * m1_p * b0_p - 3 * m2_p * b1_p
    cv = ma.sqrt(m2_p - m1_p ** 2) / m1_p
    cs = (m3_p - 3 * m2_p * m1_p + 2 * m1_p ** 3) / (cv ** 3 * m1_p ** 3)
    return cv, cs

def estimate_cv (m1, m2):
    CV = ma.sqrt(m2 - m1 ** 2) / m1
    return CV

def estimate_cs(m1,m2,cv):
    CS = (m3 - 3 * m2 * m1 + 2 * m1 ** 3) / (cv ** 3 * m1 ** 3)
    return CS
###################################################################################################







