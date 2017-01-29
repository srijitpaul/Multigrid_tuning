#!/bin/bash -l


#SBATCH -p debug
#SBATCH -N 864
#SBATCH -t 30:00

#SBATCH -J 20736_12c12_edison_mg 
#SBATCH -o 1_12c12_20736.out 
#SBATCH -e 1_12c12_20736.err 


srun -n 20736  ./qlua_edison  plaquette.qlua load_gauge_field.qlua stout_smear.qlua 1.qlua 

