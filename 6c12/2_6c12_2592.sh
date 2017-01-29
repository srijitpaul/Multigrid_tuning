#!/bin/bash -l


#SBATCH -p debug
#SBATCH -N 108
#SBATCH -t 30:00

#SBATCH -J 2592_6c12_edison_mg 
#SBATCH -o 2_6c12_2592.out 
#SBATCH -e 2_6c12_2592.err 


srun -n 2592  ./qlua_edison  plaquette.qlua load_gauge_field.qlua stout_smear.qlua 2.qlua 

