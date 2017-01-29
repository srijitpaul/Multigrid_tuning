#!/bin/bash -l


#SBATCH -p debug
#SBATCH -N 8
#SBATCH -C haswell
#SBATCH -t 30:00
#SBATCH -J 256_4c4_haswell_mg 
#SBATCH -o 4_4c4_256.out 
#SBATCH -e 4_4c4_256.err 


srun -n 256  ./qlua_cori  plaquette.qlua load_gauge_field.qlua stout_smear.qlua 4.qlua 

