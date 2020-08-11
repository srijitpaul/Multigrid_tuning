#!/bin/bash -x
#SBATCH --account=lqcdm2020
#SBATCH --nodes=3
#SBATCH --ntasks=12
#SBATCH --ntasks-per-node=4
#SBATCH --output=mg_N3_12gpu_1-1-1-12__4_4_4_2__2_2_2_2.out
#SBATCH --error=mg_N3_12gpu_1-1-1-12__4_4_4_2__2_2_2_2.err
#SBATCH --time=01:00:00
#SBATCH --partition=gpus

#SBATCH --gres=gpu:4

##Modules needed
module restore gnu_module

##Ensemble
ENSEMBLE="C101"

##Tuning directory
TUNE_DIR=${PWD}/tuning/8GPU
mkdir -p ${TUNE_DIR}
export QUDA_RESOURCE_PATH=${TUNE_DIR}

##MG PARAMS
export META="--verbosity verbose --dim 48 48 48 8 --gridsize 1 1 1 12 --kappa 0.13675962  --dslash-type wilson --solve-type direct-pc --load-gauge /p/scratch/lqcdm2020/C101/configs/C101r014n1.lime"
export SOLVER_PARAM="--precon-type mr --inv-type gcr --prec double --prec-sloppy single --prec-precondition single --recon 12 --recon-sloppy 12 --tol 1e-12"
export MG_PARAM="--mg-levels 3 --mg-generate-nullspace false --mg-save-vec 1 /tmp/null"
export LEVEL0_PARAM="--mg-nu-pre 0 0 --mg-nu-post 0 2 --mg-block-size 0 4 4 4 2 --mg-nvec 0 6 --mg-setup-inv 0 cg --mg-smoother 0 ca-gcr"
export LEVEL1_PARAM="--mg-nu-pre 1 0 --mg-nu-post 1 2 --mg-block-size 1 2 2 2 2 --mg-nvec 1 6 --mg-setup-inv 1 cg --mg-smoother 1 ca-gcr"
export LEVEL2_PARAM="--mg-coarse-solver 2 ca-gcr --mg-coarse-solver-maxiter 2 10"

##EXECUTABLE_DIR
EXECUTABLE=/p/project/lqcdm2020/build/external/test/old_quda/tests/multigrid_invert_test

##RUN_COMMAND
CHECK_COMMAND="srun env | grep CUDA"
RUN_COMMAND="srun ${EXECUTABLE} $META $SOLVER_PARAM $MG_PARAM $LEVEL0_PARAM $LEVEL1_PARAM $LEVEL2_PARAM"

echo "Starting job"
echo `date`
echo ${RUN_COMMAND}
#eval ${CHECK_COMMAND}
eval ${RUN_COMMAND}
echo `date`
echo "Finished job"

