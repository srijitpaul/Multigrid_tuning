#!/bin/bash -l


#SBATCH -p debug
#SBATCH -N 12
#SBATCH -C haswell
#SBATCH -t 30:00
#SBATCH -J 384_4c6_haswell_mg 
#SBATCH -o 2_4c6_384.out 
#SBATCH -e 2_4c6_384.err 


srun -n 384  ./qlua_cori  plaquette.qlua load_gauge_field.qlua stout_smear.qlua 2.qlua 

