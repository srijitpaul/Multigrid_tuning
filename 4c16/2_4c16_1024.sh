#!/bin/bash -l


#SBATCH -p debug
#SBATCH -N 43
#SBATCH -t 30:00

#SBATCH -J 1024_4c16_edison_mg 
#SBATCH -o 2_4c16_1024.out 
#SBATCH -e 2_4c16_1024.err 


srun -n 1024  ./qlua_edison  plaquette.qlua load_gauge_field.qlua stout_smear.qlua 2.qlua 

