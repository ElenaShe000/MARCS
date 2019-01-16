#!/bin/bash
#to calculate the yearly values from the monthly values
#use the data by NOAA: precip.mon.total.v401.nc [sm/month] and air.mon.mean.v401.nc [degC]

#  Experiment: 12 FINNISH RIVERS, 05.03.2018
#  Code Owner: Elena Shevnina, the Finnish Meteorological Institute
#  ph. +358449185446
#  e-mail:eshevnina@gmail.com

#calculate yearly precipitation,mm/year
cdo yearsum precip.mon.total.v401.nc pre_yearly1900_2014mm.nc
cdo mulc,0.01 pre_yearly1900_2014mm.nc pre_yearly1900_2014.nc
#calculate yearly air temperature, degC
cdo yearmean air.mon.mean.v401.nc tas_yearly1900_2014.nc

#to calculate mean values for time period 1911-2007 (Tana River hydrological observations)
#12/108 the time steps bounded the interval: 1900(0+1(+11))=1911 and 2014(115-1(-7))=2007
cdo seltimestep,12/108 pre_yearly1900_2014.nc pre_yearly1911_2007.nc
cdo seltimestep,12/108 tas_yearly1900_2014.nc tas_yearly1911_2007.nc

cdo timmean pre_yearly1911_2007.nc pre_mean1911_2007.nc
cdo timmean tas_yearly1911_2007.nc tas_mean1911_2007.nc

#reprojection to -180,180
cdo sellonlatbox,-180,180,-90,90 pre_mean1911_2007.nc pre_mean1911_2007_repr.nc
cdo sellonlatbox,-180,180,-90,90 tas_mean1911_2007.nc tas_mean1911_2007_repr.nc
#export to txt
cdo outputtab,lon,lat,value pre_mean1911_2007_repr.nc > pre_mean1911_2007.txt
cdo outputtab,lon,lat,value tas_mean1911_2007_repr.nc > tas_mean1911_2007.txt
rm tas_yearly1900_2014.nc pre_yearly1900_2014.nc pre_yearly1900_2014mm.nc pre_yearly1911_2007.nc tas_yearly1911_2007.nc pre_mean1911_2007.nc tas_mean1911_2007.nc pre_mean1911_2007_repr.nc tas_mean1911_2007_repr.nc
