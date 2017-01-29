#!/bin/bash -l


#SBATCH -p debug
#SBATCH -N 1152
#SBATCH -t 30:00

#SBATCH -J 27648_12c16_edison_mg 
#SBATCH -o 1_12c16_27648.out 
#SBATCH -e 1_12c16_27648.err 


srun -n 27648  ./qlua_edison  plaquette.qlua load_gauge_field.qlua stout_smear.qlua 1.qlua 

