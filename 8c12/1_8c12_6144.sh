#!/bin/bash -l


#SBATCH -p debug
#SBATCH -N 192
#SBATCH -C haswell
#SBATCH -t 30:00
#SBATCH -J 6144_8c12_haswell_mg 
#SBATCH -o 1_8c12_6144.out 
#SBATCH -e 1_8c12_6144.err 


srun -n 6144  ./qlua_cori  plaquette.qlua load_gauge_field.qlua stout_smear.qlua 1.qlua 

