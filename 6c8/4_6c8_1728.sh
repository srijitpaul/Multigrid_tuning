#!/bin/bash -l


#SBATCH -p debug
#SBATCH -N 72
#SBATCH -t 30:00

#SBATCH -J 1728_6c8_edison_mg 
#SBATCH -o 4_6c8_1728.out 
#SBATCH -e 4_6c8_1728.err 


srun -n 1728  ./qlua_edison  plaquette.qlua load_gauge_field.qlua stout_smear.qlua 4.qlua 

