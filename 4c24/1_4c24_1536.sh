#!/bin/bash -l


#SBATCH -p debug
#SBATCH -N 64
#SBATCH -t 30:00

#SBATCH -J 1536_4c24_edison_mg 
#SBATCH -o 1_4c24_1536.out 
#SBATCH -e 1_4c24_1536.err 


srun -n 1536  ./qlua_edison  plaquette.qlua load_gauge_field.qlua stout_smear.qlua 1.qlua 

