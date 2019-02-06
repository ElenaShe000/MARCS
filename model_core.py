#!/usr/bin/python 
#  Description: MARCS CORE 0.3: BASIC PARAMETRIZATION 
#  Experiment: SINGLE CATCHMENT
#  06.02.2019
#  Code Owner: Elena Shevnina, Finnish Meteorological Institute
#  ph. +358449185446
#  e-mail:eshevnina@gmail.com

import sys
import math as ma
import string
import csv
from scipy.stats import pearson3

# Input Variables:
# WID - id of the watershed
# M1_REF = a first statistical moment of annual runoff, [mm year-1]; reference period
# M2_REF = a second statistical moment of annual runoff, [mm year-1]^2; reference period
# M3_REF = a third statistical moment of annual runoff, [mm year-1]^3; reference period
# NPRE_REF = a mean annual precipitation amount, [mm year-1]; reference period
# NPRE_PROJ 0 = a mean annual precipitation, [mm year-1]; projected period


# Output Variables:
# M1_PROJ = a first statistical moment of annual runoff, [mm year-1]; projected period
# M2_PROJ = a second statistical moment of annual runoff, [mm year-1]^2; projected period
# M3_PROJ = a third statistical moment of annual runoff, [mm year-1]^3; projected period
# CV_PROJ = a coefficient of variation of annual runoff, [mm year-1]^2; projected period
# CS_PROJ = a coefficient of skewness of annual runoff, [mm year-1]^3; projected period
# CV_REF = a coefficient of variation of annual runoff, [mm year-1]^2; reference period
# CS_REF = a coefficient of skewness of annual runoff, [mm year-1]^3; reference period

# Inner Variables:
# a, b0, b1 = the parameters of the Pearson Equation (as denoted in Andreev et al., 2005); reference period
# a_proj, b0_proj, b1_proj = the parameters of the Pearson Equation
# (as denoted in Andreev et al., 2005); projected period
# c, Gcn, Gn = the parameters of the Fokker-Plank-Kolmogorov Equation
# (as denoted in Kovalenko et al., 2006); reference period
# c_proj, Gcn_proj, Gn_proj = the parameters of the Fokker-Plank-Kolmogorov Equation (Shevnina and Silaev, 2018);
# projected period

# Temporal Variables:

# WORKING DIRECTORY
# WD = './'
WD = '/home/shevnina/Manuscripts/2019/UnivGeosc/support_data/'

# CATCHMENT ID
WID = str(sys.argv[1])

# REFERENCE PERIOD: 1950-1990
# AND PROJECTED PERIOD: 2020-2050

###################################### FUNCTIONS ##########################################
# Convert string argument to digit
def to_digit(x):
    try:
        if x.isdigit():
            return int(x)
        return float(x)
    except ValueError:
        return False

# PARAMETERIZATION: GENERAL SCHEME, CONSTANT PARAMETERS
# Equations 23-25 (Shevnina and Silaev, 2018) and (Kovalenko et al., 2006 p. 247-249)
def basic_param_pearson(m1, m2, m3):
    low_index = 2 * (m2 - m1 ** 2)
    a_local = (5 * m1 * m2 - 4 * m1 ** 3 - m3) / low_index
    b0_local = (m2 * m1 ** 2 - 2 * m2 ** 2 + m1 * m3) / low_index
    b1_local = (3 * m1 * m2 - 2 * m1 ** 3 - m3) / low_index
    return a_local, b0_local, b1_local


# Equations 26-28 (Shevnina and Silaev, 2018) and (Kovalenko et. al 2006).
def basic_param_fpk(a_local, b0_local, b1_local, npre_local):
    low_index = (a_local - b1_local / 2)
    gcn = npre_local * b1_local / low_index
    gn = -2 * npre_local * b0_local / low_index
    c = npre_local / low_index
    return c, gn, gcn


def foo_0(gcn_p, c_p, npre_proj):
    # see Eq. (22-24) in Shevnina and Silaev, 2018
    a_p = (gcn_p + 2 * npre_proj) / (2 * c_p)
    b0_p = - gn_proj / (2 * c_p)
    b1_p = gcn_p / c_p
    return a_p, b0_p, b1_p


def foo_1(m1, m2, m3, a_p, b0_p, b1_p):
    # see Eq. (25-27) in Shevnina and Silaev, 2018
    m1_p = a_p - b1_p
    m2_p = a_p * m1_p - 2 * m1_p * b1_p - b0_p
    m3_p = m2_p * a_p - 2 * m1_p * b0_p - 3 * m2_p * b1_p
    # Coefficient of variation (CV) based on the moments (Rogdestvensky, 1988)
    cv_r = ma.sqrt(m2 - m1 ** 2) / m1
    cv_p = ma.sqrt(m2_p - m1_p ** 2) / m1_p
    # Moment skweness coefficient (Kovalenko et al. 2006, p.249)
    cs_r = (m3 - 3 * m2 * m1 + 2 * m1 ** 3) / (cv_r ** 3 * m1 ** 3)
    cs_p = (m3_p - 3 * m2_p * m1_p + 2 * m1_p ** 3) / (cv_p ** 3 * m1_p ** 3)
    return cs_r, cs_p, m1_p, m2_p, cv_p, cv_r

