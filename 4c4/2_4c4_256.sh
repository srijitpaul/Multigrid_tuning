#!/bin/bash -l


#SBATCH -p debug
#SBATCH -N 4
#SBATCH -C knl,quad,cache
#SBATCH -t 30:00
#SBATCH -J 256_4c4_knl_mg 
#SBATCH -o 2_4c4_256.out 
#SBATCH -e 2_4c4_256.err 


srun -n 256  ./qlua_cori  plaquette.qlua load_gauge_field.qlua stout_smear.qlua 2.qlua 

