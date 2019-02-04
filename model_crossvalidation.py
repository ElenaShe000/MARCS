#!/usr/bin/python

#  Description: MARCS MODEL CROSS VALIDATION BLOCK
#  Experiment: SINGLE CATCHMENT
#  30.01.2019
#  Code Owner: Elena Shevnina, Finnish Meteorological Institute
#  ph. +358449185446
#  e-mail:eshevnina@gmail.com

import sys
import numpy as np
import pandas as pd
from scipy.stats import moment
from scipy import stats
import math as ma
from sys import exit
from scipy.stats import pearson3

##################### ARGUMENTS ##########################################################
# agrv1 is the GRDC ID of a gauging site
gid = str(sys.argv[1])

###################### WORKING DIRECTORY #################################################
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
fn = WD+'pvm_'+gid+'.txt'
arr = []

with open(fn, encoding="utf8", errors='ignore') as f:
     arr = f.readlines()

grdc = arr[8][25:-1]
area = float(arr[14][26:-1])
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


########################## FUNCTIONS ########################################################### 
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

def estimate_cs(m1, m2, m3, cv):
    CS = (m3 - 3 * m2 * m1 + 2 * m1 ** 3) / (cv ** 3 * m1 ** 3)
    return CS

# to define years to split observational period into training and control periods with the floating window/point algoritms to define training and control periods for model cross-validation (Shevnina et. al, 2017; Kovalenko, 1993)
# variables: n is length of floating window (15); alpha is the level of statistical significance (0.5/0.10); t is array of t-values 2 sided Student test: https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.ttest_ind.html;  p is array of p-values to test difference in two mean values; years is selected years with p<alpha
 
def define_split_year(rr, n, alpha, test):
    t = [] 
    p = []
    years = []
    lim = int(len(rr.values)-2*n-1)  # the split years by floating window
    for i in range (0, lim):
        index=rr.index[i+n-1]
        if test == 'st':
           t,p = stats.ttest_ind(rr.values[i:(i+n-1)],rr.values[i+n:i+lim], nan_policy='omit')
        else:
           t, p = stats.ks_2samp(rr.values[i:(i+n-1)],rr.values[i+n:i+lim])
#         print(index, p)
        if p < alpha:
#            print(rr.index[i]+n-1)
           years.append(rr.index[i]+n-1)
    lim = int(len(rr.values))        # the split years by floating point
    for i in range (0, lim-2*n-1):
        index=rr.index[i+n]
        if test == 'st':
           t,p = stats.ttest_ind(rr.values[0:(i+n)],rr.values[(i+n+1):lim],nan_policy='omit')
        else:
           t, p = stats.ks_2samp(rr.values[0:(i+n)],rr.values[(i+n+1):lim])

        if p < alpha:
           years.append(rr.index[i]+n-1)
    return years

# cross-validation with basic parameterization scheme (Shevnina et al., 2017; Kovalenko, 1993)
def crossvalidation_basic(arr_train, arr_contr, pre_train, pre_contr):
# to estimate the non-central statistical moments of runoff for the training period (the Method of Moments)
     m1_tr = np.nanmean(arr_train) 
     m2_tr = moment(arr_train, moment=2, nan_policy='omit') + m1_tr * m1_tr
     m3_tr = moment(arr_train, moment=3,nan_policy='omit') + 3 * m2_tr * m1_tr - 2 * m1_tr * m1_tr * m1_tr
# cv is a coefficient of variation (CV) based on the moments (Rogdestvensky, 1988)
# cs is moment skweness coefficient (Kovalenko et al. 2006, p.249)
     v_tr = estimate_cv(m1_tr, m2_tr)
     cv_tr = estimate_cv(m1_tr, m2_tr)
     cs_tr = estimate_cs(m1_tr, m2_tr, m3_tr, cv_tr)
# to simulate three parameters of the Pearson System for the control period (a_con, b0_con, b1_con)
     a_tr, b0_tr, b1_tr = basic_param_pearson(m1_tr, m2_tr, m3_tr)# basic parameterization
     c_tr, gn_tr, gcn_tr =  basic_param_fpk(a_tr, b0_tr, b1_tr, pre_train)
     a_con, b0_con, b1_con = simulate_param_pearson3(gcn_tr, gn_tr, c_tr, pre_contr) # constant parameters
# to simulate CV and CS for the Pearson type 3 distribution for the control period
     cv_con, cs_con = simulate_skw(a_con, b0_con, b1_con)
# to compare the empirical Pt3 distribution for the control period with the Pt3 distribution simulated form CS for the control period by the Kolmogorov-Smirnov test on two samples
     data = arr_contr
     normed_data = (data - np.nanmean(data))/np.nanstd(data)# sample 1: normed data series in the control
     r_con = pearson3.rvs(cs_con,size=len(arr_contr))#sample 2: generated by pearson3 with simulated cs for the control period
     ks_con, pks_con = stats.ks_2samp(normed_data, r_con)
     return ks_con, pks_con


###################################################################################################

# to define years to split the observed time series into training and control periods 
# 
alpha = 0.05
years = define_split_year(rr, 15, alpha, 'ks')
if not years:
   alpha = 0.10
   years = define_split_year(rr, 15, alpha, 'ks')

if not years:
   output = str(grdc)+" periods not founded on 0.05 and 0.10 levels of statistical significance"+"\n"
   with open(WD + 'ModelCrossValidRes.txt', 'a') as f:
        f.write(output)
 
   exit(0)

############# CROSS VALIDATION: Shevnina et l., 2017; Kovalenko, 1993 ############################################
# to choose the year to split the observational period into the training and control periods
# what to do if there are no values in the array? change the level of statistical significance
split_year = max(years)

# to define periods for the cross-validation
training_period = str(rr.index[0]) + " - " + str(split_year)
controling_period = str(split_year+1) + " - " + str(rr.index[numb-1])
training = rr.loc[rr.index[0]:split_year].values
controling = rr.loc[split_year+1:rr.index[numb-1]].values

# to calulate mean values of precipitation for the trainig and controling periods
pre_tr = np.nanmean(pre_obs.loc[rr.index[0]:split_year].values) # training 
pre_con = np.nanmean(pre_obs.loc[split_year+1:rr.index[numb-1]].values) # controling 

# compare the EPC with the simulated EPC by the Kolmogorov Smirnov test
ks1, pval1 = crossvalidation_basic(training, controling, pre_tr, pre_con)
ks1s = str(round(ks1,2))
pval1s = str(round(pval1,2))
# and vice versa
ks2, pval2 = crossvalidation_basic(controling, training, pre_con, pre_tr)
ks2s = str(round(ks2,2))
pval2s = str(round(pval2,2))

# TO OUTPUT DATA TO THE RESULT FILE ############################################################
with open(WD + 'ModelCrossValidRes.txt', 'a') as f:
    f.write("%s %s %s %s %s %s %s %s\n" % (grdc, alpha, training_period, ks2s, pval2s, controling_period, ks1s, pval1s))