# to calculate the percentile of the EPC within Pearson type 3 distribution according to 
# “Using Modern Computing Tools to Fit the Pearson Type III Distribution to Aviation Loads Data”, Office of Aviation Research (2003). 
def pt3_percentiles(csl, m1l, m2l):
    x_loc = pearson3.ppf([0.001, 0.003, 0.005, 0.01, 0.03, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.95, 0.97, 0.99, 0.995, 0.997, 0.999], csl)
    mu2_loc = m2l - m1l * m1l
    #to calculate the runoff rate of particular exceedance probabilities
    ex = m1l + x_loc * ma.sqrt(mu2_loc)
    return ex

def pt3_extremes(csl, m1l, m2l):
    x_loc = pearson3.ppf([0.1, 0.5, 0.90], csl)
    mu2_loc = m2l - m1l * m1l
    #to calculate the runoff rate of particular exceedance probabilities
    ex = m1l + x_loc * ma.sqrt(mu2_loc)
    return ex

# to print the results to the output file   
def add_tofile(filename, inlist):
              with open(filename, 'a') as f:
                  for item in inlist:
                      f.write('%s ' % item)
                      with open(filename, 'a') as f:
                           f.write('%s' % '\n')
##############################################################################################################################

############################# MAIN CODE ######################################################################################
# MODEL INPUT: ANNUAL RUNOFF STATISTICAL MOMENTS AND REFERENCE PRECIPITATION
fn = WD + 'Modelsetup_reference.txt'
arr = []
with open(fn, 'r') as f:
     arr = f.readlines()
        
f.close()

# for the first gauge in the file 
reference = arr[0]

gid, m1r, m2r,m3r,pr = reference.split(' ')
M1_REF = to_digit(m1r) # (MM YR-1)
M2_REF = to_digit(m2r)
M3_REF = to_digit(m3r)
NPRE_REF = to_digit(pr) # (MM YR-1)
del m1r, m2r,m3r,pr

# MODEL FORCING: MEAN ANNUAL PRECIPIPATION (MM YR-1)

WCl = '/home/shevnina/Manuscripts/2019/UnivGeosc/support_data/regional_climate_forcing.csv'
climate_tmp = []
with open(WCl,'r') as f:
      for line in f:
          climate_tmp = f.read().split('\n')
        
climate = []     
for i in range(0, len(climate_tmp)):
    tmp = climate_tmp[i].split(',')
    tmp_id = tmp[0]
    if tmp_id == gid:
        climate = tmp
         
            
RIVER = climate[1]
STATION = climate[2]
rcp26 = float(climate[9])
rcp45 = float(climate[10])
rcp85 = float(climate[11])

########### AAR PROJECTION FOR THE RCP26 CC ##################################################################################
SCENARIO = 'RCP26'
NPRE_PROJ = rcp26
if not NPRE_PROJ:
    print('Use command: python model_core.py NPRE_PROJ')
    exit(1)
# PREDICTION: GENERAL SCHEME, CONSTANT PARAMETERS
a, b0, b1 = basic_param_pearson(M1_REF, M2_REF, M3_REF)
c_proj, gn_proj, gcn_proj = basic_param_fpk(a, b0, b1, NPRE_REF)
a_proj, b0_proj, b1_proj = foo_0(gcn_proj, c_proj, NPRE_PROJ)
cs_ref, cs_proj, m1_proj, m2_proj, cv_proj, cv_ref = foo_1(M1_REF, M2_REF, M3_REF, a_proj, b0_proj, b1_proj)

# CONSTRUCTION OF EPC WITH PEARSON TYPE III
ex_ref = pt3_extremes(cs_ref,M1_REF,M2_REF)
ex_proj = pt3_extremes(cs_proj,m1_proj,m2_proj)


# OUTPUT: to add the header
fo = WD + 'model_output_regional.txt'
header = 'GRDC,RIVER,STATION,EVALUATION,10,50,90'

invert = header
with open(fo,'a') as f:
        f.write(header + '\n')
        
        
with open(fo,'a') as f:
         line = gid +',' + RIVER + ','+ STATION + ',1950-1990,'+ '%d' % (ex_ref[0])+ ','+ '%d' % (ex_ref[1]) + ','+ '%d' % (ex_ref[2]) 
         f.write(line + '\n')

with open(fo,'a') as f:
         line = gid +',' + RIVER + ','+ STATION + ','+ SCENARIO + ','+ '%d' % (ex_proj[0])+ ','+ '%d' % (ex_proj[1]) + ','+ '%d' % (ex_proj[2])
         f.write(line + '\n')


