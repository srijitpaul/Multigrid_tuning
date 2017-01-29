#!/bin/bash -l


#SBATCH -p debug
#SBATCH -N 512
#SBATCH -t 30:00

#SBATCH -J 12288_8c24_edison_mg 
#SBATCH -o 1_8c24_12288.out 
#SBATCH -e 1_8c24_12288.err 


srun -n 12288  ./qlua_edison  plaquette.qlua load_gauge_field.qlua stout_smear.qlua 1.qlua 

