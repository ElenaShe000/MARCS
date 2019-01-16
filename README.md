# MARCS
Probabilistic hydrological model MARKov Chain System:  application to Finland (Shevnina et al., 2018: 10.13140/RG.2.2.19380.55681)
# General Description
This setup of the model includes the code on Python and CDO driving by BASH scripts. There are four blocks of the code: 

the model_core.py includes the model core version 0.3 (Shevnina and Silaev, 2018: https://doi.org/10.5194/gmd-2018-108);

the model_setup.py includes calculation of the annual specific discharges (mm yr-1) from the datafiles of GRDC;

the reference_climate.sh includes the bash/cdo script to calculate the yearly values from the monthly values using the data by NOAA: precip.mon.total.v401.nc [sm/month] and air.mon.mean.v401.nc [degC];
