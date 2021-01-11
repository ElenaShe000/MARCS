##  MARCS:HYDRO v1.2
## contribution from AFEC project: Jan,20212 to ...

(e.shevnina, t.vihma, a.karpechko)
# Introduction 

Humans traditionally use water of lakes and rivers in energy production. The hydropower generation is among others social activities highly related to weather phenomena and hydrological regime of the rivers and lakes. The risks of in the hydropower generation is in close relation to hydrological events of rare occurrence (or extreme). The hydrological extremes (including floods and drought) are traditionally estimated from time series of the lake level and/or river water discharge observed at a network of gauges. The hydrological observation are mostly launched in begging of the last century, and almost until end of 1990s, no significant trend are observed in the hydrological time series. It allows to apply statistical methods of the frequency analyse (XX) while estimating the hydrological events of rare occurrence, i.e. the floods happened once per 10, 100, or 1000 years. The exceedance probability curves of yearly maximum river runoff provides whole information to assessment of the risks connected to extreme floods in a particular hydropower construction (XX;XX; Shevnina, 2014; Kovalenko, 2004).
Since late 1990s, the statistically significant trends are detected in many time series of yearly average, maximal and minimal river discharges (XXX; XXX; XXX). ... These trends are connected either human activities (water regulation; change of a land cover) and/or natural fluctuations in weather and climate patterns, however they limit the application of the frequency analyses due to a stationarity hypothesis (XX;XX). In the stationary climate, the hydrological risks are evaluated from the observations. In changing climate, the risks are usually evaluated with hydrological models relayed on projections of meteorological parameters for the near future. 


