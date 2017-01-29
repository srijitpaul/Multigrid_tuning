#!/bin/bash -l


#SBATCH -p debug
#SBATCH -N 144
#SBATCH -t 30:00

#SBATCH -J 3456_6c16_edison_mg 
#SBATCH -o 1_6c16_3456.out 
#SBATCH -e 1_6c16_3456.err 


srun -n 3456  ./qlua_edison  plaquette.qlua load_gauge_field.qlua stout_smear.qlua 1.qlua 

