#!/bin/bash -l


#SBATCH -p debug
#SBATCH -N 171
#SBATCH -t 30:00

#SBATCH -J 4096_8c8_edison_mg 
#SBATCH -o 4_8c8_4096.out 
#SBATCH -e 4_8c8_4096.err 


srun -n 4096  ./qlua_edison  plaquette.qlua load_gauge_field.qlua stout_smear.qlua 4.qlua 

