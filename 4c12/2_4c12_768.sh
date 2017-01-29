#!/bin/bash -l


#SBATCH -p debug
#SBATCH -N 32
#SBATCH -t 30:00

#SBATCH -J 768_4c12_edison_mg 
#SBATCH -o 2_4c12_768.out 
#SBATCH -e 2_4c12_768.err 


srun -n 768  ./qlua_edison  plaquette.qlua load_gauge_field.qlua stout_smear.qlua 2.qlua 

