#!/bin/bash -l


#SBATCH -p debug
#SBATCH -N 8
#SBATCH -t 30:00

#SBATCH -J haswell_mg
#SBATCH -o mg.out
#SBATCH -e mg.err


srun -n $((64*8))  ./qlua_edison  plaquette.qlua load_gauge_field.qlua stout_smear.qlua mg_test_knl.qlua

