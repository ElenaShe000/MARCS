# MARCS:HYDRO v1.2
## Story
Probabilistic hydrological model MARKov Chain System: hydrology (MARCS:HYDRO) is started in 2015 within version 0.1 (Shevnina, 2015). The model includes six blocks to separate the tasks into groups. There are two blocks to analysis and screening of observed data, the block with the model parametrization, cross-validation and hind casts (Shevnina et al., 2017), the block to visualize model’s results and the block with socio-economic applications (Shevnina and Gaidukova, 2017). In the version 0.1 (annex to Shevnina et al., 2017), the set of codes with mix computer's languages are used in the blocks, which are connected by a bash script.  
The MARCS:HYDRO model version 0.1 is used on a regional scale studies on floods (Shevnina, 2015; Shevnina et al., 2017), it needs to be improved in many sences. The model core version 0.2 is introduced in (Shevnina and Silaev, 2018).

## Basic approach and limitations
An Advanced of Frequency Analysis (AFA) method is introduced by Kovalenko (1993) relying on a theory of stochastic
systems (Pugachev et al., 1974). The basic idea behind the method is to calulate statistical estimators of multi-year
runoff (annual, minimal and maximal) from statistical estimators of precipitation and air temperature on a climate scale. The  calculated non-central momements' estimates are then futher applied to construct exceedance probability curve
(EPC) with distributions from the Pearson System (1895). The Pearson Type III distribution is among others transitional distributions used in water engineering (Rogdestvenskiy and Chebotarev,1974; Matalas and Wallis, 1973; Sokolovskiy, 1964). 
Recently, the model application is limited by only a prediction on the climate scale. The MARCS HYDRO model simulates three non-central statistical moments of multi-year runoff based on means of precipitation calculated over a period of 20–30 years The AFA approach have found the practical applications to the building constructions (Shevnina et al., 2017; Kovalenko, 2009).

## Place among others hydrological models
Long-term plannig on a socio-economic development needs for a climate scale prediction of water resources and exreme runoff events such as floods and drougths. The main feature of the MARCS:HYRRO model is a close connection to water engineering due to probabilistic form of runoff projection in combination with low computational costs. it allows to "express analysis" of water extremes according to a new generation of climate projections. 

## To be implemented 
The implementation of the regional oriented parametrization scheme (Shevnina, 2011) is our next step further. Also, a “beta criterion” method (Kovalenko, 2004) needs to be implemented to the block of data analysis. The model development is limited by 6 months a year. 

## References
Kovalenko, V. V.: Modelling of hydrological processes, Gidrometeizdat, St. Petersburg, Russia, 1993. (In Russian).
Kovalenko, V.V.: Hydrological security of building projects with climate change, Russian State Hydrometeorological
University Press, St. Petersburg, Russia, 2009. (In Russian)
Pugachev, V.S., Kazakov, I.E. and Evlanov, L.G.: Basics of statistical theory of automatic system, Mashinostroenie, Moscow,
USSR, 1974. (In Russian).
Pearson, K.: Contributions to the mathematical theory of evolution, II: Skew variation in homogeneous material. Philosophi-
cal Transactions of the Royal Society, 186, 343–414, doi:10.1098/rsta.1895.0010, 1895.
Shevnina, E.: Long-term assessment of the multi-year statistical characteristics of the maximal runoff under the climate
change over the Russian Arctic, Doctor of science thesis, Russian State Hydrometeorological University, Russia, 355 pp.,
2015. (in Russian).
Shevnina, E., Kourzeneva, E., Kovalenko, V., and Vihma, T.: Assessment of extreme flood events in a changing climate for a
long-term planning of socio-economic infrastructure in the Russian Arctic, Hydrol. Earth Syst. Sci., 21, 2559-2578,
doi:10.5194/hess-21-2559-2017, 2017.
Shevnina, E. and Gaidukova E.V.: Hydrological probabilistic model MARCS and its application to simulate the probability
density functions of multi-year maximal runoff: the Russian Arctic as a case of study, in: The Interconnected Arctic, Springer International Publishing, 77–87, doi: 10.1007/978-3-319-57532-2_8, 2017.
Shevnina E & Silaev A. 2018. The probabilistic hydrological model MARCS (MARkov Chain System): the theoretical basis for the core version 0.2, doi: 10.5194/gmd-2018-108.

