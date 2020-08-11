#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Packages needed
import numpy as np
import sys
import itertools
import operator
import functools
import os
import subprocess


# In[2]:


def is_prime(a):
    return all(a % i for i in range(2, a))
def primes(n):
    primfac = []
    d = 2
    while d*d <= n:
        while (n % d) == 0:
            primfac.append(d)  # supposing you want multiple factors repeated
            n //= d
        d += 1
    if n > 1:
       primfac.append(n)
    return primfac
def sorted_k_partitions(seq, k):
    """Returns a list of all unique k-partitions of `seq`.

    Each partition is a list of parts, and each part is a tuple.

    The parts in each individual partition will be sorted in shortlex
    order (i.e., by length first, then lexicographically).

    The overall list of partitions will then be sorted by the length
    of their first part, the length of their second part, ...,
    the length of their last part, and then lexicographically.
    """
    n = len(seq)
    groups = []  # a list of lists, currently empty

    def generate_partitions(i):
        if i >= n:
            yield list(set(list(map(tuple, groups))))
        else:
            if n - i > k - len(groups):
                for group in groups:
                    group.append(seq[i])
                    yield from generate_partitions(i + 1)
                    group.pop()

            if len(groups) < k:
                groups.append([seq[i]])
                yield from generate_partitions(i + 1)
                groups.pop()

    result = generate_partitions(0)
    # Sort the parts in each partition in shortlex order
    result = [sorted(ps, key = lambda p: (len(p), p)) for ps in result]
    # Sort partitions by the length of each part, then lexicographically.
    result = sorted(result, key = lambda ps: (*map(len, ps), ps))
    for ps in result:
        if len(ps)==1:
            ps.append(*ps)
            

    result = list(set(tuple(x) for x in result))
    
    return result

def unique_rows(a):
    a = np.ascontiguousarray(a)
    unique_a = np.unique(a.view([('', a.dtype)]*a.shape[1]))
    return unique_a.view(a.dtype).reshape((unique_a.shape[0], a.shape[1]))


# In[3]:


#Lattice size patameters
L = 48
T = 96
cores_per_node = 64
host_name = "gpu"
feature = "quda"
gpu_per_node = 4
test_conf="/p/scratch/lqcdm2020/C101/configs/C101r014n1.lime"
ensemble="C101"
print(is_prime(gpu_per_node))


# In[4]:


prime_factors_L = primes(L)
prime_factors_T = primes(T)
num_prime_factors_L = len(prime_factors_L)
num_prime_factors_T = len(prime_factors_T)
print("Number of prime factors of effective L",L/gpu_per_node, num_prime_factors_L)
print(prime_factors_L)
print("Number of prime factors of effective T", T/gpu_per_node, num_prime_factors_T)
print(prime_factors_T)


# In[7]:


min_nodes = 1
max_nodes = 16

