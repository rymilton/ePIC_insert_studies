#!/usr/bin/bash

me=$(basename -- "$0")
if [ $# -lt 1 ]; then
    echo "No input file provided"
    echo "$me input_file [output_prefix] [output_suffix]"
    exit 1
fi

input_file=$1
if ! [ -f $input_file ]; then
    echo "Input file doesn't exist: $input_file"
    exit 2
fi

output_prefix=djangoh
if [ $# -ge 2 ]; then
    output_prefix=$2
fi

output_suffix=tmp
if [ $# -ge 3 ]; then
    output_suffix=$3
fi

ftmp=${input_file%.in}_${output_suffix}.in
if [ -f $ftmp ]; then 
    echo "tmp file ${ftmp} already exist, please remove it"
    exit 3
fi
cp $input_file $ftmp
input_file=$ftmp
output_name=$(grep -A1 'OUTFILENAM' $input_file | tail -n1)
output_name=$(basename $output_name)
sed -i "s/$output_name/${output_prefix}_${output_suffix}/" $input_file
output_name=$(grep -A1 'OUTFILENAM' $input_file | tail -n1)

export LHAPDF5='/cvmfs/eic.opensciencegrid.org/gcc-8.3/opt/fun4all/core/lhapdf-5.9.1/'
export LHAPATH='/cvmfs/sft.cern.ch/lcg/external/lhapdfsets/5.9.1/share/PDFsets'
export LD_LIBRARY_PATH="$LHAPDF5/lib":$LD_LIBRARY_PATH

echo "-----------------------------------"
echo "Running DJANGOH Simulation for ep Collider!!!"
echo "-----------------------------------"

OUTFILE1=${output_name}_evt.dat
OUTFILE2=${output_name}_out.dat
OUTFILE3=${output_name}_smp.dat
for f in "$OUTFILE1" "$OUTFILE2" "$OUTFILE3"; do
    if test -f "$f"; then
	rm -f "$f"
    fi
done

WORKDIR='/gpfs02/eic/wbzhang/epic/hcal_insert/condor/'
bin_dir='/gpfs02/eic/wbzhang/epic/hcal_insert/djangoh/'
pushd $WORKDIR
$bin_dir/djangoh < "$input_file" 

echo "Completed Simulation!!!"
rm $input_file
popd
