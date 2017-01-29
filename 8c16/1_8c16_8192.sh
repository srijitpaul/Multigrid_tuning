#!/bin/bash -l


#SBATCH -p debug
#SBATCH -N 342
#SBATCH -t 30:00

#SBATCH -J 8192_8c16_edison_mg 
#SBATCH -o 1_8c16_8192.out 
#SBATCH -e 1_8c16_8192.err 


srun -n 8192  ./qlua_edison  plaquette.qlua load_gauge_field.qlua stout_smear.qlua 1.qlua 

