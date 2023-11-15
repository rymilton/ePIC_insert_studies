#!/bin/bash
me=$(basename -- "$0")
WORKDIR=`pwd`

usage(){
    echo "${me} 
    --help		    show this help message
    --numberOfJobs N	    number of jobs
    --numberOfProcesses N   number of processes per job
    --numberOfEvents N      number of events in each job process 
    --inputCard input_file  input card for djangoh
    --outputPrefix prefix   prefix for output file
    "
}

# Input simulation parameters
OPTIONS=$(getopt --options h --longoptions  \
numberOfJobs:,\
numberOfProcesses:,\
numberOfEvents:,\
inputCard:,\
outputPrefix:,\
help \
--name "${me}" \
-- "$@")
if [ $? != 0 ] ; then echo "Terminating..." >&2 ; exit 1 ; fi

eval set -- "$OPTIONS"

numberOfJobs=1
numberOfProcesses=1
numberOfEvents=1000
inputCard="btest10x100.R_sph=2.5_inelas.in"
outputPrefix=djangoh

while true; do
    case "$1" in
	-h | --help)	    usage;	exit 0 ;;
	--numberOfJobs)	    numberOfJobs="$2";	    shift 2 ;;
	--numberOfProcesses)numberOfProcesses="$2"; shift 2 ;;
	--numberOfEvents)   numberOfEvents="$2";    shift 2 ;;
	--inputCard)	    inputCard="$2";	    shift 2 ;;
	--outputPrefix)	    outputPrefix="$2";	    shift 2 ;;
	--) shift; break ;;
	*) break ;;
    esac
done

for (( i=1; i<=${numberOfJobs}; i++ ))
do
    CONDOR_JOB=condor_${i}.job
    [ -f $CONDOR_JOB ] && rm $CONDOR_JOB
    cat << END >> ${CONDOR_JOB}
Universe        = vanilla
Notification    = Never
Executable      = ${WORKDIR}/djangoh.sh
Arguments       = $(realpath $inputCard) ${outputPrefix} \$(ClusterID)_\$(ProcID)
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
Queue ${numberOfProcesses}
END
    condor_submit ${CONDOR_JOB}
done
