#!/bin/bash -l


#SBATCH -p debug
#SBATCH -N 128
#SBATCH -C knl,quad,cache
#SBATCH -t 30:00
#SBATCH -J 4096_8c8_knl_mg 
#SBATCH -o 1_8c8_4096.out 
#SBATCH -e 1_8c8_4096.err 


srun -n 4096  ./qlua_cori  plaquette.qlua load_gauge_field.qlua stout_smear.qlua 1.qlua 

