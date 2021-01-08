##  MARCS:HYDRO v1.2
## contribution from AFEC project: Jan,20212 to ...

(e.shevnina, t.vihma)
# Introduction 


## data by 15.01.2021
# hydrological observations

In our study we used two collections of the water discharches (daily and monthly) distributed by Global Discharge Dataset ( https://www.bafg.de/GRDC/EN/01_GRDC/grdc_node.htm), specifically  the data collected in gauges located on rivers not disturbed by human activity such us runoff regulation nor land cover changes ( https://www.bafg.de/GRDC/EN/04_spcldtbss/46_CSS/css_node.html). The gauges are mostly located in France and nearby regions, UK, Iceland, Sweden and Finland. Thefore, we additionally used the data provided by the RActic dataset (https://www.bafg.de/GRDC/EN/04_spcldtbss/41_ARDB/ardb_node.html)  to include river catchments located in the Russian Federation.

TV: How about Ukraine, Belorus and the Baltic countries? 

TV: Are they not included in the data set of pristine rivers?

ES: " I would need a couple of weeks to explore the RArctic data, then it would be possible to have an overview of the data available for the further analyses. " by 4.01.2021


Further, we selected the gauges on river catchment area within the appropriate scale: from 1000 km2 (to skip off local scale features on small catchments) to 50000 km2 (to miss out big catchments with the hydrological regime affected by global scale features). 
I am not convinced that we should exclude catchments larger than 50 000 km2. An area as small as 200 km x 250 km already makes 50 000 km, which is much smaller than a typical radius of a synoptic-scale cyclone. I agree that analysis addressing discharge of a very large river may be challenging, as inter-annual variations in atmospheric circulation, moisture transport and precipitation may be different in different parts of the river basin, but I think it should still be possible to discover the net effect of meteorological factors to discharge. Further, the map of pristine basins at https://www.bafg.de/GRDC/EN/04_spcldtbss/46_CSS/css_node.html
seems not include very large river basins. Shouldn’t we rather select such rivers that represent a reasonable population of important (large discharge) rivers in different parts of Europe. 


Perhaps no more than 4 rivers from France, 3 from UK, 4 from Finland, 3/3 Norway/Sweden, 3 from Iceland, 3 Baltic contrries ...
all those that are in the map in other European countries.... 10 from Russia. 


## methods
2.  “beta criterion” method (Kovalenko, 2004) needs to be implemented to the block of data analysis. 


## References 


