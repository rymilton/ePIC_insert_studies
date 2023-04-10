#!/bin/bash

# Input simulation parameters
particle="e-"
beam_energy=1
num_events=1000
theta=3.459 # in degrees

# Output file names
info_string="${particle}_${beam_energy}GeV_theta_${theta}deg"
hepmcfile="input/gen_${info_string}.hepmc"

# Generating hepmc file
root -l -b -q "input/gen_particles.cxx(\
${num_events},\
\"${hepmcfile}\",\
\"${particle}\",\
${theta},\
${theta},\
0,\
360,\
${beam_energy})"


#If you want to run EICRecon only, comment npsim part and uncomment soft links

source /opt/detector/setup.sh

mkdir -p "output"

#Run 1
echo "Running simulation !!!"
#Simulation
npsim --compactFile $DETECTOR_PATH/epic_brycecanyon.xml --numberOfEvents ${num_events} --inputFiles ${hepmcfile} --outputFile output.edm4hep.root | tee dd4hep_out.dat

#ln -s output/output.gen_${particle}_1GeV_theta_2.83deg.edm4hep.root output.edm4hep.root

#Reconstruction: Full output, scaled
eicrecon \
-Ppodio:output_file=eicrecon_out.root \
-Pjana:nevents=${num_events} \
-Pdd4hep:xml_files=epic_brycecanyon.xml \
output.edm4hep.root | tee eicrecon_out.dat

#unlink output.edm4hep.root

mv output.edm4hep.root output/output.gen_${info_string}.edm4hep.root
mv eicrecon_out.root   output/eicrecon_out.gen_${info_string}.root
