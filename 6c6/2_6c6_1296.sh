#!/bin/bash -l


#SBATCH -p debug
#SBATCH -N 54
#SBATCH -t 30:00

#SBATCH -J 1296_6c6_edison_mg 
#SBATCH -o 2_6c6_1296.out 
#SBATCH -e 2_6c6_1296.err 


srun -n 1296  ./qlua_edison  plaquette.qlua load_gauge_field.qlua stout_smear.qlua 2.qlua 

