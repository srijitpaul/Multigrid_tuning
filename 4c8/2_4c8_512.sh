#!/bin/bash -l


#SBATCH -p debug
#SBATCH -N 22
#SBATCH -t 30:00

#SBATCH -J 512_4c8_edison_mg 
#SBATCH -o 2_4c8_512.out 
#SBATCH -e 2_4c8_512.err 


srun -n 512  ./qlua_edison  plaquette.qlua load_gauge_field.qlua stout_smear.qlua 2.qlua 

