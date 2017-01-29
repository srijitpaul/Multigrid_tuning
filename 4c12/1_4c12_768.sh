#!/bin/bash -l


#SBATCH -p debug
#SBATCH -N 12
#SBATCH -C knl,quad,cache
#SBATCH -t 30:00
#SBATCH -J 768_4c12_knl_mg 
#SBATCH -o 1_4c12_768.out 
#SBATCH -e 1_4c12_768.err 


srun -n 768  ./qlua_knl_cori  plaquette.qlua load_gauge_field.qlua stout_smear.qlua 1.qlua 

