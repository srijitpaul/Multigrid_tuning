#!/bin/bash -l


#SBATCH -p debug
#SBATCH -N 11
#SBATCH -t 30:00

#SBATCH -J 256_4c4_edison_mg 
#SBATCH -o 10_4c4_256.out 
#SBATCH -e 10_4c4_256.err 


srun -n 256  ./qlua_edison  plaquette.qlua load_gauge_field.qlua stout_smear.qlua 10.qlua 

