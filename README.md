# MARCS
Probabilistic hydrological model MARKov Chain System:  application to Finland (Shevnina et al., 2018: 10.13140/RG.2.2.19380.55681)
# General Description
This setup of the model includes the code on Python and CDO driving by BASH scripts. There are four blocks of the code: 

model_core.py includes the model core version 0.3 (Shevnina and Silaev, 2018: https://doi.org/10.5194/gmd-2018-108);

model_setup.py includes calculation of the annual specific discharges (mm yr-1) from the datafiles of GRDC;

timeseries_meteo.sh includes cdo script to extract the yearly precipitation time series from the CMIP5 climate projections (RCP26, RCP45 and RCP 85) and the climatology of NOAA dataset for the period of 1990-2014. The time series are extracted at the grid node nearest to a watershed centroide (crd_wcentr.txt);

timeseries_meteo_regional.sh includes cdo script to extract the mean precipitation for the lon/lat box covering Finland from the CORDEX climate projection of the RCM4 model under RCP26, RCP45 and RCP 85;


Results:
pvm_GRDC.zip includes the yearly time series extracted from the GRDC dataset;
reference_climate.zip includes the yearly values from the monthly values using the data by NOAA: precip.mon.total.v401.nc;

