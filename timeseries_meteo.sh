#!/bin/bash
#  Description: METEOROLOGIAL MODULE OF THE MODEL 
#  Experiment: PAN-ARCTIC
#  25 Jul 2016, 16:00
#  Lines embraced with "#Variable" contain name and description of variable 
#                 with "#" are comments that may be helpful to a user.
#  Current Code Owner: FMI, Elena Shevnina
#  ph. +358449185446
#  e-mail:eshevnina@gmail.com

#Note: Define the paths to the Working directory (WD), file with the GCMs(RCMs) historical run (CS) and projections (CSP), and to the grided dataset with the reference climatology (RefC)
#all input datafile are netCDF, with lat 0..360 and they contain monthly air temperatures and precipitation
#Important: the GCMs(RCMs) historical run and projections contain the preciputation expressed in kg sec-1m-2 (check it) and the air temperature is in Kelvin 

#WD='/home/shevnina/2016/MidLat/MARC/meteo_input'
#WDU='/home/shevnina/2016/MidLat/MARC/meteo_output/hadcmrcp85'

#modification 18.01.2019
WD='/home/shevnina/Manuscripts/2019/UnivGeosc/support_data'
WDU='/home/shevnina/Manuscripts/2019/UnivGeosc/support_data/tst'
CS='/home/shevnina/DCW/CMIP5/MPI_LR_maxPlank/hist1.1/'
RefC='/home/shevnina/DCW/Meteo_history/'

infile_pre_hm=$CS'pr_Amon_MPI-ESM-LR_historical_r1i1p1_185001-200512.nc'
infile_pre_ho=$RefC'precip.mon.total.v401.nc'
infile_pre_pr26='/home/shevnina/DCW/CMIP5/MPI_LR_maxPlank/RCP26/pr_Amon_MPI-ESM-LR_rcp26_r1i1p1_200601-210012.nc'
infile_pre_pr45='/home/shevnina/DCW/CMIP5/MPI_LR_maxPlank/RCP45/pr_Amon_MPI-ESM-LR_rcp45_r1i1p1_200601-210012.nc'
infile_pre_pr85='/home/shevnina/DCW/CMIP5/MPI_LR_maxPlank/RCP85/pr_Amon_MPI-ESM-LR_rcp85_r1i1p1_200601-210012.nc'

#And to calculate the precipitation in [mm] from the precipitation_flux [kg m-2 s-1]and to obtaine the yearly values of precipitation in [mm]

cdo mulc,2592000 $infile_pre_hm $WD/pre_mm_hm.nc
cdo yearsum $WD/pre_mm_hm.nc $WD/pre_year_mm_hm.nc

cdo mulc,2592000 $infile_pre_pr26 $WD/pre_mm_pr26.nc
cdo yearsum $WD/pre_mm_pr26.nc $WD/pre_year_mm_pr26.nc

cdo mulc,2592000 $infile_pre_pr45 $WD/pre_mm_pr45.nc
cdo yearsum $WD/pre_mm_pr45.nc $WD/pre_year_mm_pr45.nc

cdo mulc,2592000 $infile_pre_pr85 $WD/pre_mm_pr85.nc
cdo yearsum $WD/pre_mm_pr85.nc $WD/pre_year_mm_pr85.nc

cdo mulc,10 $infile_pre_ho $WD/pre_mm_ho.nc
cdo yearsum $WD/pre_mm_ho.nc $WD/pre_year_mm_ho.nc
rm $WD/pre_mm*

#Reprojection to -180 180 W
cdo sellonlatbox,-180,180,-90,90 $WD/pre_year_mm_ho.nc $WD/pre_year180_mm_ho.nc
cdo sellonlatbox,-180,180,-90,90 $WD/pre_year_mm_pr26.nc $WD/pre_year180_mm_pr26.nc
cdo sellonlatbox,-180,180,-90,90 $WD/pre_year_mm_pr45.nc $WD/pre_year180_mm_pr45.nc
cdo sellonlatbox,-180,180,-90,90 $WD/pre_year_mm_pr85.nc $WD/pre_year180_mm_pr85.nc
cdo sellonlatbox,-180,180,-90,90 $WD/pre_year_mm_hm.nc $WD/pre_year180_mm_hm.nc
rm $WD/pre_year_*

