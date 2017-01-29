#!/bin/bash -l


#SBATCH -p debug
#SBATCH -N 16
#SBATCH -t 30:00

#SBATCH -J 384_4c6_edison_mg 
#SBATCH -o 5_4c6_384.out 
#SBATCH -e 5_4c6_384.err 


srun -n 384  ./qlua_edison  plaquette.qlua load_gauge_field.qlua stout_smear.qlua 5.qlua 

