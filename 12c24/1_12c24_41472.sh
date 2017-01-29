#!/bin/bash -l


#SBATCH -p debug
#SBATCH -N 1728
#SBATCH -t 30:00

#SBATCH -J 41472_12c24_edison_mg 
#SBATCH -o 1_12c24_41472.out 
#SBATCH -e 1_12c24_41472.err 


srun -n 41472  ./qlua_edison  plaquette.qlua load_gauge_field.qlua stout_smear.qlua 1.qlua 