#Note: the followibng part of the code performs the calculations of the meteorological timeseries at the point with specific coodinates: the nearest point to the centroid of the watersheds. The geogaphical coordinates are stored on the file crd.txt with the format lat lon lat lon GRDC_ID
#list='138.018906647275543,60.92442176818637,138.018906647275543,60.924421768186370,2903070'

#First: we define the nearest points to the waterseds' centroids
while read filename; do 
      list=$filename
      id=$(echo $list | cut -d "," -f 1)
      lon=$(echo $list | cut -d "," -f 2)
      lat=$(echo $list | cut -d "," -f 3)

#The CGMs modeled data is represented in grids with different resolution lat/lon Degrees, thus the neasert point is searchin within 1/2 lat/lon in degrees boundaries
#CanESM2: 2.8/2.8 = 1.4/1.4; GFDL_CM3: 2.0/2.5 = 1.0/1.25
#INMCM4: 1.5/2.0 = 0.75/1.0; MPI: 1.8/1.8 = 0.9/0.9
      lat1=`echo "$lat + 0.9" | bc`
      lat2=`echo "$lat - 0.9" | bc`
      lon1=`echo "$lon + 0.9" | bc`
      lon2=`echo "$lon - 0.9" | bc`

      cdo sellonlatbox,$lon2,$lon1,$lat2,$lat1 $WD/pre_year180_mm_hm.nc $WD/'tmp_prehm.nc'
      cdo sellonlatbox,$lon2,$lon1,$lat2,$lat1 $WD/pre_year180_mm_pr26.nc $WD/'tmp_prepr26.nc'
      cdo sellonlatbox,$lon2,$lon1,$lat2,$lat1 $WD/pre_year180_mm_pr45.nc $WD/'tmp_prepr45.nc'
      cdo sellonlatbox,$lon2,$lon1,$lat2,$lat1 $WD/pre_year180_mm_pr85.nc $WD/'tmp_prepr85.nc'

#Output the timeseries to separate files
      cdo outputtab,lat,lon,year,value $WD/'tmp_prehm.nc' > $WDU/$id'_pre_mod.txt'
      cdo outputtab,lat,lon,year,value $WD/'tmp_prepr26.nc' >> $WDU/$id'_pre_mod26.txt'
      cdo outputtab,lat,lon,year,value $WD/'tmp_prepr45.nc' >> $WDU/$id'_pre_mod45.txt'
      cdo outputtab,lat,lon,year,value $WD/'tmp_prepr85.nc' >> $WDU/$id'_pre_mod85.txt'

      sed -i '/^#/d' $WDU/$id'_pre_mod*.txt'
      sed -i 's/ \{2,\}/,/g' $WDU/$id'_pre_mod*.txt'
      sed -i 's/,/ /g' $WDU/$id'_pre_mod*.txt'


#delete temporal nc
      rm $WD/tmp_*

#The observed data is represented in the grids with resolution of 0.5x0.5 Degrees, thus the neasert point is found in the boundaries of 0.5 degrees
     lat1=`echo "$lat + 0.25" | bc`
     lat2=`echo "$lat - 0.25" | bc`
     lon1=`echo "$lon + 0.25" | bc`
     lon2=`echo "$lon - 0.25" | bc`

     cdo sellonlatbox,$lon2,$lon1,$lat2,$lat1 $WD/pre_year180_mm_ho.nc $WD/'tmp_preho.nc'
     cdo outputtab,lat,lon,year,value $WD/'tmp_preho.nc' > $WDU/$id'_pre_obs.txt'

     sed -i '/^#/d' $WDU/$id'_pre_obs.txt'
     sed -i 's/ \{2,\}/,/g' $WDU/$id'_pre_obs.txt'
     sed -i 's/,/ /g' $WDU/$id'_pre_obs.txt'
     rm $WD/tmp_*
     
done < $WD/crd_wcentr.txt


