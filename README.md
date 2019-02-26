# MARCS
Probabilistic hydrological model MARKov Chain System:  application to Finland (Shevnina et al., 2018: 10.13140/RG.2.2.19380.55681)
### General Description
This setup of the model includes the code on Python and CDO driving by BASH scripts. There are four blocks of the code: 

model_core.py includes the model core version 0.3 (Shevnina and Silaev, 2018: https://doi.org/10.5194/gmd-2018-108);

model_setup.py includes calculation of the annual specific discharges (mm yr-1) from the datafiles of GRDC;

model_crossvalidation.py includes the procedure of hindcasting according to Shevnina et al., 2017; Kovalenko, 1993;

timeseries_meteo.sh includes cdo script to extract the yearly precipitation time series from the CMIP5 climate projections (RCP26, RCP45 and RCP 85) and the climatology of NOAA dataset for the period of 1990-2014. The time series are extracted at the grid node nearest to a watershed centroide (crd_wcentr.txt);

timeseries_meteo_regional.sh includes cdo script to extract the mean precipitation for the lon/lat box covering Finland from the CORDEX climate projection of the RCM4 model under RCP26, RCP45 and RCP 85;


### Results:
pvm_GRDC.zip includes the yearly time series extracted from the GRDC dataset;

reference_climate.zip includes the yearly values from the monthly values using the data by NOAA: precip.mon.total.v401.nc;

regional_climate_forcing.csv includes the delta corrected mean values of annual precipitation (mm yr-1) extracted from the regional climate model RCA4 of the MPI-ESM-LR (Standberg et al., 2014) for the RCP26, RCP45 and RCP85 climate scenarios;

global_climate_forcing.csv includes the delta corrected mean values of annual precipitation (mm yr-1) extracted from the global climate models HadGEM2-ES (Collins et al., 2011) and MPI-ES-LR (Giorgetta et
al., 2013) under and three Representative Concentration Pathways (RCP26, RCP45 and RCP85) scenarios;
 
ModelCrossvalidationRes.txt includes the results of the model validation with the basic parameterization scheme

model_output_global.txt includes the mean and 10/90% extremes of annual runoff rate (mm yr-1) simulated from the forcing of the global model MPI-ESM-LR (one model grid point per catchment). 

model_output_regional.txt includes the mean and 10/90% extremes of annual runoff rate (mm yr-1) simulated from the forcing of the regional model RCA4 of the MPI-ESM-LR (several grid points per catchment).

### GIS layers and coordinates:

catchment_att.zip includes the boundary for 12 Finnis river according to the GRDC;

crd_wcentr.txt includes the coordinates of the watersheds’ centroids calculated from the polygons of river basins; 

valu1005120800383_453212_7191507.zip includes the catchment of Oulunjoki at Leppiniemi (Montta hydropower plant)





