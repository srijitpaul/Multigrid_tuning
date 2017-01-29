#!/bin/bash -l

filelocation=$1

qlua_filename=$2

nodes=$3

cores=$4

sed '5s/.*/#SBATCH -N '$nodes'/' mg_edison.sh > $filelocation/node.sh
sed '8s/.*/#SBATCH -J '$cores'_'$filelocation'_edison_mg /' $filelocation/node.sh > $filelocation/job_name.sh
sed '9s/.*/#SBATCH -o '$qlua_filename'_'$filelocation'_'$cores'.out /' $filelocation/job_name.sh > $filelocation/out.sh
sed '10s/.*/#SBATCH -e '$qlua_filename'_'$filelocation'_'$cores'.err /' $filelocation/out.sh > $filelocation/err.sh
sed '13s#.*#srun -n '$cores'  ./qlua_edison  plaquette.qlua load_gauge_field.qlua stout_smear.qlua '$qlua_filename'.qlua #' $filelocation/err.sh > $filelocation/${qlua_filename}_${filelocation}_${cores}.sh
rm $filelocation/node.sh
rm $filelocation/job_name.sh
rm $filelocation/out.sh
rm $filelocation/err.sh