## data by 15.01.2021
# hydrological observations
In our study we used two collections of the water discharches (daily and monthly) distributed by Global Discharge Dataset ( https://www.bafg.de/GRDC/EN/01_GRDC/grdc_node.htm), specifically  the data collected in gauges located on rivers not disturbed by human activity such us runoff regulation nor land cover changes ( https://www.bafg.de/GRDC/EN/04_spcldtbss/46_CSS/css_node.html). The gauges are mostly located in France and nearby regions, UK, Iceland, Sweden and Finland. Thefore, we additionally used the data provided by the RActic dataset (https://www.bafg.de/GRDC/EN/04_spcldtbss/41_ARDB/ardb_node.html)  to include river catchments located in the Russian Federation.

TV: How about Ukraine, Belorus and the Baltic countries? 

TV: Are they not included in the data set of pristine rivers?

ES: " I would need a couple of weeks to explore the RArctic data, then it would be possible to have an overview of the data available for the further analyses. " by 4.01.2021

AK by 11.01.2021: "I am also not convinced that we should restrict ourselves to catchments smaller than 50000 km2. Yes, river gauges located downstream of large catchment areas will be affected by processes occurring over large areas which may complicate understanding of the processes. For example, there may be compensation between increased precipitation in one region and decreased precipitation in another region leading to no signal in the river discharge downstream. However it will still be interesting to relate river discharge data to certain types of circulation. Maybe even river gauges from the same catchment area but located in different parts of the catchment will show different signals, which is still interesting I think. To me more important criteria should be the length of the gauge data. It’s pity there is no data after 2014."



Further, we selected the gauges on river catchment area within the appropriate scale: from 1000 km2 (to skip off local scale features on small catchments) to 50000 km2 (to miss out big catchments with the hydrological regime affected by global scale features). 
I am not convinced that we should exclude catchments larger than 50 000 km2. An area as small as 200 km x 250 km already makes 50 000 km, which is much smaller than a typical radius of a synoptic-scale cyclone. I agree that analysis addressing discharge of a very large river may be challenging, as inter-annual variations in atmospheric circulation, moisture transport and precipitation may be different in different parts of the river basin, but I think it should still be possible to discover the net effect of meteorological factors to discharge. Further, the map of pristine basins at https://www.bafg.de/GRDC/EN/04_spcldtbss/46_CSS/css_node.html
seems not include very large river basins. Shouldn’t we rather select such rivers that represent a reasonable population of important (large discharge) rivers in different parts of Europe. 


TV by 07.01.2021: "Perhaps no more than 4 rivers from France, 3 from UK, 4 from Finland, 3/3 Norway/Sweden, 3 from Iceland, 3 Baltic contrries ... all those that are in the map in other European countries.... 10 from Russia." 

# meteorological observations

reference SYNOP stations... 




# meteorological reanalyses 

TV by 7.01.2021: "Tuomas wrote that he has already downloaded ERA5 data on Z200, Z500, precipitation and evaporation. I guess from 1979 to almost present."

AK by 11.01.2021: "The reanalysis before 1979 may be not as good as that after 1979 but it does not necessarily mean that these data is not useful. I’ve never studied how the quality of reanalyses drops before 1979, perhaps there are studies that are relevant for us? But I would expect that at least large-scale circulation should be reasonably well constrained in the Northern hemisphere also before 1979. Of course the amount of reanalysis data that would need to be downloaded can be large, which is another issue." 




## methods
2.  “beta criterion” method (Kovalenko, 2004) needs to be implemented to the block of data analysis. 


## References 

hydrological datasets:
grided... Ghiggi, G., Humphrey, V., Seneviratne, S. I., and Gudmundsson, L.: GRUN: an observation-based global gridded runoff dataset from 1902 to 2014, Earth Syst. Sci. Data, 11, 1655–1674, https://doi.org/10.5194/essd-11-1655-2019, 2019. 
pointed... 

EU hydropower: Bergström,  S.,  Andréasson,  J.,  Veijalainen,  N.,  Vehviläinen,  B.,  Einarsson,  B.,  Jónsson,   S.,   Kurpniece,   L.,   Kriaučiūnienė   ,   J.,   Meilutytė-Barauskienė,   D.,   Beldring, S., Lawrence, D. & Roald, L. 2012. Modelling climate change impacts on the hydropower system. In: Thorsteinsson, T. & Björnsson, H. (Eds.). Climate Change  and  Energy  Systems:  Impacts,  Risks  and  Adaptation  in  the  Nordic  and  Baltic    Countries.    TemaNord    2011:502.    Nordic    Council    of    Ministers,    Copenhagen. pp. 113–146

EU Lakes: Blenckner,   T.,   Adrian,   R.,   Arvola,   L.,   Järvinen,   M.,   Nõges,   P.,   Nõges,   T.,   Pettersson,  K.  &  Weyhenmeyer,  G.A.  2010.  The  Impact  of  Climate  Change  on  Lakes  in  Northern  Europe.  In:  George,  G.  (Ed.)  The  Impact  of  Climate  Change  on European Lakes. Springer, Dordrecht. pp. 339–358. 

precipitation variability: Busuioc,  A.,  Chen,  D.  &  Hellström,  C.  2001.  Temporal  and  spatial  variability  of  precipitation in Sweden and its link with the large scale atmospheric circulation. Tellus A 53(3), 348–367.

Danilovich, I., Wrzesínski, D. & Nekrasova, L. 2007. Impact of the North Atlantic Oscillation  on  river  runoff  in  the  Belarus  part  of  the  Baltic  Sea  basin.  Nordic Hydrology 38(4-5), 413–423.

Hodgkins,  G.A.,  Whitfield,  P.H.,  Burn,  D.H.,  Hannaford,  J.,  Renard,  B.,  Stahl,  K.,  Fleig,  A.K.,  Madsen,  H.,  Mediero,  L.,  Korhonen,  J.,  Murphy,  C.  &  Wilson,  D.  2017.  Climate-driven  variability  in  the  occurrence  of  major  floods  across  North  America and Europe. Journal of Hydrology 552, 704–717. 

Korhonen, J. & Kuusisto, E. 2010. Long-term changes in the discharge regime in Finland. Hydrology Research41(3-4), 253–268.

Veijalainen, N., Korhonen, J., Vehviläinen, B. & Koivusalo, H. 2012. Modelling and statistical analysis of catchment water balance and discharge in Finland in 1951–2099 using transient climate scenarios. Journal of Water and Climate Change3(1), 55–78. 

