
# coding: utf-8

# In[1]:

import numpy as np
import sys
import itertools
import operator
import functools
import os
import subprocess


# In[2]:

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



# In[3]:

#Lattice size patameters
L = 32
T = 48


# In[4]:

prime_factors_L = primes(L)
prime_factors_T = primes(T)
num_prime_factors_L = len(prime_factors_L)
num_prime_factors_T = len(prime_factors_T)
print(num_prime_factors_L)
print(num_prime_factors_T)


# In[10]:

#We investigate first the possible sizes of the Coarsest Grid
#For that we start with any smallest combination fo prime numbers >= 4.
for nL in range(2,num_prime_factors_L-1):
    for nT in range(2,num_prime_factors_T-1):
        if nL<=nT:
            num_L_coarse = list(set(list(itertools.combinations((prime_factors_L),nL))))
            num_T_coarse = list(set(list(itertools.combinations((prime_factors_T),nT))))
            
            coarse_L = [functools.reduce(operator.mul, item, 1) for item in num_L_coarse]
            coarse_T = [functools.reduce(operator.mul, item, 1) for item in num_T_coarse]
            coarse_lat = itertools.product(coarse_L,coarse_T)
            coarse_lat_2 = itertools.product(coarse_L,coarse_T)
            #print(nL, coarse_L)
            #print(nT, coarse_T)
            #for core in coarse_lat_2:
               # if core[0]<=core[1]:
                    #print("Possible number of cores:", core[0]*core[0]*core[0]*core[1])
            for i in coarse_lat:
                if i[0]<=i[1]:
                    L_coarse = i[0]
                    T_coarse = i[1]
                    print("Possible number of cores:", i[0]*i[0]*i[0]*i[1])
                    print("Making directory:{}c{}".format(L_coarse,T_coarse))
                    path = "{}c{}".format(L_coarse,T_coarse)
                    os.makedirs(path, exist_ok=True)
                    #print("Prime factors of L for deciding the block sizes: {}".format(primes(L/L_coarse)))
                    #print("Prime factors of T for deciding the block sizes: {}".format(primes(T/T_coarse)))
                    prime_fac_partition_L = primes(L/L_coarse)
                    prime_fac_partition_T = primes(T/T_coarse)
                    filename_counter = 1
                    for L_partitions in sorted_k_partitions(prime_fac_partition_L,2):
                        for T_partitions in sorted_k_partitions(prime_fac_partition_T,2):
                            L_blocks = [functools.reduce(operator.mul, item, 1) for item in L_partitions]
                            T_blocks = [functools.reduce(operator.mul, item, 1) for item in T_partitions]
                            #print(L_blocks, T_blocks)
                            block_size =[list(zip(L_blocks, p)) for p in itertools.permutations(T_blocks)]
                            if functools.reduce(operator.mul,block_size[0][0],1)<functools.reduce(operator.mul,block_size[0][1],1):
                                dummy = block_size[0][0] 
                                block_size[0][0] = block_size[0][1]
                                block_size[0][1] = dummy
                            if functools.reduce(operator.mul,block_size[1][0],1)<functools.reduce(operator.mul,block_size[1][1],1):
                                dummy = block_size[1][0]
                                block_size[1][0] = block_size[1][1]
                                block_size[1][1] = dummy
                            block_size = list(set(tuple(x) for x in block_size))
                            #print("Block size length:",len(block_size))
                            #print("Block_1 size:",block_size[0][1])
                            for j in range(1,len(block_size)+1):
                                print("Block_0 size :", block_size[j-1][0])
                                print("Block_1 size :", block_size[j-1][1])
                                print("This is filename: {}.qlua".format(filename_counter))
                                bashcall = "./make_qlua.sh {} {} {} {} {} {}".format(path, filename_counter, block_size[j-1][0][0], block_size[j-1][0][1], block_size[j-1][1][0], block_size[j-1][1][1])
                                print(bashcall)
                                subprocess.call(bashcall, shell=True)
                                filename_counter = filename_counter + 1
                                print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
                            
                            
                            
                            
                    
            print("----------------")
            print("----------------")


# In[ ]:



