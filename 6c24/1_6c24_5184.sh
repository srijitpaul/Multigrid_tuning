#!/bin/bash -l


#SBATCH -p debug
#SBATCH -N 216
#SBATCH -t 30:00

#SBATCH -J 5184_6c24_edison_mg 
#SBATCH -o 1_6c24_5184.out 
#SBATCH -e 1_6c24_5184.err 


srun -n 5184  ./qlua_edison  plaquette.qlua load_gauge_field.qlua stout_smear.qlua 1.qlua 

