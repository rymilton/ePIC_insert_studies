#!/usr/bin/bash

CONDOR='/gpfs02/eic/wbzhang/epic/hcal_insert/condor/'

me=$(basename -- "$0")
if [ $# -lt 2 ]; then
    echo -e "FATAL:\tNo input_file/num_events provided"
    echo "Usage:"
    echo "$me input_file num_events"
    exit 1
fi

input_file=$1
if ! [ -f $input_file ]; then
    echo -e "ERROR:\tInput file doesn't exist: $input_file"
    exit 2
fi
input_file=$(realpath $input_file)
prefix=${input_file%.dat}

num_events=$2

compact_file=$CONDOR/epic_brycecanyon.xml
if [ $# -ge 3 ]; then
    compact_file=$(realpath $3)
fi

outputDir=''
if [ $# -eq 4 ]; then
    outputDir=$(realpath $4)
    prefix=${outputDir}/$(basename $prefix)
fi

echo -e "INFO:\tinput file -- ${input_file}
\tnumber of events -- ${num_events}
\tcompact file -- ${compact_file}
\toutput directory -- ${outputDir}"


#-------------------------------------------------------
echo -e "INFO:\tMaking hepmc file from input: ${input_file}"
export PATH="/gpfs02/eic/wbzhang/epic/local/bin:$PATH"
export LD_LIBRARY_PATH="/gpfs02/eic/wbzhang/epic/local/lib:$LD_LIBRARY_PATH"
abconv_file="${prefix}_abconv.hepmc"
if [ -f $abconv_file ]; then
    echo -e "INFO:\thepmc file already exist: $abconv_file, skip this step"
else
    root -l -q  "${CONDOR}/analysis.C(\"$input_file\")"
    hepmc_file="${input_file%.dat}.hepmc"
    abconv -o ${prefix}_abconv $hepmc_file
fi

#-------------------------------------------------------
echo -e "INFO:\tRunning simulation"
# source /opt/detector/epic-23.09.0/setup.sh
source /opt/detector/epic-nightly/setup.sh
sim_file="${prefix}.edm4hep.root"
if [ -f $sim_file ]; then
    echo -e "INFO:\tSim file already exist: $sim_file, skip this step"
else
    ddsim --compactFile ${compact_file} --numberOfEvents ${num_events} --inputFiles ${abconv_file} --outputFile ${sim_file} 
    if [ $? -ne 0 ]; then
	echo -e "ERROR:\tfail to run ddsim, please check it"
	exit 4
    fi
fi

echo -e "INFO:\tRunning Reconstruction"
reco_file="${prefix}_reco.root"
if [ -f $reco_file ]; then
    echo -e "INFO:\treco file already exist: $reco_file, skip this step"
else
eicrecon \
-Ppodio:output_file=${reco_file} \
-Pjana:nevents=${num_events} \
-Pdd4hep:xml_files=${compact_file} \
${sim_file} 

    if [ $? -ne 0 ]; then
	echo -e "ERROR:\tfail to run eirrecon, please check it"
	exit 4
    fi
fi

echo -e "INFO:\tDone!!!"
