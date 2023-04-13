# ePIC_insert_studies
This repository focuses on the studies of the hadronic endcap (forward endcap) insert in the [official ePIC simulations](https://github.com/eic/epic). For our previous studies and a description of the detector, see our [publication](https://www.sciencedirect.com/science/article/pii/S0168900222011585?via%3Dihub).

### Note to contributors
Feel free to add anything you find useful/relevant for these studies. But please stay organized (tried to make good directories) and include helpful commit messages, files with descriptive titles, and code with good comments.

## Prerequisites
* [eic-shell](https://github.com/eic/eic-shell)
  * Contains all the software needed for these simulation studies, including the ePIC simulation model, npsim, and EICrecon.
 ## Getting started
 1. Clone this repository
 2. Enter eic-shell
 3. Can now do data generation, simulation, and analysis (see below)

## Data generation
Due to the lack of official ePIC data in the insert region (3 < &eta; < 4), we are generating our own. This is done with `input/gen_particles.cxx`. This code generates a hepmc file of single-particles generated along the hadron beam axis (contains a rotation from the electron beam axis to hadron beam axis). Currently, only single-particle hepmc files are being generated.
### Scripts
The generation can be done with `input/generate_input.sh` and `gen_and_sim_brycecanyon.sh` (latter in combination with simulation and reconstruction).

## Simulation and reconstruction
The generated hepmc files can now be fed into `npsim` and the ePIC model to simulate the propagation of the single particles through the ePIC detector (uses Geant4).

Steps:
1. `source /opt/detector/setup.sh` to load the ePIC detector model.
2. `npsim --compactFile $DETECTOR_PATH/epic_brycecanyon.xml --numberOfEvents ${num_events} --inputFiles ${hepmcfile} --outputFile output.edm4hep.root`
3. `eicrecon -Ppodio:output_file=eicrecon_out.root -Pjana:nevents=${num_events} -Pdd4hep:xml_files=epic_brycecanyon.xml output.edm4hep.root`

#2 starts the simulation. `epic_brycecanyon.xml` is the XML file of the ePIC system including the insert. **Do not use arches**. There is no insert in arches. The `${hepmcfile}` in `--inputFiles ${hepmcfile}` option should be the file created during data generation.

#3 takes the output npsim/Geant4 file and feeds it to [EICrecon](https://github.com/eic/EICrecon). The last argument is the input file from step #2.

### Scripts
This simulation can be done with `run_sim_brycecanyon.sh` or `gen_and_sim_brycecanyon.sh` (latter in combination with data generation). Note these scripts will move your output files to a directory `output`. **If files with the same name exist in the output directory, they will be overwritten.**

## Analysis
The analysis directory contains analysis code for both validation and physics studies. Analysis code should be in ROOT, Python, or Jupyter notebooks. To promote collaboration and easy accessibility, Jupyter notebooks are encouraged.

## Results
This directory should contain relevant plots and files completed during these studies. Any presentations made on these studies should also be put here.
