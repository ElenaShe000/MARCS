#!/usr/bin/python 
#  Description: MARCS MAIN MODULE WITH BASIC PARAMETRIZATION
#  Experiment: SINGLE CATCHMENT
#  05.03.2018
#  Code Owner: Elena Shevnina, Finnish Meteorological Institute
#  ph. +358449185446
#  e-mail:eshevnina@gmail.com

import sys
import math as ma

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
WD = './'

# MODEL INPUT: RUNOFF STATISTICAL MOMENTS, Reference climatology
M1_REF = 379.230447067
M2_REF = 149343.387513
M3_REF = 60811610.4455
NPRE_REF = 625.49223301

# CATCHMENT ID
WID = '6854600'


# REFERENCE PERIOD: 1911-2014
# AND PROJECTED PERIOD: 2020-2050


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
    m2_proj = a_p * m1_p - 2 * m1_p * b1_p - b0_p
    m3_proj = m2_proj * a_p - 2 * m1_p * b0_p - 3 * m2_proj * b1_p

    # Coefficient of variation (CV) based on the moments (Rogdestvensky, 1988)
    cv_r = ma.sqrt(m2 - m1 ** 2) / m1
    cv_p = ma.sqrt(m2_proj - m1_p ** 2) / m1_p

    # Moment skweness coefficient (Kovalenko et al. 2006, p.249)
    cs_r = (m3 - 3 * m2 * m1 + 2 * m1 ** 3) / (cv_r ** 3 * m1 ** 3)
    cs_p = (m3_proj - 3 * m2_proj * m1_p + 2 * m1_p ** 3) / (cv_p ** 3 * m1_p ** 3)

    return cs_r, cs_p, m1_p, cv_p, cv_r


# MAIN CODE

# MODEL INPUT: projected climatology
# NPRE_PROJ = 670
NPRE_PROJ = to_digit(sys.argv[1])
# Name_sce = str(sys.argv[1])

if not NPRE_PROJ:
    print('Use command: python model_core.py NPRE_PROJ')
    exit(1)

# PREDICTION: GENERAL SCHEME, CONSTANT PARAMETERS

a, b0, b1 = basic_param_pearson(M1_REF, M2_REF, M3_REF)

c_proj, gn_proj, gcn_proj = basic_param_fpk(a, b0, b1, NPRE_REF)

a_proj, b0_proj, b1_proj = foo_0(gcn_proj, c_proj, NPRE_PROJ)

cs_ref, cs_proj, m1_proj, cv_proj, cv_ref = foo_1(M1_REF, M2_REF, M3_REF, a_proj, b0_proj, b1_proj)

# OUTPUT: TEXT LINE: WID, M1_REF, NPRE_REF, CV_REF, CS_REF, c, Gn, Gcn, M1_PROJ, NPRE_PROJ, CV_PROJ, CS_PROJ

with open(WD + 'model_GPSCH.txt', 'a') as f:
    f.write("%s %s %s %s %s %s %s %s %s %s %s %s\n" % (
        WID, M1_REF, NPRE_REF, cv_ref, cs_ref, c_proj, gn_proj, gcn_proj, m1_proj, NPRE_PROJ, cv_proj, cs_proj))
