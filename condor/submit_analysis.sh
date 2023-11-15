#!/bin/bash
me=$(basename -- "$0")
CONDOR=$(realpath $(dirname -- "$0"))
WORKDIR=`pwd`

usage(){
    echo "${me} 
    --help		    show this help message
    --numberOfEvents N	    number of events to be precess
    --compactFile f	    compactFile
    --outputDir	dir	    
    list of input files
    "
}

# Input simulation parameters
OPTIONS=$(getopt --options h --longoptions  \
numberOfEvents:,\
compactFile:,\
outputDir:,\
help \
--name "${me}" \
-- "$@")
if [ $? != 0 ] ; then echo "Terminating..." >&2 ; exit 1 ; fi

eval set -- "$OPTIONS"

numberOfEvents=0
compactFile=''
outputDir=''

while true; do
    case "$1" in
	-h | --help)	    usage;	exit 0 ;;
	--numberOfEvents)   numberOfEvents=$2;	    shift 2 ;;
	--compactFile)	    compactFile=$(realpath $2);	    shift 2 ;;
	--outputDir)	    outputDir=$(realpath $2);	    shift 2 ;;
	--) shift; break ;;
	*) break ;;
    esac
done

if ! [ $numberOfEvents -gt 0 ]; then
    echo -e "FATAL:\tno number of events specified"
    usage
    exit 2
fi

if [ -z "$compactFile" ] && ! [ -z "$outputDir" ]; then
    echo "compact file is needed if outputDir is specified"
    exit 3
fi


let i=1
for f in $@; do
    input_file=$(realpath $f)
    CONDOR_JOB=condor_${i}.job
    [ -f $CONDOR_JOB ] && rm $CONDOR_JOB
    cat << END >> ${CONDOR_JOB}
Universe        = vanilla
Notification    = Never
Executable      = ${CONDOR}/run_eic.csh
Arguments       = ${CONDOR}/analysis.sh ${input_file} $numberOfEvents $compactFile $outputDir
Requirements    = (CPU_Speed >= 2)
Rank		= CPU_Speed
request_memory  = 2GB
request_cpus    = 1
Priority        = 20
GetEnv          = False
Initialdir      = ${WORKDIR}
# Input         = ${ROOTDIR}/backwards_insert.xml
# transfer_input_files = file1,file2
Output          = \$(ClusterID)_\$(ProcID).out
Error           = \$(ClusterID)_\$(ProcID).err
Log             = \$(ClusterID)_\$(ProcID).log
should_transfer_files = YES
when_to_transfer_output = ON_EXIT_OR_EVICT
PeriodicHold    = (NumJobStarts >= 1 && JobStatus == 1)
Notify_user     = weibinz@ucr.edu
Queue 1
END
    condor_submit ${CONDOR_JOB}
    let i++
done