total_volume = L*L*L*T
grid = np.array([])
subprocess.call("rm -r */", shell=True)
for node in range(min_nodes, max_nodes+1):
    totalGPUs = node*gpu_per_node
    #prime_factors = primes(totalGPUs)
    if(total_volume%totalGPUs == 0 ):
        print("Number of allowed GPUs:", totalGPUs, " with nodes ", node)
        print("Making directory : {}node{}GPU".format(node, totalGPUs))
        #path = "{}node{}GPU".format(node, totalGPUs)
        #os.makedirs(path, exist_ok=True)
        
        totalgrids = np.empty(shape=(1,4), dtype=int)
        primefacGPU = primes(totalGPUs) 
        #print(primefacGPU)
    
        for nfac in range(1, len(primefacGPU)+1):
            num_fac_GPU = list(set(list(itertools.combinations((primefacGPU),nfac))))
            #print(nfac, num_fac_GPU)
            T_GPUs = [functools.reduce(operator.mul, item, 1) for item in num_fac_GPU]
            #print(T_GPUs)
            for tgrid in T_GPUs:
                #print(tgrid)
                if((T%tgrid == 0)):
                    if(int(totalGPUs/tgrid)<tgrid):
                        
                        #grid = np.append(grid, [1,1,int(totalGPUs/tgrid),tgrid], axis=0)
                        grid = np.sort([1,1,int(totalGPUs/tgrid),tgrid])
                        #print(1,1,int(totalGPUs/tgrid),tgrid)
                        #print(grid)
                        totalgrids = np.vstack((totalgrids, grid))
                    else:
                        grid = [1,1,int(totalGPUs/tgrid),tgrid]
                        #grid = [1,1,tgrid,int(totalGPUs/tgrid)]
                        #print("Issue", grid)
                        if(grid[2] >1):
                            primefac_xyzgrid = primes(grid[2])
                            #print(primefac_xyzgrid)
                            if(len(primefac_xyzgrid)==2):
                                grid = np.sort([1, primefac_xyzgrid[0], primefac_xyzgrid[1], tgrid])
                                #print(grid)
                                totalgrids = np.vstack((totalgrids, grid))
                            if(len(primefac_xyzgrid)==3):
                                grid = np.sort([primefac_xyzgrid[0], primefac_xyzgrid[1], primefac_xyzgrid[2], tgrid])
                                    #print(grid)
                                totalgrids = np.vstack((totalgrids, grid))

                                    

        totalgrids = np.delete(totalgrids, 0, axis=0)
        totalgrids = unique_rows(totalgrids)
        #print(totalgrids)
        for igrid in totalgrids:
            eff_grid = np.array([int(L/igrid[0]), int(L/igrid[1]), int(L/igrid[2]), int(T/igrid[3])])
            print(eff_grid, igrid)
            
            eff_L = np.min([eff_grid[0], eff_grid[1], eff_grid[2]])
            eff_T = eff_grid[3]
            prime_factors_eff_L = primes(eff_L)
            prime_factors_eff_T = primes(eff_T)
            num_prime_factors_eff_L = len(prime_factors_eff_L)
            num_prime_factors_eff_T = len(prime_factors_eff_T)
            
            coarsegrids = np.empty(shape=(1,4), dtype=int)
            for nL in range(2,num_prime_factors_eff_L-1):
                for nT in range(1,num_prime_factors_eff_T-1):

                    #print(nL, nT)
                    num_L_coarse = list(set(list(itertools.combinations((prime_factors_eff_L),nL))))
                    num_T_coarse = list(set(list(itertools.combinations((prime_factors_eff_T),nT))))
                    #print(num_L_coarse)
                    #print(num_T_coarse)
                    coarse_L = [functools.reduce(operator.mul, item, 1) for item in num_L_coarse]
                    coarse_T = [functools.reduce(operator.mul, item, 1) for item in num_T_coarse]
                    coarse_lat = itertools.product(coarse_L,coarse_T)


                    for i in coarse_lat:
                        if (i[0]>=i[1] and i[0] <= 8):
                            L_coarse = i[0]
                            T_coarse = i[1]
                            #print("Possible coarse Volume:{}, {}, {}, {}".format(L_coarse, L_coarse, L_coarse, T_coarse))
                            coarsegrids = np.vstack((coarsegrids, [L_coarse, L_coarse, L_coarse, T_coarse]))
            coarsegrids = np.delete(coarsegrids, 0, axis=0)
            #print(coarsegrids)
            for icoarsegrid in coarsegrids:
                
                #Outer
                block_0 = np.empty(shape=(1,4), dtype=int)
                #Inner
                block_1 = np.empty(shape=(1,4), dtype=int)
                print(icoarsegrid)
                print("Making subdirectory : {}node{}GPU/part_{}_{}_{}_{}/coarse_{}_{}_{}_{}".format(node, totalGPUs, igrid[0], igrid[1], igrid[2], igrid[3],
                                                                                                     icoarsegrid[0], icoarsegrid[1], icoarsegrid[2], icoarsegrid[3]))
                path = "{}node{}GPU/part_{}_{}_{}_{}/coarse_{}_{}_{}_{}".format(node, totalGPUs, igrid[0], igrid[1], igrid[2], igrid[3],
                                                                                                     icoarsegrid[0], icoarsegrid[1], icoarsegrid[2], icoarsegrid[3])
                os.makedirs(path, exist_ok=True)
                ## grid which needs to be factorized n times for n level multigrid
                factor_grid = eff_grid/icoarsegrid
                print(factor_grid)
                if(factor_grid[0] == factor_grid[1] and factor_grid[1] == factor_grid[2]):
                    L_pfac = primes(factor_grid[0])
                    T_pfac = primes(factor_grid[3])
                    for L_partitions in sorted_k_partitions(L_pfac, 2):
                        for T_partitions in sorted_k_partitions(T_pfac, 2):
                            L_blocks = [functools.reduce(operator.mul, item, 1) for item in L_partitions]
                            T_blocks = [functools.reduce(operator.mul, item, 1) for item in T_partitions]
                            
                            block_0 = np.vstack((block_0, [L_blocks[1], L_blocks[1], L_blocks[1], T_blocks[1]]))
                            block_1 = np.vstack((block_1, [L_blocks[0], L_blocks[0], L_blocks[0], T_blocks[0]]))

                              
                #Any two would be equal
                
                elif(factor_grid[0] == factor_grid[1]):
                    L1_grid = factor_grid[0]
                    L2_grid = factor_grid[2]
                    L1_pfac = primes(L1_grid)
                    L2_pfac = primes(L2_grid)
                    T_pfac = primes(factor_grid[3])
                    for L1_partitions in sorted_k_partitions(L1_pfac, 2):
                        for L2_partitions in sorted_k_partitions(L2_pfac, 2):
                            for T_partitions in sorted_k_partitions(T_pfac, 2):
                                L1_blocks = [functools.reduce(operator.mul, item, 1) for item in L1_partitions]
                                L2_blocks = [functools.reduce(operator.mul, item, 1) for item in L2_partitions]
                                T_blocks = [functools.reduce(operator.mul, item, 1) for item in T_partitions]
                                #print("P", L1_blocks, L2_blocks, T_blocks)
                                
                                block_0 = np.vstack((block_0, [L1_blocks[1], L1_blocks[1], L2_blocks[1], T_blocks[1]]))
                                block_1 = np.vstack((block_1, [L1_blocks[0], L1_blocks[0], L2_blocks[0], T_blocks[0]]))
                                

                elif(factor_grid[0] == factor_grid[2]):
                    L1_grid = factor_grid[0]
                    L2_grid = factor_grid[1]
                    L1_pfac = primes(L1_grid)
                    L2_pfac = primes(L2_grid)
                    T_pfac = primes(factor_grid[3])
                    for L1_partitions in sorted_k_partitions(L1_pfac, 2):
                        for L2_partitions in sorted_k_partitions(L2_pfac, 2):
                            for T_partitions in sorted_k_partitions(T_pfac, 2):
                                L1_blocks = [functools.reduce(operator.mul, item, 1) for item in L1_partitions]
                                L2_blocks = [functools.reduce(operator.mul, item, 1) for item in L2_partitions]
                                T_blocks = [functools.reduce(operator.mul, item, 1) for item in T_partitions]
                                #print("P", L1_blocks, L2_blocks, T_blocks)
                                
                                block_0 = np.vstack((block_0, [L1_blocks[1], L2_blocks[1], L1_blocks[1], T_blocks[1]]))
                                block_1 = np.vstack((block_1, [L1_blocks[0], L2_blocks[0], L1_blocks[0], T_blocks[0]]))
                                
                elif(factor_grid[2] == factor_grid[1]):
                    L1_grid = factor_grid[0]
                    L2_grid = factor_grid[2]
                    L1_pfac = primes(L1_grid)
                    L2_pfac = primes(L2_grid)
                    T_pfac = primes(factor_grid[3])
                    for L1_partitions in sorted_k_partitions(L1_pfac, 2):
                        for L2_partitions in sorted_k_partitions(L2_pfac, 2):
                            for T_partitions in sorted_k_partitions(T_pfac, 2):
                                L1_blocks = [functools.reduce(operator.mul, item, 1) for item in L1_partitions]
                                L2_blocks = [functools.reduce(operator.mul, item, 1) for item in L2_partitions]
                                T_blocks = [functools.reduce(operator.mul, item, 1) for item in T_partitions]
                                #print("P", L1_blocks, L2_blocks, T_blocks)
                                
                                block_0 = np.vstack((block_0, [L1_blocks[1], L2_blocks[1], L2_blocks[1], T_blocks[1]]))
                                block_1 = np.vstack((block_1, [L1_blocks[0], L2_blocks[0], L2_blocks[0], T_blocks[0]]))
                else:
                    print("Dont try this partition")
                    
                block_0 = np.delete(block_0, 0, axis=0)
                block_1 = np.delete(block_1, 0, axis=0)
                #b_size = np.hstack((block_0, block_1))
                block_0 = block_0.astype(int)
                block_1 = block_1.astype(int)
                #print("P", b_size)
                for j in range(0,len(block_0)):
                    print("Block_0 size :", block_0[j])
                    print("Block_1 size :", block_1[j])
                 
                    name="mg_N{}_{}gpu_{}-{}-{}-{}__{}_{}_{}_{}__{}_{}_{}_{}".format(node, totalGPUs, igrid[0], igrid[1], igrid[2], igrid[3], 
                                                                                       block_0[j][0], block_0[j][1], block_0[j][2], block_0[j][3],
                                                                                           block_1[j][0], block_1[j][1], block_1[j][2], block_1[j][3])
                    
                    filename="{}/mg_N{}_{}gpu_{}-{}-{}-{}__{}_{}_{}_{}__{}_{}_{}_{}".format(path, node, totalGPUs, igrid[0], igrid[1], igrid[2], igrid[3], 
                                                                                       block_0[j][0], block_0[j][1], block_0[j][2], block_0[j][3],
                                                                                           block_1[j][0], block_1[j][1], block_1[j][2], block_1[j][3])
                    print(filename)
                    with open (filename+".sh", 'w') as rsh:
                        rsh.write('''#!/bin/bash -x
#SBATCH --account=lqcdm2020
#SBATCH --nodes={}
#SBATCH --ntasks={}
#SBATCH --ntasks-per-node={}
#SBATCH --output={}.out
#SBATCH --error={}.err
#SBATCH --time=01:00:00
#SBATCH --partition=gpus

#SBATCH --gres=gpu:{}

##Modules needed
module restore gnu_module

##Ensemble
ENSEMBLE="{}"

##Tuning directory
TUNE_DIR=$PWD/tuning/{}
mkdir -p $TUNE_DIR
export QUDA_RESOURCE_PATH=$TUNE_DIR

##MG PARAMS
export META="--verbosity verbose --dim {} {} {} {} --gridsize {} {} {} {} --kappa 0.13675962  --dslash-type wilson --solve-type direct-pc --load-gauge {}"
export SOLVER_PARAM="--precon-type mr --inv-type gcr --prec double --prec-sloppy single --prec-precondition single --recon 12 --recon-sloppy 12 --tol 1e-12"
export MG_PARAM="--mg-levels 3 --mg-generate-nullspace false --mg-save-vec 1 /tmp/null"
export LEVEL0_PARAM="--mg-nu-pre 0 0 --mg-nu-post 0 2 --mg-block-size 0 {} {} {} {} --mg-nvec 0 6 --mg-setup-inv 0 cg --mg-smoother 0 ca-gcr"
export LEVEL1_PARAM="--mg-nu-pre 1 0 --mg-nu-post 1 2 --mg-block-size 1 {} {} {} {} --mg-nvec 1 6 --mg-setup-inv 1 cg --mg-smoother 1 ca-gcr"
export LEVEL2_PARAM="--mg-coarse-solver 2 ca-gcr --mg-coarse-solver-maxiter 2 10"

##EXECUTABLE_DIR
EXECUTABLE=/p/project/lqcdm2020/build/external/test/old_quda/tests/multigrid_invert_test

##RUN_COMMAND
CHECK_COMMAND="srun env | grep CUDA"
RUN_COMMAND="srun $EXECUTABLE $META $SOLVER_PARAM $MG_PARAM $LEVEL0_PARAM $LEVEL1_PARAM $LEVEL2_PARAM"

echo "Starting job"
echo `date`
echo $RUN_COMMAND
#eval $CHECK_COMMAND
eval $RUN_COMMAND
echo `date`
echo "Finished job"
                        '''.format(node, totalGPUs, gpu_per_node, name, name, gpu_per_node, ensemble, name,
                                  eff_grid[0], eff_grid[1], eff_grid[2], eff_grid[3], igrid[0], igrid[1], igrid[2], igrid[3], test_conf,
                                  block_0[j][0], block_0[j][1], block_0[j][2], block_0[j][3],
                                  block_1[j][0], block_1[j][1], block_1[j][2], block_1[j][3]))


# In[ ]:




