# Physics studies

Djangoh generator files
-----------------------
[Djangoh](https://eic.github.io/software/djangoh.html) events in HepMC3 format which have been passed through the [beam effects afterburner](https://eicweb.phy.anl.gov/monte_carlo/afterburner):

|Data Set| Generator | Beam Energies     | Run Information                                                                   | Link to file     |
|:-------|:---------:|:-----------------:|:---------------------------------------------------------------------------------:|:----------------:|
|1       | Djangoh   | 18x275  GeV e-p   | Q<sup>2</sup> > 100 GeV<sup>2</sup>; NC unpolarized; QED Radiation OFF            | [HepMC3 File](https://drive.google.com/file/d/1AQrfj1LakfrXk8pyBPKdfzNyX_WGTK-N/view?usp=sharing) |
|2       | Djangoh   | 10x100  GeV e-p   | Q<sup>2</sup> > 0.5 GeV<sup>2</sup>; NC unpolarized; QED Radiation OFF            | [HepMC3 File](https://drive.google.com/file/d/1Y-oWOc9stiJftt6GbBOAcO9VXUp4v2vB/view?usp=sharing)                                     | 
|3       | Djangoh   | 10x100  GeV e-p   | Q<sup>2</sup><sub>e</sub> > 0.5 GeV<sup>2</sup>; NC unpolarized; QED Radiation ON | [HepMC3 File](https://drive.google.com/file/d/1SMYbVowTzud8wIQfMRO21GQrkXJ4JRV6/view?usp=sharing) |

Detector simulation output
-------------------------
The analysis code in this directory uses the ROOT file found [here](https://drive.google.com/file/d/1zQ_mjz8uCLJOpF909LgTZn0xyOhhRpwP/view?usp=sharing) as input. This ROOT file was produced by running the 18x275 GeV <i>Djangoh</i> events listed in the above table through the hadron endcap calorimeter standalone DD4Hep simulation [here](https://github.com/rymilton/eic_endcap_insert).
