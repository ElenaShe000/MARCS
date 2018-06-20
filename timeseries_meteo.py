# -*- coding: utf-8 -*-
import sys
from netCDF4 import Dataset, num2date, date2index
from math import ceil, floor
from numpy import where, array
from os import unlink

#
# CONFIG
#

IN_DIR = './'
OUT_DIR = './'

# Description
#    'fname':  input filename (without directory)
#    'value': name of "variable" (inside netCDF container) which contains a needed information
#        (air temperature, precipitation, etc)
#    'fn_postfix': tail of output file (with extension)
#    'coef': arithmetic  function, that will be applied to each value (you can use any of python arithmetical functions)
#    'group_func': group function, that will be applied for each year (it must be a numpy.ndarray method)
#    'lat_resolution': lat grids resolution
#    'lat_zero':   means the lat's grid is started from
#        (for example: = 0 if the first value of variables["lat"] is 0)
#    'lon_resolution': lon grids resolution
#    'lon_zero': means the lon's grid is started from
#        (for example: = 0 if the first value of variables["lon"] is 0)

IF = {}

IF['TAS_HM'] = {
    'fname': 'tas_Amon_HadGEM2-AO_historical_r1i1p1_186001-200512.nc',
    'value': 'tas',
    'fn_postfix': '_tas_mod.txt',
    'coef': ' - 272.15',
    'group_func': 'mean()',
    'lat_resolution': 1.25,
    'lat_zero': 0,
    'lon_resolution': 1.875,
    'lon_zero': 0
}

IF['TAS_PR'] = {
    'fname': 'tas_Amon_HadGEM2-AO_rcp85_r1i1p1_200601-210012.nc',
    'value': 'tas',
    'fn_postfix': '_tas_mod.txt',
    'coef': ' - 272.15',
    'group_func': 'mean()',
    'lat_resolution': 1.25,
    'lat_zero': 0,
    'lon_resolution': 1.875,
    'lon_zero': 0
}

IF['TAS_HO'] = {
    'fname': 'air.mon.mean.v401.nc',
    'value': 'air',
    'fn_postfix': '_tas_obs.txt',
    'coef': '',
    'group_func': 'mean()',
    'lat_resolution': 0.5,
    'lat_zero': 0.25,
    'lon_resolution': 0.5,
    'lon_zero': 0.25
}

IF['PRE_HM'] = {
    'fname': 'pr_Amon_HadGEM2-AO_historical_r1i1p1_186001-200512.nc',
    'value': 'pr',
    'fn_postfix': '_pre_mod.txt',
    'coef': ' * 2592000',
    'group_func': 'sum()',
    'lat_resolution': 1.25,
    'lat_zero': 0,
    'lon_resolution': 1.875,
    'lon_zero': 0
}

IF['PRE_PR'] = {
    'fname': 'pr_Amon_HadGEM2-AO_rcp85_r1i1p1_200601-210012.nc',
    'value': 'pr',
    'fn_postfix': '_pre_obs.txt',
    'coef': ' * 2592000',
    'group_func': 'sum()',
    'lat_resolution': 1.25,
    'lat_zero': 0,
    'lon_resolution': 1.875,
    'lon_zero': 0
}

IF['PRE_HO'] = {
    'fname': 'precip.mon.total.v401.nc',
    'value': 'precip',
    'fn_postfix': '_pre_obs.txt',
    'coef': ' * 10',
    'group_func': 'sum()',
    'lat_resolution': 0.5,
    'lat_zero': 0.25,
    'lon_resolution': 0.5,
    'lon_zero': 0.25
}


#
# END CONFIG
#

# functions
def to_digit(x):
    try:
        if x.isdigit():
            return int(x)
        return float(x)
    except ValueError:
        return False


# Finding  nearest grid square
def find_nearest(coord, scale, zero):
    sign = 1
    if coord < 0:
        sign = -1
        coord = abs(coord)

    node = ceil(coord / scale) if coord - floor(coord / scale) > scale / 2 else floor(coord / scale)
    return (node * scale - zero) * sign


# Working with data
def get_data_by_year(t_elem, config, f_lat, f_lon):
    yearsum = {}
    lon = find_nearest(f_lon, config['lon_resolution'], config['lon_zero'])
    lat = find_nearest(f_lat, config['lat_resolution'], config['lat_zero'])

    idx_lat = where(t_elem.variables["lat"][:] == lat)[0][0]
    idx_lon = where(t_elem.variables["lon"][:] == lon)[0][0]

    calendar = t_elem.variables["time"].calendar if hasattr(t_elem.variables["time"], 'calendar') else 'standard'
    dates = num2date(t_elem.variables["time"][:], t_elem.variables["time"].units, calendar=calendar)

    for time in dates:
        time_id = date2index(time, t_elem.variables["time"])
        if time.year not in yearsum:
            yearsum[time.year] = [t_elem.variables[config['value']][time_id][idx_lat][idx_lon]]
        else:
            yearsum[time.year].append(t_elem.variables[config['value']][time_id][idx_lat][idx_lon])

    for tyear in yearsum:
        yearsum[tyear] = array(yearsum[tyear])
        yearsum[tyear] = eval("yearsum[tyear]." + config['group_func'])
        yearsum[tyear] = eval("yearsum[tyear] " + config['coef'])
    return yearsum, lon, lat


# input parameters
if len(sys.argv) < 4:
    print('Use command: python3 timeseries_meteo.py LON LAT ID')
    exit(1)

LON = to_digit(sys.argv[1])
LAT = to_digit(sys.argv[2])
ID = to_digit(sys.argv[3])

if not LON or not LAT or not ID:
    print('Use command: python3 timeseries_meteo.py LON LAT ID')
    exit(1)

if LON > 360 or LAT > 90 or LAT < -90:
    print('Wrong coordinates')
    exit(1)

# load all data from files
rootgrp = {}

for i in IF:
    try:
        rootgrp[i] = Dataset(IN_DIR + str(IF[i]['fname']), "r")
    except OSError:
        print("Can't open file: %s" % IN_DIR + str(IF[i]['fname']))
        exit(1)

# remove old files
for i in IF:
    try:
        unlink('{}{}{}'.format(OUT_DIR, ID, IF[i]['fn_postfix']))
    except OSError:
        continue

# create new files
for i in rootgrp:
    print(IF[i]['fname'])
    result, grid_lon, grid_lat = get_data_by_year(rootgrp[i], IF[i], LAT, LON)
    if result:
        with open('{}{}{}'.format(OUT_DIR, ID, IF[i]['fn_postfix']), 'a') as file:
            for year in result:
                file.write('%s %s %s %s \n' % (grid_lat, grid_lon, year, result[year]))
