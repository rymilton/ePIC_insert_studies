#!/bin/bash

#If you want to run EICRecon only, comment npsim part and uncomment soft links

source /opt/detector/setup.sh

numevents=1000
particle="e-"
energy=1
angle=3.459
mkdir -p "output"

#Run 1
echo "Running simulation!!!"
#Simulation
npsim --compactFile $DETECTOR_PATH/epic_brycecanyon.xml --numberOfEvents ${numevents} --inputFiles input/gen_${particle}_${energy}GeV_theta_${angle}deg.hepmc --outputFile output.edm4hep.root | tee dd4hep_out.dat

#ln -s output/output.gen_${particle}_1GeV_theta_2.83deg.edm4hep.root output.edm4hep.root

#Reconstruction: Full output, scaled
eicrecon \
-Ppodio:output_file=eicrecon_out.root \
-Pjana:nevents=${numevents} \
-Pdd4hep:xml_files=epic_brycecanyon.xml \
output.edm4hep.root | tee eicrecon_out.dat

#unlink output.edm4hep.root

mv output.edm4hep.root output/output.gen_${particle}_${energy}GeV_theta_${angle}deg.edm4hep.root
mv eicrecon_out.root   output/eicrecon_out.gen_${particle}_${energy}GeV_theta_${angle}deg.root
